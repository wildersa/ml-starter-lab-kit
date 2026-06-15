import unittest
import os

TEMPLATES_DIR = "templates/project/docs"

REQUIRED_REFERENCES = {
    "mab-lab.md.tpl": ["Slivkins", "scikit-learn", "Limitation"],
    "mab-lab.pt-BR.md.tpl": ["Slivkins", "scikit-learn", "Limitação"],
    "bandit-walkthrough.md.tpl": ["Slivkins", "scikit-learn", "Limitation"],
    "bandit-walkthrough.pt-BR.md.tpl": ["Slivkins", "scikit-learn", "Limitação"],
    "synthetic-data-lab.md.tpl": ["scikit-learn", "Limitation"],
    "synthetic-data-lab.pt-BR.md.tpl": ["scikit-learn", "Limitação"],
}

class TestLearningReferencesDocs(unittest.TestCase):
    def test_template_contains_references(self):
        for template_name, keywords in REQUIRED_REFERENCES.items():
            filepath = os.path.join(TEMPLATES_DIR, template_name)
            if not os.path.exists(filepath):
                continue

            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            for keyword in keywords:
                self.assertIn(keyword, content, f"Keyword '{keyword}' missing in {template_name}")

if __name__ == "__main__":
    unittest.main()
