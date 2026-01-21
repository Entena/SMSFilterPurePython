from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import logging
from .routers import sms_filter
from settings import get_settings

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Loading tokenizer...")
    app.state.tokenizer = AutoTokenizer.from_pretrained(
        "Qwen/Qwen3Guard-Gen-0.6B",
    )
    logging.info("Tokenizer loaded.")
    logging.info("Loading model...")
    app.state.model = AutoModelForCausalLM.from_pretrained(
        "Qwen/Qwen3Guard-Gen-0.6B",
        dtype=torch.bfloat16,
        device_map="auto",
    )
    logging.info("Model loaded.")
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="SMS Filter",
        description="API for using the SMS Filter tool.",
        version="0.0.2",
        lifespan=lifespan,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(sms_filter.router, prefix="/api", tags=["SMS Filter"])
    return app


app = create_app()
