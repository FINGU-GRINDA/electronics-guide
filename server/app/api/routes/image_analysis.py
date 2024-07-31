from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from app.services.image_service import analyze_image, provide_project_details_service
from app.models.image import ImageAnalysisResponse, ProjectDetailsResponse
from typing import Generator

router = APIRouter()

@router.post("/analyze_image/", response_model=ImageAnalysisResponse)
async def analyze_image_endpoint(file: UploadFile = File(...)):
    image_data = await file.read()
    response = analyze_image(image_data)
    print(f"Response to client: {response}")
    if not response.project_ideas:
        raise HTTPException(status_code=500, detail="Failed to generate project ideas")
    return response

@router.post("/project_details/", response_model=ProjectDetailsResponse)
async def project_details_endpoint(project: str = Form(...)):
    def project_details_generator() -> Generator[str, None, None]:
        for step in provide_project_details_service(project):
            if isinstance(step, dict):
                yield str(step)
            else:
                yield step
            yield "\n\n"

    return StreamingResponse(project_details_generator(), media_type="text/plain")
