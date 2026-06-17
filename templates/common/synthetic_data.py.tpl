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
    BANDIT_SCENARIOS = ["bandit_simple", "bandit_contextual_events", "bank_campaign_bandit"]

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
                "activation_success": "Project configuration updated! Raw data now points to: {path}",
                "next_steps_title": "\nNext Steps:",
                "next_step_data": "1. Run data preparation: python -m {pkg}.lab data",
                "next_step_train": "2. Run training:         python -m {pkg}.lab train",
                "next_step_eval": "3. Run evaluation:       python -m {pkg}.lab evaluate",
                "next_step_manual_title": "Manual configuration required:",
                "next_step_manual_raw": "- Set 'data.raw_path' to '{path}'",
                "next_step_manual_target": "- Set 'target.column' to '{target}'",
                "bandit_report_section": "## Bandit Scenario Analysis",
                "bandit_arm_stats": "### Arm Statistics",
                "bandit_logged_data_title": "### Logged Contextual Bandit Data",
                "bandit_logged_data_expl": "This dataset represents logged interactions where a behavior policy (logging policy) selected actions. It includes context, the selected action, and the observed reward.",
                "bandit_prob_dist": "### Action Probability Distribution",
                "bandit_delay_summary": "### Reward Delay Summary",
                "table_arm": "Arm",
                "table_events": "Events",
                "table_conv_rate": "Conv. Rate",
                "table_avg_revenue": "Avg. Revenue",
                "table_total_revenue": "Total Revenue",
                "table_avg_delay": "Avg. Delay (days)",
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
                "activation_success": "Configuração do projeto atualizada! Os dados brutos agora apontam para: {path}",
                "next_steps_title": "\nPróximos Passos:",
                "next_step_data": "1. Preparar os dados: python -m {pkg}.lab data",
                "next_step_train": "2. Treinar o modelo:  python -m {pkg}.lab train",
                "next_step_eval": "3. Avaliar o modelo:   python -m {pkg}.lab evaluate",
                "next_step_manual_title": "Configuração manual necessária:",
                "next_step_manual_raw": "- Defina 'data.raw_path' como '{path}'",
                "next_step_manual_target": "- Defina 'target.column' como '{target}'",
                "bandit_report_section": "## Análise do Cenário de Bandit",
                "bandit_arm_stats": "### Estatísticas dos Braços (Arms)",
                "bandit_logged_data_title": "### Dados de Bandit Contextual Logados",
                "bandit_logged_data_expl": "Este conjunto de dados representa interações registradas onde uma política de comportamento (logging policy) selecionou as ações. Inclui o contexto, a ação selecionada e a recompensa observada.",
                "bandit_prob_dist": "### Distribuição de Probabilidade de Ação",
                "bandit_delay_summary": "### Resumo de Atraso de Recompensa",
                "table_arm": "Braço (Arm)",
                "table_events": "Eventos",
                "table_conv_rate": "Taxa de Conv.",
                "table_avg_revenue": "Receita Média",
                "table_total_revenue": "Receita Total",
                "table_avg_delay": "Atraso Médio (dias)",
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

    def generate_bank_campaign_bandit(self, params: dict[str, Any]):
        n_samples = params.get("n_samples", 1000)
        np.random.seed(self.seed)

        arms = [
            "term_deposit_email",
            "term_deposit_phone",
            "investment_advisor_call",
            "credit_card_push"
        ]
        jobs = ["admin", "technician", "services", "management", "retired"]
        segments = ["low_value", "medium_value", "high_value"]
        channels = ["email", "phone", "mobile", "branch"]

        # Generate Context
        ages = np.random.randint(18, 70, n_samples)
        balances = np.random.randint(100, 15000, n_samples)
        job_indices = np.random.randint(0, len(jobs), n_samples)
        segment_indices = np.random.randint(0, len(segments), n_samples)
        channel_indices = np.random.randint(0, len(channels), n_samples)
        prev_contacts = np.random.randint(0, 10, n_samples)

        # Generate Actions (Uniform random for logging policy)
        arm_indices = np.random.randint(0, len(arms), n_samples)

        data = []
        for i in range(n_samples):
            age = ages[i]
            balance = balances[i]
            job = jobs[job_indices[i]]
            segment = segments[segment_indices[i]]
            channel_pref = channels[channel_indices[i]]
            contacts = prev_contacts[i]
            arm_name = arms[arm_indices[i]]

            # Reward logic
            score = 0
            # senior_high_balance customers respond better to investment_advisor_call
            if arm_name == "investment_advisor_call" and age > 50 and balance > 5000:
                score += 3.0
            # customers with email preference respond better to email arms
            if arm_name == "term_deposit_email" and channel_pref == "email":
                score += 2.0
            # young_low_balance customers respond better to credit_card_push
            if arm_name == "credit_card_push" and age < 30 and balance < 2000:
                score += 2.5

            # many previous contacts reduce conversion probability
            if contacts > 5:
                score -= 1.5

            prob = 1 / (1 + np.exp(- (score - 2.0))) # Base probability roughly 12% if score=0
            conversion = 1 if np.random.random() < prob else 0

            reward = conversion
            revenue = conversion * (150 if arm_name == "investment_advisor_call" else 40)
            delay_days = np.random.poisson(2) if conversion else 0

            data.append({
                "event_id": f"evt_{1000 + i}",
                "timestamp": f"2023-10-01 {10 + (i // 3600):02d}:{(i // 60) % 60:02d}:{i % 60:02d}",
                "customer_id": f"cust_{2000 + (i % (n_samples // 4 + 1))}",
                "age": age,
                "balance": balance,
                "job": job,
                "segment": segment,
                "channel_preference": channel_pref,
                "previous_contacts": contacts,
                "arm_name": arm_name,
                "action_probability": 1.0 / len(arms),
                "policy_name": "uniform_random_logging_policy",
                "reward": reward,
                "conversion": conversion,
                "revenue": revenue,
                "delay_days": delay_days
            })

        return pd.DataFrame(data)

    def _get_target_column(self, scenario: str) -> str:
        if scenario == "timeseries":
            return "value"
        if scenario in self.BANDIT_SCENARIOS:
            return "reward"
        return "target"

    def activate_dataset(self, scenario: str, csv_path: Path):
        config_path = project_root() / "configs/config.json"
        if not config_path.exists():
            return

        try:
            with open(config_path, "r", encoding="utf-8") as f:
                project_config = json.load(f)

            # Update data path
            # Use relative path from project root for portability
            rel_csv_path = csv_path.relative_to(project_root())
            project_config["data"]["raw_path"] = str(rel_csv_path)

            # Update target column based on scenario
            target_scenarios = ["classification", "regression", "timeseries"] + self.BANDIT_SCENARIOS
            if scenario in target_scenarios:
                project_config["target"]["column"] = self._get_target_column(scenario)

            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(project_config, f, indent=2, ensure_ascii=False)

            print(self.t["activation_success"].format(path=rel_csv_path))
        except Exception as e:
            print(f"Warning: Could not auto-activate dataset: {e}")

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
            elif scenario == "bank_campaign_bandit":
                df = self.generate_bank_campaign_bandit(params)
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

        if self.config.get("activate_as_project_dataset"):
            self.activate_dataset(scenario, csv_path)

        self.update_report(scenario, meta, df)

        # Print Next Steps
        pkg = "your_package"
        try:
            config_path = project_root() / "configs/config.json"
            if config_path.exists():
                with open(config_path, "r", encoding="utf-8") as f:
                    project_config = json.load(f)
                    pkg = project_config.get("project", {}).get("package", pkg)
        except:
            pass

        print(self.t["next_steps_title"])
        if self.config.get("activate_as_project_dataset"):
            print(self.t["next_step_data"].format(pkg=pkg))
            print(self.t["next_step_train"].format(pkg=pkg))
            print(self.t["next_step_eval"].format(pkg=pkg))
        else:
            rel_csv_path = csv_path.relative_to(project_root())
            target = self._get_target_column(scenario)

            print(self.t["next_step_manual_title"])
            print(self.t["next_step_manual_raw"].format(path=rel_csv_path))
            print(self.t["next_step_manual_target"].format(target=target))
            print(f"\n{self.t['next_step_data'].format(pkg=pkg)}")
            print(self.t["next_step_train"].format(pkg=pkg))
            print(self.t["next_step_eval"].format(pkg=pkg))

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

        if scenario == "bank_campaign_bandit":
            md.append("")
            md.append(self.t["bandit_report_section"])
            md.append("")
            md.append(self.t["bandit_logged_data_title"])
            md.append(self.t["bandit_logged_data_expl"])
            md.append("")

            # Arm Statistics
            md.append(self.t["bandit_arm_stats"])
            md.append(f"| {self.t['table_arm']} | {self.t['table_events']} | {self.t['table_conv_rate']} | {self.t['table_avg_revenue']} | {self.t['table_total_revenue']} |")
            md.append("| :--- | :--- | :--- | :--- | :--- |")

            stats = df.groupby("arm_name").agg({
                "reward": ["count", "mean"],
                "revenue": ["mean", "sum"]
            })

            for arm, row in stats.iterrows():
                count = int(row[("reward", "count")])
                conv_rate = f"{row[('reward', 'mean')]:.2%}"
                avg_rev = f"{row[('revenue', 'mean')]:.2f}"
                total_rev = f"{row[('revenue', 'sum')]:.2f}"
                md.append(f"| {arm} | {count} | {conv_rate} | {avg_rev} | {total_rev} |")

            md.append("")

            # Action Probability Distribution
            md.append(self.t["bandit_prob_dist"])
            prob_dist = df["action_probability"].value_counts(normalize=True).sort_index()
            md.append("| Prob | % |")
            md.append("| :--- | :--- |")
            for prob, val in prob_dist.items():
                md.append(f"| {prob:.4f} | {val:.2%} |")

            md.append("")

            # Delay Summary
            md.append(self.t["bandit_delay_summary"])
            md.append(self.t["table_header"])
            md.append(self.t["table_sep"])
            # delay_days is only relevant for converted users
            converted = df[df["conversion"] == 1]
            avg_delay = converted["delay_days"].mean() if not converted.empty else 0
            md.append(f"| {self.t['table_avg_delay']} | {avg_delay:.2f} |")

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
