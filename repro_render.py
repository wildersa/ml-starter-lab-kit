import re

def render(content: str, values: dict[str, str]) -> str:
    # 1. Simple placeholders: {{KEY}}
    for key, value in values.items():
        content = content.replace("{{" + key + "}}", value)

    # 2. Recursive conditional blocks: {% if KEY == "value" %}...{% else %}...{% endif %}
    def process(text):
        # Find the first {% if ... %}
        match = re.search(r'{%\s*if\s+(\w+)\s*==\s*"([^"]+)"\s*%}', text)
        if not match:
            return text

        if_start = match.start()
        if_tag_len = len(match.group(0))
        key = match.group(1)
        val = match.group(2)

        # Find matching endif, and optional else at the same level
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
            # Unbalanced tags: ignore this if and continue
            return text[:if_start] + text[if_start + if_tag_len:]

        if else_pos != -1:
            if_content = text[if_start + if_tag_len : else_pos]
            else_content = text[else_pos + else_tag_len : endif_pos]
            if values.get(key) == val:
                selected = if_content
            else:
                selected = else_content
        else:
            if_content = text[if_start + if_tag_len : endif_pos]
            if values.get(key) == val:
                selected = if_content
            else:
                selected = ""

        # Recurse on the resulting text to handle other tags at the same level or nested ones
        return process(text[:if_start] + selected + text[endif_pos + endif_tag_len:])

    content = process(content)

    # 3. Handle leftover empty lines from conditional blocks
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)

    return content

template = """
{% if LEARNING_ENABLED == "true" %}
streamlit
{% else %}
{% if GENERATE_BANDIT == "true" %}
streamlit
{% endif %}
{% endif %}
"""

print("Test 1: LEARNING_ENABLED=true, GENERATE_BANDIT=true")
print(render(template, {"LEARNING_ENABLED": "true", "GENERATE_BANDIT": "true"}))

print("\nTest 2: LEARNING_ENABLED=false, GENERATE_BANDIT=true")
print(render(template, {"LEARNING_ENABLED": "false", "GENERATE_BANDIT": "true"}))

print("\nTest 3: LEARNING_ENABLED=false, GENERATE_BANDIT=false")
print(render(template, {"LEARNING_ENABLED": "false", "GENERATE_BANDIT": "false"}))

print("\nTest 4: Original failing template with 'or'")
template_fail = """
{% if LEARNING_ENABLED == "true" or GENERATE_BANDIT == "true" %}
streamlit
{% endif %}
"""
print(render(template_fail, {"LEARNING_ENABLED": "false", "GENERATE_BANDIT": "true"}))
