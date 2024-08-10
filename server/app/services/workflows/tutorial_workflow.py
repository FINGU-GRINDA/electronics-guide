import asyncio
import logging
import json
from typing import AsyncGenerator, Dict
from app.utils.markdown import process_markdown
from app.utils.save_image_to_temp import consume_async_generator
from fastapi import APIRouter, Form
from app.core.config import settings
from .llm import client  # Your existing Gemini client

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Custom memory class to work with your Gemini client
class CustomMemoryBuffer:
    def __init__(self, max_token_limit=1000):
        self.memory = []
        self.max_token_limit = max_token_limit

    def add(self, content):
        self.memory.append(content)
        # Implement token counting and truncation logic here if needed
        # For simplicity, we're just keeping a fixed number of recent items
        if len(self.memory) > 5:
            self.memory = self.memory[-5:]

    def get(self):
        return "\n\n".join(self.memory)

# Initialize the custom memory buffer
memory = CustomMemoryBuffer()

async def generate_section_content(project: str, section: str) -> AsyncGenerator[Dict[str, str], None]:
    # Get the current memory content
    history_text = memory.get()

    prompt = f"""
    You are an expert at writing structured tutorials with proper Markdown formatting. Please generate content for the following section of a project tutorial:
    
    Project: {project}
    Section: {section}
    
    Previous content summary:
    {history_text}

    Requirements:
    - Use appropriate Markdown syntax for headers, lists, and code blocks.
    - Start with a header for the section title.
    - For any list of items, use either ordered or unordered lists as appropriate.
    - If including code, format it using triple backticks (```), specify the language, and ensure the code is indented properly.
    - Ensure there are proper line breaks and paragraphs.
    - Avoid unnecessary punctuation or random line breaks.
    - Refer to information from previous sections when relevant.

    Provide detailed explanations and keep the response under 1000 words. If this section involves code, provide a detailed code example with comments. The code should be complete, not half-done.
    """

    try:
        response_stream = await client.astream_complete(prompt=prompt, image_documents=[])

        full_content = ""
        async for chunk in response_stream:
            if chunk.text:
                full_content += chunk.text
                yield {"section": section, "content": chunk.text}
        
        # Add a summary of the generated content to the memory
        summary = f"Summary of {section}: " + full_content[:200] + "..."  # Simple summarization
        memory.add(summary)
        
        yield {"section": section, "content": "\n\n"}
    except Exception as e:
        logger.error(f"Error generating content for section '{section}': {e}")
        yield {"section": section, "content": f"Error generating content: {str(e)}"}

async def provide_project_details(project: str) -> AsyncGenerator[Dict[str, str], None]:
    prompt = f"""Provide a brief overview of how to implement this electronic project: {project}
    Include:
    1. A list of main components needed
    2. Basic steps to connect the components
    3. A brief description of how the project works"""

    try:
        response_stream = await client.astream_complete(prompt=prompt, image_documents=[])

        async for chunk in response_stream:
            if chunk.text:
                yield {"project_overview": chunk.text}
        yield {"project_overview": "\n\n"}
        
    except Exception as e:
        logger.error(f"Error generating project overview: {e}")
        yield {"project_overview": f"Error generating project overview: {str(e)}"}

section_titles = [
    "1. Introduction to the project",
    "2. List of components and tools needed",
    "3. Step-by-step instructions",
    "4. Circuit diagram or wiring instructions",
    "5. Code explanation",
    "6. Troubleshooting guide",
    "7. Safety precautions",
    "8. Conclusion"
]

async def provide_project_details_service(project: str) -> AsyncGenerator[str, None]:
    tasks = [
        consume_async_generator(provide_project_details(project))
    ] + [
        consume_async_generator(generate_section_content(project, section))
        for section in section_titles
    ]

    for task in tasks:
        async for chunk in task:
            yield json.dumps(chunk)