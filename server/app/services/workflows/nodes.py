import logging
import asyncio
from typing import Dict
from llama_index.core.schema import ImageDocument
from app.models.workflow import GraphState
from .llm import mm_llm, provide_project_details

logger = logging.getLogger(__name__)

async def generate_section_content(state: GraphState, section: str) -> Dict[str, str]:
    image_doc = ImageDocument(image_path=state.image_path)
    prompt = f"""Based on the following project and overview, generate content for this section of the tutorial:
    Project: {state.selected_project}
    Overview: {state.project_overview}
    Section: {section}
    Provide detailed explanations and keep the response under 1000 words.
    Format the response in modern, styled HTML. Use advanced HTML5 and CSS3 techniques to ensure a polished and professional look.
    If this section involves code, provide a detailed code example with comments. The code should be complete, not half-done."""

    for attempt in range(3):
        try:
            response = await mm_llm.acomplete(prompt=prompt, image_documents=[image_doc])
            return {"section": section, "content": response.text}
        except Exception as e:
            logger.error(f"Attempt {attempt + 1} failed for section '{section}': {e}")
            if attempt == 2:
                return {"section": section, "content": f"Error generating content: {str(e)}"}
            await asyncio.sleep(2)

async def project_details_node(state: GraphState) -> Dict[str, str]:
    state.project_overview = await provide_project_details(state.selected_project, state.image_path)
    logger.debug(f"Project overview generated in node: {state.project_overview}")
    return {"project_overview": state.project_overview}

async def section_node(state: GraphState, section: str) -> Dict[str, str]:
    section_content = await generate_section_content(state, section)
    state.sections.append(section_content)
    state.current_section = section_content["section"]
    state.section_content = section_content["content"]
    logger.debug(f"Generated content for section {section}: {section_content['content']}")
    return {"current_section": state.current_section, "section_content": state.section_content}
