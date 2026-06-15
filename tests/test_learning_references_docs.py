import unittest
import os

TEMPLATES_DIR = "templates/project/docs"

URLS = {
    "slivkins": "https://arxiv.org/abs/1904.07272",
    "sklearn_eval": "https://scikit-learn.org/stable/modules/model_evaluation.html",
    "sklearn_gen": "https://scikit-learn.org/stable/datasets/sample_generators.html",
}

REQUIRED_REFERENCES = {
    "mab-lab.md.tpl": [URLS["slivkins"], URLS["sklearn_eval"], "Limitation"],
    "mab-lab.pt-BR.md.tpl": [URLS["slivkins"], URLS["sklearn_eval"], "Limitação"],
    "bandit-walkthrough.md.tpl": [URLS["slivkins"], URLS["sklearn_eval"], "Limitation"],
    "bandit-walkthrough.pt-BR.md.tpl": [URLS["slivkins"], URLS["sklearn_eval"], "Limitação"],
    "synthetic-data-lab.md.tpl": [URLS["sklearn_gen"], URLS["sklearn_eval"], "Limitation"],
    "synthetic-data-lab.pt-BR.md.tpl": [URLS["sklearn_gen"], URLS["sklearn_eval"], "Limitação"],
}

class TestLearningReferencesDocs(unittest.TestCase):
    def test_template_contains_references(self):
        for template_name, expected_strings in REQUIRED_REFERENCES.items():
            filepath = os.path.join(TEMPLATES_DIR, template_name)
            self.assertTrue(os.path.exists(filepath), f"Template {template_name} is missing")

            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            for expected in expected_strings:
                self.assertIn(expected, content, f"Expected content '{expected}' missing in {template_name}")

if __name__ == "__main__":
    unittest.main()
