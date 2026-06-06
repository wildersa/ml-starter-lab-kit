import unittest
from pathlib import Path
import shutil
import tempfile
from ml_starter_generator import scaffold

class TestReadmeClarity(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.values = {
            "PROJECT_NAME": "Test Project",
            "PACKAGE_NAME": "test_project",
            "TASK": "supervised",
            "DATASET_PATH": "data/raw/dataset.csv",
            "TARGET_COLUMN": "target",
            "ADVISOR_COMMAND": "python -m test_project.advisor",
            "ADVISOR_QUICKSTART": """
### 6. Dataset Advisor (Optional)
Run the Dataset Advisor to get expert-like feedback on your data:
```bash
python -m test_project.advisor
```
It generates:
- `reports/dataset-advice.md`: A report with data quality findings and model recommendations.
- `src/test_project/suggested_pipeline.py`: A starter scikit-learn pipeline with appropriate preprocessing for your specific columns.
"""
        }

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_readme_contains_p0_objectives(self):
        scaffold.create_readme(self.test_dir, self.values, force=True)
        readme_path = self.test_dir / "README.md"
        content = readme_path.read_text()

        # P0.1 — Default dataset path
        self.assertIn("data/raw/dataset.csv", content)

        # P0.2 — Config fields
        self.assertIn("data.raw_path", content)
        self.assertIn("data.processed_path", content)
        self.assertIn("target.column", content)

        # P0.3/P0.4 — Target vs Features
        self.assertIn("Target vs Features", content)
        self.assertIn("Target**: The single column", content)
        self.assertIn("Features**: The many columns", content)
        self.assertIn("age,city,income,bought_product", content)

        # P0.5 — Baseline meaning
        self.assertIn("baseline model", content.lower())
        self.assertIn("starting benchmark", content)
        self.assertIn("not** a final production model", content.lower())

        # P0.6 — features.py
        self.assertIn("features.py", content)
        self.assertIn("calculated features", content)
        self.assertIn("existing columns in your CSV are already candidate features", content)

        # P0.7 — Advisor
        self.assertIn("Dataset Advisor", content)
        self.assertIn("suggested_pipeline.py", content)
        self.assertIn("python -m test_project.advisor", content)

    def test_readme_advisor_conditional(self):
        # Test when advisor is NOT enabled
        values_no_advisor = self.values.copy()
        values_no_advisor["ADVISOR_COMMAND"] = ""
        values_no_advisor["ADVISOR_QUICKSTART"] = ""

        scaffold.create_readme(self.test_dir, values_no_advisor, force=True)
        readme_path = self.test_dir / "README.md"
        content = readme_path.read_text()

        # Should NOT contain advisor section
        self.assertNotIn("### 6. Dataset Advisor", content)
        self.assertNotIn("reports/dataset-advice.md", content)

if __name__ == "__main__":
    unittest.main()
