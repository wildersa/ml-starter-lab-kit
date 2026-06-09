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
import csv
import sys
from typing import Any, Dict, List, Tuple
from pathlib import Path

from .core.config import project_root


class BernoulliEnvironment:
    """Stochastic Bernoulli environment for Multi-Armed Bandit."""

    def __init__(self, arms: List[Dict[str, Any]], seed: int = 42):
        self.arms = arms
        self.rng = random.Random(seed)
        self.probabilities = [arm["true_reward_probability"] for arm in arms]
        self.best_prob = max(self.probabilities)
        self.best_arm_index = self.probabilities.index(self.best_prob)

    def pull(self, arm_index: int) -> int:
        """Returns a reward (0 or 1) for the selected arm."""
        if self.rng.random() < self.probabilities[arm_index]:
            return 1
        return 0

    def get_regret(self, arm_index: int) -> float:
        """Calculates the expected regret for selecting a specific arm."""
        return self.best_prob - self.probabilities[arm_index]


class RandomPolicy:
    """Policy that selects arms uniformly at random."""

    def __init__(self, n_arms: int, seed: int = 42):
        self.n_arms = n_arms
        self.rng = random.Random(seed)

    def select_arm(self) -> int:
        return self.rng.randint(0, self.n_arms - 1)

    def update(self, arm_index: int, reward: int) -> None:
        """Random policy does not learn from rewards."""
        pass


class EpsilonGreedyPolicy:
    """Policy that explores with probability epsilon and exploits otherwise."""

    def __init__(self, n_arms: int, epsilon: float = 0.1, seed: int = 42):
        self.n_arms = n_arms
        self.epsilon = epsilon
        self.rng = random.Random(seed)
        self.counts = [0] * n_arms
        self.values = [0.0] * n_arms

    def select_arm(self) -> int:
        if self.rng.random() < self.epsilon:
            return self.rng.randint(0, self.n_arms - 1)

        max_val = max(self.values)
        indices = [i for i, v in enumerate(self.values) if v == max_val]
        return self.rng.choice(indices)

    def update(self, arm_index: int, reward: int) -> None:
        self.counts[arm_index] += 1
        n = self.counts[arm_index]
        value = self.values[arm_index]
        # Incremental average update
        new_value = ((n - 1) / n) * value + (1 / n) * reward
        self.values[arm_index] = new_value


