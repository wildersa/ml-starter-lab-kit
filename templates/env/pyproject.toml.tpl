[project]
name = "{{PACKAGE_NAME}}"
version = "0.1.0"
description = "{{PROJECT_NAME}}"
requires-python = "{{PYTHON_REQUIRES}}"

# Intencionalmente sem dependências.
# Adicione pandas, scikit-learn, xgboost, tensorflow, keras etc. somente quando o projeto precisar.

[tool.pytest.ini_options]
pythonpath = ["."]
testpaths = ["tests"]
