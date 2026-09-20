from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.query import router
from app.core.config import settings
from app.services.retrieval import RetrievalService
from app.services.generation import GenerationService
from app.utils.logging_config import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):

    setup_logging()

    print("Starting UniGuide AI backend...")

    # Load services once when the application starts.
    app.state.retrieval_service = RetrievalService()
    app.state.generation_service = GenerationService()

    print("Retrieval service loaded.")
    print("Generation service loaded.")
    print(
        f"Loaded Chroma collection: "
        f"{settings.chroma_collection}"
    )

    yield

    print("UniGuide AI backend stopped.")


app = FastAPI(
    title="UniGuide AI API",
    description="RAG-powered university information assistant",
    version="1.0.0",
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.frontend_origin
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(router)