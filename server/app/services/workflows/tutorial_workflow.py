import logging
import json
import asyncio
from typing import AsyncGenerator, Dict
from fastapi import APIRouter, Form
from app.core.config import settings
from ai71 import AI71

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

client = AI71(settings.AI71_API_KEY)

async def generate_section_content(project: str, section: str) -> AsyncGenerator[Dict[str, str], None]:
    prompt = f"""Based on the following project, generate content for this section of the tutorial:
    Project: {project}
    Section: {section}
    Provide detailed explanations and keep the response under 1000 words.
    If this section involves code, provide a detailed code example with comments. The code should be complete, not half-done."""

    try:
        response = await asyncio.to_thread(client.chat.completions.create,
            model="tiiuae/falcon-180B-chat",
            messages=[
                {"role": "system", "content": """You are a book writer,   
                  You're an expert in electronics and you're writing a book for beginners to understand how to implement a project.
                  Provide detailed explanations and keep the response under 1000 words.
"""},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.7,
            stream=True,
        )
        for chunk in response:
            if chunk.choices and chunk.choices[0].delta.content:
                logger.debug(f"Streaming chunk for section '{section}': {chunk.choices[0].delta.content}")
                yield {"section": section, "content": chunk.choices[0].delta.content}
            await asyncio.sleep(0)  # Small delay to prevent overwhelming the client
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
        response = await asyncio.to_thread(client.chat.completions.create,
            model="tiiuae/falcon-180B-chat",
            messages=[
                {"role": "system", "content": """You are a book writer,   
                  You're an expert in electronics and you're writing a book for beginners to understand how to implement a project.
                  Provide detailed explanations and keep the response under 1000 words.
"""},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7,
            stream=True,
        )
        for chunk in response:
            if chunk.choices and chunk.choices[0].delta.content:
                logger.debug(f"Streaming chunk for project overview: {chunk.choices[0].delta.content}")
                yield {"project_overview": chunk.choices[0].delta.content}
            await asyncio.sleep(0)  # Small delay to prevent overwhelming the client
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

async def consume_async_generator(generator):
    async for item in generator:
        yield item

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
            await asyncio.sleep(0.1)