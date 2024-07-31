import os
from llama_index.multi_modal_llms.gemini import GeminiMultiModal
from llama_index.core.schema import ImageDocument
from app.models.image import ImageAnalysisResponse, ProjectDetailsResponse
from app.utils import save_image_to_temp_file
from langgraph.graph import StateGraph, END
from typing import TypedDict
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize Gemini Multi Modal
os.environ["GOOGLE_API_KEY"] = "AIzaSyAkVA-oDthTPC5CAKvokSgEg0y8OnQRhJQ"

# Initialize Gemini Multi Modal
mm_llm = GeminiMultiModal(model_name="models/gemini-1.5-flash")

class GraphState(TypedDict):
    image_path: str
    project_ideas: str
    selected_project: str
    tutorial_step1: str
    tutorial_step2: str
    tutorial_step3: str
    tutorial_step4: str
    current_step: int

def analyze_image_and_suggest_projects(image_path: str) -> str:
    image_doc = ImageDocument(image_path=image_path)
    response = mm_llm.complete(
        prompt="""Analyze this image of electronic parts and provide the following:
        1. A list of all identifiable electronic components in the image.
        2. Suggest 4 project ideas that can be created with these components. Number each idea from 1 to 4.
        
        Format your response as follows:
        Components:
        - [List of components]

        Project Ideas:
        1. [Project 1]
        2. [Project 2]
        3. [Project 3]
        4. [Project 4]
        """,
        image_documents=[image_doc]
    )
    return response.text

def provide_project_details_step(step: int, project: str) -> str:
    step_prompts = [
        f"""Step 1: Give general information about the following project: {project}. Include a brief description of the project and the purpose of each component.""",
        f"""Step 2: Provide detailed instructions on how to connect and use each component for the following project: {project}.""",
        f"""Step 3: Provide a sample code (if applicable) to make the project work for the following project: {project}. Include explanations for each part of the code.""",
        f"""Step 4: Provide any safety precautions or tips for successful implementation, and possible variations or extensions of the following project: {project}."""
    ]

    response = mm_llm.complete(
        prompt=step_prompts[step - 1],
        image_documents=[]
    )
    return response.text

def define_guide_workflow():
    workflow = StateGraph(GraphState)

    def project_details_step1_node(state: GraphState) -> dict:
        logger.debug(f"Executing project_details_step1_node with initial state: {state}")
        state["tutorial_step1"] = provide_project_details_step(1, state["selected_project"])
        state["current_step"] = 2
        logger.debug(f"State after project_details_step1_node: {state}")
        return state

    def project_details_step2_node(state: GraphState) -> dict:
        logger.debug(f"Executing project_details_step2_node with initial state: {state}")
        state["tutorial_step2"] = provide_project_details_step(2, state["selected_project"])
        state["current_step"] = 3
        logger.debug(f"State after project_details_step2_node: {state}")
        return state

    def project_details_step3_node(state: GraphState) -> dict:
        logger.debug(f"Executing project_details_step3_node with initial state: {state}")
        state["tutorial_step3"] = provide_project_details_step(3, state["selected_project"])
        state["current_step"] = 4
        logger.debug(f"State after project_details_step3_node: {state}")
        return state

    def project_details_step4_node(state: GraphState) -> dict:
        logger.debug(f"Executing project_details_step4_node with initial state: {state}")
        state["tutorial_step4"] = provide_project_details_step(4, state["selected_project"])
        state["current_step"] = END
        logger.debug(f"State after project_details_step4_node: {state}")
        return state

    workflow.add_node("project_details_step1", project_details_step1_node)
    workflow.add_node("project_details_step2", project_details_step2_node)
    workflow.add_node("project_details_step3", project_details_step3_node)
    workflow.add_node("project_details_step4", project_details_step4_node)
    workflow.set_entry_point("project_details_step1")

    workflow.add_edge("project_details_step1", "project_details_step2")
    workflow.add_edge("project_details_step2", "project_details_step3")
    workflow.add_edge("project_details_step3", "project_details_step4")
    workflow.add_edge("project_details_step4", END)

    return workflow

