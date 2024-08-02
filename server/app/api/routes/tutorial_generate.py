import os
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import StreamingResponse, FileResponse
from app.services.tutorial_service import provide_project_details_service
from app.services.ideas_service import analyze_image, save_image_to_temp_file

from app.models.image import ImageAnalysisResponse, ProjectDetailsResponse
from typing import Generator
router = APIRouter()

@router.post("/project_details/")
async def project_details_endpoint(project: str = Form(...), file: UploadFile = File(...)):
    image_data = await file.read()
    image_path = save_image_to_temp_file(image_data)

    return StreamingResponse(provide_project_details_service(project, image_path), media_type="application/json")
@router.get("/download_tutorial/")
async def download_tutorial():
    file_path = "project_tutorial.pdf"
    if os.path.exists(file_path):
        return FileResponse(file_path, filename="project_tutorial.pdf", media_type="application/pdf")
    else:
        raise HTTPException(status_code=404, detail="Tutorial PDF not found")
