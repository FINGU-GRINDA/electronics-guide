import json
import os
from typing import List, TypedDict, Generator
from llama_index.multi_modal_llms.gemini import GeminiMultiModal
from llama_index.core.schema import ImageDocument
from langgraph.graph import StateGraph, END
import logging
import markdown
import pdfkit
from jinja2 import Template
import base64

from app.utils import save_image_to_temp_file

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

os.environ["GOOGLE_API_KEY"] = "AIzaSyAkVA-oDthTPC5CAKvokSgEg0y8OnQRhJQ"

# Initialize models
mm_llm = GeminiMultiModal(model_name="models/gemini-1.5-flash-latest" , temperature=0.7)

# Function to encode image to base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Agent 1: Image Analysis and Project Ideas
def analyze_image_and_suggest_projects(image_path: str) -> str:
    logger.debug(f"Analyzing image: {image_path}")
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


# Agent 2: Project Implementation Details
def provide_project_details(project: str, image_path: str) -> str:
    print(f"Generating tutorial for project: {project}")
    image_doc = ImageDocument(image_path=image_path)
    response = mm_llm.complete(
        prompt=f"""Provide a brief overview of how to implement this electronic project: {project}
        Include:
        1. A list of main components needed
        2. Basic steps to connect the components
        3. A brief description of how the project works

        Keep the response under 300 words.""",
        image_documents=[image_doc]
    )
    return response.text

# Agent 3: Gemini Tutorial Generator
def generate_gemini_tutorial(project: str, overview: str, image_path: str) -> str:
    image_doc = ImageDocument(image_path=image_path)
    sections = [
        "1. Introduction to the project",
        "2. List of components and tools needed",
        "3. Step-by-step instructions",
        "4. Circuit diagram or wiring instructions",
        "5. Code explanation",
        "6. Troubleshooting guide",
        "7. Safety precautions",
        "8. Conclusion"
    ]

    full_tutorial = f"# {project}\n\n"

    for section in sections:
        prompt = f"""Based on the following project and overview, generate content for this section of the tutorial:

        Project: {project}
        Overview: {overview}

        Section: {section}

        Provide detailed explanations and keep the response under 500 words.
        If this section involves code, provide a detailed code example with comments."""

        response = mm_llm.complete(prompt=prompt, image_documents=[image_doc])
        content = response.text

        full_tutorial += f"\n\n## {section}\n\n{content}"

    return full_tutorial


# Function to save tutorial as PDF
def save_tutorial_as_pdf(tutorial: str, filename: str, image_path: str):
    # Convert Markdown to HTML
    html = markdown.markdown(tutorial, extensions=['codehilite', 'fenced_code'])

    # Create a template for the PDF
    template = Template('''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>{{ project_title }}</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }
            h1 { color: #2c3e50; border-bottom: 2px solid #2c3e50; padding-bottom: 10px; font-size: 16px; }
            h2 { color: #34495e; margin-top: 30px; font-size: 16px; }
            p { font-size: 12px; }
            pre { background-color: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }
            code { font-family: Consolas, Monaco, 'Andale Mono', monospace; white-space: pre-wrap; word-wrap: break-word; font-size: 12px; }
            img { max-width: 100%; height: auto; }
            .page-break { page-break-after: always; }
        </style>
    </head>
    <body>
        <h1>{{ project_title }}</h1>
        <img src="data:image/png;base64,{{ input_image }}" alt="Input Image">
        {{ content | safe }}
    </body>
    </html>
    ''')

    # Render the template
    project_title = tutorial.split('\n')[0].strip('# ')
    input_image = encode_image(image_path)
    rendered_html = template.render(content=html, project_title=project_title, input_image=input_image)

    # Specify the path to the wkhtmltopdf executable
    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'

    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    # Convert HTML to PDF
  # Convert HTML to PDF
    pdfkit.from_string(rendered_html, filename, options={
        'page-size': 'A4',
        'margin-top': '20mm',
        'margin-right': '20mm',
        'margin-bottom': '20mm',
        'margin-left': '20mm',
        'encoding': "UTF-8",
        'custom-header': [('Accept-Encoding', 'gzip')],
        'no-outline': None
    }, configuration=config)

class GraphState(TypedDict):
    image_path: str
    project_ideas: str
    selected_project: str
    project_overview: str
    # tutorial_step1: str
    # tutorial_step2: str
    # tutorial_step3: str
    # tutorial_step4: str
    # current_step: int

