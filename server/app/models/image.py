from pydantic import BaseModel

class ImageAnalysisRequest(BaseModel):
    file: bytes
from pydantic import BaseModel

from pydantic import BaseModel

class ImageAnalysisResponse(BaseModel):
    components: list[str]
    project_ideas: list[str]
class ProjectDetailsResponse(BaseModel):
    tutorial: str
