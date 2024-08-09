import asyncio
import logging
import json
from typing import AsyncGenerator, Dict
from app.utils.markdown import process_markdown
from app.utils.save_image_to_temp import consume_async_generator
from fastapi import APIRouter, Form
from app.core.config import settings
from .llm import client  # Using your existing client

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
async def generate_section_content(project: str, section: str) -> AsyncGenerator[Dict[str, str], None]:
    prompt = f"""
    You are an expert at writing structured tutorials with proper Markdown formatting. Please generate content for the following section of a project tutorial:
    
    Project: {project}
    Section: {section}
    
    Requirements:
    - Use appropriate Markdown syntax for headers, lists, and code blocks.
    - Start with a header for the section title.
    - For any list of items, use either ordered or unordered lists as appropriate.
    - If including code, format it using triple backticks (```), specify the language, and ensure the code is indented properly.
    - Ensure there are proper line breaks and paragraphs.
    - Avoid unnecessary punctuation or random line breaks.

    Provide detailed explanations and keep the response under 1000 words. If this section involves code, provide a detailed code example with comments. The code should be complete, not half-done.
    """

    try:
        response_stream = await client.astream_complete(prompt=prompt, image_documents=[])

        async for chunk in response_stream:
            if chunk.text:
                # No need to split by sentences if Markdown is properly generated
                yield {"section": section, "content": chunk.text}
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
        # Stream content using your existing client
        response_stream = await client.astream_complete(prompt=prompt,image_documents=[])

        # Streaming the response in larger chunks (e.g., sentences)
        async for chunk in response_stream:
            if chunk.text:
                sentences = chunk.text.split('. ')
                for sentence in sentences:
                    yield {"project_overview": sentence + ". "}
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
            processed_chunk = process_markdown(chunk.get('content', ''))
            chunk['content'] = processed_chunk
            yield json.dumps(chunk)
            await asyncio.sleep(0.1)