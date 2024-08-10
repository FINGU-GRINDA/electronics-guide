import logging
from llama_index.multi_modal_llms.gemini import GeminiMultiModal
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from app.core.config import settings


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)




client = GeminiMultiModal(model_name="models/gemini-1.5-flash-latest", temperature=0.7, api_key=settings.GOOGLE_API_KEY,safety_settings=
                          
                          { HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT:HarmBlockThreshold.BLOCK_NONE
        
        }
                          
                          )

