import unittest
import sys
from pathlib import Path
from importlib.machinery import SourceFileLoader
import types

# Ensure we can import from the generator
sys.path.append(str(Path(__file__).parent.parent))
from ml_starter_generator.templates import render

class TestMetricsTemplate(unittest.TestCase):
    def setUp(self):
        self.template_path = Path("templates/common/metrics.py.tpl")
        self.template_content = self.template_path.read_text(encoding="utf-8")

        # Render the template with dummy values (no placeholders in metrics.py.tpl currently)
        self.rendered_code = render(self.template_content, {})

        # Dynamically load the rendered code as a module
        self.module_name = "test_metrics_rendered"
        self.module = types.ModuleType(self.module_name)
        exec(self.rendered_code, self.module.__dict__)

    def test_accuracy(self):
        self.assertEqual(self.module.accuracy([1, 0, 1], [1, 0, 0]), 2/3)

    def test_precision(self):
        self.assertEqual(self.module.precision([1, 1, 0, 0], [1, 0, 1, 0], positive_label=1), 0.5)
        self.assertEqual(self.module.precision([1, 1], [0, 0], positive_label=1), 0.0)

    def test_recall(self):
        self.assertEqual(self.module.recall([1, 1, 0, 0], [1, 0, 1, 0], positive_label=1), 0.5)
        self.assertEqual(self.module.recall([0, 0], [1, 1], positive_label=1), 0.0)

    def test_f1_score(self):
        self.assertEqual(self.module.f1_score([1, 1, 0, 0], [1, 0, 1, 0], positive_label=1), 0.5)
        self.assertEqual(self.module.f1_score([1, 1], [0, 0], positive_label=1), 0.0)

    def test_mae(self):
        self.assertEqual(self.module.mean_absolute_error([1.0, 2.0], [1.5, 2.5]), 0.5)

    def test_rmse(self):
        self.assertEqual(self.module.root_mean_squared_error([1.0, 2.0], [2.0, 3.0]), 1.0)

    def test_mape(self):
        self.assertAlmostEqual(self.module.mean_absolute_percentage_error([100, 200], [110, 180]), 0.1)
        self.assertEqual(self.module.mean_absolute_percentage_error([0, 100], [10, 110]), 0.1)

    def test_r_squared(self):
        self.assertAlmostEqual(self.module.r_squared([1, 2, 3], [1, 2, 3]), 1.0)
        self.assertAlmostEqual(self.module.r_squared([1, 2, 3], [2, 2, 2]), 0.0)
        self.assertEqual(self.module.r_squared([1, 1, 1], [1, 1, 1]), 0.0)

    def test_bandit_metrics(self):
        rewards = [1, 0, 1]
        summary = self.module.bandit_summary(rewards)
        self.assertEqual(summary['total_reward'], 2.0)
        self.assertEqual(summary['average_reward'], 2/3)
        self.assertEqual(summary['count'], 3)

    def test_arm_counts(self):
        arms = ["A", "B", "A"]
        counts = self.module.arm_counts(arms)
        self.assertEqual(counts, {"A": 2, "B": 1})

    def test_calculate_lift(self):
        self.assertEqual(self.module.calculate_lift(120, 100), 0.2)
        self.assertEqual(self.module.calculate_lift(100, 0), 0.0)

if __name__ == "__main__":
    unittest.main()
