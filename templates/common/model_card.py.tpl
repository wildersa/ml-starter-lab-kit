from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from .core.config import load_config, project_root

class ModelCardGenerator:
    def __init__(self, lang: str = "en"):
        self.lang = lang
        self.t = {
            "en": {
                "report_title": "Model Card — {{PROJECT_NAME}}",
                "not_production_note": "> **Note**: This is a starter model card for educational purposes, not for production governance.",
                "section_summary": "## 1. Project Summary",
                "section_dataset": "## 2. Dataset and Features",
                "section_baseline": "## 3. Baseline and Model",
                "section_metrics": "## 4. Performance Metrics",
                "section_quality": "## 5. Data Quality and Risks",
                "section_usage": "## 6. Intended Use and Limitations",
                "section_next_steps": "## 7. Next Experiments",
                "task": "Task",
                "target_column": "Target Column",
                "dataset_path": "Dataset Path",
                "rows": "Total Rows",
                "columns": "Total Columns",
                "features": "Selected/Known Features",
                "baseline_model": "Baseline Model",
                "diagnostic_model": "Diagnostic Model",
                "metrics_label": "Metrics",
                "intended_use": "Intended Use",
                "intended_use_text": "This model is intended for educational exploration and as a baseline for the {{PROJECT_NAME}} project.",
                "limitations": "Limitations",
                "limitations_text": "Not suitable for production use. The model was trained on a specific dataset and may not generalize to other contexts.",
                "non_goals": "Non-Goals",
                "non_goals_text": "This is not intended to be a high-performance production model or to handle real-time decision-making without further validation.",
                "quality_issues": "Known Data Quality Issues",
                "leakage_warnings": "Leakage Warnings",
                "next_steps": "Next Steps",
                "none_detected": "None detected.",
                "no_data": "Not available yet (run the corresponding lab/pipeline step).",
                "placeholder": "TODO: Fill this section with your observations.",
                "goal_label": "Project Goal",
            },
            "pt-BR": {
                "report_title": "Model Card — {{PROJECT_NAME}}",
                "not_production_note": "> **Nota**: Este é um model card inicial para fins educacionais, não para governança de produção.",
                "section_summary": "## 1. Resumo do Projeto",
                "section_dataset": "## 2. Dataset e Features",
                "section_baseline": "## 3. Baseline e Modelo",
                "section_metrics": "## 4. Métricas de Desempenho",
                "section_quality": "## 5. Qualidade de Dados e Riscos",
                "section_usage": "## 6. Uso Pretendido e Limitações",
                "section_next_steps": "## 7. Próximos Experimentos",
                "task": "Tarefa",
                "target_column": "Coluna Alvo (Target)",
                "dataset_path": "Caminho do Dataset",
                "rows": "Total de Linhas",
                "columns": "Total de Colunas",
                "features": "Features Selecionadas/Conhecidas",
                "baseline_model": "Modelo Baseline",
                "diagnostic_model": "Modelo Diagnóstico",
                "metrics_label": "Métricas",
                "intended_use": "Uso Pretendido",
                "intended_use_text": "Este modelo destina-se à exploração educacional e como um baseline para o projeto {{PROJECT_NAME}}.",
                "limitations": "Limitações",
                "limitations_text": "Não adequado para uso em produção. O modelo foi treinado em um dataset específico e pode não generalizar para outros contextos.",
                "non_goals": "Não-objetivos",
                "non_goals_text": "Este não se destina a ser um modelo de produção de alto desempenho ou a lidar com tomadas de decisão em tempo real sem validação adicional.",
                "quality_issues": "Problemas de Qualidade de Dados Conhecidos",
                "leakage_warnings": "Avisos de Leakage (Vazamento)",
                "next_steps": "Próximos Passos",
                "none_detected": "Nenhum detectado.",
                "no_data": "Ainda não disponível (execute o lab/passo do pipeline correspondente).",
                "placeholder": "TODO: Preencha esta seção com suas observações.",
                "goal_label": "Objetivo do Projeto",
            }
        }[self.lang]

    def _load_json(self, path: Path) -> dict[str, Any]:
        if path.exists():
            try:
                return json.loads(path.read_text(encoding="utf-8"))
            except:
                pass
        return {}

    def generate(self):
        root = project_root()

        # Load artifacts
        config = load_config()
        profile = self._load_json(root / "configs/problem_profile.json")
        insights = self._load_json(root / "reports/data-insights.json")
        baseline = self._load_json(root / "configs/baseline_results.json")
        quick_model = self._load_json(root / "reports/quick-model-metrics.json")
        metrics = self._load_json(root / "reports/metrics.json")

        md = [
            f"# {self.t['report_title']}",
            "",
            self.t["not_production_note"],
            "",
            self.t["section_summary"],
            f"- **{self.t['task']}**: {config.get('project', {}).get('task', 'N/A')}",
            f"- **{self.t['goal_label']}**: {profile.get('goal', self.t['placeholder'])}",
            "",
            self.t["section_dataset"],
            f"- **{self.t['target_column']}**: {config.get('target', {}).get('column', 'N/A')}",
            f"- **{self.t['dataset_path']}**: {config.get('data', {}).get('raw_path', 'N/A')}",
        ]

        # Dataset details from insights
        if insights:
            quality = insights.get("quality", {})
            md.append(f"- **{self.t['rows']}**: {quality.get('rows', 'N/A')}")
            md.append(f"- **{self.t['columns']}**: {quality.get('columns', 'N/A')}")

            features = [f["column"] for f in insights.get("features", [])]
            if features:
                md.append(f"- **{self.t['features']}**: {', '.join(features[:10])}{'...' if len(features) > 10 else ''}")
        else:
            md.append(f"- **{self.t['rows']}**: {self.t['no_data']}")

        md.append("")
        md.append(self.t["section_baseline"])

        if baseline:
            md.append(f"- **{self.t['baseline_model']}**: {baseline.get('model_type', 'N/A')}")
        else:
            md.append(f"- **{self.t['baseline_model']}**: {self.t['no_data']}")

        if quick_model:
            md.append(f"- **{self.t['diagnostic_model']}**: Random Forest (Diagnostic)")
        else:
            md.append(f"- **{self.t['diagnostic_model']}**: {self.t['no_data']}")

        md.append("")
        md.append(self.t["section_metrics"])

        has_metrics = False
        if metrics:
            has_metrics = True
            md.append(f"### Final Model Metrics")
            for k, v in metrics.items():
                if isinstance(v, (int, float)):
                    md.append(f"- **{k.upper()}**: {v:.4f}")

        if quick_model:
            has_metrics = True
            md.append(f"### Diagnostic Metrics")
            for k, v in quick_model.get("metrics", {}).items():
                md.append(f"- **{k.upper()}**: {v:.4f}")

        if not has_metrics:
            md.append(self.t["no_data"])

        md.append("")
        md.append(self.t["section_quality"])

        md.append(f"### {self.t['quality_issues']}")
        if insights and insights.get("warnings"):
            for w in insights["warnings"]:
                if w.get("type") not in ["leakage_name", "leakage_signal"]:
                    md.append(f"- [{w.get('type', 'WARNING')}] {w.get('message', '')}")
        else:
            md.append(self.t["none_detected"])

        md.append("")
        md.append(f"### {self.t['leakage_warnings']}")
        leakage_found = False
        if insights and insights.get("warnings"):
            for w in insights["warnings"]:
                if w.get("type") in ["leakage_name", "leakage_signal"]:
                    leakage_found = True
                    md.append(f"- [{w.get('type')}] {w.get('message')}")

        if quick_model and quick_model.get("warnings"):
            leakage_found = True
            for w in quick_model["warnings"]:
                md.append(f"- [DIAGNOSTIC] {w}")

        if not leakage_found:
            md.append(self.t["none_detected"])

        md.append("")
        md.append(self.t["section_usage"])
        md.append(f"### {self.t['intended_use']}")
        md.append(self.t["intended_use_text"])
        md.append(f"### {self.t['limitations']}")
        md.append(self.t["limitations_text"])
        md.append(f"### {self.t['non_goals']}")
        md.append(self.t["non_goals_text"])

        md.append("")
        md.append(self.t["section_next_steps"])
        if profile and profile.get("next_steps"):
            for step in profile.get("next_steps")[:5]:
                md.append(f"- {step}")
        else:
            md.append(self.t["placeholder"])

        # Write file
        report_path = root / "reports/model-card.md"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text("\n".join(md), encoding="utf-8")
        print(f"Model Card generated at {report_path}")

def main():
    root = project_root()

    # Language detection
    lang = "en"
    profile_path = root / "configs/problem_profile.json"
    if profile_path.exists():
        try:
            profile = json.loads(profile_path.read_text(encoding="utf-8"))
            lang = profile.get("language", "en")
        except: pass

    gen = ModelCardGenerator(lang=lang)
    gen.generate()

if __name__ == "__main__":
    main()
