"""Global exception handlers for the API"""

import logging
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)

async def auth_exception_handler(request: Request, exc: HTTPException):
    """Handle authentication exceptions"""
    logger.error("Authentication error: %s", exc.detail)
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "Authentication failed",
            "message": exc.detail,
            "type": "auth_error"
        }
    )

async def validation_exception_handler(request: Request, exc: HTTPException):
    """Handle validation exceptions"""
    logger.error("Validation error: %s", exc.detail)
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "Validation failed",
            "message": exc.detail,
            "type": "validation_error"
        }
    )

async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    logger.error("Unexpected error: %s", str(exc))
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred",
            "type": "server_error"
        }
    )
