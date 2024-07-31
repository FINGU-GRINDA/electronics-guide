from fastapi import APIRouter, UploadFile, File, Form
from app.services.image_service import analyze_image, provide_project_details
from app.models.image import ImageAnalysisResponse, ProjectDetailsResponse
from app.workflows.image_workflow import handle_image_upload

router = APIRouter()

@router.post("/analyze_image/", response_model=ImageAnalysisResponse)
async def analyze_image_endpoint(file: UploadFile = File(...)):
    image_data = await file.read()
    return analyze_image(image_data)

@router.post("/project_details/", response_model=ProjectDetailsResponse)
async def project_details_endpoint(file: UploadFile = File(...), project: str = Form(...)):
    image_data = await file.read()
    return provide_project_details(project, image_data)

@router.post("/workflow/")
async def workflow_endpoint(file: UploadFile = File(...)):
    return await handle_image_upload(file)
