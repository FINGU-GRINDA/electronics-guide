import logging
import re
from app.core.config import Settings
from app.utils import save_image_to_temp
from app.services.workflows.tools.tavily.tavily_tool_spec import ImageTavilyToolSpec
from llama_index.agent.openai import OpenAIAgent

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize the Tavily tool with the API key
tavily_tool = ImageTavilyToolSpec(api_key=Settings.TAVILY_API_KEY)

# Initialize the OpenAIAgent with the Tavily tool
agent = OpenAIAgent.from_tools(tavily_tool.to_tool_list())

async def fetch_relevant_image(section: str, project: str) -> str:
    """Fetch relevant image using Tavily search."""
    try:
        # Define search query based on section and project
        search_query = f"Find me relevant images for my project: {project} in this section: {section}"
        logger.debug(f"Search query: {search_query}")
        
        # Use the Tavily tool to perform the image search
        response = await agent.achat(search_query)
        
        # Check the type of response
        if isinstance(response.response, dict):
            # Log the full response for debugging
            response_dict = response.response
            logger.debug(f"Full Tavily search response: {response_dict}")

            # Extract image URLs directly from the 'images' field in the response
            image_urls = response_dict.get('images', [])
            logger.debug(f"Extracted image URLs: {image_urls}")

            for url in image_urls:
                # Check if the URL points to an image and save it
                if url.endswith(('.jpg', '.jpeg', '.png')):
                    logger.debug(f"Found image URL: {url}")
                    image_path = await save_image_to_temp(url)
                    return image_path
        
        elif isinstance(response.response, str):
            logger.debug(f"Textual response received: {response.response}")
            # Handle the case where the response is just a string message
            logger.error(f"No valid image URL found in the results for section '{section}'.")
            return ""
        
    except Exception as e:
        logger.error(f"Error fetching image for section '{section}': {e}")
        return ""