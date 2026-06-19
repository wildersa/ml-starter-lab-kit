import unittest
import shutil
import tempfile
import os
from pathlib import Path
from tests.helpers import run_generator

class TestLearningMaterials(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_learning_materials_supervised_en(self):
        run_generator(
            project_name="supervised_en",
            package_name="supervised_en",
            task="2", # supervised
            output_dir=self.test_dir,
            language="1" # en
        )

        learning_path = self.test_dir / "docs/learning-path.md"
        experiment_notes = self.test_dir / "reports/experiment-notes.md"

        self.assertTrue(learning_path.exists())
        self.assertTrue(experiment_notes.exists())

        content = learning_path.read_text()
        self.assertIn("Supervised learning means training a model", content)
        self.assertIn("Accuracy/F1", content)
        self.assertIn("Target Leakage", content)

        notes_content = experiment_notes.read_text()
        self.assertIn("# Experiment Notes", notes_content)
        self.assertIn("Hypothesis", notes_content)

    def test_learning_materials_supervised_pt(self):
        run_generator(
            project_name="supervised_pt",
            package_name="supervised_pt",
            task="2", # supervised
            output_dir=self.test_dir,
            language="2" # pt-BR
        )

        learning_path = self.test_dir / "docs/learning-path.pt-BR.md"
        experiment_notes = self.test_dir / "reports/experiment-notes.pt-BR.md"

        self.assertTrue(learning_path.exists())
        self.assertTrue(experiment_notes.exists())

        content = learning_path.read_text()
        self.assertIn("O aprendizado supervisionado consiste em treinar um modelo", content)
        self.assertIn("Acurácia/F1", content)
        self.assertIn("Vazamento de Alvo", content)

        notes_content = experiment_notes.read_text()
        self.assertIn("# Notas de Experimento", notes_content)
        self.assertIn("Hipótese", notes_content)

    def test_learning_materials_bandit_en(self):
        run_generator(
            project_name="bandit_en",
            package_name="bandit_en",
            task="6", # bandit
            output_dir=self.test_dir,
            language="1" # en
        )

        learning_path = self.test_dir / "docs/learning-path.md"
        self.assertTrue(learning_path.exists())

        content = learning_path.read_text()
        self.assertIn("Multi-Armed Bandit (MAB)", content)
        self.assertIn("Cumulative Reward", content)

    def test_learning_materials_timeseries_en(self):
        run_generator(
            project_name="ts_en",
            package_name="ts_en",
            task="4", # timeseries
            output_dir=self.test_dir,
            language="1" # en
        )

        learning_path = self.test_dir / "docs/learning-path.md"
        self.assertTrue(learning_path.exists())

        content = learning_path.read_text()
        self.assertIn("Time series analysis deals with data points", content)
        self.assertIn("Time Index", content)
        self.assertIn("Chronological Leakage", content)

if __name__ == "__main__":
    unittest.main()
