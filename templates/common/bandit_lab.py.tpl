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
import math
import argparse
from typing import Any, Dict, List, Tuple
from pathlib import Path

from .core.config import project_root
from .metrics import bandit_total_reward, bandit_average_reward, bandit_lift


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


class UCB1Policy:
    """Policy that uses Upper Confidence Bound (UCB1) for exploration."""

    def __init__(self, n_arms: int, seed: int = 42):
        self.n_arms = n_arms
        self.rng = random.Random(seed)
        self.counts = [0] * n_arms
        self.values = [0.0] * n_arms
        self.t = 0

    def select_arm(self) -> int:
        self.t += 1
        # Initial sweep: select each arm at least once
        for i in range(self.n_arms):
            if self.counts[i] == 0:
                return i

        # Calculate UCB score for each arm
        ucb_values = [0.0] * self.n_arms
        for i in range(self.n_arms):
            bonus = math.sqrt((2 * math.log(self.t)) / self.counts[i])
            ucb_values[i] = self.values[i] + bonus

        max_ucb = max(ucb_values)
        indices = [i for i, v in enumerate(ucb_values) if v == max_ucb]
        return self.rng.choice(indices)

    def update(self, arm_index: int, reward: int) -> None:
        self.counts[arm_index] += 1
        n = self.counts[arm_index]
        value = self.values[arm_index]
        # Incremental average update
        new_value = ((n - 1) / n) * value + (1 / n) * reward
        self.values[arm_index] = new_value


