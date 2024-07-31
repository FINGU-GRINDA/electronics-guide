from typing import TypedDict

from fastapi import UploadFile
from fastapi.encoders import jsonable_encoder
from app.services.image_service import analyze_image, provide_project_details
from langgraph.graph import StateGraph, END


class GraphState(TypedDict):
    image_data: bytes
    project_ideas: list[str]
    selected_project: str
    tutorial: str

def define_workflow():
    workflow = StateGraph(GraphState)

    # Node 1: Image Analysis and Project Suggestions
    def image_analysis_node(state: GraphState) -> dict:
        state["project_ideas"] = analyze_image(state["image_data"]).project_ideas
        print("Image analysis completed. Project ideas generated.")
        return state

    # Node 2: Project Selection
    def project_selection_node(state: GraphState) -> dict:
        print("Project Ideas:")
        print(state["project_ideas"])

        selection = input("\nPlease select a project (1-4): ")

        state["selected_project"] = state["project_ideas"][int(selection) - 1]
        print(f"\nSelected Project: {state['selected_project']}")
        return state

    # Node 3: Project Implementation Details
    def project_details_node(state: GraphState) -> dict:
        state["tutorial"] = provide_project_details(state["selected_project"], state["image_data"]).tutorial
        print("Tutorial generation completed.")
        return state

    # Add nodes to the workflow
    workflow.add_node("image_analysis", image_analysis_node)
    workflow.add_node("project_selection", project_selection_node)
    workflow.add_node("project_details", project_details_node)

    # Define edges
    workflow.set_entry_point("image_analysis")
    workflow.add_edge("image_analysis", "project_selection")
    workflow.add_edge("project_selection", "project_details")
    workflow.add_edge("project_details", END)

    return workflow

async def handle_image_upload(file: UploadFile):
    image_data = await file.read()
    initial_state = GraphState(image_data=image_data, project_ideas=[], selected_project="", tutorial="")

    print("\nStarting workflow...")

    # Initialize and run the workflow
    workflow = define_workflow().compile()

    final_state = None
    for step, state in enumerate(workflow.stream(initial_state)):
        print(f"\nStep {step + 1} completed.")
        final_state = state

    return jsonable_encoder(final_state)