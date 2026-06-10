"""Educational Multi-Armed Bandit Lab."""
from __future__ import annotations

import csv
import json
import random
import sys
from pathlib import Path
from typing import Any

from .core.config import project_root


class BernoulliEnvironment:
    def __init__(self, arms: list[dict[str, Any]], seed: int = 42):
        self.arms = arms
        self.rng = random.Random