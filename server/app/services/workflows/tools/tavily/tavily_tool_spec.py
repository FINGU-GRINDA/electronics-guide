import logging
from typing import List, Optional
from llama_index.core.schema import Document
from llama_index.tools.tavily_research import TavilyToolSpec

logger = logging.getLogger(__name__)

class ImageTavilyToolSpec(TavilyToolSpec):
    """Extended Tavily tool spec to include an image-specific search."""

    def search_images(self, query: str, max_results: Optional[int] = 6) -> List[str]:
        """
        Run query through Tavily Search and return only image URLs.

        Args:
            query: The query to search for.
            max_results: The maximum number of results to return.

        Returns:
            image_urls: A list of image URLs.
        """
        # Perform the search with images included
        response = self.client.search(
            query, 
            max_results=max_results, 
            search_depth="advanced", 
            include_images=True  # Ensure images are included in the results
        )

        # Log the full response for debugging
        logger.debug(f"Full Tavily search response: {response}")

        # Extract and return only the image URLs
        image_urls = []
        for result in response.get("results", []):
            images = result.get("images", [])
            logger.debug(f"Images in result: {images}")
            image_urls.extend(images)

        logger.debug(f"Final extracted image URLs: {image_urls}")
        return image_urls
