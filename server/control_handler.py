import uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
from executor.playbook import WebControlExecutor

# 라우터 생성
router = APIRouter()

# 요청 데이터 모델 정의
class PlaybookRequest(BaseModel):
    playbook: List[str]
    inventory: str
    passwords: Optional[dict] = None

# 전역 Executor 객체를 저장하는 딕셔너리 (UUID로 식별)
executors: Dict[str, WebControlExecutor] = {}

@router.post("/run/")
def run_playbook(request: PlaybookRequest):
    playbook_id = str(uuid.uuid4())
    executor = WebControlExecutor(
        playbook=request.playbook,
        inventory=request.inventory,
        passwords=request.passwords
    )
    executors[playbook_id] = executor
    result = executor.run_playbook()
    return {"message": "Playbook executed", "result": result, "playbook_id": playbook_id}

@router.post("/stop/{playbook_id}")
def stop_playbook(playbook_id: str):
    if playbook_id not in executors:
        raise HTTPException(status_code=400, detail="Invalid playbook ID")
    executors[playbook_id].stop_playbook()
    return {"message": f"Playbook with ID {playbook_id} stopped"}

@router.post("/pause/{playbook_id}")
def pause_playbook(playbook_id: str):
    if playbook_id not in executors:
        raise HTTPException(status_code=400, detail="Invalid playbook ID")
    executors[playbook_id].pause_playbook()
    return {"message": f"Playbook with ID {playbook_id} paused"}

@router.post("/restart/{playbook_id}")
def restart_playbook(playbook_id: str):
    if playbook_id not in executors:
        raise HTTPException(status_code=400, detail="Invalid playbook ID")
    executors[playbook_id].restart_playbook()
    return {"message": f"Playbook with ID {playbook_id} restarted"}
