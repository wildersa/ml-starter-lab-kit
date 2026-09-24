"""Integration tests for FastAPI Portal API and LabRL endpoints."""
import os
import unittest
from fastapi.testclient import TestClient

# Use temporary test database
os.environ["PORTAL_DB_PATH"] = "test_api_portal.db"

from portal.api.main import app
from portal.api import database

client = TestClient(app)


class TestPortal(unittest.TestCase):
    def setUp(self):
        database.init_db("test_api_portal.db")
        database.reset_learner_db("test_api_portal.db")

    def tearDown(self):
        if os.path.exists("test_api_portal.db"):
            os.remove("test_api_portal.db")

    def test_get_graph_and_workspace(self):
        res = client.get("/api/graph")
        self.assertEqual(res.status_code, 200)
        nodes = res.json()["nodes"]
        self.assertEqual(len(nodes), 7)
        self.assertEqual(nodes[0]["id"], "rl-vocab")
        self.assertEqual(nodes[0]["state"], "available")
        self.assertEqual(nodes[1]["state"], "locked")

        res_ws = client.get("/api/workspace/rl-vocab")
        self.assertEqual(res_ws.status_code, 200)
        self.assertEqual(res_ws.json()["id"], "rl-vocab")

    def test_evaluate_and_unlock_flow(self):
        # Submit correct answer for rl-vocab
        eval_res = client.post("/api/evaluate", json={
            "skill_id": "rl-vocab",
            "activity_id": "act_vocab_1",
            "given_answer": "Reward",
        })
        self.assertEqual(eval_res.status_code, 200)
        data = eval_res.json()
        self.assertTrue(data["is_correct"])

        # Verify reward-return is now unlocked
        res = client.get("/api/graph")
        nodes = {n["id"]: n["state"] for n in res.json()["nodes"]}
        self.assertEqual(nodes["rl-vocab"], "acquired")
        self.assertEqual(nodes["reward-return"], "available")

    def test_lab_rl_reset_and_step(self):
        reset_res = client.post("/api/lab/reset?seed=42")
        self.assertEqual(reset_res.status_code, 200)
        data = reset_res.json()
        self.assertEqual(data["state"], [0, 0])

        # Step RIGHT (1)
        step_res = client.post("/api/lab/step", json={"action": 1})
        self.assertEqual(step_res.status_code, 200)
        step_data = step_res.json()
        self.assertEqual(step_data["step_record"]["transition"]["state"], [0, 0])
        self.assertEqual(step_data["step_record"]["transition"]["next_state"], [0, 1])
        self.assertIn("diagnostic", step_data)
        diag = step_data["diagnostic"]
        self.assertEqual(diag["old_q"], 0.0)
        self.assertEqual(diag["reward"], -0.1)
        self.assertEqual(diag["target"], -0.1)
        self.assertEqual(diag["td_error"], -0.1)
        self.assertEqual(diag["new_q"], -0.01)  # 0 + 0.1 * (-0.1 - 0) = -0.01


if __name__ == "__main__":
    unittest.main()
