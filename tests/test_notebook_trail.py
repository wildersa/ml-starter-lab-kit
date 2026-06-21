import unittest
import tempfile
import shutil
from pathlib import Path
from ml_starter_generator.scaffold import create_notebook_trail, create_dirs

class TestNotebookTrail(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.package_name = "test_pkg"
        create_dirs(self.test_dir, self.package_name, "none", False)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_notebook_trail_supervised(self):
        values = {"TASK": "supervised", "PACKAGE_NAME": self.package_name, "PROJECT_NAME": "Test Project", "LANGUAGE": "en"}
        create_notebook_trail(self.test_dir, values, force=True)

        expected_files = [
            "00_start_here.ipynb",
            "01_data_understanding.ipynb",
            "02_eda.ipynb",
            "03_preprocessing_and_features.ipynb",
            "04_baseline_classification_or_regression.ipynb",
            "05_evaluation_and_interpretation.ipynb",
            "06_experiment_notes_and_next_steps.ipynb"
        ]

        for f in expected_files:
            self.assertTrue((self.test_dir / "notebooks" / f).exists(), f"{f} should exist for supervised task")

    def test_notebook_trail_unsupervised(self):
        values = {"TASK": "unsupervised", "PACKAGE_NAME": self.package_name, "PROJECT_NAME": "Test Project", "LANGUAGE": "en"}
        create_notebook_trail(self.test_dir, values, force=True)

        expected_files = [
            "00_start_here.ipynb",
            "01_data_understanding.ipynb",
            "02_eda.ipynb",
            "03_preprocessing_and_features.ipynb",
            "04_clustering_baseline.ipynb",
            "05_cluster_interpretation.ipynb",
            "06_experiment_notes_and_next_steps.ipynb"
        ]

        for f in expected_files:
            self.assertTrue((self.test_dir / "notebooks" / f).exists(), f"{f} should exist for unsupervised task")

    def test_notebook_trail_timeseries(self):
        values = {"TASK": "timeseries", "PACKAGE_NAME": self.package_name, "PROJECT_NAME": "Test Project", "LANGUAGE": "en"}
        create_notebook_trail(self.test_dir, values, force=True)

        expected_files = [
            "00_start_here.ipynb",
            "01_data_understanding.ipynb",
            "02_eda.ipynb",
            "03_temporal_split.ipynb",
            "04_naive_temporal_baseline.ipynb",
            "05_evaluation_and_interpretation.ipynb",
            "06_experiment_notes_and_next_steps.ipynb"
        ]

        for f in expected_files:
            self.assertTrue((self.test_dir / "notebooks" / f).exists(), f"{f} should exist for timeseries task")

    def test_notebook_trail_bandit(self):
        values = {"TASK": "bandit", "PACKAGE_NAME": self.package_name, "PROJECT_NAME": "Test Project", "LANGUAGE": "en"}
        create_notebook_trail(self.test_dir, values, force=True)

        expected_files = [
            "00_start_here.ipynb",
            "01_data_understanding.ipynb",
            "02_eda.ipynb",
            "03_actions_rewards_context.ipynb",
            "04_policy_simulation_baseline.ipynb",
            "05_evaluation_and_interpretation.ipynb",
            "06_experiment_notes_and_next_steps.ipynb"
        ]

        for f in expected_files:
            self.assertTrue((self.test_dir / "notebooks" / f).exists(), f"{f} should exist for bandit task")

if __name__ == "__main__":
    unittest.main()
