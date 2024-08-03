import json
import os
from typing import Dict, AsyncGenerator, Generator, Optional
from llama_index.multi_modal_llms.gemini import GeminiMultiModal
from llama_index.core.schema import ImageDocument
from langgraph.graph import StateGraph, END
import logging
import markdown
import pdfkit
from jinja2 import Template
import base64
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import StreamingResponse, FileResponse
from pydantic import BaseModel
from ..core.config import settings  # Import the settings object

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize models
mm_llm = GeminiMultiModal(model_name="models/gemini-1.5-flash-latest", temperature=0.7, api_key=settings.GOOGLE_API_KEY)

class GraphState(BaseModel):
    image_path: str
    project_ideas: str
    selected_project: str
    project_overview: str
    gemini_tutorial: str

    current_section: Optional[str] = None
    section_content: Optional[str] = None

# Function to encode image to base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Agent 2: Project Implementation Details
async def provide_project_details(project: str, image_path: str) -> str:
    print(f"Generating tutorial for project: {project}")
    image_doc = ImageDocument(image_path=image_path)
    response = await mm_llm.acomplete(
        prompt=f"""Provide a brief overview of how to implement this electronic project: {project}
        Include:
        1. A list of main components needed
        2. Basic steps to connect the components
        3. A brief description of how the project works

        Keep the response under 300 words.""",
        image_documents=[image_doc]
    )
    return response.text
import asyncio

async def generate_gemini_tutorial(project: str, overview: str, image_path: str) -> AsyncGenerator[Dict[str, str], None]:
    image_doc = ImageDocument(image_path=image_path)
    sections = [
        "1. Introduction to the project",
        "2. List of components and tools needed",
        "3. Step-by-step instructions",
        "4. Circuit diagram or wiring instructions",
        "5. Code explanation",
        "6. Troubleshooting guide",
        "7. Safety precautions",
        "8. Conclusion"
    ]

    for section in sections:
        prompt = f"""Based on the following project and overview, generate content for this section of the tutorial:

        Project: {project}
        Overview: {overview}

        Section: {section}

        Provide detailed explanations and keep the response under 1000 words.
        If this section involves code, provide a detailed code example with comments. The code should be complete, not half-done."""

        for attempt in range(3):  # Retry up to 3 times
            try:
                response = await mm_llm.acomplete(prompt=prompt, image_documents=[image_doc])
                content = response.text
                yield {
                    "section": section,
                    "content": content
                }
                break  # Break out of the retry loop on success
            except Exception as e:
                logger.error(f"Attempt {attempt + 1} failed for section '{section}': {e}")
                if attempt == 2:
                    yield {
                        "section": section,
                        "content": f"Error generating content: {str(e)}"
                    }
                    break  # No more retries left, break the loop
                await asyncio.sleep(2)  # Wait a bit before retrying


async def project_details_node(state: GraphState) -> GraphState:
    state.project_overview = await provide_project_details(state.selected_project, state.image_path)
    logger.debug(f"Project overview generated in node: {state.project_overview}")
    return state

async def gemini_tutorial_generation_node(state: GraphState) -> AsyncGenerator[GraphState, None]:
    async for part in generate_gemini_tutorial(state.selected_project, state.project_overview, state.image_path):
        state.current_section = part["section"]
        state.section_content = part["content"]
        
        # Yield the state after each section is generated
        yield state

    # After all sections are generated
    state.gemini_tutorial = "Tutorial generation completed"
    yield state

def define_guide_workflow() -> StateGraph:
    workflow = StateGraph(GraphState)

    workflow.add_node("project_details", project_details_node)
    workflow.add_node("gemini_tutorial_generation", gemini_tutorial_generation_node)
    workflow.set_entry_point("project_details")

    workflow.add_edge("project_details", "gemini_tutorial_generation")
    workflow.add_edge("gemini_tutorial_generation", END)
    
    return workflow
async def provide_project_details_service(project: str, image_path: str) -> AsyncGenerator[str, None]:
    initial_state = GraphState(
        image_path=image_path,
        project_ideas="",
        selected_project=project,
        project_overview="",
        gemini_tutorial="",
    )

    workflow = define_guide_workflow().compile()

    async for state in workflow.astream(initial_state, stream_mode="updates"):
        state_dict = dict(state)
        logger.debug(f"Current state: {state_dict}")

        if "project_details" in state_dict:
            yield json.dumps({
                "project_overview": state_dict['project_details']["project_overview"],
            }, indent=2)
        
        if "gemini_tutorial_generation" in state_dict:
            try:
                current_section = state_dict["gemini_tutorial_generation"]["current_section"]
                section_content = state_dict["gemini_tutorial_generation"]["section_content"]
                
                if current_section and section_content:
                    yield json.dumps({
                        "current_section": current_section,
                        "section_content": section_content,
                    }, indent=2)
                
                if state_dict["gemini_tutorial_generation"]["gemini_tutorial"] == "Tutorial generation completed":
                    break
            except KeyError as e:
                logger.error(f"Missing key in state dictionary: {e}")