def define_idea_workflow():
    workflow = StateGraph(GraphState)

    def image_analysis_node(state: GraphState) -> dict:
        logger.debug(f"Executing image_analysis_node with initial state: {state}")
        if not state["project_ideas"]:
            state["project_ideas"] = analyze_image_and_suggest_projects(state["image_path"])
        logger.debug(f"State after image_analysis_node: {state}")
        return state

    def project_selection_node(state: GraphState) -> dict:
        logger.debug(f"Executing project_selection_node with initial state: {state}")
        project_ideas = state["project_ideas"].split("Project Ideas:")[1].strip().split('\n')
        selected_project_index = int(state["selected_project"]) - 1  # Convert to zero-based index
        state["selected_project"] = project_ideas[selected_project_index].strip()
        logger.debug(f"State after project_selection_node: {state}")
        return state

    workflow.add_node("image_analysis", image_analysis_node)
    workflow.add_node("project_selection", project_selection_node)
    workflow.set_entry_point("image_analysis")

    workflow.add_edge("image_analysis", "project_selection")
    workflow.add_edge("project_selection", END)

    return workflow

def analyze_image(image_data: bytes) -> ImageAnalysisResponse:
    image_path = save_image_to_temp_file(image_data)
    initial_state = GraphState(
        image_path=image_path, 
        project_ideas="", 
        selected_project="", 
        tutorial_step1="", 
        tutorial_step2="", 
        tutorial_step3="", 
        tutorial_step4="", 
        current_step=0
    )
    workflow = define_idea_workflow().compile()

    state = initial_state
    for output in workflow.stream(state):
        logger.debug(f"Workflow output: {output}")
        if isinstance(output, dict) and 'image_analysis' in output:
            state = output['image_analysis']
            break

    logger.info(f"Final state after image analysis: {state}")

    if "project_ideas" not in state or not state["project_ideas"]:
        logger.error("No project ideas generated")
        return ImageAnalysisResponse(components=[], project_ideas=[])

    try:
        parts = state["project_ideas"].split("Project Ideas:")
        if len(parts) != 2:
            logger.error(f"Unexpected format in project_ideas: {state['project_ideas']}")
            return ImageAnalysisResponse(components=[], project_ideas=[])

        components, projects = parts

        components = [comp.strip() for comp in components.split("Components:")[1].strip().split("-") if comp.strip()]

        project_ideas = [idea.strip() for idea in projects.strip().split("\n") if idea.strip()]

        return ImageAnalysisResponse(components=components, project_ideas=project_ideas)
    except Exception as e:
        logger.exception("Error parsing project ideas")
        return ImageAnalysisResponse(components=[], project_ideas=[])

def provide_project_details_service(project: str):
    initial_state = GraphState(
        image_path="",  # This is not needed for project details
        project_ideas="",
        selected_project=project,
        tutorial_step1="",
        tutorial_step2="",
        tutorial_step3="",
        tutorial_step4="",
        current_step=1
    )
    workflow = define_guide_workflow().compile()

    logger.info(f"Initial state: {initial_state}")

    state = initial_state

    def update_state(src: dict, dst: dict):
        for key, value in src.items():
            dst[key] = value

    for output in workflow.stream(state):
        logger.debug(f"Workflow output: {output}")
        if isinstance(output, dict):
            if 'project_details_step1' in output and state["current_step"] == 1:
                update_state(output['project_details_step1'], state)
                state["current_step"] = 2
                yield state["tutorial_step1"]
            elif 'project_details_step2' in output and state["current_step"] == 2:
                update_state(output['project_details_step2'], state)
                state["current_step"] = 3
                yield state["tutorial_step2"]
            elif 'project_details_step3' in output and state["current_step"] == 3:
                update_state(output['project_details_step3'], state)
                state["current_step"] = 4
                yield state["tutorial_step3"]
            elif 'project_details_step4' in output and state["current_step"] == 4:
                update_state(output['project_details_step4'], state)
                state["current_step"] = END
                yield state["tutorial_step4"]

    logger.info(f"Final state after providing project details: {state}")
