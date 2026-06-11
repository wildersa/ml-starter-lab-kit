import unittest
from pathlib import Path

class TestMetricsDocs(unittest.TestCase):
    def setUp(self):
        self.docs_dir = Path("docs/metrics")
        self.files = [
            "classification.md",
            "regression.md",
            "time-series.md",
            "clustering.md",
            "vision.md",
            "bandits.md"
        ]
        self.pt_files = [f.replace(".md", ".pt-BR.md") for f in self.files]

    def test_shared_concept_link(self):
        """P0.6: Each page references the shared evaluation/monitoring concept page."""
        for filename in self.files + self.pt_files:
            filepath = self.docs_dir / filename
            content = filepath.read_text(encoding="utf-8")
            self.assertIn("evaluation-and-monitoring.md", content, f"{filename} missing link to evaluation concept")

    def test_classification_terms(self):
        """P0.1: Classification page contains required metric/error-cost terms."""
        terms = [
            "confusion matrix", "precision", "recall", "f1",
            "roc-auc", "threshold", "false negative cost", "false positive cost"
        ]
        content = (self.docs_dir / "classification.md").read_text(encoding="utf-8").lower()
        for term in terms:
            self.assertIn(term, content, f"classification.md missing term: {term}")

        # PT-BR check
        pt_terms = ["matriz de confusão", "precisão", "recall", "f1", "threshold", "custo do falso negativo"]
        pt_content = (self.docs_dir / "classification.pt-BR.md").read_text(encoding="utf-8").lower()
        for term in pt_terms:
            self.assertIn(term, pt_content, f"classification.pt-BR.md missing term: {term}")

    def test_regression_and_timeseries_terms(self):
        """P0.2: Regression/time-series pages contain MAPE limitation and backtesting/horizon language."""
        reg_content = (self.docs_dir / "regression.md").read_text(encoding="utf-8").lower()
        ts_content = (self.docs_dir / "time-series.md").read_text(encoding="utf-8").lower()

        for content, filename in [(reg_content, "regression.md"), (ts_content, "time-series.md")]:
            self.assertIn("mae", content)
            self.assertIn("rmse", content)
            self.assertIn("mape", content)
            if filename == "regression.md":
                self.assertIn("r²", content)
                self.assertIn("limitation", content)
                self.assertIn("zero", content)
            else:
                self.assertIn("backtesting", content)
                self.assertIn("horizon", content)

    def test_clustering_and_vision_terms(self):
        """P0.3: Clustering/vision pages contain distinct non-generic metric families."""
        cluster_content = (self.docs_dir / "clustering.md").read_text(encoding="utf-8").lower()
        vision_content = (self.docs_dir / "vision.md").read_text(encoding="utf-8").lower()

        self.assertIn("inertia", cluster_content)
        self.assertIn("silhouette", cluster_content)
        self.assertIn("qualitative", cluster_content)

        self.assertIn("map", vision_content)
        self.assertIn("iou", vision_content)
        self.assertIn("dice", vision_content)

    def test_bandits_terms(self):
        """P0.4: Bandits page contains reward/regret/lift/exploration/user-drift language."""
        content = (self.docs_dir / "bandits.md").read_text(encoding="utf-8").lower()
        terms = ["reward", "cumulative reward", "regret", "lift", "exploration cost", "user drift"]
        for term in terms:
            self.assertIn(term, content, f"bandits.md missing term: {term}")

    def test_consistent_structure(self):
        """P0.5: Each page follows a consistent beginner-friendly structure."""
        structure_markers = ["what it answers", "when to use", "when to avoid", "common trap", "example"]
        for filename in self.files:
            filepath = self.docs_dir / filename
            content = filepath.read_text(encoding="utf-8").lower()
            for marker in structure_markers:
                self.assertIn(marker, content, f"{filename} missing structure marker: {marker}")

if __name__ == "__main__":
    unittest.main()
