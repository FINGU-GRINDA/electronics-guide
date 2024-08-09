import logging
from llama_index.multi_modal_llms.gemini import GeminiMultiModal
from app.core.config import settings
from llama_index.core.schema import ImageDocument
from langchain.schema import HumanMessage, SystemMessage


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

from ai71 import AI71


client = AI71(settings.AI71_API_KEY)

# mm_llm = GeminiMultiModal(model_name="models/gemini-1.5-flash-latest", temperature=0.7, api_key=settings.GOOGLE_API_KEY)


async def provide_project_details(project: str) -> str:
    response = client.chat.completions.create(
        model="tiiuae/falcon-180B-chat",
        messages=[
            {"role": "system", "content": """
 You are a helpful assistant. 
             Answer in details and keep the response under 1000 words.
             You're an expert in electronics and you're helping a beginner understand how to implement a project.

           
"""},
            {"role": "user", "content": f"""Provide a brief overview of how to implement this electronic project: {project}
              Include:
            1. A list of main components needed
            2. Basic steps to connect the components
            3. A brief description of how the project works
           
             """}
        ],
        max_tokens=1000,
        temperature=0.7,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    
    return response.choices[0].message.content
