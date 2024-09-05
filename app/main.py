"""Main Application"""

from fastapi import FastAPI

from routers import auth, company, task, user

app = FastAPI()

if(auth.router):
    app.include_router(auth.router)

app.include_router(company.router)
app.include_router(task.router)
app.include_router(user.router)

@app.get("/", tags=["Health Check"])
async def health_check():
    """
    Endpoint for checking the health status of the API service.

    Returns:
        str: A message indicating that the API service is up and running.

    """
    return "API Service is up and running!"
