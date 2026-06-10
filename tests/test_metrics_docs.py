import unittest
from pathlib import Path

class TestMetricsDocs(unittest.TestCase):
    def setUp(self):
        self.docs_dir = Path("docs/metrics")
        self.required_files = [
            "classification.md",
            "regression.md",
            "time-series.md",
            "clustering.md",
            "vision.md",
            "bandits.md",
            "README.md"
        ]

    def test_files_exist(self):
        for filename in self.required_files:
            with self.subTest(file=filename):
                self.assertTrue((self.docs_dir / filename).exists())
                # Check Portuguese version too
                pt_filename = filename.replace(".md", ".pt-BR.md")
                self.assertTrue((self.docs_dir / pt_filename).exists())

    def test_classification_content(self):
        # P0.1 coverage
        content = (self.docs_dir / "classification.md").read_text()
        required_terms = [
            "Confusion Matrix", "Precision", "Recall", "F1-Score",
            "ROC-AUC", "Threshold", "False Negative", "False Positive"
        ]
        for term in required_terms:
            self.assertIn(term, content)

        # P0.5: Shared structure
        self.assertIn("What it answers", content)
        self.assertIn("When to use it", content)
        self.assertIn("Common trap", content)
        self.assertIn("Example", content)

        # P0.6: Reference to evaluation concept
        self.assertIn("../checklists/before-evaluation.md", content)

    def test_regression_time_series_content(self):
        # P0.2 coverage
        reg_content = (self.docs_dir / "regression.md").read_text()
        ts_content = (self.docs_dir / "time-series.md").read_text()

        for term in ["MAE", "RMSE", "MAPE", "R²"]:
            self.assertIn(term, reg_content)

        self.assertIn("MAPE", ts_content)
        self.assertIn("Backtesting", ts_content)
        self.assertIn("Horizon", ts_content)
        self.assertIn("Window", ts_content)

        self.assertIn("Practical Tip", reg_content)
        self.assertIn("Practical Tip", ts_content)

        self.assertIn("../checklists/before-evaluation.md", reg_content)
        self.assertIn("../checklists/before-evaluation.md", ts_content)

    def test_clustering_vision_content(self):
        # P0.3 coverage
        clu_content = (self.docs_dir / "clustering.md").read_text()
        vis_content = (self.docs_dir / "vision.md").read_text()

        self.assertIn("Inertia", clu_content)
        self.assertIn("Silhouette", clu_content)
        self.assertIn("Qualitative Interpretation", clu_content)

        self.assertIn("mAP", vis_content)
        self.assertIn("IoU", vis_content)
        self.assertIn("Dice", vis_content)

        self.assertIn("../checklists/before-evaluation.md", clu_content)
        self.assertIn("../checklists/before-evaluation.md", vis_content)

    def test_bandits_content(self):
        # P0.4 coverage
        content = (self.docs_dir / "bandits.md").read_text()
        required_terms = [
            "Reward", "Cumulative Reward", "Regret", "Lift vs. Baseline",
            "Arm Distribution", "Exploration Cost", "User Behavior Drift"
        ]
        for term in required_terms:
            self.assertIn(term, content)

        self.assertIn("../checklists/before-evaluation.md", content)

if __name__ == "__main__":
    unittest.main()
