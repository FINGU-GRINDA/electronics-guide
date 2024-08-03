import json
import os
from typing import Dict, AsyncGenerator, List, Optional
from llama_index.multi_modal_llms.gemini import GeminiMultiModal
from llama_index.core.schema import ImageDocument
from langgraph.graph import StateGraph, END, START
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
    sections: List[Dict[str, str]] = []

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

async def generate_section_content(state: GraphState, section: str) -> Dict[str, str]:
    image_doc = ImageDocument(image_path=state.image_path)
    prompt = f"""Based on the following project and overview, generate content for this section of the tutorial:

    Project: {state.selected_project}
    Overview: {state.project_overview}

    Section: {section}

    Provide detailed explanations and keep the response under 1000 words.
    If this section involves code, provide a detailed code example with comments. The code should be complete, not half-done."""

    for attempt in range(3):  # Retry up to 3 times
        try:
            response = await mm_llm.acomplete(prompt=prompt, image_documents=[image_doc])
            content = response.text
            return {
                "section": section,
                "content": content
            }
        except Exception as e:
            logger.error(f"Attempt {attempt + 1} failed for section '{section}': {e}")
            if attempt == 2:
                return {
                    "section": section,
                    "content": f"Error generating content: {str(e)}"
                }
            await asyncio.sleep(2)  # Wait a bit before retrying

async def project_details_node(state: GraphState) -> Dict[str, str]:
    state.project_overview = await provide_project_details(state.selected_project, state.image_path)
    logger.debug(f"Project overview generated in node: {state.project_overview}")
    return {"project_overview": state.project_overview}

async def section_node(state: GraphState, section: str) -> Dict[str, str]:
    section_content = await generate_section_content(state, section)
    state.sections.append(section_content)
    state.current_section = section_content["section"]
    state.section_content = section_content["content"]
    logger.debug(f"Generated content for section {section}: {section_content['content']}")
    return {
        "current_section": state.current_section,
        "section_content": state.section_content
    }

async def section_1_node(state: GraphState) -> Dict[str, str]:
    return await section_node(state, "1. Introduction to the project")

async def section_2_node(state: GraphState) -> Dict[str, str]:
    return await section_node(state, "2. List of components and tools needed")

async def section_3_node(state: GraphState) -> Dict[str, str]:
    return await section_node(state, "3. Step-by-step instructions")

async def section_4_node(state: GraphState) -> Dict[str, str]:
    return await section_node(state, "4. Circuit diagram or wiring instructions")

async def section_5_node(state: GraphState) -> Dict[str, str]:
    return await section_node(state, "5. Code explanation")

async def section_6_node(state: GraphState) -> Dict[str, str]:
    return await section_node(state, "6. Troubleshooting guide")

async def section_7_node(state: GraphState) -> Dict[str, str]:
    return await section_node(state, "7. Safety precautions")

async def section_8_node(state: GraphState) -> Dict[str, str]:
    return await section_node(state, "8. Conclusion")

def define_guide_workflow() -> StateGraph:
    workflow = StateGraph(GraphState)

    workflow.add_node("project_details", project_details_node)
    workflow.add_node("section_1", section_1_node)
    workflow.add_node("section_2", section_2_node)
    workflow.add_node("section_3", section_3_node)
    workflow.add_node("section_4", section_4_node)
    workflow.add_node("section_5", section_5_node)
    workflow.add_node("section_6", section_6_node)
    workflow.add_node("section_7", section_7_node)
    workflow.add_node("section_8", section_8_node)
    
    workflow.set_entry_point("project_details")
    workflow.add_edge("project_details", "section_1")
    workflow.add_edge("section_1", "section_2")
    workflow.add_edge("section_2", "section_3")
    workflow.add_edge("section_3", "section_4")
    workflow.add_edge("section_4", "section_5")
    workflow.add_edge("section_5", "section_6")
    workflow.add_edge("section_6", "section_7")
    workflow.add_edge("section_7", "section_8")
    workflow.add_edge("section_8", END)

    return workflow
async def provide_project_details_service(project: str, image_path: str) -> AsyncGenerator[str, None]:
    initial_state = GraphState(
        image_path=image_path,
        project_ideas="",
        selected_project=project,
        project_overview="",
        gemini_tutorial="",
        sections=[]
    )

    workflow = define_guide_workflow().compile()

    async for state in workflow.astream(initial_state, stream_mode="updates"):
        state_dict = dict(state)
        logger.debug(f"Current state: {state_dict}")

        if "project_details" in state_dict and "project_overview" in state_dict["project_details"]:
            yield json.dumps({
                "project_overview": state_dict["project_details"]["project_overview"],
            }, indent=2)
        
        if "section_1" in state_dict and "section_content" in state_dict["section_1"]:
            
            yield json.dumps({
                "section": "1. Introduction to the project",
                "content": state_dict["section_1"]["section_content"]
            }, indent=2)
        
        if "section_2" in state_dict:
            yield json.dumps({
                "section": "2. List of components and tools needed",
                "content": state_dict["section_2"]["section_content"]
            }, indent=2)

        if "section_3" in state_dict:
            yield json.dumps({
                "section": "3. Step-by-step instructions",
                "content": state_dict["section_3"]["section_content"]
            }, indent=2)
        
        if "section_4" in state_dict:
            yield json.dumps({
                "section": "4. Circuit diagram or wiring instructions",
                "content": state_dict["section_4"]["section_content"]
            }, indent=2)
        
        if "section_5" in state_dict:
            yield json.dumps({
                "section": "5. Code explanation",
                "content": state_dict["section_5"]["section_content"]
            }, indent=2)
        
        if "section_6" in state_dict:
            yield json.dumps({
                "section": "6. Troubleshooting guide",
                "content": state_dict["section_6"]["section_content"]
            }, indent=2)
        
        if "section_7" in state_dict:
            yield json.dumps({
                "section": "7. Safety precautions",
                "content": state_dict["section_7"]["section_content"]
            }, indent=2)
        
        if "section_8" in state_dict:
            yield json.dumps({
                "section": "8. Conclusion",
                "content": state_dict["section_8"]["section_content"]
            }, indent=2)

        if state_dict.get("gemini_tutorial") == "Tutorial generation completed":
            break
