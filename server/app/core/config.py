import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Electronics Project Generator"
    API_V1_STR: str = "/api/v1"
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "default_value")  # Provide a default value if the key is not found
    AI71_API_KEY: str = os.getenv("AI71_API_KEY", "")
    TAVILY_API_KEY : str = os.getenv("TAVILY_API_KEY","")

settings = Settings()
