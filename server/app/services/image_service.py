import os
from llama_index.multi_modal_llms.gemini import GeminiMultiModal
from llama_index.core.schema import ImageDocument
from app.models.image import ImageAnalysisResponse, ProjectDetailsResponse
from app.core.config import settings
from PIL import Image
import io
import tempfile

# Initialize Gemini Multi Modal
mm_llm = GeminiMultiModal(model_name="models/gemini-1.5-flash")

def save_image_to_temp_file(image_data: bytes) -> str:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
        image = Image.open(io.BytesIO(image_data))
        image.save(temp_file, format="PNG")
        return temp_file.name

def analyze_image(image_data: bytes) -> ImageAnalysisResponse:
    image_path = save_image_to_temp_file(image_data)
    image_doc = ImageDocument(image_path=image_path)
    response = mm_llm.complete(
        prompt="Analyze this image of electronic parts and suggest 4 unique project ideas that can be created with these components. Number each idea from 1 to 4.",
        image_documents=[image_doc]
    )
    project_ideas = response.text.split('\n')
    return ImageAnalysisResponse(project_ideas=project_ideas)

def provide_project_details(project: str, image_data: bytes) -> ProjectDetailsResponse:
    image_path = save_image_to_temp_file(image_data)
    image_doc = ImageDocument(image_path=image_path)
    response = mm_llm.complete(
        prompt=f"""Provide a detailed, step-by-step tutorial for implementing the following electronic project: {project}
        Include the following:
        1. A list of all components needed in details and models (if applicable)
        2. Detailed instructions on how to connect and use each component
        3. A detailed code in steps (if applicable) to make the project work
        4. Any safety precautions or tips for successful implementation
        5. Possible variations or extensions of the project

        Base your tutorial on the components visible in the provided image.""",
        image_documents=[image_doc]
    )
    return ProjectDetailsResponse(tutorial=response.text)
