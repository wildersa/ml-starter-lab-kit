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

if __name__ == "__main__":
    unittest.main()
