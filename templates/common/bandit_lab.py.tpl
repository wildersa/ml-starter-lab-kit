"""Educational Multi-Armed Bandit Lab.

This module implements a Bernoulli Multi-Armed Bandit simulation to help
understand the exploration-exploitation trade-off and sequential decision making.

Command:
    python -m {{PACKAGE_NAME}}.lab bandit

Outputs:
    configs/bandit_results.json
    reports/bandit-results.md
    reports/bandit-history.csv
"""

from __future__ import annotations

import json
import random
import