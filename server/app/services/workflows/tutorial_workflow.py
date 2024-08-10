import asyncio
import logging
import json
from typing import AsyncGenerator, Dict
from app.services.memory.section_summary_memory import CustomMemoryBuffer
from app.utils.markdown import process_markdown
from app.utils.save_image_to_temp import consume_async_generator
from fastapi import APIRouter, Form
from app.core.config import settings
from app.constants.prompts import Prompts  # Import prompts
from app.constants.section_titles import SectionTitles  # Import section titles
from app.services.llm import client  # Your existing Gemini client

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize the custom memory buffer
memory = CustomMemoryBuffer()

async def generate_section_content(project: str, section: SectionTitles) -> AsyncGenerator[Dict[str, str], None]:
    # Get the current memory content
    history_text = memory.get()

    prompt = Prompts.GENERATE_SECTION_CONTENT.value.format(project=project, section=section.value, history_text=history_text)

    try:
        response_stream = await client.astream_complete(prompt=prompt, image_documents=[])

        full_content = ""
        async for chunk in response_stream:
            if chunk.text:
                full_content += chunk.text
                yield {"section": section.value, "content": chunk.text}
        
        # Generate a summary using the client
        summary_prompt = Prompts.GENERATE_SUMMARY.value.format(section=section.value, project=project, full_content=full_content)
        
        summary_response = await client.acomplete(prompt=summary_prompt, image_documents=[])
        summary = f"Summary of {section.value}: {summary_response.text}"
        
        # Add the generated summary to the memory
        memory.add(summary)
        
        yield {"section": section.value, "content": "\n\n"}
    except Exception as e:
        logger.error(f"Error generating content for section '{section.value}': {e}")
        yield {"section": section.value, "content": f"Error generating content: {str(e)}"}

async def provide_project_details(project: str) -> AsyncGenerator[Dict[str, str], None]:
    prompt = Prompts.PROVIDE_PROJECT_DETAILS.value.format(project=project)

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
        for section in SectionTitles
    ]

    for task in tasks:
        async for chunk in task:
            yield json.dumps(chunk)
