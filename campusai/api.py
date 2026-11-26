"""HTTP API for the chat frontend.

Run locally with ``uvicorn campusai.api:app --reload``.
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import Literal

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from campusai import __version__
from campusai.config import Settings
from campusai.engine import Answer, CampusAI
from campusai.ratelimit import RateLimiter
from campusai.suggestions import get_suggestions

logger = logging.getLogger("campusai.api")

Language = Literal["auto", "en", "hi", "mr"]


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, description="The user's question.")
    language: Language = "auto"


class SourceOut(BaseModel):
    id: str
    document: str
    section: str
    text: str


class ChatResponse(BaseModel):
    answer: str
    status: Literal["answered", "not_found", "refused"]
    language: str
    confidence: float
    sources: list[SourceOut]
    reason: str | None = None


class HealthResponse(BaseModel):
    status: Literal["ok"]
    version: str
    sections: int
    languages: list[str]


def _to_response(answer: Answer) -> ChatResponse:
    return ChatResponse(
        answer=answer.text,
        status=answer.status,
        language=answer.lang,
        confidence=answer.confidence,
        reason=answer.reason,
        sources=[
            SourceOut(id=s.chunk_id, document=s.title, section=s.section_title, text=s.text)
            for s in answer.sources
        ],
    )


def _client_key(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def create_app(settings: Settings | None = None, bot: CampusAI | None = None) -> FastAPI:
    settings = settings or Settings.from_env()
    limiter = RateLimiter(settings.rate_limit_per_minute)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        app.state.bot = bot or CampusAI.from_directory(settings.docs_dir)
        yield

    app = FastAPI(title="CampusAI", version=__version__, lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_methods=["GET", "POST"],
        allow_headers=["Content-Type"],
    )

    @app.get("/health", response_model=HealthResponse)
    def health(request: Request) -> HealthResponse:
        engine: CampusAI = request.app.state.bot
        return HealthResponse(
            status="ok",
            version=__version__,
            sections=engine.section_count,
            languages=engine.languages,
        )

    @app.get("/suggestions", response_model=list[str])
    def suggestions(lang: Language = "en") -> list[str]:
        return get_suggestions("en" if lang == "auto" else lang)

    @app.post("/chat", response_model=ChatResponse)
    def chat(payload: ChatRequest, request: Request):
        if not limiter.allow(_client_key(request)):
            return JSONResponse(
                {"detail": "Too many requests. Please wait a minute and try again."},
                status_code=429,
                headers={"Retry-After": "60"},
            )
        if len(payload.message) > settings.max_message_length:
            limit = settings.max_message_length
            return JSONResponse(
                {"detail": f"Message is too long (limit {limit} characters)."}, status_code=422
            )
        lang = None if payload.language == "auto" else payload.language
        engine: CampusAI = request.app.state.bot
        return _to_response(engine.ask(payload.message, lang))

    return app


app = create_app()
