import unittest
import shutil
import tempfile
import json
import io
from pathlib import Path
from unittest.mock import patch
from ml_starter_generator.cli import main
from tests.helpers import run_generator

class TestWizardValidation(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_default_flow_supervised(self):
        """Verify that pressing Enter through defaults works for supervised task."""
        output_dir = self.test_dir / "default_supervised"
        run_generator(
            language="", # Default: English
            project_name="default_supervised",
            package_name="", # Default
            task="", # Default: supervised
            experience_mode="", # Default: minimal
            dataset_path="", # Default
            target_column="", # Default
            include_demo="", # Default: no
            problem_goal="",
            problem_priority="",
            problem_error_cost="",
            problem_size="",
            problem_baseline="",
            problem_note="",
            include_pyproject="n", # Skip environment for speed
            output_dir=output_dir
        )
        self.assertTrue((output_dir / "configs/config.json").exists())
        with open(output_dir / "configs/config.json", "r") as f:
            config = json.load(f)
        self.assertEqual(config["project"]["task"], "supervised")

    def test_default_flow_generic(self):
        output_dir = self.test_dir / "default_generic"
        run_generator(
            task="1", # generic
            include_pyproject="n",
            output_dir=output_dir
        )
        self.assertTrue((output_dir / "configs/config.json").exists())

    def test_default_flow_unsupervised(self):
        output_dir = self.test_dir / "default_unsupervised"
        run_generator(
            task="3", # unsupervised
            include_pyproject="n",
            output_dir=output_dir
        )
        self.assertTrue((output_dir / "configs/config.json").exists())

    def test_default_flow_timeseries(self):
        output_dir = self.test_dir / "default_timeseries"
        run_generator(
            task="4", # timeseries
            include_pyproject="n",
            output_dir=output_dir
        )
        self.assertTrue((output_dir / "configs/config.json").exists())

    def test_default_flow_vision(self):
        output_dir = self.test_dir / "default_vision"
        run_generator(
            task="5", # vision
            include_pyproject="n",
            output_dir=output_dir
        )
        self.assertTrue((output_dir / "configs/config.json").exists())

    def test_default_flow_bandit(self):
        output_dir = self.test_dir / "default_bandit"
        # Bandit task is "6"
        # It has different framing questions
        inputs = [
            "1", # en
            "default_bandit",
            "default_bandit",
            "6", # bandit
            "1", # minimal
            "data.csv",
            "reward",
            "n", # demo
            "", "", "", "", "", # 5 bandit defaults
            "", # note
            "n", # env
            "n", # docs
            "1", # profile
            "4", str(output_dir), "y", "y"
        ]
        with patch("ml_starter_generator.cli.input", side_effect=inputs):
            with patch("sys.stdout", new=io.StringIO()):
                main()
        self.assertTrue((output_dir / "configs/config.json").exists())

    def test_invalid_fixed_choice_retry(self):
        """Verify retry on invalid fixed-choice menu input."""
        output_dir = self.test_dir / "retry_menu"
        # Task selection: 99 (invalid), then 2 (supervised)
        inputs = [
            "1", "retry_menu", "retry_menu",
            "99", "2",
            "1", "data.csv", "target", "n",
            "", "", "", "", "", "", # Framing
            "n", "n", "1", "4", str(output_dir), "y", "y"
        ]
        with patch("ml_starter_generator.cli.input", side_effect=inputs):
            with patch("sys.stdout", new=io.StringIO()) as fake_out:
                main()
                output = fake_out.getvalue()
        self.assertIn("Invalid option", output)
        self.assertTrue((output_dir / "configs/config.json").exists())

    def test_invalid_yes_no_retry(self):
        """Verify retry on invalid yes/no input."""
        output_dir = self.test_dir / "retry_yesno"
        # Include demo: "maybe" (invalid), then "n"
        inputs = [
            "1", "retry_yesno", "retry_yesno", "2", "1", "data.csv", "target",
            "maybe", "n",
            "", "", "", "", "", "", # Framing
            "n", "n", "1", "4", str(output_dir), "y", "y"
        ]
        with patch("ml_starter_generator.cli.input", side_effect=inputs):
            with patch("sys.stdout", new=io.StringIO()) as fake_out:
                main()
                output = fake_out.getvalue()
        self.assertIn("Invalid option", output)
        self.assertTrue((output_dir / "configs/config.json").exists())

    def test_bilingual_ptbr_validation(self):
        """Verify pt-BR validation and yes/no behavior."""
        output_dir = self.test_dir / "ptbr_validation"
        # language 2 (pt-BR)
        # include_demo: "talvez" (invalid), then "s" (yes)
        inputs = [
            "2", "ptbr_proj", "ptbr_pkg", "2", "1", "dados.csv", "alvo",
            "talvez", "s",
            "", "", "", "", "", "", # Framing
            "n", "n", "1", "4", str(output_dir), "y", "y"
        ]
        with patch("ml_starter_generator.cli.input", side_effect=inputs):
            with patch("sys.stdout", new=io.StringIO()) as fake_out:
                main()
                output = fake_out.getvalue()
        self.assertIn("Opção inválida", output)
        self.assertTrue((output_dir / "configs/config.json").exists())
        with open(output_dir / "configs/config.json", "r") as f:
            config = json.load(f)
        # INCLUDE_DEMO affects raw_path in config.json
        self.assertEqual(config["data"]["raw_path"], "data/raw/demo_dataset.csv")

if __name__ == "__main__":
    unittest.main()
