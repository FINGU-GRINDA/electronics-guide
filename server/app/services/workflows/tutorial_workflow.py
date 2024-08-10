import asyncio
import logging
import json
from typing import AsyncGenerator, Dict
from app.services.memory.section_summary_memory import CustomMemoryBuffer
from app.utils.markdown import process_markdown
from app.utils.save_image_to_temp import consume_async_generator
from fastapi import APIRouter, Form
from app.core.config import settings
from .llm import client  # Your existing Gemini client

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
section_titles = [
    "1. Project Overview and Objectives",
    "2. Components and Tools Needed",
    "3. Setting Up Your Workspace and Safety Tips",
    "4. Written Wiring Instructions (If Applicable)",
    "5. Setting Up Your Development Environment",
    "6. Core Code: Writing and Explanation",
    "7. Code Expansion: Adding Features",
    "8. Code Testing and Debugging",
    "9. Final Integration: Bringing It All Together",
    "10. Troubleshooting and Optimization",
    "11. Best Practices and Precautions",
    "12. Project Conclusion and Next Steps"
]


# Initialize the custom memory buffer
memory = CustomMemoryBuffer()
async def generate_section_content(project: str, section: str) -> AsyncGenerator[Dict[str, str], None]:
    # Get the current memory content
    history_text = memory.get()

    prompt = f"""
    You are an expert in creating detailed and user-friendly project tutorials. Please generate content for the following section of a project tutorial:

    **Project Name:** {project}
    **Section Title:** {section}

    **Context from Previous Sections:**
    {history_text}

    **Content Requirements:**
    - Use clear and concise language that guides the user through each step.
    - Begin with a relevant and engaging header for the section title.
    - Include lists, bullet points, or steps where applicable for better readability.
    - For code sections, provide complete, fully functional, and well-commented code examples within triple backticks (```).
    - Ensure that the code is not truncated or incomplete. If the code is lengthy, break it into logical segments, but ensure each segment is fully functional and runnable on its own.
    - For wiring instructions, provide detailed, step-by-step written instructions, specifying each connection clearly without relying on circuit diagrams. Describe the wiring process using text only.
    - Ensure the content is formatted properly with appropriate Markdown syntax for headings, lists, and code blocks.
    - Reference relevant details from previous sections for continuity.
    - Tailor the content to be under 1000 words while covering all necessary information comprehensively.

    **Goal:** Provide actionable and easy-to-follow instructions that empower the user to complete this part of the project confidently.
    """

    try:
        response_stream = await client.astream_complete(prompt=prompt, image_documents=[])

        full_content = ""
        async for chunk in response_stream:
            if chunk.text:
                full_content += chunk.text
                yield {"section": section, "content": chunk.text}
        
        # Generate a summary using the client
        summary_prompt = f"""
        Please provide a concise summary of the following content for the section "{section}" of the project "{project}". 
        The summary should be about 2-3 sentences long and capture the key points:

        {full_content}
        """
        
        summary_response = await client.acomplete(prompt=summary_prompt, image_documents=[])
        summary = f"Summary of {section}: {summary_response.text}"
        
        # Add the generated summary to the memory
        memory.add(summary)
        
        yield {"section": section, "content": "\n\n"}
    except Exception as e:
        logger.error(f"Error generating content for section '{section}': {e}")
        yield {"section": section, "content": f"Error generating content: {str(e)}"}



async def provide_project_details(project: str) -> AsyncGenerator[Dict[str, str], None]:
    prompt = f"""Provide a Project Title and a very short description for this project: {project}
   
    -Ensure the content is formatted properly with appropriate Markdown syntax for headings
    
"""

    try:
        response_stream = await client.astream_complete(prompt=prompt, image_documents=[])

        async for chunk in response_stream:
            if chunk.text:
                yield {"project_overview": chunk.text}
        yield {"project_overview": "\n\n"}
        
    except Exception as e:
        logger.error(f"Error generating project overview: {e}")
        yield {"project_overview": f"Error generating project overview: {str(e)}"}

async def provide_project_details_service(project: str) -> AsyncGenerator[str, None]:
    # First, yield the project title
    yield json.dumps({"project_title": project})

    # Then, continue with the tasks for project details and section content
    tasks = [
        consume_async_generator(provide_project_details(project))
    ] + [
        consume_async_generator(generate_section_content(project, section))
        for section in section_titles
    ]

    for task in tasks:
        async for chunk in task:
            yield json.dumps(chunk)
