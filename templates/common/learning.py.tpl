from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .core.config import load_config, project_root


class LearningNotesGenerator:
    def __init__(self, eda_summary: dict[str, Any], problem_profile: dict[str, Any], config: dict[str, Any]):
        self.eda = eda_summary
        self.profile = problem_profile
        self.config = config
        self.lang = problem_profile.get("language", "en")
        self.t = {
            "en": {
                "report_title": "Dataset Learning Notes",
                "intro": "These notes explain ML concepts using your actual dataset.",
                "target_section": "🎯 The Target: {target}",
                "target_desc": "The target is what you want to predict. In your case, it is '{target}'.",
                "target_stats": "Found {unique_count} unique values for this target.",
                "features_section": "🧪 Features",
                "features_desc": "Features are the data used to make predictions. Your dataset has {feat_count} columns that can be used as features.",
                "missing_data": "Column '{col}' has {count} missing values. This is a common real-world issue that requires 'imputation' (filling in the blanks).",
                "baseline_section": "🔬 Baseline Concept",
                "baseline_desc": "A baseline is a simple starting point. For your '{goal}' goal, a good baseline would be {baseline_idea}.",
                "metrics_section": "📈 Success Metrics",
                "metrics_desc": "To know if your model is good, we use metrics. Based on your priority of '{priority}', we suggest focusing on {metric_suggestion}.",
                "risks_section": "⚠️ Data Risks",
                "risks_desc": "Based on EDA, we found some things to watch out for:",
                "risk_imbalance": "Class imbalance detected: some outcomes are much rarer than others.",
                "risk_high_cardinality": "Column '{col}' has many unique values, which might be an ID or high-cardinality category.",
                "next_steps_section": "🚀 Recommended Next Steps",
                "artifact_created": "Learning artifacts created in configs/ and reports/",
                "eda_prerequisite": "Learning notes require an EDA summary. Please run EDA first.",
                "classification_baseline": "predicting the most frequent category (Mode)",
                "regression_baseline": "predicting the average value (Mean)",
                "clustering_baseline": "measuring distance to random centroids",
                "timeseries_baseline": "using the last known value (Naive forecast)",
            },
            "pt-BR": {
                "report_title": "Notas de Aprendizado do Dataset",
                "intro": "Estas notas explicam conceitos de ML usando seu dataset real.",
                "target_section": "🎯 O Alvo (Target): {target}",
                "target_desc": "O alvo é o que você deseja prever. No seu caso, é '{target}'.",
                "target_stats": "Encontrados {unique_count} valores únicos para este alvo.",
                "features_section": "🧪 Features (Características)",
                "features_desc": "Features são os dados usados para fazer previsões. Seu dataset tem {feat_count} colunas que podem ser usadas como features.",
                "missing_data": "A coluna '{col}' tem {count} valores ausentes. Isso é um problema comum no mundo real que exige 'imputação' (preenchimento de lacunas).",
                "baseline_section": "🔬 Conceito de Baseline",
                "baseline_desc": "Um baseline é um ponto de partida simples. Para o seu objetivo de '{goal}', um bom baseline seria {baseline_idea}.",
                "metrics_section": "📈 Métricas de Sucesso",
                "metrics_desc": "Para saber se seu modelo é bom, usamos métricas. Com base na sua prioridade de '{priority}', sugerimos focar em {metric_suggestion}.",
                "risks_section": "⚠️ Riscos nos Dados",
                "risks_desc": "Com base na EDA, encontramos alguns pontos de atenção:",
                "risk_imbalance": "Desbalanceamento de classes detectado: alguns resultados são muito mais raros que outros.",
                "risk_high_cardinality": "A coluna '{col}' tem muitos valores únicos, o que pode ser um ID ou categoria de alta cardinalidade.",
                "next_steps_section": "🚀 Próximos Passos Recomendados",
                "artifact_created": "Artefatos de aprendizado criados em configs/ e reports/",
                "eda_prerequisite": "As notas de aprendizado exigem um resumo de EDA. Por favor, execute a EDA primeiro.",
                "classification_baseline": "prever a categoria mais frequente (Moda)",
                "regression_baseline": "prever o valor médio (Média)",
                "clustering_baseline": "medir a distância para centroides aleatórios",
                "timeseries_baseline": "usar o último valor conhecido (Previsão Naive)",
            }
        }[self.lang]

    def _get_baseline_idea(self) -> str:
        goal = self.profile.get("goal", "").lower()
        if "category" in goal or "categoria" in goal:
            return self.t["classification_baseline"]
        if "number" in goal or "número" in goal:
            return self.t["regression_baseline"]
        if "group" in goal or "agrupar" in goal:
            return self.t["clustering_baseline"]
        if "forecast" in goal or "prever valores futuros" in goal:
            return self.t["timeseries_baseline"]
        return "a simple rule-based model"

    def _get_metric_suggestion(self) -> str:
        priority = self.profile.get("priority", "").lower()
        goal = self.profile.get("goal", "").lower()

        if "performance" in priority:
            return "Accuracy/F1-Score" if "category" in goal else "RMSE/MAE"
        if "imbalanced" in priority:
            return "Precision-Recall AUC or F1-Score"
        if "interpretability" in priority:
            return "R-squared or simple accuracy to ensure the model logic holds"
        return "standard cross-validation scores"

    def generate(self) -> tuple[dict[str, Any], str]:
        target = self.eda.get("target_column", "unknown")
        unique_targets = len(self.eda.get("target_distribution", {}))
        feat_count = len(self.eda.get("columns", [])) - (1 if self.eda.get("target_exists") else 0)

        # Build JSON context
        context = {
            "target": {
                "name": target,
                "concepts": [
                    self.t["target_desc"].format(target=target),
                    self.t["target_stats"].format(unique_count=unique_targets)
                ]
            },
            "features": {
                "count": feat_count,
                "concepts": [
                    self.t["features_desc"].format(feat_count=feat_count)
                ]
            },
            "baseline": {
                "idea": self._get_baseline_idea(),
                "description": self.t["baseline_desc"].format(
                    goal=self.profile.get("goal", "ML"),
                    baseline_idea=self._get_baseline_idea()
                )
            },
            "metrics": {
                "suggestion": self._get_metric_suggestion(),
                "description": self.t["metrics_desc"].format(
                    priority=self.profile.get("priority", "learning"),
                    metric_suggestion=self._get_metric_suggestion()
                )
            },
            "risks": []
        }

        # Add data-driven risks
        missing = self.eda.get("missing_summary", {})
        for col, count in missing.items():
            if count > 0:
                context["risks"].append(self.t["missing_data"].format(col=col, count=count))

        uniques = self.eda.get("unique_counts", {})
        rows = self.eda.get("rows", 0)
        for col, count in uniques.items():
            if count / (rows + 1e-6) > 0.9 and rows > 10:
                context["risks"].append(self.t["risk_high_cardinality"].format(col=col))

        # Build Markdown
        md = [
            f"# {self.t['report_title']}",
            "",
            self.t["intro"],
            "",
            f"## {self.t['target_section'].format(target=target)}",
            self.t["target_desc"].format(target=target),
            self.t["target_stats"].format(unique_count=unique_targets),
            "",
            f"## {self.t['features_section']}",
            self.t["features_desc"].format(feat_count=feat_count),
            ""
        ]

        if context["risks"]:
            md.append(f"### {self.t['risks_section']}")
            md.append(self.t["risks_desc"])
            for risk in context["risks"]:
                md.append(f"- {risk}")
            md.append("")

        md.extend([
            f"## {self.t['baseline_section']}",
            context["baseline"]["description"],
            "",
            f"## {self.t['metrics_section']}",
            context["metrics"]["description"],
            "",
            f"## {self.t['next_steps_section']}",
            f"1. Review `configs/learning_context.json`",
            f"2. Explore your features in the Learning Workspace",
            f"3. Run `python -m {self.config['project']['package']}.lab train`"
        ])

        return context, "\n".join(md)


