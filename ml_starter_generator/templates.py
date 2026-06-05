from __future__ import annotations

from pathlib import Path
from .constants import STARTER_ROOT

def render(content: str, values: dict[str, str]) -> str:
    for key, value in values.items():
        content = content.replace("{{" + key + "}}", value)
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
