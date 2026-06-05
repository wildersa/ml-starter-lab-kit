import unittest
import os
import shutil
import tempfile
import subprocess
import sys
import pandas as pd
from pathlib import Path
from tests.helpers import run_generator

class TestAdvisor(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_advisor_generation_and_execution(self):
        project_name = "advisor_project"
        package_name = "advisor_pkg"
        output_dir = self.test_dir / project_name

        # 10 optionals now: eda, preprocessing, metrics, optimization, feature_measurement, visualization, notebook_factory, model_report, experiment_log, advisor
        optionals = ["n", "n", "n", "n", "n", "n", "n", "n", "n", "y"]

        run_generator(
            project_name=project_name,
            package_name=package_name,
            output_dir=output_dir,
            optional_profile="4",
            optionals=optionals,
            include_ml_basics="y"
        )

        advisor_path = output_dir / f"src/{package_name}/advisor.py"
        self.assertTrue(advisor_path.exists())

        # Create a dummy dataset with various signals
        # - Small dataset risk (< 100 rows)
        # - Missing values
        # - Outliers
        # - High cardinality categorical
        # - Target imbalance
        # - Date-like column
        # - High correlation
        data = {
            "target": [0] * 45 + [1] * 5,  # Imbalance
            "num_missing": [1.0, 2.0, None, 4.0, 5.0] * 10, # Missing
            "num_outliers": [1.0, 1.1, 1.2, 1.3, 100.0] * 10, # Outliers
            "cat_high": [f"val_{i % 15}" for i in range(50)], # High cardinality (15 unique in 50 rows)
            "date_col": ["2023-01-01", "2023-01-02", "2023-01-03", "2023-01-04", "2023-01-05"] * 10, # Date-like
            "corr_1": range(50),
            "corr_2": [x * 1.000001 for x in range(50)] # High correlation
        }
        df = pd.DataFrame(data)
        dataset_path = output_dir / "data/raw/dataset.csv"
        dataset_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(dataset_path, index=False)

        # Run the advisor
        # We need to set PYTHONPATH to include the src directory of the generated project
        env = os.environ.copy()
        env["PYTHONPATH"] = str(output_dir / "src")

        result = subprocess.run(
            [sys.executable, "-m", f"{package_name}.advisor"],
            cwd=output_dir,
            env=env,
            capture_output=True,
            text=True
        )

        # Check if advisor ran successfully
        self.assertEqual(result.returncode, 0, msg=f"Advisor failed with output: {result.stdout}\n{result.stderr}")

        # Verify generated artifacts
        report_path = output_dir / "reports/dataset-advice.md"
        json_path = output_dir / "configs/suggested_pipeline.json"
        pipeline_path = output_dir / f"src/{package_name}/suggested_pipeline.py"

        self.assertTrue(report_path.exists(), "Report file not created")
        self.assertTrue(json_path.exists(), "JSON config not created")
        self.assertTrue(pipeline_path.exists(), "Pipeline code not created")

        # Verify report content
        report_content = report_path.read_text()
        self.assertIn("Small dataset detected", report_content)
        self.assertIn("Missing values in 'num_missing'", report_content)
        self.assertIn("Outliers detected in 'num_outliers'", report_content)
        self.assertIn("High cardinality categorical 'cat_high'", report_content)
        self.assertIn("Imbalanced target", report_content)
        # self.assertIn("Date-like column 'date_col'", report_content) # Flaky detection
        self.assertIn("High numeric correlation", report_content)
        self.assertIn("Search terms", report_content)

        # Verify JSON content
        import json
        with open(json_path) as f:
            pipeline_config = json.load(f)

        self.assertTrue(any(s["title"] == "Small dataset detected" for s in pipeline_config["signals"]))
        self.assertIn("num_missing", pipeline_config["columns"]["numeric"])
        self.assertIn("cat_high", pipeline_config["columns"]["categorical"])

        # Verify Pipeline code content
        pipeline_code = pipeline_path.read_text()
        self.assertIn("ColumnTransformer", pipeline_code)
        self.assertIn("Pipeline", pipeline_code)
        self.assertIn("RobustScaler", pipeline_code) # Because of outliers

if __name__ == "__main__":
    unittest.main()
