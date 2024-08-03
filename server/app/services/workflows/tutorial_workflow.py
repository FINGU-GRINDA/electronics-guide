from langgraph.graph import StateGraph, END
from app.models.workflow import GraphState
from app.services.nodes import project_details_node, section_node

section_titles = [
    "1. Introduction to the project",
    "2. List of components and tools needed",
    "3. Step-by-step instructions",
    "4. Circuit diagram or wiring instructions",
    "5. Code explanation",
    "6. Troubleshooting guide",
    "7. Safety precautions",
    "8. Conclusion"
]

def define_guide_workflow() -> StateGraph:
    workflow = StateGraph(GraphState)
    workflow.add_node("project_details", project_details_node)
    
    for i, title in enumerate(section_titles, start=1):
        async def section_node_factory(state: GraphState, title=title):
            return await section_node(state, title)
        workflow.add_node(f"section_{i}", section_node_factory)

    workflow.set_entry_point("project_details")
    workflow.add_edge("project_details", "section_1")
    for i in range(1, len(section_titles)):
        workflow.add_edge(f"section_{i}", f"section_{i+1}")
    workflow.add_edge(f"section_{len(section_titles)}", END)

    return workflow
