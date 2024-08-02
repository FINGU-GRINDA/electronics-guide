from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import StreamingResponse, FileResponse
from app.services.tutorial_service import provide_project_details_service
from app.services.ideas_service import analyze_image, save_image_to_temp_file

from app.models.image import ImageAnalysisResponse, ProjectDetailsResponse
from typing import Generator
import os

router = APIRouter()

@router.post("/analyze_image/", response_model=ImageAnalysisResponse)
async def analyze_image_endpoint(file: UploadFile = File(...)):
    image_data = await file.read()
    response = analyze_image(image_data)
    if not response["project_ideas"]:
        raise HTTPException(status_code=500, detail="Failed to generate project ideas")
    return ImageAnalysisResponse(**response)

