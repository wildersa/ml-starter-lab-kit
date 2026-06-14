from __future__ import annotations

import json
import argparse
import sys
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Any

try:
    from sklearn.datasets import make_classification, make_regression, make_blobs
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

from .core.config import project_root

class SyntheticDataLab:
    def __init__(self, config: dict[str, Any], lang: str = "en"):
        self.config = config
        self.lang = lang
        self.seed = config.get("seed", 42)
        self.output_dir = project_root() / config.get("output_dir", "data/synthetic")
        self.report_path = project_root() / "reports/synthetic-data-summary.md"

        self.translations = {
            "en": {
                "generating": "Generating synthetic data for scenario: {scenario}...",
                "success": "Success! Artifacts saved to: {path}",
                "report_title": "# Synthetic Data Lab Summary",
                "report_intro": "This report summarizes the synthetic data generated for study and testing.",
                "sklearn_missing": "Scikit-learn is required for this scenario. Please install it with 'pip install scikit-learn'.",
                "invalid_scenario": "Error: Unknown scenario '{scenario}'.",
                "reproducibility_note": "Deterministic generation using seed: {seed}",
                "scenario_details": "## Scenario Details",
                "table_header": "| Attribute | Value |",
                "table_sep": "| :--- | :--- |",
            },
            "pt-BR": {
                "generating": "Gerando dados sintéticos para o cenário: {scenario}...",
                "success": "Sucesso! Artefatos salvos em: {path}",
                "report_title": "# Resumo do Synthetic Data Lab",
                "report_intro": "Este relatório resume os dados sintéticos gerados para estudo e testes.",
                "sklearn_missing": "O Scikit-learn é necessário para este cenário. Instale-o com 'pip install scikit-learn'.",
                "invalid_scenario": "Erro: Cenário desconhecido '{scenario}'.",
                "reproducibility_note": "Geração determinística usando semente (seed): {seed}",
                "scenario_details": "## Detalhes do Cenário",
                "table_header": "| Atributo | Valor |",
                "table_sep": "| :--- | :--- |",
            }
        }
        self.t = self.translations.get(lang, self.translations["en"])

    def _ensure_output_dir(self):
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.report_path.parent.mkdir(parents=True, exist_ok=True)

    def generate_classification(self, params: dict[str, Any]):
        if not SKLEARN_AVAILABLE:
            raise ImportError(self.t["sklearn_missing"])

        n_samples = params.get("n_samples", 1000)
        n_features = params.get("n_features", 10)
        weights = params.get("weights", [0.5, 0.5])

        X, y = make_classification(
            n_samples=n_samples,
            n_features=n_features,
            n_informative=params.get("n_informative", 5),
            n_redundant=params.get("n_redundant", 2),
            weights=weights,
            random_state=self.seed
        )

        cols = [f"feature_{i:02d}" for i in range(n_features)]
        df = pd.DataFrame(X, columns=cols)
        df["target"] = y
        return df

    def generate_regression(self, params: dict[str, Any]):
        if not SKLEARN_AVAILABLE:
            raise ImportError(self.t["sklearn_missing"])

        n_samples = params.get("n_samples", 1000)
        n_features = params.get("n_features", 10)
        noise = params.get("noise", 1.0)

        X, y = make_regression(
            n_samples=n_samples,
            n_features=n_features,
            noise=noise,
            random_state=self.seed
        )

        cols = [f"feature_{i:02d}" for i in range(n_features)]
        df = pd.DataFrame(X, columns=cols)
        df["target"] = y
        return df

    def generate_clustering(self, params: dict[str, Any]):
        if not SKLEARN_AVAILABLE:
            raise ImportError(self.t["sklearn_missing"])

        n_samples = params.get("n_samples", 1000)
        n_features = params.get("n_features", 2)
        centers = params.get("centers", 3)

        X, _ = make_blobs(
            n_samples=n_samples,
            n_features=n_features,
            centers=centers,
            random_state=self.seed
        )

        cols = [f"feature_{i:02d}" for i in range(n_features)]
        df = pd.DataFrame(X, columns=cols)
        return df

    def generate_timeseries(self, params: dict[str, Any]):
        n_periods = params.get("n_periods", 365)
        freq = params.get("freq", "D")
        start_date = params.get("start_date", "2023-01-01")

        np.random.seed(self.seed)
        dates = pd.date_range(start=start_date, periods=n_periods, freq=freq)

        # Components
        time = np.arange(n_periods)
        trend = time * params.get("trend_slope", 0.1)
        seasonality = 10 * np.sin(2 * np.pi * time / params.get("seasonal_period", 30))
        noise = np.random.normal(0, params.get("noise_std", 1.0), n_periods)

        values = trend + seasonality + noise

        df = pd.DataFrame({
            "date": dates,
            "value": values
        })

        if params.get("include_promotion", True):
            df["on_promotion"] = (np.random.random(n_periods) < params.get("promo_prob", 0.1)).astype(int)
            # Add impact of promotion
            df.loc[df["on_promotion"] == 1, "value"] += params.get("promo_impact", 5.0)

        return df

    def generate_bandit_simple(self, params: dict[str, Any]):
        n_rounds = params.get("n_rounds", 1000)
        arms = params.get("arms", ["arm_a", "arm_b", "arm_c"])
        probs = params.get("probabilities", [0.05, 0.08, 0.12])

        np.random.seed(self.seed)
        history = []

        for r in range(n_rounds):
            arm_idx = np.random.randint(0, len(arms))
            reward = 1 if np.random.random() < probs[arm_idx] else 0
            history.append({
                "round": r + 1,
                "arm": arms[arm_idx],
                "reward": reward
            })

        return pd.DataFrame(history)

    def generate_bandit_contextual(self, params: dict[str, Any]):
        n_samples = params.get("n_samples", 1000)
        n_features = params.get("n_features", 4)
        arms = params.get("arms", ["offer_a", "offer_b"])

        np.random.seed(self.seed)

        # Context (features)
        X = np.random.normal(0, 1, (n_samples, n_features))
        cols = [f"context_{i:02d}" for i in range(n_features)]
        df = pd.DataFrame(X, columns=cols)

        # Action/Arm assignment (random for history)
        arm_indices = np.random.randint(0, len(arms), n_samples)
        df["action"] = [arms[i] for i in arm_indices]

        # Reward logic: some context features influence some arms
        # reward = sigmoid(dot(X, weights[arm])) + noise
        rewards = []
        for i in range(n_samples):
            # Simple interaction: context_00 likes offer_a, context_01 likes offer_b
            if df.loc[i, "action"] == "offer_a":
                score = df.loc[i, "context_00"] * 2.0
            else:
                score = df.loc[i, "context_01"] * 2.0

            prob = 1 / (1 + np.exp(-score))
            rewards.append(1 if np.random.random() < prob else 0)

        df["reward"] = rewards

        if params.get("include_delay", False):
            df["delay_steps"] = np.random.poisson(params.get("avg_delay", 2), n_samples)

        return df

    def run(self):
        self._ensure_output_dir()
        scenario = self.config.get("scenario", "classification")
        params = self.config.get("parameters", {})

        print(self.t["generating"].format(scenario=scenario))

        try:
            if scenario == "classification":
                df = self.generate_classification(params)
            elif scenario == "regression":
                df = self.generate_regression(params)
            elif scenario == "clustering":
                df = self.generate_clustering(params)
            elif scenario == "timeseries":
                df = self.generate_timeseries(params)
            elif scenario == "bandit_simple":
                df = self.generate_bandit_simple(params)
            elif scenario == "bandit_contextual_events":
                df = self.generate_bandit_contextual(params)
            else:
                print(self.t["invalid_scenario"].format(scenario=scenario))
                sys.exit(1)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)

        # Save artifacts
        filename = f"{scenario}.csv"
        csv_path = self.output_dir / filename
        df.to_csv(csv_path, index=False)

        json_path = self.output_dir / f"{scenario}_meta.json"
        meta = {
            "scenario": scenario,
            "seed": self.seed,
            "n_samples": len(df),
            "columns": list(df.columns),
            "parameters": params
        }
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2)

        print(self.t["success"].format(path=self.output_dir))

        self.update_report(scenario, meta, df)

    def update_report(self, scenario: str, meta: dict[str, Any], df: pd.DataFrame):
        md = [
            self.t["report_title"],
            "",
            self.t["report_intro"],
            "",
            f"## Scenario: {scenario}",
            self.t["reproducibility_note"].format(seed=self.seed),
            "",
            self.t["scenario_details"],
            self.t["table_header"],
            self.t["table_sep"],
            f"| Rows | {len(df)} |",
            f"| Columns | {len(df.columns)} |",
        ]

        for k, v in meta["parameters"].items():
            md.append(f"| {k} | {v} |")

        md.append("")
        md.append("### Data Preview")
        md.append("```")
        md.append(df.head().to_string(index=False))
        md.append("```")

        with open(self.report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(md))

def main():
    parser = argparse.ArgumentParser(description="Synthetic Data Lab Generator")
    parser.add_argument("--config", type=str, default="configs/synthetic_data.json", help="Path to synthetic data config")

    # Strip 'synthetic' command if called from lab.py
    argv = sys.argv[1:]
    if argv and argv[0] == "synthetic":
        argv = argv[1:]

    args = parser.parse_args(argv)

    try:
        config_path = project_root() / args.config
        if not config_path.exists():
            print(f"Config file not found: {config_path}")
            sys.exit(1)

        with open(config_path, "r", encoding="utf-8") as f:
            full_config = json.load(f)

        # Detect language from problem profile if possible
        lang = "en"
        profile_path = project_root() / "configs/problem_profile.json"
        if profile_path.exists():
            try:
                profile = json.loads(profile_path.read_text(encoding="utf-8"))
                lang = profile.get("language", "en")
            except:
                pass

        lab = SyntheticDataLab(full_config, lang=lang)
        lab.run()

    except Exception as e:
        print(f"Error in Synthetic Data Lab: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
