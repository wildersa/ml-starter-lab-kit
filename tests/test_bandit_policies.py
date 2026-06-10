import unittest
from pathlib import Path
import shutil
import tempfile
import os
import sys
import subprocess
import json
import csv
from tests.helpers import run_generator

class TestBanditPolicies(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_ucb1_and_thompson_execution(self):
        """Verify that UCB1 and Thompson Sampling run and produce expected results."""
        package_name = "bandit_policies_pkg"
        output_dir = self.test_dir / "bandit_policies_project"

        run_generator(
            project_name="Bandit Policies Project",
            package_name=package_name,
            output_dir=output_dir,
            experience_mode="2" # Guided
        )

        # Run the bandit lab
        env = os.environ.copy()
        env["PYTHONPATH"] = str(output_dir / "src")
        result = subprocess.run(
            [sys.executable, "-m", f"{package_name}.lab", "bandit"],
            cwd=output_dir,
            env=env,
            capture_output=True,
            text=True
        )

        self.assertEqual(result.returncode, 0, f"Bandit Lab failed: {result.stderr}")

        # Check artifacts
        results_json_path = output_dir / "configs/bandit_results.json"
        results_md_path = output_dir / "reports/bandit-results.md"
        history_csv_path = output_dir / "reports/bandit-history.csv"

        self.assertTrue(results_json_path.exists())
        self.assertTrue(results_md_path.exists())
        self.assertTrue(history_csv_path.exists())

        # P0.3: Verify all policies in JSON
        with open(results_json_path, "r") as f:
            results = json.load(f)

        for policy in ["random", "epsilon_greedy", "ucb1", "thompson_sampling"]:
            self.assertIn(policy, results)
            metrics = results[policy]
            self.assertIn("total_reward", metrics)
            self.assertIn("average_reward", metrics)
            self.assertIn("cumulative_regret", metrics)

        # P0.4: Verify history CSV
        with open(history_csv_path, "r") as f:
            reader = csv.DictReader(f)
            history = list(reader)

        # 4 policies * 1000 rounds = 4000 rows
        self.assertEqual(len(history), 4000)

        policies_found = set(row["policy"] for row in history)
        self.assertEqual(policies_found, {"random", "epsilon_greedy", "ucb1", "thompson_sampling"})

        # P0.1: UCB1 first phase touches all arms
        # Default config has 3 arms: A, B, C
        ucb1_history = [row for row in history if row["policy"] == "ucb1"]
        first_three_arms = [row["selected_arm"] for row in ucb1_history[:3]]
        self.assertEqual(len(set(first_three_arms)), 3, "UCB1 should select each arm at least once initially")

        # P0.5: Verify educational content in Markdown
        md_content = results_md_path.read_text()
        self.assertIn("UCB1 (Upper Confidence Bound)", md_content)
        self.assertIn("Thompson Sampling", md_content)
        self.assertIn("uncertainty bonus", md_content)
        self.assertIn("Beta posterior", md_content)
        self.assertIn("exploration", md_content)
        self.assertIn("exploitation", md_content)

    def test_thompson_posterior_updates(self):
        """P0.2: Verify Thompson Sampling updates alpha/beta correctly in the generated module."""
        package_name = "bandit_thompson_pkg"
        output_dir = self.test_dir / "bandit_thompson_project"

        run_generator(
            project_name="Bandit Thompson Project",
            package_name=package_name,
            output_dir=output_dir,
            experience_mode="2"
        )

        # We will run a small script inside the generated project's environment
        # to test ThompsonSamplingPolicy directly.
        test_script = f"""
import sys
from pathlib import Path
sys.path.append(str(Path('{output_dir}') / 'src'))
from {package_name}.bandit_lab import ThompsonSamplingPolicy

policy = ThompsonSamplingPolicy(n_arms=3, seed=42)

# Initial state: Beta(1, 1) for all arms
assert all(a == 1.0 for a in policy.alphas)
assert all(b == 1.0 for b in policy.betas)

# Update arm 0 with reward 1
policy.update(0, 1)
assert policy.alphas[0] == 2.0
assert policy.betas[0] == 1.0

# Update arm 1 with reward 0
policy.update(1, 0)
assert policy.alphas[1] == 1.0
assert policy.betas[1] == 2.0

# Arm 2 should remain unchanged
assert policy.alphas[2] == 1.0
assert policy.betas[2] == 1.0

print("Thompson posterior updates verified successfully.")
"""
        env = os.environ.copy()
        env["PYTHONPATH"] = str(output_dir / "src")
        result = subprocess.run(
            [sys.executable, "-c", test_script],
            capture_output=True,
            text=True,
            env=env
        )

        self.assertEqual(result.returncode, 0, f"Thompson behavioral test failed: {result.stderr}")
        self.assertIn("Thompson posterior updates verified successfully", result.stdout)

if __name__ == "__main__":
    unittest.main()
