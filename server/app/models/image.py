from pydantic import BaseModel
from typing import List

class ImageAnalysisResponse(BaseModel):
    components: List[str]
    project_ideas: List[str]

class ProjectDetailsResponse(BaseModel):
    content: str


class ProjectOverviewResponse(BaseModel):
    image_path: str
    project_ideas: List[str]
    selected_project: str
    project_overview: str
    gemini_tutorial: str

class SectionContentResponse(BaseModel):
    current_section: str
    section_content: str

class FullTutorialResponse(BaseModel):
    project_overview: str
    section_content: str
