import unittest
import shutil
import tempfile
import os
import subprocess
import json
import sys
from pathlib import Path
from tests.helpers import run_generator

class TestEvaluationReport(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.project_name = "eval_proj"
        self.package_name = "eval_pkg"

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_evaluation_report_generation_en(self):
        # 1. Generate project (English)
        run_generator(
            project_name=self.project_name,
            package_name=self.package_name,
            task="2", # supervised
            dataset_path="data/raw/train.csv",
            target_column="target",
            output_dir=self.test_dir,
            include_ml_basics="n",
            language="1" # English
        )

        # 2. Create dummy data and model
        data_dir = self.test_dir / "data/processed"
        data_dir.mkdir(parents=True, exist_ok=True)
        train_csv = data_dir / "modeling_table.csv"
        with open(train_csv, "w") as f:
            f.write("feature1,target\n1,A\n2,B\n3,A\n")

        models_dir = self.test_dir / "models"
        models_dir.mkdir(parents=True, exist_ok=True)
        model_json = models_dir / "model.json"
        with open(model_json, "w") as f:
            json.dump({
                "model_type": "majority_class_baseline",
                "target_column": "target",
                "prediction": "A"
            }, f)

        # 3. Run evaluate.py
        env = os.environ.copy()
        env["PYTHONPATH"] = str(self.test_dir / "src")

        subprocess.check_call(
            [sys.executable, "-m", f"{self.package_name}.evaluate"],
            cwd=self.test_dir,
            env=env
        )

        # 4. Assertions
        metrics_path = self.test_dir / "reports/metrics.json"
        report_path = self.test_dir / "reports/evaluation-report.md"

        self.assertTrue(metrics_path.exists(), "metrics.json should exist")
        self.assertTrue(report_path.exists(), "evaluation-report.md should exist")

        with open(metrics_path) as f:
            metrics = json.load(f)
            self.assertIn("accuracy", metrics)
            self.assertEqual(metrics["model_type"], "majority_class_baseline")

        report_content = report_path.read_text(encoding="utf-8")
        self.assertIn("# Evaluation Report", report_content)
        self.assertIn("## Summary", report_content)
        self.assertIn("## Metrics", report_content)
        self.assertIn("## Interpretation", report_content)
        self.assertIn("## Next experiment", report_content)
        self.assertIn("## How to read this report", report_content)
        self.assertIn("**Project:** eval_proj", report_content)
        self.assertIn("**Task:** supervised", report_content)
        self.assertIn("Accuracy:", report_content)
        # Real metric value assertion (3 samples, 2 A, 1 B -> 2/3 = 0.6667)
        self.assertIn("0.6667", report_content)
        self.assertIn("66.67%", report_content)

    def test_evaluation_report_generation_pt_br(self):
        # 1. Generate project (Portuguese)
        run_generator(
            project_name=self.project_name,
            package_name=self.package_name,
            task="2", # supervised
            dataset_path="data/raw/train.csv",
            target_column="target",
            output_dir=self.test_dir,
            include_ml_basics="n",
            language="2" # pt-BR
        )

        # 2. Create dummy data and model
        data_dir = self.test_dir / "data/processed"
        data_dir.mkdir(parents=True, exist_ok=True)
        train_csv = data_dir / "modeling_table.csv"
        with open(train_csv, "w") as f:
            f.write("feature1,target\n1,A\n2,B\n3,A\n")

        models_dir = self.test_dir / "models"
        models_dir.mkdir(parents=True, exist_ok=True)
        model_json = models_dir / "model.json"
        with open(model_json, "w") as f:
            json.dump({
                "model_type": "majority_class_baseline",
                "target_column": "target",
                "prediction": "A"
            }, f)

        # 3. Run evaluate.py
        env = os.environ.copy()
        env["PYTHONPATH"] = str(self.test_dir / "src")

        subprocess.check_call(
            [sys.executable, "-m", f"{self.package_name}.evaluate"],
            cwd=self.test_dir,
            env=env
        )

        # 4. Assertions
        report_path = self.test_dir / "reports/evaluation-report.md"
        self.assertTrue(report_path.exists())

        report_content = report_path.read_text(encoding="utf-8")
        self.assertIn("# Relatório de Avaliação", report_content)
        self.assertIn("## Resumo", report_content)
        self.assertIn("## Métricas", report_content)
        self.assertIn("## Interpretação", report_content)
        self.assertIn("## Próximo experimento", report_content)
        self.assertIn("## Como ler este relatório", report_content)
        self.assertIn("**Projeto:** eval_proj", report_content)

    def test_evaluation_report_missing_reports_dir(self):
        # 1. Generate project
        run_generator(
            project_name=self.project_name,
            package_name=self.package_name,
            task="2",
            output_dir=self.test_dir,
            include_ml_basics="n"
        )

        # 2. Setup data/model
        data_dir = self.test_dir / "data/processed"
        data_dir.mkdir(parents=True, exist_ok=True)
        with open(data_dir / "modeling_table.csv", "w") as f:
            f.write("feature1,target\n1,A\n")

        models_dir = self.test_dir / "models"
        models_dir.mkdir(parents=True, exist_ok=True)
        with open(models_dir / "model.json", "w") as f:
            json.dump({"model_type": "majority_class_baseline", "target_column": "target", "prediction": "A"}, f)

        # 3. DELETE reports dir if it exists (it might have been created by scaffold)
        reports_dir = self.test_dir / "reports"
        if reports_dir.exists():
            shutil.rmtree(reports_dir)

        # 4. Run evaluate.py
        env = os.environ.copy()
        env["PYTHONPATH"] = str(self.test_dir / "src")
        subprocess.check_call([sys.executable, "-m", f"{self.package_name}.evaluate"], cwd=self.test_dir, env=env)

        # 5. Assert reports dir was created
        self.assertTrue(reports_dir.exists())
        self.assertTrue((reports_dir / "evaluation-report.md").exists())

if __name__ == "__main__":
    unittest.main()
