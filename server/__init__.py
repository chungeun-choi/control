from uvicorn import run
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from server.control_handler import router as control_router

# Initialize FastAPI application with metadata for title, description, and version
app = FastAPI(
    title="Example strategy module",  # Application title
    description="Example that strategy module for control task",  # Application description
    version="0.0.1",  # Version of the application
    docs_url="/docs"  # URL for the automatically generated documentation (Swagger UI)
)


@app.exception_handler(Exception)
async def custom_500_handler(request: Request, exc: Exception):
    """
    Custom handler for unhandled exceptions (HTTP 500).
    """
    error_message = str(exc)  # Convert the exception to a string for error logging

    # Return a JSON response with a 500 status code and error details
    return JSONResponse(
        status_code=500,
        content={
            "detail": "An internal server error occurred.",  # Generic error message
            "error_message": error_message,  # Specific error message for debugging
        }
    )


def create_app(host, port):
    """
    Function to create and run the FastAPI application with a specified host and port.
    """
    # Include the router for playbook control endpoints under the "/playbook" prefix
    app.include_router(control_router, prefix="/playbook", tags=["Playbook"])

    # Start the FastAPI application using Uvicorn's ASGI server
    run(app, host=host, port=port)
