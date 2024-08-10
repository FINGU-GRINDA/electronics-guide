import json
import os
from typing import Dict, Generator, TypedDict, Any
from app.services.memory.ideas_memory import ProjectMemory
from llama_index.multi_modal_llms.gemini import GeminiMultiModal
from llama_index.core.schema import ImageDocument
from langgraph.graph import StateGraph, END
import logging
import base64
from .workflows.llm import client
from ..core.config import settings
from app.utils.save_image_to_temp import save_image_to_temp_file
import random
import re

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize memory
project_memory = ProjectMemory()

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

async def analyze_image_and_suggest_projects(image_path: str) -> str:
    logger.debug(f"Analyzing image: {image_path}")
    image_doc = ImageDocument(image_path=image_path)
    
    previous_projects = project_memory.get_previous_projects()
    previous_projects_str = "\n".join(f"- {project}" for project in previous_projects) if previous_projects else "No previous projects."

    prompt = f"""Analyze this image of electronic parts and provide the following:
    1. A list of all identifiable electronic components in the image.
    2. Suggest 4 random, unique, and creative project ideas that can be created with these components. Ensure each title is detailed and imaginative.
    
    Previous project titles (do not repeat these or create very similar ideas):
    {previous_projects_str}
    
    Format your response as follows:
    Components:
    - [List of components]

    Project Ideas:
    1. [Project 1 Title]: [Brief description]
    2. [Project 2 Title]: [Brief description]
    3. [Project 3 Title]: [Brief description]
    4. [Project 4 Title]: [Brief description]
    """

    response = await client.acomplete(prompt=prompt, image_documents=[image_doc])
    return response.text

class GraphState(TypedDict):
    image_path: str
    project_ideas: str
    selected_project: str
    project_overview: str
    gemini_tutorial: str

def define_idea_workflow() -> StateGraph:
    workflow = StateGraph(GraphState)
    
    async def image_analysis_node(state: GraphState) -> GraphState:
        logger.debug(f"Executing image_analysis_node with initial state: {state}")
        
        if not state["project_ideas"]:
            state["project_ideas"] = await analyze_image_and_suggest_projects(state["image_path"])
        
        logger.debug(f"State after image_analysis_node: {state}")
        return state

    workflow.add_node("image_analysis", image_analysis_node)
    workflow.set_entry_point("image_analysis")
    workflow.add_edge("image_analysis", END)

    return workflow

async def analyze_image(image_data: bytes) -> dict:
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
    async for output in workflow.astream(initial_state):
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

        # Add new project ideas to memory
        project_memory.add_projects(project_ideas)

        return {"components": components, "project_ideas": project_ideas}
    except Exception as e:
        logger.exception("Error parsing project ideas")
        return {"components": [], "project_ideas": []}