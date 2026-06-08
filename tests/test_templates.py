import unittest
from pathlib import Path
from ml_starter_generator.templates import load_template

class TestTemplates(unittest.TestCase):
    def test_load_template_success(self):
        # We know README.md.tpl exists in templates/project/
        # It uses {{PROJECT_NAME}}
        content = load_template("README.md", {"PROJECT_NAME": "Test Project"}, folder="project")
        self.assertIn("# Test Project", content)

    def test_load_template_missing_raises_error(self):
        with self.assertRaises(FileNotFoundError) as cm:
            load_template("non_existent_file.txt", {}, folder="project")

        self.assertIn("non_existent_file.txt", str(cm.exception))
        self.assertIn("Template not found", str(cm.exception))

    def test_learning_workspace_template(self):
        values = {
            "PROJECT_NAME": "Test Project",
            "PACKAGE_NAME": "test_pkg",
            "LEARNING_ENABLED": "true"
        }
        content = load_template("learning_workspace.py", values)

        # Check required sections
        self.assertIn("Setup Check", content)
        self.assertIn("Guided EDA", content)
        self.assertIn("Target Analysis", content)
        self.assertIn("Feature Explorer", content)
        self.assertIn("Model Suggestions", content)
        self.assertIn("Baseline Lab", content)
        self.assertIn("Train & Evaluate", content)
        self.assertIn("Experiments & MLflow", content)

        # Check core delegation
        self.assertIn("from config import load_config, project_root", content)
        self.assertIn("from core.readiness import check_dataset_readiness", content)
        # It also has absolute import logic
        self.assertIn("importlib.import_module(f\"{module_name}.config\")", content)

if __name__ == "__main__":
    unittest.main()
