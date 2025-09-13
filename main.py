"""Main application entry point for Personal Finance Manager API"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from routers import transaction, auth, user
import traceback

app = FastAPI(
    title="Personal Finance Manager API 🚀",
    description="A comprehensive API for managing personal finances with Firebase authentication",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],  # Specific origins for development
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],  # Allow all headers including Authorization
)


# Add global exception handler to ensure CORS headers are always present
@app.exception_handler(Exception)
async def global_exception_handler(_: Request, exc: Exception):
    """Global exception handler to ensure CORS headers are included in error responses"""
    print(f"Global exception caught: {type(exc).__name__}: {exc}")
    print(f"Traceback: {traceback.format_exc()}")

    response = JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"},
        headers={
            "Access-Control-Allow-Origin": "http://localhost:5173",
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        },
    )
    return response


# Include routers
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(transaction.router)


@app.get("/")
def root():
    """Root endpoint to check API status"""
    return {
        "message": "Personal Finance Manager API is running! 🚀",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "auth": "/auth",
            "users": "/users",
            "transactions": "/transactions",
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, log_level="info")