class BanditLab:
    """Simulation runner and reporter for the Multi-Armed Bandit Lab."""

    def __init__(self, bandit_config: Dict[str, Any], lang: str = "en"):
        self.config = bandit_config
        self.lang = lang
        self.n_rounds = bandit_config.get("n_rounds", 1000)
        self.seed = bandit_config.get("seed", 42)
        self.arms = bandit_config.get("arms", [])
        self.n_arms = len(self.arms)
        self.t = self._get_translations(lang)

    def _get_translations(self, lang: str) -> Dict[str, str]:
        translations = {
            "en": {
                "report_title": "Multi-Armed Bandit Lab Results",
                "intro": "Simulation results for Bernoulli Multi-Armed Bandit environment.",
                "summary_section": "Summary",
                "total_reward": "Total Reward",
                "avg_reward": "Average Reward",
                "cumulative_regret": "Cumulative Regret",
                "best_arm_rate": "Best Arm Selection Rate",
                "arm_counts": "Arm Selection Counts",
                "status_running": "Running {policy} policy simulation...",
                "status_complete": "Bandit Lab simulation complete.",
            },
            "pt-BR": {
                "report_title": "Resultados do Bandit Lab",
                "intro": "Resultados da simulação de ambiente Bernoulli Multi-Armed Bandit.",
                "summary_section": "Resumo",
                "total_reward": "Recompensa Total",
                "avg_reward": "Recompensa Média",
                "cumulative_regret": "Regret Acumulado",
                "best_arm_rate": "Taxa de Escolha do Melhor Arm",
                "arm_counts": "Contagem de Escolha dos Arms",
                "status_running": "Executando simulação da política {policy}...",
                "status_complete": "Simulação do Bandit Lab concluída.",
            }
        }
        return translations.get(lang, translations["en"])

    def validate_config(self) -> None:
        """Validates that the configuration contains all required fields."""
        required = ["n_rounds", "seed", "arms", "policies"]
        for field in required:
            if field not in self.config:
                print(f"Error: Missing required field '{field}' in bandit_config.json")
                sys.exit(1)

        if not self.arms:
            print("Error: 'arms' list cannot be empty in bandit_config.json")
            sys.exit(1)

        for arm in self.arms:
            if "name" not in arm or "true_reward_probability" not in arm:
                print("Error: Each arm must have 'name' and 'true_reward_probability'.")
                sys.exit(1)

    def run(self) -> Tuple[Dict[str, Any], List[Dict[str, Any]], str]:
        """Runs the simulation for all configured policies."""
        results = {}
        all_history = []

        for policy_name in self.config["policies"]:
            print(self.t["status_running"].format(policy=policy_name))

            env = BernoulliEnvironment(self.arms, self.seed)
            if policy_name == "random":
                policy = RandomPolicy(self.n_arms, self.seed)
            elif policy_name == "epsilon_greedy":
                epsilon = self.config.get("epsilon", 0.1)
                policy = EpsilonGreedyPolicy(self.n_arms, epsilon, self.seed)
            else:
                print(f"Warning: Policy '{policy_name}' is not implemented in this version. Skipping.")
                continue

            history, metrics = self._simulate(env, policy, policy_name)
            results[policy_name] = metrics
            all_history.extend(history)

        report_md = self._generate_report(results)
        return results, all_history, report_md

    def _simulate(self, env: BernoulliEnvironment, policy: Any, policy_name: str) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        history = []
        total_reward = 0
        cumulative_regret = 0.0
        best_arm_count = 0
        arm_counts = [0] * self.n_arms

        for r in range(1, self.n_rounds + 1):
            arm_idx = policy.select_arm()
            reward = env.pull(arm_idx)
            policy.update(arm_idx, reward)

            total_reward += reward
            regret = env.get_regret(arm_idx)
            cumulative_regret += regret
            arm_counts[arm_idx] += 1
            if arm_idx == env.best_arm_index:
                best_arm_count += 1

            history.append({
                "round": r,
                "policy": policy_name,
                "selected_arm": self.arms[arm_idx]["name"],
                "reward": reward,
                "cumulative_reward": total_reward,
                "cumulative_regret": round(cumulative_regret, 4)
            })

        metrics = {
            "total_reward": total_reward,
            "average_reward": round(total_reward / self.n_rounds, 4),
            "cumulative_regret": round(cumulative_regret, 4),
            "best_arm_selection_rate": round(best_arm_count / self.n_rounds, 4),
            "arm_counts": {self.arms[i]["name"]: arm_counts[i] for i in range(self.n_arms)}
        }
        return history, metrics

    def _generate_report(self, results: Dict[str, Any]) -> str:
        md = [
            f"# {self.t['report_title']}",
            "",
            self.t["intro"],
            "",
            f"## {self.t['summary_section']}",
        ]

        for policy, metrics in results.items():
            md.extend([
                "",
                f"### {policy}",
                f"- **{self.t['total_reward']}**: {metrics['total_reward']}",
                f"- **{self.t['avg_reward']}**: {metrics['average_reward']}",
                f"- **{self.t['cumulative_regret']}**: {metrics['cumulative_regret']}",
                f"- **{self.t['best_arm_rate']}**: {metrics['best_arm_selection_rate'] * 100:.2f}%",
                "",
                f"**{self.t['arm_counts']}**:",
            ])
            for arm, count in metrics["arm_counts"].items():
                md.append(f"- {arm}: {count}")

        return "\n".join(md)


def main() -> None:
    """Entry point for the Bandit Lab."""
    root = project_root()
    config_path = root / "configs/bandit_config.json"

    # Language detection fallback
    lang = "en"
    profile_path = root / "configs/problem_profile.json"
    if profile_path.exists():
        try:
            profile = json.loads(profile_path.read_text(encoding="utf-8"))
            lang = profile.get("language", "en")
        except Exception:
            pass

    if not config_path.exists():
        print(f"Error: Bandit configuration not found at {config_path}")
        sys.exit(1)

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            bandit_config = json.load(f)

        lab = BanditLab(bandit_config, lang)
        lab.validate_config()

        results, history, report_md = lab.run()

        # Save artifacts
        results_path = root / "configs/bandit_results.json"
        with open(results_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        report_path = root / "reports/bandit-results.md"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report_md)

        history_path = root / "reports/bandit-history.csv"
        if history:
            keys = history[0].keys()
            with open(history_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(history)

        print(lab.t["status_complete"])
        print(f"- {results_path}")
        print(f"- {report_path}")
        print(f"- {history_path}")

    except Exception as e:
        print(f"Error in Bandit Lab: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
