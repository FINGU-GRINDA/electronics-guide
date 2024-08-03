import json
import logging
import base64
import asyncio
from typing import Dict, AsyncGenerator, List, Optional
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import StreamingResponse, FileResponse
from pydantic import BaseModel
from app.models.workflow import GraphState
from .workflows.tutorial_workflow import define_guide_workflow, section_titles

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def encode_image(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

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
            yield json.dumps({"project_overview": state_dict["project_details"]["project_overview"]}, indent=2)
        
        for i, title in enumerate(section_titles, start=1):
            if f"section_{i}" in state_dict:
                yield json.dumps({"section": title, "content": state_dict[f"section_{i}"]["section_content"]}, indent=2)

        if state_dict.get("gemini_tutorial") == "Tutorial generation completed":
            break
