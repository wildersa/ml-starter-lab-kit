"""Integration tests for FastAPI Portal API control plane and Lab Runtime proxying."""
import os
import unittest
from unittest.mock import patch, MagicMock

# Try importing fastapi and TestClient safely for environments where optional dependencies are not installed
try:
    from fastapi.testclient import TestClient
    from portal.api.main import app
    from portal.api import database
    from portal.api.runtime_client import RuntimeUnavailableError
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False


@unittest.skipUnless(FASTAPI_AVAILABLE, "fastapi or test dependencies not installed")
class TestPortal(unittest.TestCase):
    def setUp(self):
        os.environ["PORTAL_DB_PATH"] = "test_api_portal.db"
        database.init_db("test_api_portal.db")
        database.reset_learner_db("test_api_portal.db")
        self.client = TestClient(app)

    def tearDown(self):
        if os.path.exists("test_api_portal.db"):
            os.remove("test_api_portal.db")

    def test_get_graph_and_workspace(self):
        res = self.client.get("/api/graph")
        self.assertEqual(res.status_code, 200)
        nodes = res.json()["nodes"]
        self.assertEqual(len(nodes), 7)
        self.assertEqual(nodes[0]["id"], "rl-vocab")
        self.assertEqual(nodes[0]["state"], "available")
        self.assertEqual(nodes[1]["state"], "locked")

        res_ws = self.client.get("/api/workspace/rl-vocab")
        self.assertEqual(res_ws.status_code, 200)
        self.assertEqual(res_ws.json()["id"], "rl-vocab")

    def test_evaluate_and_unlock_flow(self):
        # Submit correct answer for rl-vocab
        eval_res = self.client.post("/api/evaluate", json={
            "skill_id": "rl-vocab",
            "activity_id": "act_vocab_1",
            "given_answer": "Reward",
        })
        self.assertEqual(eval_res.status_code, 200)
        data = eval_res.json()
        self.assertTrue(data["is_correct"])

        # Verify reward-return is now unlocked
        res = self.client.get("/api/graph")
        nodes = {n["id"]: n["state"] for n in res.json()["nodes"]}
        self.assertEqual(nodes["rl-vocab"], "acquired")
        self.assertEqual(nodes["reward-return"], "available")

    def test_runtime_offline_graceful_handling(self):
        """Portal API remains fully functional and handles lab endpoints with 503 when runtime is offline."""
        with patch("portal.api.runtime_client.runtime_client.get_status") as mock_status, \
             patch("portal.api.runtime_client.runtime_client.reset_simulation") as mock_reset, \
             patch("portal.api.runtime_client.runtime_client.step_simulation") as mock_step:

            mock_status.return_value = {"status": "offline", "error": "Connection refused"}
            mock_reset.side_effect = RuntimeUnavailableError("Lab Runtime unavailable")
            mock_step.side_effect = RuntimeUnavailableError("Lab Runtime unavailable")

            # Status endpoint
            status_res = self.client.get("/api/runtime/status")
            self.assertEqual(status_res.status_code, 200)
            self.assertEqual(status_res.json()["status"], "offline")

            # Lab reset returns 503
            reset_res = self.client.post("/api/lab/reset?seed=42")
            self.assertEqual(reset_res.status_code, 503)

            # Lab step returns 503
            step_res = self.client.post("/api/lab/step", json={"action": 1})
            self.assertEqual(step_res.status_code, 503)

            # Control plane endpoints still work perfectly
            res_graph = self.client.get("/api/graph")
            self.assertEqual(res_graph.status_code, 200)

    def test_lab_rl_reset_and_step_online(self):
        """Portal API proxies lab requests to Runtime when online."""
        mock_reset_data = {
            "session_id": "default-rl-session",
            "state": [0, 0],
            "grid_size": 3,
            "goal_state": [2, 2],
            "pit_state": [1, 1],
            "q_table": {"0,0": [0.0, 0.0, 0.0, 0.0]},
            "step_count": 0,
            "done": False,
        }
        mock_step_data = {
            "session_id": "default-rl-session",
            "step_record": {
                "step_number": 1,
                "transition": {
                    "state": [0, 0],
                    "action": 1,
                    "reward": -0.1,
                    "next_state": [0, 1],
                    "done": False,
                },
                "info": {"action_name": "RIGHT", "pit_hit": False},
            },
            "diagnostic": {
                "state": [0, 0],
                "action": 1,
                "reward": -0.1,
                "next_state": [0, 1],
                "done": False,
                "old_q": 0.0,
                "max_next_q": 0.0,
                "target": -0.1,
                "td_error": -0.1,
                "new_q": -0.01,
                "alpha": 0.1,
                "gamma": 0.9,
            },
            "q_table": {"0,0": [0.0, -0.01, 0.0, 0.0]},
            "done": False,
        }

        with patch("portal.api.runtime_client.runtime_client.reset_simulation") as mock_reset, \
             patch("portal.api.runtime_client.runtime_client.step_simulation") as mock_step:

            mock_reset.return_value = mock_reset_data
            mock_step.return_value = mock_step_data

            reset_res = self.client.post("/api/lab/reset?seed=42")
            self.assertEqual(reset_res.status_code, 200)
            self.assertEqual(reset_res.json()["state"], [0, 0])

            step_res = self.client.post("/api/lab/step", json={"action": 1})
            self.assertEqual(step_res.status_code, 200)
            step_data = step_res.json()
            self.assertEqual(step_data["diagnostic"]["new_q"], -0.01)


if __name__ == "__main__":
    unittest.main()
