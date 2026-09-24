"""FastAPI Lab Runtime Execution Plane Service."""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Any, Dict, List

from portal.runtime.session import session_manager, RuntimeSession

app = FastAPI(title="Lab Runtime Execution Plane", version="0.1.0")


class SessionRequest(BaseModel):
    capability: str = "rl_simulation"
    session_id: Optional[str] = None
    alpha: float = 0.1
    gamma: float = 0.9


class ResetRequest(BaseModel):
    session_id: Optional[str] = None
    seed: Optional[int] = 42


class StepRequest(BaseModel):
    session_id: Optional[str] = None
    action: int


@app.get("/health")
def health():
    return {"status": "ok", "service": "lab_runtime"}


@app.get("/capabilities")
def list_capabilities():
    return {
        "capabilities": ["rl_simulation", "python_execution"],
        "version": "0.1.0",
        "description": "Lab Runtime execution plane for RL simulation and python sandboxing.",
    }


@app.post("/sessions")
def create_session(req: SessionRequest):
    if req.capability not in ["rl_simulation", "python_execution"]:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported capability '{req.capability}'. Available: ['rl_simulation', 'python_execution']",
        )

    session = session_manager.create_session(
        capability=req.capability,
        session_id=req.session_id,
        alpha=req.alpha,
        gamma=req.gamma,
    )
    return {
        "session_id": session.session_id,
        "capability": session.capability,
        "status": "active",
        "created_at": session.created_at,
    }


@app.get("/sessions/{session_id}")
def get_session_info(session_id: str):
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found.")
    return {
        "session_id": session.session_id,
        "capability": session.capability,
        "step_count": session.env.step_count,
        "done": session.env.done,
        "last_accessed": session.last_accessed,
    }


@app.delete("/sessions/{session_id}")
@app.post("/sessions/{session_id}/cancel")
def cancel_session(session_id: str):
    success = session_manager.cancel_session(session_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found.")
    return {"session_id": session_id, "status": "cancelled"}


@app.post("/rl/reset")
def reset_rl(req: Optional[ResetRequest] = None):
    req = req or ResetRequest()
    if req.session_id:
        session = session_manager.get_session(req.session_id)
        if not session:
            raise HTTPException(status_code=404, detail=f"Session '{req.session_id}' not found.")
    else:
        session = session_manager.get_or_create_default()

    return session.reset(seed=req.seed)


@app.post("/rl/step")
def step_rl(req: StepRequest):
    if req.session_id:
        session = session_manager.get_session(req.session_id)
        if not session:
            raise HTTPException(status_code=404, detail=f"Session '{req.session_id}' not found.")
    else:
        session = session_manager.get_or_create_default()

    try:
        return session.step(action=req.action)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
