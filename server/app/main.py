from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from app.api.routes import image_analysis, tutorial_generate
from app.core.config import settings
from app.shared_resources import shutdown_event

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application startup.")
    yield
    logger.info("Application shutdown. Stopping ongoing tasks...")
    shutdown_event.set()

# Initialize FastAPI application
app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://edison-client.192.3.155.238.sslip.io"],  # Allows requests from this origin
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(image_analysis.router, prefix=settings.API_V1_STR)
app.include_router(tutorial_generate.router, prefix=settings.API_V1_STR)
