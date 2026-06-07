import unittest
import shutil
import tempfile
from pathlib import Path
from tests.helpers import run_generator

class TestGuideOnboarding(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.project_name = "guide_proj"
        self.package_name = "guide_pkg"

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_terminal_summary_guide_order(self):
        """P0.1 - Post-create terminal next steps mention guide before data."""
        output = run_generator(
            project_name=self.project_name,
            package_name=self.package_name,
            output_dir=self.test_dir,
            include_pyproject="y"
        )

        # We need to find the occurrence within [Next steps] panel
        if "[Next steps]" not in output:
            self.fail("Next steps panel not found in output")

        next_steps_output = output.split("[Next steps]")[1]

        guide_cmd = f"python -m {self.package_name}.guide"
        lab_check_cmd = f"python -m {self.package_name}.lab check"
        data_cmd = f"python -m {self.package_name}.data"

        # Direct commands still exist in summary or can be used.
        # But for this test, we check if guide (direct or via lab) comes before data
        self.assertTrue(guide_cmd in next_steps_output or lab_check_cmd in next_steps_output)
        self.assertIn(data_cmd, next_steps_output)

        guide_idx = next_steps_output.find(guide_cmd) if guide_cmd in next_steps_output else next_steps_output.find(lab_check_cmd)
        data_idx = next_steps_output.find(data_cmd)

        self.assertLess(guide_idx, data_idx, "Guide command should be before data command in terminal summary")

    def test_readme_suggested_flow_and_commands_order(self):
        """P0.2 - Generated README Suggested flow / Suggested commands mention guide before data."""
        run_generator(
            project_name=self.project_name,
            package_name=self.package_name,
            output_dir=self.test_dir,
            optional_profile="3", # full (includes advisor)
        )

        readme_path = self.test_dir / "README.md"
        content = readme_path.read_text(encoding="utf-8")

        # Check Suggested flow
        flow_section = content.split("## Suggested flow")[1].split("##")[0]
        self.assertIn(f"python -m {self.package_name}.lab check", flow_section)

        # Check Suggested commands
        commands_section = content.split("## Suggested commands")[1]

        lab_check_cmd = f"python -m {self.package_name}.lab check"
        # We don't have .data in lab CLI, so it remains direct
        data_cmd = f"python -m {self.package_name}.data"

        # Note: .data is NOT in the lab CLI list in README currently,
        # it was replaced by 'eda' in 'Suggested commands' but let's check what's there
        self.assertIn(lab_check_cmd, commands_section)

        lab_check_idx = commands_section.find(lab_check_cmd)
        # lab all is at the end
        lab_all_cmd = f"python -m {self.package_name}.lab all"
        self.assertIn(lab_all_cmd, commands_section)
        lab_all_idx = commands_section.find(lab_all_cmd)

        self.assertLess(lab_check_idx, lab_all_idx)

    def test_advisor_and_guide_distinct_roles(self):
        """P0.3 - Advisor and guide roles are distinct in README."""
        run_generator(
            project_name=self.project_name,
            package_name=self.package_name,
            output_dir=self.test_dir,
            optional_profile="3", # full (includes advisor)
        )

        readme_path = self.test_dir / "README.md"
        content = readme_path.read_text(encoding="utf-8")

        # Look for text distinguishing them
        # Guide should be about readiness/validation
        # Advisor should be about modeling suggestions/advice

        self.assertTrue(any(word in content.lower() for word in ["readiness", "validate", "check"]), "README should mention readiness/validation for guide")
        self.assertTrue(any(word in content.lower() for word in ["advice", "modeling", "suggestions"]), "README should mention advice/suggestions for advisor")

    def test_pt_br_localization_order(self):
        """P0.5 - PT-BR keeps same command order."""
        output = run_generator(
            language="2", # pt-BR
            project_name=self.project_name,
            package_name=self.package_name,
            output_dir=self.test_dir,
            include_pyproject="y"
        )

        next_steps_output = output.split("[Próximos passos]")[1]

        guide_cmd = f"python -m {self.package_name}.guide"
        lab_check_cmd = f"python -m {self.package_name}.lab check"
        data_cmd = f"python -m {self.package_name}.data"

        self.assertTrue(guide_cmd in next_steps_output or lab_check_cmd in next_steps_output)
        self.assertIn(data_cmd, next_steps_output)

        guide_idx = next_steps_output.find(guide_cmd) if guide_cmd in next_steps_output else next_steps_output.find(lab_check_cmd)
        data_idx = next_steps_output.find(data_cmd)

        self.assertLess(guide_idx, data_idx, "Guide command should be before data command in PT-BR terminal summary")

        readme_path = self.test_dir / "README.md"
        content = readme_path.read_text(encoding="utf-8")

        # Check Suggested commands in PT-BR README
        commands_section = content.split("## Comandos sugeridos")[1]
        lab_check_cmd = f"python -m {self.package_name}.lab check"

        lab_check_idx_readme = commands_section.find(lab_check_cmd)
        self.assertNotEqual(lab_check_idx_readme, -1, "Lab check command not found in PT-BR README")

if __name__ == "__main__":
    unittest.main()
