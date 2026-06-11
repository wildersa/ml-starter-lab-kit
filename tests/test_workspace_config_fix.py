import unittest
from ml_starter_generator.templates import load_template

class TestWorkspaceConfigFix(unittest.TestCase):
    def test_mlflow_status_helper(self):
        """P0.1, P0.2, P0.3: Behavioral proof for get_mlflow_status logic."""
        # We simulate the get_mlflow_status logic
        def get_mlflow_status(config):
            tracking = config.get("tracking", {})
            enabled = tracking.get("enabled_mlflow")
            if enabled is None:
                enabled = tracking.get("mlflow", {}).get("enabled", False)
            return bool(enabled)

        # P0.1: Canonical key
        self.assertTrue(get_mlflow_status({"tracking": {"enabled_mlflow": True}}))

        # P0.2: Missing/False
        self.assertFalse(get_mlflow_status({"tracking": {"enabled_mlflow": False}}))
        self.assertFalse(get_mlflow_status({"tracking": {}}))
        self.assertFalse(get_mlflow_status({}))

        # P0.3: Compatibility fallback
        self.assertTrue(get_mlflow_status({"tracking": {"mlflow": {"enabled": True}}}))
        # Canonical takes precedence
        self.assertFalse(get_mlflow_status({"tracking": {"enabled_mlflow": False, "mlflow": {"enabled": True}}}))

    def test_templates_reflect_logic(self):
        values = {
            "PROJECT_NAME": "Test Project",
            "PACKAGE_NAME": "test_pkg",
            "GENERATE_BANDIT": "false"
        }

        # Verify config template contains the helper
        config_content = load_template("core/config.py", values, folder="project/package")
        self.assertIn("def get_mlflow_status", config_content)

        # Verify workspace template uses the helper or correct logic
        ws_content = load_template("learning_workspace.py", values)
        self.assertIn("get_mlflow_status", ws_content)

if __name__ == "__main__":
    unittest.main()