class ThompsonSamplingPolicy:
    """Policy that uses Thompson Sampling with Beta posterior for Bernoulli rewards."""

    def __init__(self, n_arms: int, seed: int = 42):
        self.n_arms = n_arms
        self.rng = random.Random(seed)
        # Beta(1, 1) is a uniform prior
        self.alphas = [1.0] * n_arms
        self.betas = [1.0] * n_arms

    def select_arm(self) -> int:
        samples = [self.rng.betavariate(self.alphas[i], self.betas[i]) for i in range(self.n_arms)]
        max_sample = max(samples)
        indices = [i for i, v in enumerate(samples) if v == max_sample]
        return self.rng.choice(indices)

    def update(self, arm_index: int, reward: int) -> None:
        if reward == 1:
            self.alphas[arm_index] += 1
        else:
            self.betas[arm_index] += 1


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
                "edu_header": "Understanding Multi-Armed Bandits",
                "edu_intro": "Multi-Armed Bandit (MAB) is a form of sequential decision learning. Unlike supervised learning where you have a fixed dataset and labels, MAB learns while it makes decisions through a sequence of actions.",
                "edu_cycle": "In each round, the policy chooses one arm (action) and observes the reward only for that specific arm. This partial feedback is the core challenge of MAB: you don't know what the reward would have been if you chose a different arm.",
                "edu_random": "The **Random Policy** serves as a baseline that does not learn from feedback. It helps to evaluate how much better adaptive policies can perform by effectively balancing exploration and exploitation.",
                "edu_epsilon_greedy": "The **Epsilon-Greedy** policy is a simple yet effective strategy. It explores the environment by choosing a random arm with probability `epsilon`, and exploits its current knowledge by choosing the best-performing arm otherwise.",
                "edu_ucb1": "The **UCB1 (Upper Confidence Bound)** policy uses an 'optimism in the face of uncertainty' approach. For each arm, it calculates the average reward plus an uncertainty bonus. Arms that haven't been tried much get a higher bonus, forcing the agent to explore them before focusing on the best-performing options.",
                "edu_thompson": "The **Thompson Sampling** policy is a Bayesian approach. It maintains a probability distribution (Beta posterior) for each arm. In each round, it samples from these distributions and chooses the arm with the highest sample. This naturally balances exploration (from the width of the distribution) and exploitation (from its center).",
                "summary_section": "Summary",
                "comparison_table": "Policy Comparison",
                "total_reward": "Total Reward",
                "avg_reward": "Average Reward",
                "cumulative_regret": "Cumulative Regret",
                "best_arm_rate": "Best Arm Selection Rate",
                "arm_counts": "Arm Selection Counts",
                "policy": "Policy",
                "lift_vs_random": "Lift vs. Random",
                "status_running": "Running {policy} policy simulation...",
                "status_complete": "Bandit Lab simulation complete.",
            },
            "pt-BR": {
                "report_title": "Resultados do Bandit Lab",
                "intro": "Resultados da simulação de ambiente Bernoulli Multi-Armed Bandit.",
                "edu_header": "Entendendo Multi-Armed Bandits",
                "edu_intro": "Multi-Armed Bandit (MAB) é uma forma de aprendizado por decisão sequencial. Diferente do aprendizado supervisionado onde você tem um conjunto de dados fixo e rótulos, o MAB aprende enquanto toma decisões através de uma sequência de ações.",
                "edu_cycle": "Em cada rodada, a política escolhe um 'arm' (ação) e observa a recompensa apenas para aquele arm específico. Esse feedback parcial é o desafio central do MAB: você não sabe qual teria sido a recompensa se tivesse escolhido um arm diferente.",
                "edu_random": "A **Política Aleatória (Random Policy)** serve como um baseline que não aprende com o feedback. Ela ajuda a avaliar o quanto melhor as políticas adaptativas podem performar ao equilibrar exploração (exploration) e explotação (exploitation).",
                "edu_epsilon_greedy": "A política **Epsilon-Greedy** é uma estratégia simples e eficaz. Ela explora o ambiente escolhendo um arm aleatório com probabilidade `epsilon` e explota seu conhecimento atual escolhendo o melhor arm nas outras vezes.",
                "edu_ucb1": "A política **UCB1 (Upper Confidence Bound)** utiliza uma abordagem de 'otimismo diante da incerteza'. Para cada arm, ela calcula a média de recompensa mais um bônus de incerteza. Arms pouco testados recebem um bônus maior, forçando o agente a explorá-los antes de focar nas melhores opções.",
                "edu_thompson": "A política **Thompson Sampling** é uma abordagem Bayesiana. Ela mantém uma distribuição de probabilidade (Beta posterior) para cada arm. Em cada rodada, ela sorteia uma amostra dessas distribuições e escolhe o arm com a maior amostra. Isso equilibra naturalmente exploração (pela largura da distribuição) e explotação (pelo seu centro).",
                "summary_section": "Resumo",
                "comparison_table": "Comparação de Políticas",
                "total_reward": "Recompensa Total",
                "avg_reward": "Recompensa Média",
                "cumulative_regret": "Regret Acumulado",
                "best_arm_rate": "Taxa de Escolha do Melhor Arm",
                "arm_counts": "Contagem de Escolha dos Arms",
                "policy": "Política",
                "lift_vs_random": "Melhoria vs. Aleatório",
                "status_running": "Executando simulação da política {policy}...",
                "status_complete": "Simulação do Bandit Lab concluída.",
            }
        }
        return translations.get(lang, translations["en"])

    def validate_config(self) -> None:
        """Validates that the configuration contains all required fields and correct types."""
        # Required fields and their expected types
        required_types = {
            "n_rounds": int,
            "seed": int,
            "arms": list,
            "policies": list
        }

        for field, expected_type in required_types.items():
            if field not in self.config:
                print(f"Error: Missing required field '{field}' in bandit_config.json")
                sys.exit(1)
            if not isinstance(self.config[field], expected_type):
                print(f"Error: Field '{field}' must be of type {expected_type.__name__}")
                sys.exit(1)

        if self.config["n_rounds"] <= 0:
            print("Error: 'n_rounds' must be a positive integer.")
            sys.exit(1)

        if not self.arms:
            print("Error: 'arms' list cannot be empty in bandit_config.json")
            sys.exit(1)

        # Arms validation
        for i, arm in enumerate(self.arms):
            if not isinstance(arm, dict):
                print(f"Error: Arm at index {i} must be a dictionary.")
                sys.exit(1)
            if "name" not in arm or "true_reward_probability" not in arm:
                print(f"Error: Arm at index {i} must have 'name' and 'true_reward_probability'.")
                sys.exit(1)

            p = arm["true_reward_probability"]
            if not isinstance(p, (int, float)) or not (0 <= p <= 1):
                print(f"Error: 'true_reward_probability' for arm '{arm['name']}' must be a number between 0 and 1.")
                sys.exit(1)

        # Policies validation
        valid_policies = ["random", "epsilon_greedy", "ucb1", "thompson_sampling"]
        if not self.config["policies"]:
            print("Error: 'policies' list cannot be empty.")
            sys.exit(1)

        for policy in self.config["policies"]:
            if policy not in valid_policies:
                print(f"Error: Unsupported policy '{policy}'. Supported: {valid_policies}")
                sys.exit(1)

        if "epsilon_greedy" in self.config["policies"]:
            epsilon = self.config.get("epsilon")
            if epsilon is None:
                print("Error: 'epsilon' is required when using 'epsilon_greedy' policy.")
                sys.exit(1)
            if not isinstance(epsilon, (int, float)) or not (0 <= epsilon <= 1):
                print("Error: 'epsilon' must be a number between 0 and 1.")
                sys.exit(1)

        # Reward model validation
        reward_model = self.config.get("reward_model", "bernoulli")
        if reward_model != "bernoulli":
            print(f"Error: Unsupported reward_model '{reward_model}'. Only 'bernoulli' is supported.")
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
            elif policy_name == "ucb1":
                policy = UCB1Policy(self.n_arms, self.seed)
            elif policy_name == "thompson_sampling":
                policy = ThompsonSamplingPolicy(self.n_arms, self.seed)
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

        # Gather all rewards for centralized metric calculation
        rewards = [h["reward"] for h in history]

        metrics = {
            "total_reward": bandit_total_reward(rewards),
            "cumulative_reward": bandit_total_reward(rewards),
            "average_reward": round(bandit_average_reward(rewards), 4),
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
            f"## {self.t['edu_header']}",
            "",
            self.t["edu_intro"],
            "",
            self.t["edu_cycle"],
            "",
            self.t["edu_random"],
            "",
            self.t["edu_epsilon_greedy"],
            "",
            self.t["edu_ucb1"],
            "",
            self.t["edu_thompson"],
            "",
            f"## {self.t['summary_section']}",
            "",
            f"### {self.t['comparison_table']}",
            "",
        ]

        # Table header
        header = f"| {self.t['policy']} | {self.t['total_reward']} | {self.t['avg_reward']} | {self.t['cumulative_regret']} | {self.t['best_arm_rate']} | {self.t['lift_vs_random']} |"
        separator = "| :--- | :---: | :---: | :---: | :---: | :---: |"
        md.append(header)
        md.append(separator)

        random_avg = results.get("random", {}).get("average_reward", 0.0)

        for policy, metrics in results.items():
            lift_str = "N/A"
            if policy != "random" and random_avg > 0:
                lift = bandit_lift(metrics["average_reward"], random_avg)
                lift_str = f"{lift:+.2%}"

            row = f"| {policy} | {metrics['total_reward']} | {metrics['average_reward']:.4f} | {metrics['cumulative_regret']:.2f} | {metrics['best_arm_selection_rate']:.2%} | {lift_str} |"
            md.append(row)

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
    # If called via the unified CLI (lab.py), the 'bandit' command might still be in sys.argv
    argv = sys.argv[1:]
    if argv and argv[0] == "bandit":
        argv = argv[1:]

    parser = argparse.ArgumentParser(description="Educational Multi-Armed Bandit Lab.")
    parser.add_argument("--config", type=str, default="configs/bandit_config.json", help="Path to bandit configuration file.")
    parser.add_argument("--list-policies", action="store_true", help="List available bandit policies.")
    args = parser.parse_args(argv)

    if args.list_policies:
        print("Available policies:")
        print("- random: Selects arms uniformly at random.")
        print("- epsilon_greedy: Explores with probability epsilon, exploits otherwise.")
        print("- ucb1: Upper Confidence Bound (optimism in the face of uncertainty).")
        print("- thompson_sampling: Bayesian approach using Beta distributions.")
        return

    root = project_root()
    config_path = root / args.config

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
