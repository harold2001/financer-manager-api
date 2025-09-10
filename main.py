"""Main application entry point for Personal Finance Manager API"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import transaction, auth, user

app = FastAPI(
    title="Personal Finance Manager API 🚀",
    description="A comprehensive API for managing personal finances with Firebase authentication",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
