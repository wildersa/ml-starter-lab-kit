import unittest
import shutil
import tempfile
from pathlib import Path
from tests.helpers import run_generator

class TestEvaluationDocs(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_evaluation_doc_presence(self):
        """P0.1: Generated projects include docs/evaluation.md."""
        run_generator(
            project_name="test_eval",
            package_name="test_eval",
            task="2", # supervised
            output_dir=self.test_dir
        )
        eval_path = self.test_dir / "docs/evaluation.md"
        self.assertTrue(eval_path.exists())

    def test_evaluation_doc_flow_terms(self):
        """P0.2: Generated doc contains flow terms."""
        run_generator(
            project_name="test_eval",
            package_name="test_eval",
            task="2",
            output_dir=self.test_dir
        )
        eval_content = (self.test_dir / "docs/evaluation.md").read_text()
        terms = ["split", "target", "prediction", "baseline", "metric", "interpretation"]
        for term in terms:
            self.assertIn(term, eval_content.lower())

    def test_classification_terms(self):
        """P0.3: Classification supervised generation explains specific terms."""
        # Task 2 (supervised) + default goal (predict category) = classification
        run_generator(
            project_name="test_class",
            package_name="test_class",
            task="2",
            output_dir=self.test_dir
        )
        eval_content = (self.test_dir / "docs/evaluation.md").read_text()
        self.assertIn("Confusion Matrix", eval_content)
        self.assertIn("Precision", eval_content)
        self.assertIn("Recall", eval_content)
        self.assertIn("F1-Score", eval_content)
        self.assertIn("Thresholds", eval_content)
        self.assertIn("False Positive", eval_content)
        self.assertIn("False Negative", eval_content)
        # Should NOT contain regression specific advice
        self.assertNotIn("Avoid Accuracy", eval_content)

    def test_regression_terms(self):
        """P0.4: Regression supervised generation explains specific terms."""
        # Task 2 (supervised) + Goal 2 (predict number) = regression
        run_generator(
            project_name="test_reg",
            package_name="test_reg",
            task="2",
            problem_goal="2",
            output_dir=self.test_dir
        )
        eval_content = (self.test_dir / "docs/evaluation.md").read_text()
        self.assertIn("MAE", eval_content)
        self.assertIn("RMSE", eval_content)
        self.assertIn("MAPE", eval_content)
        self.assertIn("Avoid Accuracy", eval_content)
        # Should NOT contain classification terms
        self.assertNotIn("Confusion Matrix", eval_content)

    def test_timeseries_terms(self):
        """P0.4: Time-series generation explains specific terms."""
        run_generator(
            project_name="test_ts",
            package_name="test_ts",
            task="4", # timeseries
            output_dir=self.test_dir
        )
        eval_content = (self.test_dir / "docs/evaluation.md").read_text()
        self.assertIn("Backtesting", eval_content)
        self.assertIn("Forecast Horizon", eval_content)
        self.assertNotIn("Confusion Matrix", eval_content)

    def test_other_tasks_terms(self):
        """P0.5: Clustering/vision/bandit supported outputs avoid generic wrong metric text."""
        # Unsupervised
        run_generator(
            project_name="test_un",
            package_name="test_un",
            task="3",
            output_dir=self.test_dir
        )
        eval_content = (self.test_dir / "docs/evaluation.md").read_text()
        self.assertIn("Silhouette Score", eval_content)
        self.assertNotIn("Confusion Matrix", eval_content)
        self.assertNotIn("MAE", eval_content)

        # Vision
        shutil.rmtree(self.test_dir)
        self.test_dir.mkdir()
        run_generator(
            project_name="test_vis",
            package_name="test_vis",
            task="5",
            output_dir=self.test_dir
        )
        eval_content = (self.test_dir / "docs/evaluation.md").read_text()
        self.assertIn("mAP", eval_content)

        # Bandit (Custom profile enabling bandit)
        shutil.rmtree(self.test_dir)
        self.test_dir.mkdir()
        run_generator(
            project_name="test_ban",
            package_name="test_ban",
            task="2",
            optional_profile="4", # custom
            optionals=["n"]*12 + ["y"], # last one is bandit_lab
            output_dir=self.test_dir
        )
        eval_content = (self.test_dir / "docs/evaluation.md").read_text()
        self.assertIn("Regret", eval_content)
        self.assertIn("Cumulative Reward", eval_content)

    def test_readme_reference(self):
        """P0.6: README references the evaluation doc."""
        run_generator(
            project_name="test_ref",
            package_name="test_ref",
            task="2",
            output_dir=self.test_dir
        )
        readme_content = (self.test_dir / "README.md").read_text()
        self.assertIn("Evaluate results (see `docs/evaluation.md`)", readme_content)

    def test_localization(self):
        """Verify PT-BR version."""
        run_generator(
            project_name="test_pt",
            package_name="test_pt",
            task="2",
            language="2", # PT-BR
            output_dir=self.test_dir
        )
        eval_path = self.test_dir / "docs/evaluation.md"
        self.assertTrue(eval_path.exists())
        eval_content = eval_path.read_text()
        self.assertIn("Guia de Avaliação", eval_content)
        self.assertIn("Matriz de Confusão", eval_content)

        readme_content = (self.test_dir / "README.md").read_text()
        self.assertIn("Avalie os resultados (veja `docs/evaluation.md`)", readme_content)

if __name__ == "__main__":
    unittest.main()
