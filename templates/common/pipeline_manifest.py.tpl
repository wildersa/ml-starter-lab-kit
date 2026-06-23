from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any
from datetime import datetime

from .core.config import load_config, project_root

class PipelineManifestGenerator:
    def __init__(self, lang: str = "en"):
        self.lang = lang
        self.t = {
            "en": {
                "manifest_title": "Pipeline Reproducibility Summary — {{PROJECT_NAME}}",
                "section_status": "## 1. Execution Status",
                "section_artifacts": "## 2. Generated Artifacts",
                "section_config": "## 3. Configuration & Metadata",
                "step": "Step",
                "status": "Status",
                "artifact": "Artifact",
                "path": "Relative Path",
                "executed": "✅ Executed",
                "pending": "⏳ Pending/Missing",
                "not_applicable": "N/A",
                "step_data": "Data Preparation",
                "step_eda": "Exploratory Data Analysis",
                "step_insights": "Dataset Intelligence",
                "step_screening": "Feature Screening",
                "step_train": "Model Training",
                "step_evaluate": "Model Evaluation",
                "step_model_card": "Model Card Generation",
                "metric_summary": "### Metric Summary",
                "no_metrics": "No metrics available yet.",
                "note_reproducibility": "> **Reproducibility Note**: This manifest summarizes the artifacts and configurations used in the current run. To reproduce this state, ensure you use the same dataset version and the configuration files listed below.",
            },
            "pt-BR": {
                "manifest_title": "Resumo de Reprodutibilidade do Pipeline — {{PROJECT_NAME}}",
                "section_status": "## 1. Status de Execução",
                "section_artifacts": "## 2. Artefatos Gerados",
                "section_config": "## 3. Configuração e Metadados",
                "step": "Passo",
                "status": "Status",
                "artifact": "Artefato",
                "path": "Caminho Relativo",
                "executed": "✅ Executado",
                "pending": "⏳ Pendente/Ausente",
                "not_applicable": "N/A",
                "step_data": "Preparação de Dados",
                "step_eda": "Análise Exploratória (EDA)",
                "step_insights": "Inteligência de Dados",
                "step_screening": "Triagem de Features",
                "step_train": "Treinamento do Modelo",
                "step_evaluate": "Avaliação do Modelo",
                "step_model_card": "Geração de Model Card",
                "metric_summary": "### Resumo de Métricas",
                "no_metrics": "Nenhuma métrica disponível ainda.",
                "note_reproducibility": "> **Nota de Reprodutibilidade**: Este manifesto resume os artefatos e configurações utilizados na execução atual. Para reproduzir este estado, certifique-se de usar a mesma versão do dataset e os arquivos de configuração listados abaixo.",
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
        config = load_config()
        profile = self._load_json(root / "configs/problem_profile.json")

        # Define steps and their expected artifacts
        steps_map = [
            {"id": "data", "name": self.t["step_data"], "artifact": "data/processed/"},
            {"id": "eda", "name": self.t["step_eda"], "artifact": "reports/figures/"},
            {"id": "insights", "name": self.t["step_insights"], "artifact": "reports/data-insights.json"},
            {"id": "screening", "name": self.t["step_screening"], "artifact": "reports/quick-model-metrics.json"},
            {"id": "train", "name": self.t["step_train"], "artifact": "models/model.joblib"},
            {"id": "evaluate", "name": self.t["step_evaluate"], "artifact": "reports/metrics.json"},
            {"id": "model_card", "name": self.t["step_model_card"], "artifact": "reports/model-card.md"},
        ]

        # Artifacts details
        artifacts = []
        manifest_data = {
            "project": config.get("project", {}).get("name", "{{PROJECT_NAME}}"),
            "task": config.get("project", {}).get("task", "N/A"),
            "generated_at": datetime.now().isoformat(),
            "config": {
                "raw_data": config.get("data", {}).get("raw_path", "N/A"),
                "processed_data": config.get("data", {}).get("processed_path", "N/A"),
                "target": config.get("target", {}).get("column", "N/A"),
                "seed": config.get("training", {}).get("seed", "N/A"),
            },
            "steps": [],
            "artifacts": [],
            "metrics": {}
        }

        # Check steps and artifacts
        for s in steps_map:
            path = root / s["artifact"]
            exists = path.exists()
            status = self.t["executed"] if exists else self.t["pending"]
            manifest_data["steps"].append({
                "step": s["id"],
                "name": s["name"],
                "status": "executed" if exists else "pending",
                "artifact_path": s["artifact"]
            })
            if exists:
                manifest_data["artifacts"].append({
                    "name": s["name"],
                    "path": s["artifact"]
                })

        # Metrics summary
        metrics = self._load_json(root / "reports/metrics.json")
        quick_metrics = self._load_json(root / "reports/quick-model-metrics.json")
        if metrics:
            manifest_data["metrics"]["final"] = metrics
        if quick_metrics:
            manifest_data["metrics"]["diagnostic"] = quick_metrics.get("metrics", {})

        # Baseline info
        baseline = self._load_json(root / "configs/baseline_results.json")
        if baseline:
            manifest_data["baseline"] = baseline

        # Features info
        insights = self._load_json(root / "reports/data-insights.json")
        if insights:
            manifest_data["features"] = [f["column"] for f in insights.get("features", [])]

        # Write JSON manifest
        manifest_path = root / "reports/pipeline-manifest.json"
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(json.dumps(manifest_data, indent=2, ensure_ascii=False), encoding="utf-8")

        # Generate Markdown summary
        md = [
            f"# {self.t['manifest_title']}",
            "",
            self.t["note_reproducibility"],
            "",
            self.t["section_status"],
            f"| {self.t['step']} | {self.t['status']} |",
            f"| :--- | :--- |"
        ]
        for step in manifest_data["steps"]:
            status_label = self.t["executed"] if step["status"] == "executed" else self.t["pending"]
            md.append(f"| {step['name']} | {status_label} |")

        md.append("")
        md.append(self.t["section_artifacts"])
        md.append(f"| {self.t['artifact']} | {self.t['path']} |")
        md.append(f"| :--- | :--- |")
        if not manifest_data["artifacts"]:
            md.append(f"| N/A | N/A |")
        else:
            for art in manifest_data["artifacts"]:
                md.append(f"| {art['name']} | `{art['path']}` |")

        md.append("")
        md.append(self.t["section_config"])
        md.append(f"- **Task**: {manifest_data['task']}")
        md.append(f"- **Target**: `{manifest_data['config']['target']}`")
        md.append(f"- **Raw Data**: `{manifest_data['config']['raw_data']}`")
        md.append(f"- **Seed**: `{manifest_data['config']['seed']}`")

        md.append("")
        md.append(self.t["metric_summary"])
        if not manifest_data["metrics"]:
            md.append(self.t["no_metrics"])
        else:
            if "final" in manifest_data["metrics"]:
                md.append("**Final Model:**")
                for k, v in manifest_data["metrics"]["final"].items():
                    if isinstance(v, (int, float)):
                        md.append(f"- {k}: `{v:.4f}`")
            if "diagnostic" in manifest_data["metrics"]:
                md.append("**Diagnostic Model:**")
                for k, v in manifest_data["metrics"]["diagnostic"].items():
                    if isinstance(v, (int, float)):
                        md.append(f"- {k}: `{v:.4f}`")

        # Write Markdown
        summary_path = root / "reports/pipeline-summary.md"
        summary_path.write_text("\n".join(md), encoding="utf-8")

        print(f"Pipeline manifest generated at {manifest_path}")
        print(f"Reproducibility summary generated at {summary_path}")

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

    gen = PipelineManifestGenerator(lang=lang)
    gen.generate()

if __name__ == "__main__":
    main()
