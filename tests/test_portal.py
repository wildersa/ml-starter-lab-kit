"""Integration tests for FastAPI Portal API, RL Content Pack Ingestion, and LabRL endpoints."""
import os
import unittest

# Try importing fastapi and TestClient safely for environments where optional dependencies are not installed
try:
    from fastapi.testclient import TestClient
    from portal.api.main import app
    from portal.api import database
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
        expected_ids = ["rl-vocab", "reward-return", "discounting", "mdp", "v-and-q", "bellman-backup", "td-q-learning"]
        actual_ids = [n["id"] for n in nodes]
        self.assertEqual(actual_ids, expected_ids)

        self.assertEqual(nodes[0]["id"], "rl-vocab")
        self.assertEqual(nodes[0]["state"], "available")
        self.assertEqual(nodes[1]["state"], "locked")

        # Check all workspaces return rich content without lorem/placeholders
        for skill_id in expected_ids:
            res_ws = self.client.get(f"/api/workspace/{skill_id}")
            self.assertEqual(res_ws.status_code, 200)
            ws = res_ws.json()
            self.assertEqual(ws["id"], skill_id)
            self.assertIn("theory", ws)
            self.assertIn("worked_example", ws)
            self.assertGreater(len(ws["theory"]), 50)
            self.assertGreater(len(ws["worked_example"]), 20)
            self.assertNotIn("lorem", ws["theory"].lower())
            self.assertNotIn("lorem", ws["worked_example"].lower())
            self.assertIn("review_variant", ws)
            self.assertIsNotNone(ws["review_variant"])
            self.assertIn("prompt", ws["review_variant"])
            self.assertIn("key_answer", ws["review_variant"])

    def test_misconception_tag_evaluations(self):
        # 1. Test MISC_REWARD_VS_RETURN in reward-return
        eval_res = self.client.post("/api/evaluate", json={
            "skill_id": "reward-return",
            "activity_id": "act_return_1",
            "given_answer": "-0.5",  # Gives r_1 instead of return G_0
        })
        self.assertEqual(eval_res.status_code, 200)
        data = eval_res.json()
        self.assertFalse(data["is_correct"])
        self.assertEqual(data["misconception_tag"], "MISC_REWARD_VS_RETURN")

        # 2. Test MISC_BELLMAN_DISCOUNT_OMISSION in discounting
        eval_res2 = self.client.post("/api/evaluate", json={
            "skill_id": "discounting",
            "activity_id": "act_discount_1",
            "given_answer": "18.0",  # Undiscounted sum -1 + -1 + 20
        })
        self.assertEqual(eval_res2.status_code, 200)
        data2 = eval_res2.json()
        self.assertFalse(data2["is_correct"])
        self.assertEqual(data2["misconception_tag"], "MISC_BELLMAN_DISCOUNT_OMISSION")

        # 3. Test MISC_MARKOV_MEMORY in mdp
        eval_res3 = self.client.post("/api/evaluate", json={
            "skill_id": "mdp",
            "activity_id": "act_mdp_1",
            "given_answer": "Yes",
        })
        self.assertEqual(eval_res3.status_code, 200)
        data3 = eval_res3.json()
        self.assertFalse(data3["is_correct"])
        self.assertEqual(data3["misconception_tag"], "MISC_MARKOV_MEMORY")

        # 4. Test MISC_BELLMAN_MAX_VS_AVG in v-and-q
        eval_res4 = self.client.post("/api/evaluate", json={
            "skill_id": "v-and-q",
            "activity_id": "act_vq_2",
            "given_answer": "25.0",  # Selected max instead of weighted average for uniform policy
        })
        self.assertEqual(eval_res4.status_code, 200)
        data4 = eval_res4.json()
        self.assertFalse(data4["is_correct"])
        self.assertEqual(data4["misconception_tag"], "MISC_BELLMAN_MAX_VS_AVG")

    def test_full_traversal_unlock_flow(self):
        # Activity correct answers mapping per skill
        skill_answers = [
            ("rl-vocab", [("act_vocab_1", "Reward"), ("act_vocab_2", "No")]),
            ("reward-return", [("act_return_1", "4.0"), ("act_return_2", "32.0")]),
            ("discounting", [("act_discount_1", "14.3"), ("act_discount_2", "-1.0"), ("act_discount_3", "5.0")]),
            ("mdp", [("act_mdp_1", "No"), ("act_mdp_2", "(S, A, P, R, gamma)")]),
            ("v-and-q", [("act_vq_1", "4.0"), ("act_vq_2", "17.67"), ("act_vq_3", "A2 because Q*(S, A2) = 180 > Q*(S, A1) = 100")]),
            ("bellman-backup", [("act_bellman_1", "8.9"), ("act_bellman_2", "6.0")]),
            ("td-q-learning", [("act_td_1", "3.0"), ("act_td_2", "42.2"), ("act_td_3", "19.5"), ("act_td_4", "Q(S_t, A_t) <- R_{t+1}")]),
        ]

        for skill_id, activities in skill_answers:
            for act_id, ans in activities:
                eval_res = self.client.post("/api/evaluate", json={
                    "skill_id": skill_id,
                    "activity_id": act_id,
                    "given_answer": ans,
                })
                self.assertEqual(eval_res.status_code, 200)
                data = eval_res.json()
                self.assertTrue(data["is_correct"], f"Failed activity {act_id} for skill {skill_id} with ans {ans}")

            # Verify current skill is acquired
            res = self.client.get("/api/graph")
            states = {n["id"]: n["state"] for n in res.json()["nodes"]}
            self.assertEqual(states[skill_id], "acquired")

        # Verify all skills in graph acquired
        res_final = self.client.get("/api/graph")
        final_states = [n["state"] for n in res_final.json()["nodes"]]
        self.assertTrue(all(s == "acquired" for s in final_states))

    def test_lab_rl_reset_and_step(self):
        reset_res = self.client.post("/api/lab/reset?seed=42")
        self.assertEqual(reset_res.status_code, 200)
        data = reset_res.json()
        self.assertEqual(data["state"], [0, 0])

        # Step RIGHT (1)
        step_res = self.client.post("/api/lab/step", json={"action": 1})
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
