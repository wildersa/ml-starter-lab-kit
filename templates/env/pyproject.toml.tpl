[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "{{PACKAGE_NAME}}"
version = "0.1.0"
description = "{{PROJECT_NAME}}"
requires-python = "{{PYTHON_REQUIRES}}"

# Intentionally without dependencies.
# Add pandas, scikit-learn, xgboost, tensorflow, keras etc. only when the project needs them.

[tool.setuptools.packages.find]
where = ["src"]

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