def main():
    root = project_root()
    eda_path = root / "configs/eda_summary.json"

    # P0.1: Check for EDA summary
    if not eda_path.exists():
        # We need a way to know the language before loading problem_profile
        # But we can try to load it first
        lang = "en"
        profile_path = root / "configs/problem_profile.json"
        if profile_path.exists():
            try:
                profile = json.loads(profile_path.read_text(encoding="utf-8"))
                lang = profile.get("language", "en")
            except:
                pass

        msgs = {
            "en": "Learning notes require an EDA summary. Please run EDA first:\n  python -m {pkg}.lab eda",
            "pt-BR": "As notas de aprendizado exigem um resumo de EDA. Por favor, execute a EDA primeiro:\n  python -m {pkg}.lab eda"
        }

        try:
            config = load_config()
            pkg = config.get("project", {}).get("package", "your_package")
        except:
            pkg = "your_package"

        print(msgs.get(lang, msgs["en"]).format(pkg=pkg))
        return

    try:
        config = load_config()
        with open(eda_path, "r", encoding="utf-8") as f:
            eda_summary = json.load(f)

        profile_path = root / "configs/problem_profile.json"
        if profile_path.exists():
            with open(profile_path, "r", encoding="utf-8") as f:
                problem_profile = json.load(f)
        else:
            problem_profile = {"language": "en"}

        generator = LearningNotesGenerator(eda_summary, problem_profile, config)
        context, report_md = generator.generate()

        # P0.2: Create artifacts
        context_path = root / "configs/learning_context.json"
        context_path.parent.mkdir(parents=True, exist_ok=True)
        with open(context_path, "w", encoding="utf-8") as f:
            json.dump(context, f, indent=2, ensure_ascii=False)

        report_path = root / "reports/learning-notes.md"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report_md)

        print(generator.t["artifact_created"])
        print(f"- {context_path}")
        print(f"- {report_path}")

    except Exception as e:
        print(f"Error generating learning notes: {e}")


if __name__ == "__main__":
    main()
