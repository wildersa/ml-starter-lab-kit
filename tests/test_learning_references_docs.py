import os
import pytest

TEMPLATES_DIR = "templates/project/docs"

REQUIRED_REFERENCES = {
    "mab-lab.md.tpl": ["Slivkins", "scikit-learn", "Limitation"],
    "mab-lab.pt-BR.md.tpl": ["Slivkins", "scikit-learn", "Limitação"],
    "bandit-walkthrough.md.tpl": ["Slivkins", "scikit-learn", "Limitation"],
    "bandit-walkthrough.pt-BR.md.tpl": ["Slivkins", "scikit-learn", "Limitação"],
    "synthetic-data-lab.md.tpl": ["scikit-learn", "Limitation"],
    "synthetic-data-lab.pt-BR.md.tpl": ["scikit-learn", "Limitação"],
}

@pytest.mark.parametrize("template_name,keywords", REQUIRED_REFERENCES.items())
def test_template_contains_references(template_name, keywords):
    filepath = os.path.join(TEMPLATES_DIR, template_name)
    if not os.path.exists(filepath):
        pytest.skip(f"Template {template_name} not found")

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    for keyword in keywords:
        assert keyword in content, f"Keyword '{keyword}' missing in {template_name}"
