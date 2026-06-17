import unittest
from pathlib import Path
import shutil
import tempfile
import os
import sys
import subprocess
import json
import pandas as pd
from tests.helpers import run_generator

class TestSyntheticDataLab(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_synthetic_data_generation_scenarios(self):
        """Verify that all synthetic data scenarios can be generated."""
        package_name = "synth_test_pkg"
        output_dir = self.test_dir / "synth_test_project"

        run_generator(
            project_name="Synthetic Test Project",
            package_name=package_name,
            output_dir=output_dir,
            task="2",
            experience_mode="1",
            optional_profile="3" # Full profile includes synthetic_data
        )

        scenarios = [
            "classification",
            "regression",
            "clustering",
            "timeseries",
            "bandit_simple",
            "bandit_contextual_events",
            "bank_campaign_bandit"
        ]

        env = os.environ.copy()
        env["PYTHONPATH"] = str(output_dir / "src")

        config_path = output_dir / "configs/synthetic_data.json"

        for scenario in scenarios:
            # Update config for the scenario
            with open(config_path, "r") as f:
                config = json.load(f)

            config["scenario"] = scenario
            if scenario in config.get("scenario_examples", {}):
                config["parameters"] = config["scenario_examples"][scenario]

            with open(config_path, "w") as f:
                json.dump(config, f)

            # Run synthetic data generation
            result = subprocess.run(
                [sys.executable, "-m", f"{package_name}.lab", "synthetic"],
                cwd=output_dir,
                env=env,
                capture_output=True,
                text=True
            )

            self.assertEqual(result.returncode, 0, f"Scenario {scenario} failed:\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}")

            # Check if artifacts exist
            data_file = output_dir / f"data/synthetic/{scenario}.csv"
            meta_file = output_dir / f"data/synthetic/{scenario}_meta.json"
            report_file = output_dir / "reports/synthetic-data-summary.md"

            self.assertTrue(data_file.exists(), f"Data file for {scenario} missing")
            self.assertTrue(meta_file.exists(), f"Meta file for {scenario} missing")
            self.assertTrue(report_file.exists(), f"Report file for {scenario} missing")

            # Basic data validation
            df = pd.read_csv(data_file)
            self.assertGreater(len(df), 0)

            if scenario == "classification":
                self.assertIn("target", df.columns)
            elif scenario == "regression":
                self.assertIn("target", df.columns)
            elif scenario == "timeseries":
                self.assertIn("date", df.columns)
                self.assertIn("value", df.columns)
            elif scenario == "bandit_simple":
                self.assertIn("round", df.columns)
                self.assertIn("arm", df.columns)
                self.assertIn("reward", df.columns)
            elif scenario == "bandit_contextual_events":
                self.assertIn("action", df.columns)
                self.assertIn("reward", df.columns)
                self.assertTrue(any(c.startswith("context_") for c in df.columns))
            elif scenario == "bank_campaign_bandit":
                # P0.1 Assert bank_campaign_bandit output has required columns and non-empty event rows.
                required_cols = [
                    "event_id", "timestamp", "customer_id", "age", "balance", "job",
                    "segment", "channel_preference", "previous_contacts", "arm_name",
                    "action_probability", "policy_name", "reward", "conversion",
                    "revenue", "delay_days"
                ]
                for col in required_cols:
                    self.assertIn(col, df.columns)
                self.assertGreater(len(df), 0)

    def test_synthetic_data_determinism(self):
        """Verify that synthetic data generation is deterministic with the same seed."""
        package_name = "synth_det_pkg"
        output_dir = self.test_dir / "synth_det_project"

        run_generator(
            project_name="Synthetic Determinism Project",
            package_name=package_name,
            output_dir=output_dir,
            task="2",
            experience_mode="1",
            optional_profile="3"
        )

        env = os.environ.copy()
        env["PYTHONPATH"] = str(output_dir / "src")

        # Run twice and compare
        data_paths = []
        for i in range(2):
            subprocess.run(
                [sys.executable, "-m", f"{package_name}.lab", "synthetic"],
                cwd=output_dir,
                env=env,
                capture_output=True
            )
            df = pd.read_csv(output_dir / "data/synthetic/classification.csv")
            data_paths.append(df)

        pd.testing.assert_frame_equal(data_paths[0], data_paths[1])

        # P0.2 Verify bank_campaign_bandit is deterministic
        data_paths = []
        for i in range(2):
            with open(output_dir / "configs/synthetic_data.json", "r") as f:
                config = json.load(f)
            config["scenario"] = "bank_campaign_bandit"
            config["seed"] = 42
            with open(output_dir / "configs/synthetic_data.json", "w") as f:
                json.dump(config, f)

            subprocess.run(
                [sys.executable, "-m", f"{package_name}.lab", "synthetic"],
                cwd=output_dir,
                env=env,
                capture_output=True
            )
            df = pd.read_csv(output_dir / "data/synthetic/bank_campaign_bandit.csv")
            data_paths.append(df)

        pd.testing.assert_frame_equal(data_paths[0], data_paths[1])

    def test_synthetic_data_activation_bandit(self):
        """P0.3 Verify activation treats bank_campaign_bandit as Bandit and sets target to reward."""
        package_name = "synth_act_pkg"
        output_dir = self.test_dir / "synth_act_project"

        run_generator(
            project_name="Synthetic Activation Project",
            package_name=package_name,
            output_dir=output_dir,
            task="2",
            experience_mode="1",
            optional_profile="3"
        )

        env = os.environ.copy()
        env["PYTHONPATH"] = str(output_dir / "src")
        config_path = output_dir / "configs/synthetic_data.json"

        with open(config_path, "r") as f:
            config = json.load(f)
        config["scenario"] = "bank_campaign_bandit"
        config["activate_as_project_dataset"] = True
        with open(config_path, "w") as f:
            json.dump(config, f)

        subprocess.run(
            [sys.executable, "-m", f"{package_name}.lab", "synthetic"],
            cwd=output_dir,
            env=env,
            capture_output=True
        )

        # Check project config
        with open(output_dir / "configs/config.json", "r") as f:
            proj_config = json.load(f)

        self.assertEqual(proj_config["target"]["column"], "reward")
        self.assertIn("bank_campaign_bandit.csv", proj_config["data"]["raw_path"])

    def test_synthetic_data_docs_content(self):
        """P0.4 Verify EN/PT-BR Synthetic Data Lab docs mention bank_campaign_bandit and explain concepts."""
        # We can check the templates directly since they are in the repo
        templates_dir = Path("templates/project/docs")
        en_doc = (templates_dir / "synthetic-data-lab.md.tpl").read_text(encoding="utf-8")
        pt_doc = (templates_dir / "synthetic-data-lab.pt-BR.md.tpl").read_text(encoding="utf-8")

        for doc in [en_doc, pt_doc]:
            self.assertIn("bank_campaign_bandit", doc.lower())
            # Check for context, action/arm, reward, delay
            self.assertTrue(any(x in doc.lower() for x in ["context", "contexto"]))
            self.assertTrue(any(x in doc.lower() for x in ["arm", "action", "braço", "ação"]))
            self.assertTrue(any(x in doc.lower() for x in ["reward", "recompensa"]))
            self.assertTrue(any(x in doc.lower() for x in ["delay", "atraso"]))

    def test_synthetic_data_validation_failures(self):
        """Verify that invalid config fails with non-zero exit code and no artifacts."""
        package_name = "synth_fail_pkg"
        output_dir = self.test_dir / "synth_fail_project"

        run_generator(
            project_name="Synthetic Failure Project",
            package_name=package_name,
            output_dir=output_dir,
            task="2",
            experience_mode="1",
            optional_profile="3"
        )

        env = os.environ.copy()
        env["PYTHONPATH"] = str(output_dir / "src")
        config_path = output_dir / "configs/synthetic_data.json"

        # 1. Invalid Scenario
        with open(config_path, "r") as f:
            config = json.load(f)
        config["scenario"] = "invalid_scenario_name"
        with open(config_path, "w") as f:
            json.dump(config, f)

        result = subprocess.run(
            [sys.executable, "-m", f"{package_name}.lab", "synthetic"],
            cwd=output_dir,
            env=env,
            capture_output=True,
            text=True
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Error: Unknown scenario", result.stdout + result.stderr)

        # Ensure no CSV was generated for the invalid scenario
        invalid_csv = output_dir / "data/synthetic/invalid_scenario_name.csv"
        self.assertFalse(invalid_csv.exists())

        # 2. Invalid Parameter (e.g. string where number expected in scikit-learn scenarios)
        with open(config_path, "r") as f:
            config = json.load(f)
        config["scenario"] = "classification"
        config["parameters"] = {"n_samples": "not_a_number"}
        with open(config_path, "w") as f:
            json.dump(config, f)

        result = subprocess.run(
            [sys.executable, "-m", f"{package_name}.lab", "synthetic"],
            cwd=output_dir,
            env=env,
            capture_output=True,
            text=True
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Error:", result.stdout + result.stderr)

    def test_bank_campaign_bandit_report_content(self):
        """P0.1-P0.5 Verify that for bank_campaign_bandit, the report contains Bandit-specific sections."""
        package_name = "synth_report_pkg"
        output_dir = self.test_dir / "synth_report_project"

        run_generator(
            project_name="Synthetic Report Project",
            package_name=package_name,
            output_dir=output_dir,
            task="2",
            experience_mode="1",
            optional_profile="3"
        )

        env = os.environ.copy()
        env["PYTHONPATH"] = str(output_dir / "src")
        config_path = output_dir / "configs/synthetic_data.json"

        with open(config_path, "r") as f:
            config = json.load(f)
        config["scenario"] = "bank_campaign_bandit"
        with open(config_path, "w") as f:
            json.dump(config, f)

        subprocess.run(
            [sys.executable, "-m", f"{package_name}.lab", "synthetic"],
            cwd=output_dir,
            env=env,
            capture_output=True
        )

        report_path = output_dir / "reports/synthetic-data-summary.md"
        self.assertTrue(report_path.exists())
        content = report_path.read_text(encoding="utf-8")

        # P0.1 Bandit/contextual logged-data section
        self.assertIn("Bandit Scenario Analysis", content)
        self.assertIn("Logged Contextual Bandit Data", content)

        # P0.2 Conversion/reward information grouped by arm_name
        self.assertIn("Arm Statistics", content)
        self.assertIn("Conv. Rate", content)
        self.assertIn("term_deposit_email", content)

        # P0.3 Revenue grouped by arm_name
        self.assertIn("Total Revenue", content)
        self.assertIn("Avg. Revenue", content)

        # P0.4 Action probability / logging policy interpretation
        self.assertIn("Action Probability Distribution", content)

        # P0.5 Delayed reward information using delay_days
        self.assertIn("Reward Delay Summary", content)
        self.assertIn("Avg. Delay (days)", content)

    def test_non_bandit_report_remains_generic(self):
        """P0.6 Verify that non-Bandit scenarios do not have Bandit sections."""
        package_name = "synth_generic_pkg"
        output_dir = self.test_dir / "synth_generic_project"

        run_generator(
            project_name="Synthetic Generic Project",
            package_name=package_name,
            output_dir=output_dir,
            task="1", # Classification
            experience_mode="1",
            optional_profile="3"
        )

        env = os.environ.copy()
        env["PYTHONPATH"] = str(output_dir / "src")

        subprocess.run(
            [sys.executable, "-m", f"{package_name}.lab", "synthetic"],
            cwd=output_dir,
            env=env,
            capture_output=True
        )

        report_path = output_dir / "reports/synthetic-data-summary.md"
        content = report_path.read_text(encoding="utf-8")

        self.assertNotIn("Bandit Scenario Analysis", content)
        self.assertNotIn("Arm Statistics", content)
        self.assertNotIn("Action Probability Distribution", content)
        self.assertNotIn("Reward Delay Summary", content)

    def test_bank_campaign_bandit_report_content_pt_br(self):
        """Verify PT-BR localized report for bank_campaign_bandit."""
        package_name = "synth_report_pt_pkg"
        output_dir = self.test_dir / "synth_report_pt_project"

        run_generator(
            project_name="Synthetic Report PT Project",
            package_name=package_name,
            output_dir=output_dir,
            task="2",
            experience_mode="1",
            optional_profile="3"
        )

        env = os.environ.copy()
        env["PYTHONPATH"] = str(output_dir / "src")

        # Force PT-BR in problem_profile.json
        profile_path = output_dir / "configs/problem_profile.json"
        profile = {"language": "pt-BR"}
        with open(profile_path, "w") as f:
            json.dump(profile, f)

        config_path = output_dir / "configs/synthetic_data.json"
        with open(config_path, "r") as f:
            config = json.load(f)
        config["scenario"] = "bank_campaign_bandit"
        with open(config_path, "w") as f:
            json.dump(config, f)

        subprocess.run(
            [sys.executable, "-m", f"{package_name}.lab", "synthetic"],
            cwd=output_dir,
            env=env,
            capture_output=True
        )

        report_path = output_dir / "reports/synthetic-data-summary.md"
        content = report_path.read_text(encoding="utf-8")

        self.assertIn("Análise do Cenário de Bandit", content)
        self.assertIn("Estatísticas dos Braços (Arms)", content)
        self.assertIn("Taxa de Conv.", content)
        self.assertIn("Atraso Médio (dias)", content)

if __name__ == "__main__":
    unittest.main()
