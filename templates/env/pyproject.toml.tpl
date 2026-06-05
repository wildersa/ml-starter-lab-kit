[project]
name = "{{PACKAGE_NAME}}"
version = "0.1.0"
description = "{{PROJECT_NAME}}"
requires-python = "{{PYTHON_REQUIRES}}"

# Intentionally without dependencies.
# Add pandas, scikit-learn, xgboost, tensorflow, keras etc. only when the project needs them.

[tool.pytest.ini_options]
pythonpath = ["."]
testpaths = ["tests"]
