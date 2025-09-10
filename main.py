"""Main application entry point for Personal Finance Manager API"""

from fastapi import FastAPI
from routers import transaction

app = FastAPI(title="Personal Finance Manager API 🚀")

app.include_router(transaction.router)

@app.get("/")
def root():
    """Root endpoint to check API status"""
    return {"message": "API is running"}
