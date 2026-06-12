from __future__ import annotations

import re
from pathlib import Path
from typing import Any
from .constants import STARTER_ROOT

def render(content: str, values: dict[str, Any]) -> str:
    safe_values = {k: str(v) for k, v in values.items()}

    def process(text):
        # Support == and != with optional spaces and optional quotes
        # Quotes are technically required by our current templates, but let's be flexible.
        match = re.search(r'{%\s*if\s+(\w+)\s*(!=|==)\s*"([^"]*)"\s*%}', text)
        if not match:
            return text

        if_start = match.start()
        if_tag_full = match.group(0)
        key = match.group(1)
        op = match.group(2)
        val = match.group(3)

        depth = 0
        endif_pos = -1
        endif_tag_len = 0
        else_pos = -1
        else_tag_len = 0

        for m in re.finditer(r'{%\s*(if|else|endif).*?%}', text[if_start:]):
            tag = m.group(1)
            if tag == 'if':
                depth += 1
            elif tag == 'endif':
                depth -= 1
                if depth == 0:
                    endif_pos = if_start + m.start()
                    endif_tag_len = len(m.group(0))
                    break
            elif tag == 'else' and depth == 1:
                else_pos = if_start + m.start()
                else_tag_len = len(m.group(0))

        if endif_pos == -1:
            # Malformed template: remove the tag to avoid infinite loop
            return text[:if_start] + text[if_start + len(if_tag_full):]

        actual_val = safe_values.get(key, "")
        if op == "==":
            condition_met = (actual_val == val)
        else: # !=
            condition_met = (actual_val != val)

        if else_pos != -1:
            if_content = text[if_start + len(if_tag_full) : else_pos]
            else_content = text[else_pos + else_tag_len : endif_pos]
            selected = if_content if condition_met else else_content
        else:
            if_content = text[if_start + len(if_tag_full) : endif_pos]
            selected = if_content if condition_met else ""

        return text[:if_start] + selected + text[endif_pos + endif_tag_len:]

    # Run IF/ELSE processing until convergence
    while True:
        new_content = process(content)
        if new_content == content:
            break
        content = new_content

    # 2. Simple placeholders: {{KEY}}
    for key, value in safe_values.items():
        content = content.replace("{{" + key + "}}", value)

    # 3. Clean up empty lines that were left by tag lines
    # This matches lines containing ONLY a tag (and whitespace), and removes the whole line including the newline
    content = re.sub(r'^[ \t]*{%\s*(if|else|endif).*?%}[ \t]*\n', '', content, flags=re.MULTILINE)
    # Also clean up trailing tags that might not have a newline after them
    content = re.sub(r'[ \t]*{%\s*(if|else|endif).*?%}[ \t]*', '', content)

    # 4. Final normalization of empty lines
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
