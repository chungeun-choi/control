import traceback
from uvicorn import run
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from server.control_handler import router as control_router

app = FastAPI(
    title="Example strategy module",
    description="Example that strategy module for control task",
    version="0.0.1",
    docs_url="/docs"
)


@app.exception_handler(Exception)
async def custom_500_handler(request: Request, exc: Exception):
    error_message = str(exc)

    return JSONResponse(
        status_code=500,
        content={
            "detail": "An internal server error occurred.",
            "error_message": error_message,
        }
    )


def create_app(host, port):
    app.include_router(control_router, prefix="/playbook", tags=["Playbook"])
    run(app, host=host, port=port)
