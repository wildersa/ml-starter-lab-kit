"""Unit and integration tests for Lab Runtime execution plane service."""
import unittest

# Try importing fastapi and TestClient safely for environments where optional dependencies are not installed
try:
    from fastapi.testclient import TestClient
    from portal.runtime.main import app as runtime_app
    from portal.runtime.session import session_manager
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False


@unittest.skipUnless(FASTAPI_AVAILABLE, "fastapi or test dependencies not installed")
class TestLabRuntime(unittest.TestCase):
    def setUp(self):
        # Reset session_manager state before each test
        session_manager._sessions.clear()
        self.client = TestClient(runtime_app)

    def test_health_and_capabilities(self):
        res_health = self.client.get("/health")
        self.assertEqual(res_health.status_code, 200)
        self.assertEqual(res_health.json()["status"], "ok")

        res_caps = self.client.get("/capabilities")
        self.assertEqual(res_caps.status_code, 200)
        caps = res_caps.json()["capabilities"]
        self.assertIn("rl_simulation", caps)
        self.assertIn("python_execution", caps)

    def test_session_lifecycle(self):
        # Create session
        res_create = self.client.post("/sessions", json={"capability": "rl_simulation"})
        self.assertEqual(res_create.status_code, 200)
        data = res_create.json()
        session_id = data["session_id"]
        self.assertEqual(data["capability"], "rl_simulation")

        # Get session info
        res_info = self.client.get(f"/sessions/{session_id}")
        self.assertEqual(res_info.status_code, 200)
        self.assertEqual(res_info.json()["session_id"], session_id)
        self.assertFalse(res_info.json()["done"])

        # Cancel session
        res_cancel = self.client.delete(f"/sessions/{session_id}")
        self.assertEqual(res_cancel.status_code, 200)

        # Confirm session is deleted
        res_info_404 = self.client.get(f"/sessions/{session_id}")
        self.assertEqual(res_info_404.status_code, 404)

    def test_invalid_capability_creation(self):
        res = self.client.post("/sessions", json={"capability": "unsupported_capability"})
        self.assertEqual(res.status_code, 400)
        self.assertIn("Unsupported capability", res.json()["detail"])

    def test_rl_simulation_reset_and_step(self):
        # Reset default session
        res_reset = self.client.post("/rl/reset", json={"seed": 42})
        self.assertEqual(res_reset.status_code, 200)
        data = res_reset.json()
        self.assertEqual(data["state"], [0, 0])
        self.assertEqual(data["grid_size"], 3)
        self.assertIn("0,0", data["q_table"])

        # Step RIGHT (1)
        res_step = self.client.post("/rl/step", json={"action": 1})
        self.assertEqual(res_step.status_code, 200)
        step_data = res_step.json()
        self.assertEqual(step_data["step_record"]["transition"]["state"], [0, 0])
        self.assertEqual(step_data["step_record"]["transition"]["next_state"], [0, 1])
        diag = step_data["diagnostic"]
        self.assertEqual(diag["old_q"], 0.0)
        self.assertEqual(diag["reward"], -0.1)
        self.assertEqual(diag["td_error"], -0.1)

    def test_invalid_action_error_handling(self):
        self.client.post("/rl/reset")
        res_invalid = self.client.post("/rl/step", json={"action": 99})
        self.assertEqual(res_invalid.status_code, 400)
        self.assertIn("Invalid action", res_invalid.json()["detail"])


if __name__ == "__main__":
    unittest.main()
