from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import StreamingResponse, FileResponse
from app.services.image_service import analyze_image, provide_project_details_service, save_image_to_temp_file
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

@router.post("/project_details/")
async def project_details_endpoint(project: str = Form(...), file: UploadFile = File(...)):
    image_data = await file.read()
    image_path = save_image_to_temp_file(image_data)

    def project_details_generator() -> Generator[str, None, None]:
        for step in provide_project_details_service(project, image_path):
            yield step
            yield "\n\n"

    return StreamingResponse(project_details_generator(), media_type="text/plain")

@router.get("/download_tutorial/")
async def download_tutorial():
    file_path = "project_tutorial.pdf"
    if os.path.exists(file_path):
        return FileResponse(file_path, filename="project_tutorial.pdf", media_type="application/pdf")
    else:
        raise HTTPException(status_code=404, detail="Tutorial PDF not found")
