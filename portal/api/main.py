"""FastAPI Application Server for Learning Portal and LabRL Proxy."""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict, List, Optional
import os

from portal.api import database
from portal.api import graph
from portal.lab_rl.env import GridWorldEnv
from portal.lab_rl.agent import QLearningAgent

app = FastAPI(title="Learning Portal API", version="0.1.0")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global in-memory LabRL session
lab_env = GridWorldEnv()
lab_agent = QLearningAgent(alpha=0.1, gamma=0.9)


@app.on_event("startup")
def startup_event():
    database.init_db()


class EvaluationRequest(BaseModel):
    skill_id: str
    activity_id: str
    given_answer: Any


class LabStepRequest(BaseModel):
    action: int


@app.get("/api/graph")
def get_graph():
    """Returns all skill graph nodes with state and unlock status."""
    return {"nodes": graph.get_curriculum_state()}


@app.get("/api/workspace/{skill_id}")
def get_workspace(skill_id: str):
    """Returns workspace theory, worked example, activities, and review variant for a skill."""
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
        "review_variant": node.review_variant,
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


# --- LabRL Endpoints ---

@app.post("/api/lab/reset")
def reset_lab(seed: Optional[int] = 42):
    """Resets LabRL environment and agent."""
    start_state = lab_env.reset(seed=seed)
    lab_agent.reset_q_table()
    return {
        "state": start_state,
        "grid_size": lab_env.grid_size,
        "goal_state": lab_env.goal_state,
        "pit_state": lab_env.pit_state,
        "q_table": lab_agent.get_serialized_q_table(),
        "step_count": lab_env.step_count,
        "done": lab_env.done,
    }


@app.post("/api/lab/step")
def step_lab(req: LabStepRequest):
    """Executes one step in LabRL and performs Q-learning update."""
    if lab_env.done:
        raise HTTPException(status_code=400, detail="Environment is done. Call /api/lab/reset first.")

    try:
        step_record = lab_env.step(req.action)
        diagnostic = lab_agent.update(step_record.transition)

        return {
            "step_record": {
                "step_number": step_record.step_number,
                "transition": {
                    "state": list(step_record.transition.state),
                    "action": step_record.transition.action,
                    "reward": step_record.transition.reward,
                    "next_state": list(step_record.transition.next_state),
                    "done": step_record.transition.done,
                },
                "info": step_record.info,
            },
            "diagnostic": {
                "state": list(diagnostic.state),
                "action": diagnostic.action,
                "reward": diagnostic.reward,
                "next_state": list(diagnostic.next_state),
                "done": diagnostic.done,
                "old_q": diagnostic.old_q,
                "max_next_q": diagnostic.max_next_q,
                "target": diagnostic.target,
                "td_error": diagnostic.td_error,
                "new_q": diagnostic.new_q,
                "alpha": diagnostic.alpha,
                "gamma": diagnostic.gamma,
            },
            "q_table": lab_agent.get_serialized_q_table(),
            "done": lab_env.done,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
