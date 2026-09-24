"""Integration tests for FastAPI Portal API and LabRL endpoints."""
import os
import pytest
from fastapi.testclient import TestClient

# Use temporary test database
os.environ["PORTAL_DB_PATH"] = "test_api_portal.db"

from portal.api.main import app
from portal.api import database

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_and_teardown_db():
    database.init_db("test_api_portal.db")
    database.reset_learner_db("test_api_portal.db")
    yield
    if os.path.exists("test_api_portal.db"):
        os.remove("test_api_portal.db")


def test_get_graph_and_workspace():
    res = client.get("/api/graph")
    assert res.status_code == 200
    nodes = res.json()["nodes"]
    assert len(nodes) == 7
    assert nodes[0]["id"] == "rl-vocab"
    assert nodes[0]["state"] == "available"
    assert nodes[1]["state"] == "locked"

    res_ws = client.get("/api/workspace/rl-vocab")
    assert res_ws.status_code == 200
    assert res_ws.json()["id"] == "rl-vocab"


def test_evaluate_and_unlock_flow():
    # Submit correct answer for rl-vocab
    eval_res = client.post("/api/evaluate", json={
        "skill_id": "rl-vocab",
        "activity_id": "act_vocab_1",
        "given_answer": "Reward",
    })
    assert eval_res.status_code == 200
    data = eval_res.json()
    assert data["is_correct"] is True

    # Verify reward-return is now unlocked
    res = client.get("/api/graph")
    nodes = {n["id"]: n["state"] for n in res.json()["nodes"]}
    assert nodes["rl-vocab"] == "acquired"
    assert nodes["reward-return"] == "available"


def test_lab_rl_reset_and_step():
    reset_res = client.post("/api/lab/reset?seed=42")
    assert reset_res.status_code == 200
    data = reset_res.json()
    assert data["state"] == [0, 0]

    # Step RIGHT (1)
    step_res = client.post("/api/lab/step", json={"action": 1})
    assert step_res.status_code == 200
    step_data = step_res.json()
    assert step_data["step_record"]["transition"]["state"] == [0, 0]
    assert step_data["step_record"]["transition"]["next_state"] == [0, 1]
    assert "diagnostic" in step_data
    diag = step_data["diagnostic"]
    assert diag["old_q"] == 0.0
    assert diag["reward"] == -0.1
    assert diag["target"] == -0.1
    assert diag["td_error"] == -0.1
    assert diag["new_q"] == -0.01  # 0 + 0.1 * (-0.1 - 0) = -0.01
