import logging
from llama_index.multi_modal_llms.gemini import GeminiMultiModal
from app.core.config import settings
from llama_index.core.schema import ImageDocument

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

mm_llm = GeminiMultiModal(model_name="models/gemini-1.5-flash-latest", temperature=0.7, api_key=settings.GOOGLE_API_KEY)

async def provide_project_details(project: str, image_path: str) -> str:
    image_doc = ImageDocument(image_path=image_path)
    response = await mm_llm.acomplete(
        prompt=f"""Provide a brief overview of how to implement this electronic project: {project}
        Include:
        1. A list of main components needed
        2. Basic steps to connect the components
        3. A brief description of how the project works
        Keep the response under 300 words.""",
        image_documents=[image_doc]
    )
    return response.text
