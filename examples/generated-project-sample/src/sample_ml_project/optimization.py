from __future__ import annotations

from itertools import product
from random import Random
from typing import Any, Callable


Params = dict[str, Any]
ScoreFn = Callable[[Params], float]


def grid_search(param_grid: dict[str, list[Any]], score_fn: ScoreFn) -> dict[str, Any]:
    """Tiny grid search helper.

    `score_fn` receives a parameter dictionary and returns a score.
    Higher score is considered better.
    """
    keys = list(param_grid.keys())
    values = [param_grid[key] for key in keys]

    best_params: Params | None = None
    best_score: float | None = None
    history: list[dict[str, Any]] = []

    for combination in product(*values):
        params = dict(zip(keys, combination))
        score = score_fn(params)
        history.append({"params": params, "score": score})

        if best_score is None or score > best_score:
            best_score = score
            best_params = params

    return {
        "best_params": best_params or {},
        "best_score": best_score,
        "history": history,
    }


def random_search(
    param_space: dict[str, list[Any]],
    score_fn: ScoreFn,
    *,
    n_trials: int = 10,
    random_state: int = 42,
) -> dict[str, Any]:
    """Tiny random search helper.

    Useful when the search space is larger than a small grid.
    """
    rng = Random(random_state)
    keys = list(param_space.keys())

    best_params: Params | None = None
    best_score: float | None = None
    history: list[dict[str, Any]] = []

    for _ in range(n_trials):
        params = {key: rng.choice(param_space[key]) for key in keys}
        score = score_fn(params)
        history.append({"params": params, "score": score})

        if best_score is None or score > best_score:
            best_score = score
            best_params = params

    return {
        "best_params": best_params or {},
        "best_score": best_score,
        "history": history,
    }
