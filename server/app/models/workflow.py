from typing import Dict, List, Optional

from pydantic import BaseModel


class GraphState(BaseModel):
    image_path: str
    project_ideas: str
    selected_project: str
    project_overview: str
    gemini_tutorial: str
    sections: List[Dict[str, str]] = []
    current_section: Optional[str] = None
    section_content: Optional[str] = None