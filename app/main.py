"""Main Application"""

from fastapi import FastAPI

app = FastAPI()

@app.get("/", tags=["Health Check"])
async def health_check():
    """
    Endpoint for checking the health status of the API service.

    Returns:
        str: A message indicating that the API service is up and running.

    """
    return "API Service is up and running!"
