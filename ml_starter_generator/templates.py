from __future__ import annotations

from pathlib import Path
from .constants import STARTER_ROOT

def render(content: str, values: dict[str, str]) -> str:
    # 1. Simple placeholders: {{KEY}}
    for key, value in values.items():
        content = content.replace("{{" + key + "}}", value)

    # 2. Simple conditional blocks: {% if KEY == "value" %}...{% endif %}
    # This is a very limited subset for specific P0 needs.
    import re

    pattern = re.compile(
        r'{%\s*if\s+(\w+)\s*==\s*"([^"]+)"\s*%}(.*?){%\s*endif\s*%}',
        re.DOTALL
    )

    def evaluate_condition(match):
        key = match.group(1)
        target_value = match.group(2)
        inner_content = match.group(3)

        if values.get(key) == target_value:
            return inner_content
        return ""

    content = pattern.sub(evaluate_condition, content)

    # 3. Handle leftover empty lines from conditional blocks
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)

    return content


def load_template(name: str, values: dict[str, str], folder: str = "common") -> str:
    if name.endswith(".tpl"):
        template_path = STARTER_ROOT / "templates" / folder / name
    else:
        template_path = STARTER_ROOT / "templates" / folder / f"{name}.tpl"

    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")

    content = template_path.read_text(encoding="utf-8")
    return render(content, values)
