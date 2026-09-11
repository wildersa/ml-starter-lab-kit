import unittest
import sys
import shutil
import tempfile
import subprocess
from pathlib import Path

from ml_starter_generator.templates import load_template
from tests.helpers import run_generator


class TestRLLabContractsAndRunner(unittest.TestCase):
    def setUp(self):
        # Dynamically exec rl.py.tpl content
        code = load_template("rl.py.tpl", {"PACKAGE_NAME": "test_pkg"}, folder="common")
        namespace = {}
        exec(code, namespace)
        self.rl = namespace

    def test_gridworld_env(self):
        env_cls = self.rl["GridworldToyEnv"]
        env = env_cls(grid_size=3)
        obs, info = env.reset()
        self.assertEqual(obs, (0, 0))
        self.assertEqual(env.get_state(), (0, 0))
        self.assertEqual(env.available_actions(), ["UP", "RIGHT", "DOWN", "LEFT"])

        obs2, reward, term, trunc, info = env.step("RIGHT")
        self.assertEqual(obs2, (0, 1))
        self.assertEqual(reward, -0.01)
        self.assertFalse(term)
        self.assertFalse(trunc)

        rendered = env.render_ascii()
        self.assertIn("[A]", rendered)

    def test_toy_rl_agent_and_runner(self):
        env_cls = self.rl["GridworldToyEnv"]
        agent_cls = self.rl["ToyRLAgent"]
        runner_cls = self.rl["RLRunner"]

        env = env_cls(grid_size=3)
        agent = agent_cls(alpha=0.1, gamma=0.9, epsilon=0.1)
        runner = runner_cls(env, agent)

        self.assertEqual(runner.episode_count, 1)
        self.assertEqual(runner.step_count, 0)
        self.assertEqual(len(runner.history), 0)

        # Execute manual step
        rec = runner.step(action="RIGHT")
        self.assertEqual(rec.episode, 1)
        self.assertEqual(rec.step, 1)
        self.assertEqual(rec.action, "RIGHT")
        self.assertEqual(rec.state_before, (0, 0))
        self.assertEqual(rec.state_after, (0, 1))
        self.assertIn("td_error", rec.update_info)
        self.assertEqual(len(runner.history), 1)

        # Execute step without specifying action (agent selects action)
        rec2 = runner.step()
        self.assertEqual(rec2.step, 2)
        self.assertEqual(len(runner.history), 2)

        # Test manual Q-value override
        agent.set_q_value((0, 1), "DOWN", 5.0)
        q_vals = agent.get_q_values((0, 1))
        self.assertEqual(q_vals.get("DOWN"), 5.0)

        policy = agent.get_policy((0, 1), ["UP", "RIGHT", "DOWN", "LEFT"])
        self.assertGreater(policy["DOWN"], policy["UP"])


class TestRLLabScaffolding(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_rl_scaffolded_files_generated(self):
        project_name = "rl_project"
        package_name = "rl_pkg"
        output_dir = self.test_dir / project_name

        run_generator(
            project_name=project_name,
            package_name=package_name,
            output_dir=output_dir,
            task="1",  # supervised or generic
            language="en"
        )

        rl_py = output_dir / "src" / package_name / "rl.py"
        rl_ws = output_dir / "src" / package_name / "rl_workspace.py"
        rl_doc = output_dir / "docs" / "rl-lab.md"

        self.assertTrue(rl_py.exists(), "rl.py should be generated in package")
        self.assertTrue(rl_ws.exists(), "rl_workspace.py should be generated in package")
        self.assertTrue(rl_doc.exists(), "rl-lab.md should be generated in docs")

        # Check lab.py subcommand
        lab_py = output_dir / "src" / package_name / "lab.py"
        content = lab_py.read_text()
        self.assertIn("rl-workspace", content)

        # Run lab.py rl-workspace help or check command
        cmd = [sys.executable, "-m", f"{package_name}.lab", "rl-workspace"]
        result = subprocess.run(cmd, cwd=output_dir, capture_output=True, text=True, env={"PYTHONPATH": str(output_dir / "src")})
        self.assertEqual(result.returncode, 0)
        self.assertIn("RL Workspace found", result.stdout)

    def test_rl_pt_br_scaffolded_doc(self):
        project_name = "rl_project_pt"
        package_name = "rl_pkg_pt"
        output_dir = self.test_dir / project_name

        run_generator(
            project_name=project_name,
            package_name=package_name,
            output_dir=output_dir,
            task="1",
            language="pt-BR"
        )

        rl_doc = output_dir / "docs" / "rl-lab.pt-BR.md"
        self.assertTrue(rl_doc.exists(), "rl-lab.pt-BR.md should be generated for pt-BR")


if __name__ == "__main__":
    unittest.main()
