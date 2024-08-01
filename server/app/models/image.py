from pydantic import BaseModel
from typing import List

class ImageAnalysisResponse(BaseModel):
    components: List[str]
    project_ideas: List[str]

class ProjectDetailsResponse(BaseModel):
    content: str