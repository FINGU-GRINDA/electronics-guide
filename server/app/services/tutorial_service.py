import json
import os
from typing import Dict, Generator, Optional, TypedDict, Any
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
def provide_project_details(project: str, image_path: str) -> str:
    print(f"Generating tutorial for project: {project}")
    image_doc = ImageDocument(image_path=image_path)
    response = mm_llm.complete(
        prompt=f"""Provide a brief overview of how to implement this electronic project: {project}
        Include:
        1. A list of main components needed
        2. Basic steps to connect the components
        3. A brief description of how the project works

        Keep the response under 300 words.""",
        image_documents=[image_doc]
    )
    return response.text

# Agent 3: Gemini Tutorial Generator


# Update the generator function to yield each section
def generate_gemini_tutorial(project: str, overview: str, image_path: str) -> Generator[Dict[str, str], None, None]:
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

        response = mm_llm.complete(prompt=prompt, image_documents=[image_doc])
        content = response.text

        yield {
            "section": section,
            "content": content
        }

def project_details_node(state: GraphState) -> GraphState:
    state.project_overview = provide_project_details(state.selected_project, state.image_path)
    logger.debug(f"Project overview generated in node: {state.project_overview}")
    return state

def gemini_tutorial_generation_node(state: GraphState) -> Generator[GraphState, None, GraphState]:
    for part in generate_gemini_tutorial(state.selected_project, state.project_overview, state.image_path):
        state.current_section = part["section"]
        state.section_content = part["content"]
        yield state

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


def define_guide_workflow() -> StateGraph:
    workflow = StateGraph(GraphState)



    workflow.add_node("project_details", project_details_node)
    workflow.add_node("gemini_tutorial_generation", gemini_tutorial_generation_node)
    workflow.set_entry_point("project_details")

    workflow.add_edge("project_details", "gemini_tutorial_generation")
    workflow.add_edge("gemini_tutorial_generation", END)
    return workflow
def provide_project_details_service(project: str, image_path: str) -> Generator[str, None, None]:
    initial_state = GraphState(
        image_path=image_path,
        project_ideas="",
        selected_project=project,
        project_overview="",
        gemini_tutorial="",
    )

    workflow = define_guide_workflow().compile()

    for step, state in enumerate(workflow.stream(initial_state)):
        state_dict = dict(state)  # Ensure state is treated as a dictionary
        logger.debug(f"Step {step} state: {state_dict}")

        if step != 0:
            if "gemini_tutorial_generation" not in state_dict or "current_section" not in state_dict["gemini_tutorial_generation"]:
                raise KeyError("current_section or section_content not found in state['gemini_tutorial_generation']")
            current_section = state_dict["gemini_tutorial_generation"]["current_section"]
            section_content_data = state_dict["gemini_tutorial_generation"]["section_content"]
            logger.debug(f"Step {step}: Current section: {current_section}, Section content: {section_content_data}")
            section_content = json.dumps({
                "current_section": current_section,
                "section_content": section_content_data
            }, indent=2)
            yield section_content  # Yield each section's content as you generate it

            # Check if this is the last state
            if state_dict["gemini_tutorial_generation"]["gemini_tutorial"] == "Tutorial generation completed":
                break
