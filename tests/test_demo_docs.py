import unittest
import shutil
import tempfile
import json
from pathlib import Path
from tests.helpers import run_generator

class TestDemoDocs(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_demo_scenario_doc_exists_when_demo_enabled(self):
        # P0.1: docs/demo-scenario.md exists when demo enabled
        run_generator(
            project_name="demo_proj",
            task="supervised",
            include_demo="y",
            output_dir=self.test_dir
        )
        self.assertTrue((self.test_dir / "docs/demo-scenario.md").exists())

    def test_demo_scenario_doc_absent_when_demo_disabled(self):
        run_generator(
            project_name="no_demo_proj",
            task="supervised",
            include_demo="n",
            output_dir=self.test_dir
        )
        self.assertFalse((self.test_dir / "docs/demo-scenario.md").exists())

    def test_synthetic_caveat_present(self):
        # P0.2: doc contains synthetic/learning-only limitation
        run_generator(
            project_name="demo_proj",
            task="supervised",
            include_demo="y",
            output_dir=self.test_dir
        )
        content = (self.test_dir / "docs/demo-scenario.md").read_text()
        self.assertIn("synthetic", content.lower())
        self.assertIn("learning-only", content.lower())

    def test_supervised_classification_docs(self):
        # P0.3, P0.4: scenario explained, columns/target match
        run_generator(
            project_name="demo_proj",
            task="supervised",
            problem_goal="1", # predict a category (classification)
            include_demo="y",
            output_dir=self.test_dir
        )
        content = (self.test_dir / "docs/demo-scenario.md").read_text()
        self.assertIn("Classification", content)
        self.assertIn("subscribed", content) # Target for classification demo
        self.assertIn("age", content)
        self.assertIn("job", content)
        self.assertIn("balance", content)

    def test_supervised_regression_docs(self):
        # P0.3, P0.4: scenario explained, columns/target match
        run_generator(
            project_name="demo_proj",
            task="supervised",
            problem_goal="2", # predict a number (regression)
            include_demo="y",
            output_dir=self.test_dir
        )
        content = (self.test_dir / "docs/demo-scenario.md").read_text()
        self.assertIn("Regression", content)
        self.assertIn("price", content) # Target for regression demo
        self.assertIn("sqft", content)
        self.assertIn("bedrooms", content)
        self.assertIn("age", content)

    def test_unsupervised_docs(self):
        # P0.5: unsupervised no-target explanation
        run_generator(
            project_name="demo_proj",
            task="unsupervised",
            include_demo="y",
            output_dir=self.test_dir
        )
        content = (self.test_dir / "docs/demo-scenario.md").read_text()
        self.assertIn("Unsupervised", content)
        self.assertIn("no target", content.lower())
        self.assertIn("pattern", content.lower())
        self.assertIn("customer_id", content)
        self.assertIn("spend_score", content)

    def test_timeseries_docs(self):
        # P0.6: timeseries explanation
        run_generator(
            project_name="demo_proj",
            task="timeseries",
            include_demo="y",
            output_dir=self.test_dir
        )
        content = (self.test_dir / "docs/demo-scenario.md").read_text()
        self.assertIn("Time Series", content)
        self.assertIn("date", content.lower())
        self.assertIn("forecasting", content.lower())
        self.assertIn("sales", content)
        self.assertIn("on_promotion", content)

    def test_vision_docs(self):
        # P0.7: vision metadata caveat
        run_generator(
            project_name="demo_proj",
            task="vision",
            include_demo="y",
            output_dir=self.test_dir
        )
        content = (self.test_dir / "docs/demo-scenario.md").read_text()
        self.assertIn("Vision", content)
        self.assertIn("metadata", content.lower())
        self.assertIn("does **not** include real image files", content.lower())
        self.assertIn("image_path", content)
        self.assertIn("label", content)

    def test_readme_onboarding_references_demo_doc(self):
        # P0.8: README/terminal onboarding references demo doc when demo enabled
        # Checking README first
        run_generator(
            project_name="demo_proj",
            task="supervised",
            include_demo="y",
            output_dir=self.test_dir
        )
        readme_content = (self.test_dir / "README.md").read_text()
        self.assertIn("docs/demo-scenario.md", readme_content)

        # Checking non-demo
        shutil.rmtree(self.test_dir)
        self.test_dir.mkdir()
        run_generator(
            project_name="no_demo_proj",
            task="supervised",
            include_demo="n",
            output_dir=self.test_dir
        )
        readme_content = (self.test_dir / "README.md").read_text()
        self.assertNotIn("docs/demo-scenario.md", readme_content)

    def test_terminal_summary_references_demo_doc(self):
        # P0.8: terminal points to START_HERE.md which references demo doc
        output = run_generator(
            project_name="demo_proj",
            task="supervised",
            include_demo="y",
            output_dir=self.test_dir
        )
        self.assertIn("START_HERE.md", output)

        # Checking non-demo
        shutil.rmtree(self.test_dir)
        self.test_dir.mkdir()
        output = run_generator(
            project_name="no_demo_proj",
            task="supervised",
            include_demo="n",
            output_dir=self.test_dir
        )
        self.assertIn("START_HERE.md", output)

if __name__ == "__main__":
    unittest.main()
