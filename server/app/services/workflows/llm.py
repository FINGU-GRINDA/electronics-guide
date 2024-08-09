import logging
from llama_index.multi_modal_llms.gemini import GeminiMultiModal
from app.core.config import settings
from llama_index.core.schema import ImageDocument
from langchain.schema import HumanMessage, SystemMessage


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)




client = GeminiMultiModal(model_name="models/gemini-1.5-flash-latest", temperature=0.7, api_key=settings.GOOGLE_API_KEY)


async def provide_project_details(project: str) -> str:
    prompt = """
         You're an expert in electronics and you're helping a beginner understand how to implement a project by creating a book.
          Provide a brief overview of how to implement this electronic project: {project}

            Include:
            1. A list of main components needed
            2. Basic steps to connect the components
            3. A brief description of how the project works
            4. Answer in details and keep the response under 1000 words.

"""
    response = client.acomplete(
   prompt=prompt,
   image_documents=[],
    )
    
    return response.text
