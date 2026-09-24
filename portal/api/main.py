"""FastAPI Application Server for Learning Portal Control Plane."""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict, List, Optional
import os

from portal.api import database
from portal.api import graph
from portal.api.runtime_client import runtime_client, RuntimeUnavailableError

app = FastAPI(title="Learning Portal API", version="0.1.0")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    database.init_db()


class EvaluationRequest(BaseModel):
    skill_id: str
    activity_id: str
    given_answer: Any


class LabStepRequest(BaseModel):
    action: int
    session_id: Optional[str] = None


@app.get("/api/graph")
def get_graph():
    """Returns all skill graph nodes with state and unlock status."""
    return {"nodes": graph.get_curriculum_state()}


@app.get("/api/workspace/{skill_id}")
def get_workspace(skill_id: str):
    """Returns workspace theory, worked example, and activities for a skill."""
    if skill_id not in graph.SKILL_GRAPH_NODES:
        raise HTTPException(status_code=404, detail="Skill not found")
    node = graph.SKILL_GRAPH_NODES[skill_id]
    progress = database.get_all_skill_progress().get(skill_id, {
        "state": "locked",
        "mastery_score": 0.0,
        "completed_activities": [],
    })
    return {
        "id": node.id,
        "title": node.title,
        "prerequisites": node.prerequisites,
        "theory": node.theory,
        "worked_example": node.worked_example,
        "activities": node.activities,
        "lab_rl_enabled": node.lab_rl_enabled,
        "user_progress": progress,
    }


@app.post("/api/evaluate")
def evaluate_activity_endpoint(req: EvaluationRequest):
    """Evaluates a learner activity submission."""
    try:
        res = graph.evaluate_activity(req.skill_id, req.activity_id, req.given_answer)
        return res
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/reset-progress")
def reset_progress():
    """Resets learner progress DB."""
    database.reset_learner_db()
    return {"status": "success", "graph": graph.get_curriculum_state()}


# --- Lab Runtime Status & Proxy Endpoints ---

@app.get("/api/runtime/status")
def get_runtime_status():
    """Returns availability and capability status of the separate Lab Runtime."""
    return runtime_client.get_status()


@app.post("/api/lab/reset")
def reset_lab(seed: Optional[int] = 42, session_id: Optional[str] = None):
    """Proxies reset request to the separate Lab Runtime execution plane."""
    try:
        return runtime_client.reset_simulation(session_id=session_id, seed=seed)
    except RuntimeUnavailableError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/lab/step")
def step_lab(req: LabStepRequest):
    """Proxies simulation step request to the separate Lab Runtime execution plane."""
    try:
        return runtime_client.step_simulation(action=req.action, session_id=req.session_id)
    except RuntimeUnavailableError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
