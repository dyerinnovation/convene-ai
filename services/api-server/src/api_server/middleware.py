"""CORS middleware configuration for the API server."""

from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi.middleware.cors import CORSMiddleware

from api_server.deps import get_settings

if TYPE_CHECKING:
    from fastapi import FastAPI


def setup_cors(app: FastAPI) -> None:
    """Add CORS middleware to the FastAPI application.

    Reads allowed origins from application settings and configures
    the middleware to allow credentials, all methods, and all headers.

    Args:
        app: The FastAPI application instance.
    """
    settings = get_settings()
    origins = [origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
