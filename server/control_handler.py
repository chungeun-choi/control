import uuid
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional, Dict
from executor.playbook import ExecuteController


router = APIRouter()
executors: Dict[str, ExecuteController] = {}

class PlaybookRequest(BaseModel):
    playbook: List[str]
    inventory: str
    passwords: Optional[dict] = None

@router.post("/run/")
def run_playbook(request: PlaybookRequest, background_tasks: BackgroundTasks):
    executor_id = str(uuid.uuid4())
    executor = ExecuteController(
        playbook=request.playbook,
        inventory=request.inventory,
        passwords=request.passwords,
        executor_id=executor_id,
    )
    executors[executor_id] = executor

    def run_in_background():
        try:
            executor.run_playbook()
        finally:
            del executors[executor_id]

    background_tasks.add_task(run_in_background)

    return {"message": "Playbook executed", "result": "success", "executor_id": executor_id}

@router.post("/stop/{executor_id}")
def stop_playbook(executor_id: str):
    if executor_id not in executors:
        raise HTTPException(status_code=400, detail="Invalid playbook ID")

    executors[executor_id].stop_playbook()

    return {"message": f"Playbook with ID {executor_id} stopped"}

@router.post("/pause/{executor_id}")
def pause_playbook(executor_id: str):
    if executor_id not in executors:
        raise HTTPException(status_code=400, detail="Invalid playbook ID")

    executors[executor_id].pause_playbook()

    return {"message": f"Playbook with ID {executor_id} paused"}

@router.post("/restart/{executor_id}")
def restart_playbook(executor_id: str):
    if executor_id not in executors:
        raise HTTPException(status_code=400, detail="Invalid playbook ID")

    executors[executor_id].restart_playbook()

    return {"message": f"Playbook with ID {executor_id} restarted"}
