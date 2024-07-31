from pydantic import BaseModel

class ImageAnalysisRequest(BaseModel):
    file: bytes

class ImageAnalysisResponse(BaseModel):
    project_ideas: list[str]

class ProjectDetailsResponse(BaseModel):
    tutorial: str
