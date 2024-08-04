import asyncio
import json
import os
from fastapi import APIRouter, HTTPException, Request, UploadFile, File, Form, logger
from fastapi.responses import StreamingResponse, FileResponse
from app.services.ideas_service import analyze_image, save_image_to_temp_file
from app.models.image import ProjectOverviewResponse, SectionContentResponse, FullTutorialResponse
from typing import Generator

from pydantic import BaseModel
import asyncio
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from app.services.ideas_service import analyze_image, save_image_to_temp_file
from app.models.image import ProjectOverviewResponse, SectionContentResponse, FullTutorialResponse
from typing import AsyncGenerator

from pydantic import BaseModel

from app.services.workflows.tutorial_workflow import generate_section_content, provide_project_details, provide_project_details_service

router = APIRouter()

class SectionContentResponse(BaseModel):
    section: str
    content: str

# Access the shutdown event from the main application module
from app.shared_resources import shutdown_event



@router.post("/project_details/")
async def project_details_endpoint(request: Request, project: str = Form(...)):

    async def generate() -> AsyncGenerator[str, None]:
        async for section_json in provide_project_details_service(project):
            if await request.is_disconnected():
                logger.info("Client disconnected, stopping the generator.")
                break
            yield f"{section_json}\n"
            await asyncio.sleep(0.1)  # Small delay to prevent overwhelming the client

    return StreamingResponse(generate(), media_type="application/x-ndjson")
@router.get("/download_tutorial/")
async def download_tutorial():
    file_path = "project_tutorial.pdf"
    if os.path.exists(file_path):
        return FileResponse(file_path, filename="project_tutorial.pdf", media_type="application/pdf")
    else:
        raise HTTPException(status_code=404, detail="Tutorial PDF not found")
