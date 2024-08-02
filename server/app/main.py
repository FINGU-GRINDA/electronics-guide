from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import image_analysis,tutorial_generate
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allows requests from this origin
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(image_analysis.router, prefix=settings.API_V1_STR)
app.include_router(tutorial_generate.router, prefix=settings.API_V1_STR)
