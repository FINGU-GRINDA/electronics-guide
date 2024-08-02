import json
import os
from typing import Dict, Generator, TypedDict, Any
from llama_index.multi_modal_llms.gemini import GeminiMultiModal
from llama_index.core.schema import ImageDocument
from langgraph.graph import StateGraph, END
import logging

import base64


from app.utils import save_image_to_temp_file
from ..core.config import settings  # Import the settings object

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# Initialize models
mm_llm = GeminiMultiModal(model_name="models/gemini-1.5-flash-latest", temperature=0.7, api_key=settings.GOOGLE_API_KEY)

# Function to encode image to base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Agent 1: Image Analysis and Project Ideas
def analyze_image_and_suggest_projects(image_path: str) -> str:
    logger.debug(f"Analyzing image: {image_path}")
    image_doc = ImageDocument(image_path=image_path)
    response = mm_llm.complete(
        prompt="""Analyze this image of electronic parts and provide the following:
        1. A list of all identifiable electronic components in the image.
        2. Suggest 4 project ideas that can be created with these components. Number each idea from 1 to 4.
        
        Format your response as follows:
        Components:
        - [List of components]

        Project Ideas:
        1. [Project 1]
        2. [Project 2]
        3. [Project 3]
        4. [Project 4]
        """,
        image_documents=[image_doc]
    )
    return response.text

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

# Define the idea workflow
def define_idea_workflow() -> StateGraph:
    workflow = StateGraph(GraphState)

    def image_analysis_node(state: GraphState) -> GraphState:
        logger.debug(f"Executing image_analysis_node with initial state: {state}")
        if not state["project_ideas"]:
            state["project_ideas"] = analyze_image_and_suggest_projects(state["image_path"])
        logger.debug(f"State after image_analysis_node: {state}")
        return state

    workflow.add_node("image_analysis", image_analysis_node)
    workflow.set_entry_point("image_analysis")
    workflow.add_edge("image_analysis", END)

    return workflow


def analyze_image(image_data: bytes) -> dict:
    image_path = save_image_to_temp_file(image_data)
    initial_state = GraphState(
        image_path=image_path, 
        project_ideas="", 
        selected_project="", 
        project_overview="", 
        gemini_tutorial=""
    )
    workflow = define_idea_workflow().compile()

    final_state = None
    for output in workflow.stream(initial_state):
        final_state = output

    logger.info(f"Final state after image analysis: {final_state}")

    if not final_state or 'image_analysis' not in final_state:
        logger.error("No image analysis result")
        return {"components": [], "project_ideas": []}

    image_analysis = final_state['image_analysis']

    if "project_ideas" not in image_analysis or not image_analysis["project_ideas"]:
        logger.error("No project ideas generated")
        return {"components": [], "project_ideas": []}

    try:
        parts = image_analysis["project_ideas"].split("Project Ideas:")
        if len(parts) != 2:
            logger.error(f"Unexpected format in project_ideas: {image_analysis['project_ideas']}")
            return {"components": [], "project_ideas": []}

        components, projects = parts

        components = [comp.strip() for comp in components.split("Components:")[1].strip().split("-") if comp.strip()]
        project_ideas = [idea.strip() for idea in projects.strip().split("\n") if idea.strip()]

        return {"components": components, "project_ideas": project_ideas}
    except Exception as e:
        logger.exception("Error parsing project ideas")
        return {"components": [], "project_ideas": []}
