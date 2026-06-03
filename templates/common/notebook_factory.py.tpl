from __future__ import annotations

import json
from pathlib import Path


DEFAULT_NOTEBOOK = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# {{PROJECT_NAME}} - Starter Notebook\n",
                "\n",
                "Use this notebook for quick exploration. Move reusable logic to Python modules.\n",
            ],
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Suggested flow\n",
                "\n",
                "1. Load data\n",
                "2. Inspect columns and missing values\n",
                "3. Create a baseline\n",
                "4. Try features\n",
                "5. Evaluate results\n",
            ],
        },
    ],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {
            "name": "python",
        },
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}


def create_notebook(path: str | Path) -> None:
    """Create a minimal notebook file."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(DEFAULT_NOTEBOOK, indent=2), encoding="utf-8")
