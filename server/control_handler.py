import uuid
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional, Dict
from executor.playbook import ExecuteController

# Initialize FastAPI router
router = APIRouter()

# Dictionary to store active playbook executors by their unique ID
executors: Dict[str, ExecuteController] = {}


# Pydantic model to validate playbook request data
class PlaybookRequest(BaseModel):
    playbook: List[str]  # List of playbook paths
    inventory: str  # Path to the inventory file
    passwords: Optional[dict] = None  # Optional passwords for the playbook


@router.post("/run/")
def run_playbook(request: PlaybookRequest, background_tasks: BackgroundTasks):
    """
    Endpoint to execute an Ansible playbook in the background.

    Args:
        request (PlaybookRequest): Request body containing playbook, inventory, and optional passwords.
        background_tasks (BackgroundTasks): Background task handler to run playbook asynchronously.

    Returns:
        dict: A success message with the executor ID.
    """
    # Generate a unique ID for the executor
    executor_id = str(uuid.uuid4())

    # Create an ExecuteController instance for the playbook
    executor = ExecuteController(
        playbook=request.playbook,
        inventory=request.inventory,
        passwords=request.passwords,
        executor_id=executor_id,
    )

    # Store the executor in the global dictionary
    executors[executor_id] = executor

    # Define the background task to run the playbook
    def run_in_background():
        try:
            executor.run_playbook()  # Run the playbook
        finally:
            # Remove the executor from the dictionary after execution
            del executors[executor_id]

    # Add the task to background tasks
    background_tasks.add_task(run_in_background)

    return {"message": "Playbook executed", "result": "success", "executor_id": executor_id}


@router.post("/stop/{executor_id}")
def stop_playbook(executor_id: str):
    """
    Endpoint to stop the playbook execution for the given executor ID.

    Args:
        executor_id (str): The unique ID of the playbook executor.

    Raises:
        HTTPException: If the executor ID is invalid or does not exist.

    Returns:
        dict: A message indicating the playbook has been stopped.
    """
    if executor_id not in executors:
        raise HTTPException(status_code=400, detail="Invalid playbook ID")

    # Call the stop method on the corresponding executor
    executors[executor_id].stop_playbook()

    return {"message": f"Playbook with ID {executor_id} stopped"}


@router.post("/pause/{executor_id}")
def pause_playbook(executor_id: str):
    """
    Endpoint to pause the playbook execution for the given executor ID.

    Args:
        executor_id (str): The unique ID of the playbook executor.

    Raises:
        HTTPException: If the executor ID is invalid or does not exist.

    Returns:
        dict: A message indicating the playbook has been paused.
    """
    if executor_id not in executors:
        raise HTTPException(status_code=400, detail="Invalid playbook ID")

    # Call the pause method on the corresponding executor
    executors[executor_id].pause_playbook()

    return {"message": f"Playbook with ID {executor_id} paused"}


@router.post("/restart/{executor_id}")
def restart_playbook(executor_id: str):
    """
    Endpoint to restart the playbook execution for the given executor ID.

    Args:
        executor_id (str): The unique ID of the playbook executor.

    Raises:
        HTTPException: If the executor ID is invalid or does not exist.

    Returns:
        dict: A message indicating the playbook has been restarted.
    """
    if executor_id not in executors:
        raise HTTPException(status_code=400, detail="Invalid playbook ID")

    # Call the restart method on the corresponding executor
    executors[executor_id].restart_playbook()

    return {"message": f"Playbook with ID {executor_id} restarted"}
