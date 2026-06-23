import unittest
import shutil
import tempfile
from pathlib import Path
from ml_starter_generator.scaffold import create_agent_files

class TestAgentFilesGeneration(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.values = {
            "PACKAGE_NAME": "test_pkg",
            "LANGUAGE": "en"
        }

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_agent_files_are_created(self):
        create_agent_files(self.test_dir, self.values, force=True)

        expected_files = [
            "AGENTS.md",
            ".agents/skills/ml-lab-tutor/SKILL.md",
            ".agents/skills/ml-lab-tutor/references/project-map.md",
            ".agents/skills/ml-lab-tutor/references/learning-flow.md",
            ".agents/skills/ml-lab-tutor/references/challenge-bank.md",
        ]

        for rel_path in expected_files:
            full_path = self.test_dir / rel_path
            self.assertTrue(full_path.exists(), f"File {rel_path} was not created")

            content = full_path.read_text()
            self.assertGreater(len(content), 0, f"File {rel_path} is empty")

    def test_skill_file_contains_package_name(self):
        create_agent_files(self.test_dir, self.values, force=True)
        skill_file = self.test_dir / ".agents/skills/ml-lab-tutor/SKILL.md"
        content = skill_file.read_text()
        # The template engine uses {{ PACKAGE_NAME }} not {{PACKAGE_NAME}}
        # and it seems it might be sensitive to spaces if not handled perfectly,
        # but here it is {{ PACKAGE_NAME }} with spaces in the .tpl
        self.assertIn("src/test_pkg/", content)

    def test_project_map_contains_package_name(self):
        create_agent_files(self.test_dir, self.values, force=True)
        map_file = self.test_dir / ".agents/skills/ml-lab-tutor/references/project-map.md"
        content = map_file.read_text()
        self.assertIn("src/test_pkg/", content)

if __name__ == "__main__":
    unittest.main()
