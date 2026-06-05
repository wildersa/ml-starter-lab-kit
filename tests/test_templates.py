import unittest
from pathlib import Path
import tempfile
import shutil
from unittest.mock import patch
from ml_starter_generator.templates import load_template

class TestTemplates(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp()).resolve()
        self.templates_dir = self.test_dir / "templates"
        self.templates_dir.mkdir()
        (self.templates_dir / "common").mkdir()

        # Create a dummy template
        self.valid_template = self.templates_dir / "common" / "test.tpl"
        self.valid_template.write_text("Hello {{NAME}}!")

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_load_template_success(self):
        with patch('ml_starter_generator.templates.STARTER_ROOT', self.test_dir):
            content = load_template("test", {"NAME": "World"})
            self.assertEqual(content, "Hello World!")

    def test_load_template_missing_raises_error(self):
        with patch('ml_starter_generator.templates.STARTER_ROOT', self.test_dir):
            template_name = "missing"
            expected_path = self.test_dir / "templates" / "common" / f"{template_name}.tpl"
            with self.assertRaises(FileNotFoundError) as cm:
                load_template(template_name, {})
            self.assertIn(str(expected_path), str(cm.exception))
            self.assertIn("Template not found", str(cm.exception))

if __name__ == "__main__":
    unittest.main()
