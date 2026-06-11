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

class TestBanditWiring(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.starter_root = self.test_dir / "ml-starter-lab-kit"
        self.starter_root.mkdir()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_bandit_lab_generated_with_full_profile(self):
        """P0.2: Project contains bandit_lab.py and configs/bandit_config.json when full profile is selected."""
        package_name = "bandit_full_pkg"
        output_dir = self.test_dir / "bandit_full_project"

        run_generator(
            project_name="Bandit Full Project",
            package_name=package_name,
            output_dir=output_dir,
            task="2", # Supervised
            experience_mode="1", # Minimal
            optional_profile="3" # Full profile
        )

        self.assertTrue((output_dir / f"src/{package_name}/bandit_lab.py").exists())
        self.assertTrue((output_dir / "configs/bandit_config.json").exists())

        # P0.5: Verify no placeholder text
        lab_content = (output_dir / f"src/{package_name}/bandit_lab.py").read_text()
        self.assertNotIn("Bandit Lab is planned but not implemented", lab_content)
        self.assertIn("class BernoulliEnvironment", lab_content)

        # lab.py wiring
        lab_py_content = (output_dir / f"src/{package_name}/lab.py").read_text()
        self.assertIn('subparsers.add_parser("bandit"', lab_py_content)

    def test_bandit_lab_omitted_in_minimal_mode(self):
        """P0.2: Minimal project does not contain Bandit Lab files."""
        package_name = "bandit_minimal_pkg"
        output_dir = self.test_dir / "bandit_minimal_project"

        run_generator(
            project_name="Bandit Minimal Project",
            package_name=package_name,
            output_dir=output_dir,
            experience_mode="1" # Minimal Starter
        )

        self.assertFalse((output_dir / f"src/{package_name}/bandit_lab.py").exists())
        self.assertFalse((output_dir / "configs/bandit_config.json").exists())

    def test_bandit_command_execution_real(self):
        """P0.1-P0.5: Verify the bandit command runs and produces correct artifacts."""
        package_name = "bandit_run_pkg"
        output_dir = self.test_dir / "bandit_run_project"

        run_generator(
            project_name="Bandit Run Project",
            package_name=package_name,
            output_dir=output_dir,
            task="2",
            experience_mode="1",
            optional_profile="3" # Full
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
        self.assertIn("Bandit Lab simulation complete", result.stdout)

        # P0.5: Check expected output files
        results_json_path = output_dir / "configs/bandit_results.json"
        results_md_path = output_dir / "reports/bandit-results.md"
        history_csv_path = output_dir / "reports/bandit-history.csv"

        self.assertTrue(results_json_path.exists())
        self.assertTrue(results_md_path.exists())
        self.assertTrue(history_csv_path.exists())

        # Educational content check in Markdown
        md_content = results_md_path.read_text()
        self.assertIn("Understanding Multi-Armed Bandits", md_content)
        self.assertIn("sequential decision learning", md_content)
        self.assertIn("partial feedback", md_content)
        self.assertIn("Random Policy", md_content)

        # P0.4: Check JSON metrics
        with open(results_json_path, "r") as f:
            results = json.load(f)

        for policy in ["random", "epsilon_greedy"]:
            self.assertIn(policy, results)
            metrics = results[policy]
            self.assertIn("total_reward", metrics)
            self.assertIn("average_reward", metrics)
            self.assertIn("cumulative_regret", metrics)
            self.assertIn("best_arm_selection_rate", metrics)
            self.assertIn("arm_counts", metrics)
            self.assertEqual(len(metrics["arm_counts"]), 3) # Default config has 3 arms (A, B, C)

        # P0.2 & P0.3: Check history CSV
        with open(history_csv_path, "r") as f:
            reader = csv.DictReader(f)
            history = list(reader)

        # 1000 rounds per policy (random, epsilon_greedy, ucb1, thompson_sampling) = 4000 rounds
        self.assertEqual(len(history), 4000)

        for row in history:
            # P0.2: Rewards are 0 or 1
            self.assertIn(row["reward"], ["0", "1"])
            # Each row should have these keys
            self.assertIn("round", row)
            self.assertIn("policy", row)
            self.assertIn("selected_arm", row)
            self.assertIn("cumulative_reward", row)
            self.assertIn("cumulative_regret", row)

    def test_bandit_invalid_config_fails(self):
        """P0.1: Invalid config fails with clear message."""
        package_name = "bandit_fail_pkg"
        output_dir = self.test_dir / "bandit_fail_project"

        run_generator(
            project_name="Bandit Fail Project",
            package_name=package_name,
            output_dir=output_dir,
            task="2",
            experience_mode="1",
            optional_profile="3" # Full
        )

        # Corrupt the config: remove 'n_rounds'
        config_path = output_dir / "configs/bandit_config.json"
        with open(config_path, "r") as f:
            config = json.load(f)
        del config["n_rounds"]
        with open(config_path, "w") as f:
            json.dump(config, f)

        env = os.environ.copy()
        env["PYTHONPATH"] = str(output_dir / "src")
        result = subprocess.run(
            [sys.executable, "-m", f"{package_name}.lab", "bandit"],
            cwd=output_dir,
            env=env,
            capture_output=True,
            text=True
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Missing required field 'n_rounds'", result.stdout)

    def test_bandit_invalid_policy_fails(self):
        """P0.1: Unsupported policy fails."""
        package_name = "bandit_policy_fail_pkg"
        output_dir = self.test_dir / "bandit_policy_fail_project"

        run_generator(
            project_name="Bandit Policy Fail Project",
            package_name=package_name,
            output_dir=output_dir,
            task="2",
            experience_mode="1",
            optional_profile="3" # Full
        )

        config_path = output_dir / "configs/bandit_config.json"
        with open(config_path, "r") as f:
            config = json.load(f)
        config["policies"] = ["non_existent_policy"]
        with open(config_path, "w") as f:
            json.dump(config, f)

        env = os.environ.copy()
        env["PYTHONPATH"] = str(output_dir / "src")
        result = subprocess.run(
            [sys.executable, "-m", f"{package_name}.lab", "bandit"],
            cwd=output_dir,
            env=env,
            capture_output=True,
            text=True
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Unsupported policy 'non_existent_policy'", result.stdout)

    def test_bandit_invalid_probability_fails(self):
        """P0.1: Invalid reward probability fails."""
        package_name = "bandit_prob_fail_pkg"
        output_dir = self.test_dir / "bandit_prob_fail_project"

        run_generator(
            project_name="Bandit Prob Fail Project",
            package_name=package_name,
            output_dir=output_dir,
            task="2",
            experience_mode="1",
            optional_profile="3" # Full
        )

        config_path = output_dir / "configs/bandit_config.json"
        with open(config_path, "r") as f:
            config = json.load(f)
        config["arms"][0]["true_reward_probability"] = 1.5 # Invalid
        with open(config_path, "w") as f:
            json.dump(config, f)

        env = os.environ.copy()
        env["PYTHONPATH"] = str(output_dir / "src")
        result = subprocess.run(
            [sys.executable, "-m", f"{package_name}.lab", "bandit"],
            cwd=output_dir,
            env=env,
            capture_output=True,
            text=True
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("must be a number between 0 and 1", result.stdout)

if __name__ == "__main__":
    unittest.main()
