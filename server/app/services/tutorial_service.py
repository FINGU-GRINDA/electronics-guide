import json
import os
from typing import Dict, Generator, TypedDict, Any
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

from ..core.config import settings  # Import the settings object

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# Initialize models
mm_llm = GeminiMultiModal(model_name="models/gemini-1.5-flash-latest", temperature=0.7, api_key=settings.GOOGLE_API_KEY)

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
def generate_gemini_tutorial(project: str, overview: str, image_path: str) -> Generator[str, None, None]:
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

    full_tutorial = f"# {project}\n\n"

    for section in sections:
        prompt = f"""Based on the following project and overview, generate content for this section of the tutorial:

        Project: {project}
        Overview: {overview}

        Section: {section}

        Provide detailed explanations and keep the response under 1000 words.
        If this section involves code, provide a detailed code example with comments. the code should be completed not half one."""

        response = mm_llm.complete(prompt=prompt, image_documents=[image_doc])
        content = response.text

        full_tutorial += f"\n\n## {section}\n\n{content}"
        yield {
            "section": section,
            "content": content
        }

    yield full_tutorial


class GraphState(TypedDict):
    image_path: str
    project_ideas: str
    selected_project: str
    project_overview: str
    gemini_tutorial: str


def define_guide_workflow() -> StateGraph:
    workflow = StateGraph(GraphState)

    # Node 3: Project Implementation Details
    def project_details_node(state: GraphState) -> GraphState:
        state["project_overview"] = provide_project_details(state["selected_project"], state["image_path"])
        print("Project overview generated.")
        return state

    # Node 4: Gemini Tutorial Generation
    # Update the gemini_tutorial_generation_node to stream each section
    def gemini_tutorial_generation_node(state: Dict[str, Any]) -> Generator[Dict[str, Any], None, Dict[str, Any]]:
        for part in generate_gemini_tutorial(state["selected_project"], state["project_overview"], state["image_path"]):
            if isinstance(part, dict):
                yield {
                    "current_section": part["section"],
                    "section_content": part["content"]
                }
            else:
                # This is the full tutorial, which we don't need to yield
                state["gemini_tutorial"] = part
        
        yield state

    
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
        if step == 0:
 # Assuming the state contains project details under the key "project_details"
            project_details = state["project_details"]
            state["project_overview"] = project_details  # Update the project overview with the details

            section_content = json.dumps({"project_overview": project_details}, indent=2)
        else:
            section_content = json.dumps({"section_content": state.get('gemini_tutorial_generation', '')}, indent=2)
        yield section_content