# Define the idea workflow
def define_idea_workflow():
    workflow = StateGraph(GraphState)

    def image_analysis_node(state: GraphState) -> dict:
        logger.debug(f"Executing image_analysis_node with initial state: {state}")
        if not state["project_ideas"]:
            state["project_ideas"] = analyze_image_and_suggest_projects(state["image_path"])
        logger.debug(f"State after image_analysis_node: {state}")
        return state

    workflow.add_node("image_analysis", image_analysis_node)
    workflow.set_entry_point("image_analysis")
    workflow.add_edge("image_analysis", END)

    return workflow
from langgraph.graph import END

def define_guide_workflow():
    workflow = StateGraph(GraphState)

   # Node 3: Project Implementation Details
    def project_details_node(state: GraphState) -> dict:
        state["project_overview"] = provide_project_details(state["selected_project"], state["image_path"])
        print("Project overview generated.")
        return state

    # Node 4: Gemini Tutorial Generation
    def gemini_tutorial_generation_node(state: GraphState) -> dict:
        state["gemini_tutorial"] = generate_gemini_tutorial(state["selected_project"], state["project_overview"], state["image_path"])
        print("Gemini tutorial generation completed.")
        save_tutorial_as_pdf(state["gemini_tutorial"], "project_tutorial.pdf", state["image_path"])
        print("Tutorial saved as PDF.")
        return state
    workflow.add_node("project_details", project_details_node)
    workflow.add_node("gemini_tutorial_generation", gemini_tutorial_generation_node)
    workflow.set_entry_point("project_details")

    workflow.add_edge("project_details", "gemini_tutorial_generation")
    workflow.add_edge("gemini_tutorial_generation", END)
    return workflow

def analyze_image(image_data: bytes) -> dict:
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

    final_state = None
    for output in workflow.stream(initial_state):
        final_state = output

    logger.info(f"Final state after image analysis: {final_state}")

    if not final_state or 'image_analysis' not in final_state:
        logger.error("No image analysis result")
        return {"components": [], "project_ideas": []}

    image_analysis = final_state['image_analysis']

    if "project_ideas" not in image_analysis or not image_analysis["project_ideas"]:
        logger.error("No project ideas generated")
        return {"components": [], "project_ideas": []}

    try:
        parts = image_analysis["project_ideas"].split("Project Ideas:")
        if len(parts) != 2:
            logger.error(f"Unexpected format in project_ideas: {image_analysis['project_ideas']}")
            return {"components": [], "project_ideas": []}

        components, projects = parts

        components = [comp.strip() for comp in components.split("Components:")[1].strip().split("-") if comp.strip()]
        project_ideas = [idea.strip() for idea in projects.strip().split("\n") if idea.strip()]

        return {"components": components, "project_ideas": project_ideas}
    except Exception as e:
        logger.exception("Error parsing project ideas")
        return {"components": [], "project_ideas": []}

def provide_project_details_service(project: str, image_path: str) -> Generator[str, None, None]:
    initial_state = GraphState(
        image_path=image_path,
        project_ideas="",
        selected_project=project,
        project_overview="",
        gemini_tutorial="",
    )

    print("\nStarting workflow...")

    workflow = define_guide_workflow().compile()
    final_state = None

    for step, state in enumerate(workflow.stream(initial_state)):
        print(f"\nStep {step + 1} completed.")
        
        # Collect the current state details to yield
        state_details = {key: (value[:100] + '...' if isinstance(value, str) and len(value) > 100 else value)
                         for key, value in state.items()}
        
        yield json.dumps({
            "step": step + 1,
            "state_details": state_details
        })

        final_state = state

    print("\nWorkflow completed. Final state:")
    for key, value in final_state.items():
        if isinstance(value, str) and len(value) > 100:
            print(f"{key}: {value[:100]}...")
        else:
            print(f"{key}: {value}")

    print("\nWorkflow completed. Check 'project_tutorial.pdf' for the detailed tutorial.")

    # Ensure the final state is also yielded in the same format
    final_state_details = {key: (value[:100] + '...' if isinstance(value, str) and len(value) > 100 else value)
                           for key, value in final_state.items()}
    
    yield json.dumps({
        "final_state": final_state_details
    })