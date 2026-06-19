from __future__ import annotations

import re
import os
import sys
from pathlib import Path
from .constants import STARTER_ROOT, TASKS
from .config import create_config, create_problem_profile
from .scaffold import (
    create_dirs,
    create_readme,
    create_package_files,
    create_optional_files,
    create_tests,
    create_demo_data,
    create_notebook_placeholder,
    create_docs,
    create_pyproject,
    create_env_files,
)

TRANSLATIONS = {
    "en": {
        "language_name": "English",
        "choose_language": "Choose language",
        "project_basics": "Project basics",
        "project_name": "Project name",
        "package_name": "Python package name",
        "experience_mode": "Experience Mode",
        "mode_minimal": "Minimal Starter",
        "mode_guided": "Guided Learning Mode",
        "choose_task": "Project Type (ML Task)",
        "task_generic": "generic ML structure",
        "task_supervised": "classification/regression",
        "task_unsupervised": "PCA/K-Means/clustering",
        "task_timeseries": "time series/LSTM",
        "task_vision": "image classification/detection",
        "task_bandit": "Multi-Armed Bandit / adaptive decisions",
        "choose_option": "Choose an option",
        "invalid_option": "Invalid option.",
        "dataset_target": "Dataset and target",
        "supervised_panel_title": "Supervised Learning",
        "supervised_panel_text": "In supervised learning, you need a 'target' column (what you want to predict)\nand 'features' (the data used to make the prediction).",
        "unsupervised_panel_title": "Unsupervised Learning",
        "unsupervised_panel_text": "Unsupervised learning finds patterns in data without a specific target column.",
        "dataset_path": "Dataset path",
        "target_column": "Target column name",
        "include_demo": "Include demo dataset?",
        "problem_framing": "Problem framing",
        "problem_framing_panel_title": "Problem Framing",
        "problem_framing_panel_text": "This optional wizard helps configure the starter kit to your specific goals.",
        "press_enter_defaults": "Press Enter to use defaults.",
        "goal_question": "1. Main goal?",
        "goal_label": "Goal",
        "goal_predict_category": "predict a category",
        "goal_predict_number": "predict a number",
        "goal_group_records": "group similar records",
        "goal_forecast_values": "forecast future values",
        "goal_work_images_text": "work with images/text",
        "priority_question": "2. What matters most?",
        "priority_label": "Priority",
        "priority_interpretability": "interpretability",
        "priority_performance": "predictive performance",
        "priority_speed": "speed/simplicity",
        "priority_imbalanced": "handling imbalanced classes",
        "priority_learning": "learning/experimentation",
        "error_cost_question": "3. Which error is more costly?",
        "error_cost_label": "Error cost",
        "error_cost_fp": "false positive",
        "error_cost_fn": "false negative",
        "error_cost_both": "both similar",
        "error_cost_not_sure": "not sure",
        "size_question": "4. Expected dataset size?",
        "size_label": "Size",
        "size_small": "small",
        "size_medium": "medium",
        "size_large": "large",
        "size_not_sure": "not sure",
        "baseline_question": "5. Prefer simple baseline first?",
        "domain_note_question": "6. Any domain note? (optional)",
        "environment": "Environment",
        "create_env_files": "Create pyproject.toml and environment files?",
        "python_profile": "Python Profile",
        "profile_safe": "Python 3.12 (stable)",
        "profile_modern": "Python 3.14 (experimental/recent)",
        "ml_basics": "Include basic ML dependencies (pandas, numpy, scikit-learn, matplotlib, seaborn)?",
        "torch_support": "PyTorch Support",
        "torch_none": "none",
        "torch_cpu": "cpu",
        "torch_cuda126": "cuda 12.6",
        "torch_cuda128": "cuda 12.8",
        "mlflow_tracking": "Enable MLflow experiment tracking?",
        "optional_tools": "Optional tools",
        "create_docs": "Create documentation files?",
        "optional_files_templates": "Optional files (templates):",
        "optional_profile": "Optional Template Profile",
        "profile_minimal": "minimal",
        "profile_recommended": "recommended",
        "profile_full": "full",
        "profile_custom": "custom",
        "include_eda": "Include EDA support?",
        "include_preprocessing": "Include preprocessing support?",
        "include_metrics": "Include custom metrics?",
        "include_optimization": "Include optimization scaffolding?",
        "include_feature_measurement": "Include feature measurement?",
        "include_visualization": "Include visualization support?",
        "include_notebook_factory": "Include notebook factory?",
        "include_model_report": "Include model report template?",
        "include_experiment_log": "Include experiment log template?",
        "include_advisor": "Include explainable Dataset Advisor?",
        "include_learning": "Include dataset-contextual learning notes?",
        "include_baseline_lab": "Include educational Baseline Lab?",
        "include_bandit_lab": "Include educational Multi-Armed Bandit Lab?",
        "include_monitoring": "Include lightweight monitoring/drift stub?",
        "include_synthetic_data": "Include configurable Synthetic Data Lab (for testing/learning)?",
        "synthetic_panel_title": "Synthetic Data Lab",
        "synthetic_panel_text": "The Synthetic Data Lab generates deterministic datasets for experimentation.\nSetting 'activate_as_project_dataset' to true in its config will automatically\npoint your project to use the generated synthetic data.",
        "dependency_note_title": "Dependency Note",
        "dependency_note_text": "Dataset Advisor, Baseline Lab, and Synthetic Lab require basic ML dependencies (pandas, scikit-learn).",
        "enable_ml_basics": "Enable basic ML dependencies now?",
        "output_location": "Output location",
        "dir_current": "Current directory",
        "dir_nested": "New folder in current directory",
        "dir_sibling": "Sibling folder (recommended)",
        "dir_custom": "Custom path",
        "enter_custom_path": "Enter custom path",
        "warn_inside_repo": "The selected output directory is inside the starter repository.",
        "continue_anyway": "Do you want to continue anyway?",
        "overwrite_files": "Overwrite existing files if there is a conflict?",
        "final_summary": "Final summary",
        "summary_project_name": "Project name",
        "summary_package_name": "Package name",
        "summary_task": "ML Task",
        "summary_dataset_path": "Dataset path",
        "summary_target_column": "Target column",
        "summary_include_demo": "Include demo dataset",
        "summary_python_version": "Python version",
        "summary_experience_mode": "Experience Mode",
        "summary_torch_variant": "PyTorch variant",
        "summary_ml_basics": "Include ML basics",
        "summary_output_dir": "Output directory",
        "summary_overwrite": "Overwrite files",
        "create_project_files": "Create project files?",
        "aborted": "Aborted.",
        "success_msg": "Starter-kit created successfully!",
        "destination": "Destination",
        "next_steps": "Next steps",
        "next_step_cd": "Navigate to the project directory",
        "next_step_already_in": "You are already in the project directory.",
        "next_step_setup": "Set up the environment",
        "next_step_install": "Install the package in editable mode",
        "next_step_no_setup": "Note: Package setup is required (e.g., PYTHONPATH=src) before running modules.",
        "next_step_1": "Place your dataset at",
        "next_step_2": "Review and adjust metadata in",
        "next_step_3": "Define your features in",
        "next_step_4": "Run the pipeline",
        "next_step_4_data": "Step 1 (Data)",
        "next_step_4_train": "Step 2 (Train)",
        "next_step_4_eval": "Step 3 (Evaluate)",
        "next_step_guide": "Run the Project Guide (readiness check)",
        "next_step_workspace": "Interactive Learning Workspace (Visual-first)",
        "next_step_eda_first": "IMPORTANT: Run EDA before Advisor, Baseline, or Learning Notes",
        "next_step_advisor": "Dataset Advice (modeling suggestions)",
        "next_step_bandit": "Bandit Lab (adaptive decisions)",
        "next_step_monitor": "Monitoring/Drift (educational stub)",
        "next_step_demo": "Check the demo scenario and data dictionary in docs/demo-scenario.md",
        "summary_mlflow": "MLflow Tracking",
        "yes": "yes",
        "no": "no",
        "bandit_action_question": "1. What action should the system choose?",
        "bandit_action_label": "Action",
        "bandit_action_offer": "offer/product",
        "bandit_action_message": "message/channel",
        "bandit_action_recommendation": "recommendation",
        "bandit_action_custom": "custom",
        "bandit_reward_question": "2. What reward will be observed?",
        "bandit_reward_label": "Reward",
        "bandit_reward_click": "click",
        "bandit_reward_conversion": "conversion",
        "bandit_reward_acceptance": "acceptance",
        "bandit_reward_revenue": "revenue",
        "bandit_reward_custom": "custom metric",
        "bandit_context_question": "3. Is there user/event context?",
        "bandit_context_label": "Context",
        "bandit_context_simple": "simple bandit (no context)",
        "bandit_context_contextual": "contextual bandit (uses features)",
        "bandit_delay_question": "4. Is the reward immediate or delayed?",
        "bandit_delay_label": "Delay",
        "bandit_delay_immediate": "immediate",
        "bandit_delay_delayed": "delayed",
        "bandit_baseline_question": "5. What initial baseline should be used?",
        "bandit_baseline_label": "Baseline",
        "bandit_baseline_fixed": "fixed arm",
        "bandit_baseline_historical": "historical best arm",
        "bandit_baseline_random": "random",
        "bandit_baseline_custom": "custom",
    },
    "pt-BR": {
        "language_name": "Português do Brasil",
        "choose_language": "Escolha o idioma",
        "project_basics": "Informações básicas",
        "project_name": "Nome do projeto",
        "package_name": "Nome do pacote Python",
        "experience_mode": "Modo de Experiência",
        "mode_minimal": "Starter Mínimo (Minimal Starter)",
        "mode_guided": "Modo Aprendizado Guiado (Guided Learning)",
        "choose_task": "Tipo de Projeto (Tarefa de ML)",
        "task_generic": "estrutura genérica de ML",
        "task_supervised": "classificação/regressão",
        "task_unsupervised": "PCA/K-Means/agrupamento",
        "task_timeseries": "séries temporais/LSTM",
        "task_vision": "classificação de imagem/detecção",
        "task_bandit": "Multi-Armed Bandit / decisões adaptativas",
        "choose_option": "Escolha uma opção",
        "invalid_option": "Opção inválida.",
        "dataset_target": "Dataset e alvo (target)",
        "supervised_panel_title": "Aprendizado Supervisionado",
        "supervised_panel_text": "No aprendizado supervisionado, você precisa de uma coluna 'alvo' (o que deseja prever)\ne 'features' (os dados usados para fazer a previsão).",
        "unsupervised_panel_title": "Aprendizado Não Supervisionado",
        "unsupervised_panel_text": "O aprendizado não supervisionado encontra padrões nos dados sem uma coluna alvo específica.",
        "dataset_path": "Caminho do dataset",
        "target_column": "Nome da coluna alvo",
        "include_demo": "Incluir dataset de demonstração?",
        "problem_framing": "Definição do problema",
        "problem_framing_panel_title": "Definição do Problema",
        "problem_framing_panel_text": "Este assistente opcional ajuda a configurar o kit inicial para seus objetivos específicos.",
        "press_enter_defaults": "Pressione Enter para usar os padrões.",
        "goal_question": "1. Qual o objetivo principal?",
        "goal_label": "Objetivo",
        "goal_predict_category": "prever uma categoria",
        "goal_predict_number": "prever um número",
        "goal_group_records": "agrupar registros semelhantes",
        "goal_forecast_values": "prever valores futuros",
        "goal_work_images_text": "trabalhar com imagens/texto",
        "priority_question": "2. O que é mais importante?",
        "priority_label": "Prioridade",
        "priority_interpretability": "interpretabilidade",
        "priority_performance": "desempenho preditivo",
        "priority_speed": "velocidade/simplicidade",
        "priority_imbalanced": "lidar com classes desbalanceadas",
        "priority_learning": "aprendizado/experimentação",
        "error_cost_question": "3. Qual erro é mais caro?",
        "error_cost_label": "Custo do erro",
        "error_cost_fp": "falso positivo",
        "error_cost_fn": "falso negativo",
        "error_cost_both": "ambos similares",
        "error_cost_not_sure": "não tenho certeza",
        "size_question": "4. Tamanho esperado do dataset?",
        "size_label": "Tamanho",
        "size_small": "pequeno",
        "size_medium": "médio",
        "size_large": "grande",
        "size_not_sure": "não tenho certeza",
        "baseline_question": "5. Prefere um baseline simples primeiro?",
        "domain_note_question": "6. Alguma nota sobre o domínio? (opcional)",
        "environment": "Ambiente",
        "create_env_files": "Criar pyproject.toml e arquivos de ambiente?",
        "python_profile": "Perfil de Python",
        "profile_safe": "Python 3.12 (estável)",
        "profile_modern": "Python 3.14 (experimental/recente)",
        "ml_basics": "Incluir dependências básicas de ML (pandas, numpy, scikit-learn, matplotlib, seaborn)?",
        "torch_support": "Suporte a PyTorch",
        "torch_none": "nenhum",
        "torch_cpu": "cpu",
        "torch_cuda126": "cuda 12.6",
        "torch_cuda128": "cuda 12.8",
        "mlflow_tracking": "Habilitar rastreamento de experimentos com MLflow?",
        "optional_tools": "Ferramentas opcionais",
        "create_docs": "Criar arquivos de documentação?",
        "optional_files_templates": "Arquivos opcionais (templates):",
        "optional_profile": "Perfil de Templates Opcionais",
        "profile_minimal": "mínimo",
        "profile_recommended": "recomendado",
        "profile_full": "completo",
        "profile_custom": "personalizado",
        "include_eda": "Incluir suporte a EDA?",
        "include_preprocessing": "Incluir suporte a pré-processamento?",
        "include_metrics": "Incluir métricas customizadas?",
        "include_optimization": "Incluir estrutura de otimização?",
        "include_feature_measurement": "Incluir medição de features?",
        "include_visualization": "Incluir suporte a visualização?",
        "include_notebook_factory": "Incluir fábrica de notebooks?",
        "include_model_report": "Incluir template de relatório de modelo?",
        "include_experiment_log": "Incluir template de log de experimentos?",
        "include_advisor": "Incluir Dataset Advisor explicável?",
        "include_learning": "Incluir notas de aprendizado contextuais ao dataset?",
        "include_baseline_lab": "Incluir Baseline Lab educacional?",
        "include_bandit_lab": "Incluir Bandit Lab educacional (Multi-Armed Bandit)?",
        "include_monitoring": "Incluir stub de monitoramento/drift leve?",
        "include_synthetic_data": "Incluir Synthetic Data Lab configurável (para testes/estudo)?",
        "synthetic_panel_title": "Synthetic Data Lab",
        "synthetic_panel_text": "O Synthetic Data Lab gera datasets determinísticos para experimentação.\nDefinir 'activate_as_project_dataset' como true na configuração irá automaticamente\napontar seu projeto para usar os dados sintéticos gerados.",
        "dependency_note_title": "Nota de Dependência",
        "dependency_note_text": "O Dataset Advisor, Baseline Lab e Synthetic Lab requerem dependências básicas de ML (pandas, scikit-learn).",
        "enable_ml_basics": "Ativar dependências básicas de ML agora?",
        "output_location": "Local de saída",
        "dir_current": "Diretório atual",
        "dir_nested": "Nova pasta no diretório atual",
        "dir_sibling": "Pasta irmã (recomendado)",
        "dir_custom": "Caminho personalizado",
        "enter_custom_path": "Digite o caminho personalizado",
        "warn_inside_repo": "O diretório de saída selecionado está dentro do repositório do starter.",
        "continue_anyway": "Deseja continuar assim mesmo?",
        "overwrite_files": "Sobrescrever arquivos existentes em caso de conflito?",
        "final_summary": "Resumo final",
        "summary_project_name": "Nome do projeto",
        "summary_package_name": "Nome do pacote",
        "summary_task": "Tarefa de ML",
        "summary_dataset_path": "Caminho do dataset",
        "summary_target_column": "Coluna alvo",
        "summary_include_demo": "Incluir dataset de demo",
        "summary_python_version": "Versão do Python",
        "summary_experience_mode": "Modo de Experiência",
        "summary_torch_variant": "Variante do PyTorch",
        "summary_ml_basics": "Incluir ML básico",
        "summary_output_dir": "Diretório de saída",
        "summary_overwrite": "Sobrescrever arquivos",
        "create_project_files": "Criar arquivos do projeto?",
        "aborted": "Abortado.",
        "success_msg": "Starter-kit criado com sucesso!",
        "destination": "Destino",
        "next_steps": "Próximos passos",
        "next_step_cd": "Navegue para o diretório do projeto",
        "next_step_already_in": "Você já está no diretório do projeto.",
        "next_step_setup": "Configure o ambiente",
        "next_step_install": "Instale o pacote em modo editável",
        "next_step_no_setup": "Nota: A configuração do pacote é necessária (ex: PYTHONPATH=src) antes de executar os módulos.",
        "next_step_1": "Coloque seu dataset em",
        "next_step_2": "Revise e ajuste metadados em",
        "next_step_3": "Defina suas features em",
        "next_step_4": "Execute o pipeline",
        "next_step_4_data": "Passo 1 (Dados)",
        "next_step_4_train": "Passo 2 (Treino)",
        "next_step_4_eval": "Passo 3 (Avaliação)",
        "next_step_guide": "Execute o Guia do Projeto (valida prontidão)",
        "next_step_workspace": "Workspace de Aprendizado Interativo (Visual-first)",
        "next_step_eda_first": "IMPORTANTE: Execute a EDA antes do Advisor, Baseline ou Notas de Aprendizado",
        "next_step_advisor": "Conselhos sobre o Dataset (sugestões de modelagem)",
        "next_step_bandit": "Bandit Lab (decisões adaptativas)",
        "next_step_monitor": "Monitoramento/Drift (stub educacional)",
        "next_step_demo": "Consulte o cenário de demo e o dicionário de dados em docs/demo-scenario.md",
        "summary_mlflow": "Rastreamento MLflow",
        "yes": "sim",
        "no": "não",
        "bandit_action_question": "1. Qual ação o sistema deve escolher?",
        "bandit_action_label": "Ação",
        "bandit_action_offer": "oferta/produto",
        "bandit_action_message": "mensagem/canal",
        "bandit_action_recommendation": "recomendação",
        "bandit_action_custom": "personalizado",
        "bandit_reward_question": "2. Qual recompensa será observada?",
        "bandit_reward_label": "Recompensa",
        "bandit_reward_click": "clique",
        "bandit_reward_conversion": "conversão",
        "bandit_reward_acceptance": "aceitação",
        "bandit_reward_revenue": "receita",
        "bandit_reward_custom": "métrica personalizada",
        "bandit_context_question": "3. Existe contexto de usuário/evento?",
        "bandit_context_label": "Contexto",
        "bandit_context_simple": "bandit simples (sem contexto)",
        "bandit_context_contextual": "bandit contextual (usa features)",
        "bandit_delay_question": "4. A recompensa é imediata ou atrasada?",
        "bandit_delay_label": "Atraso",
        "bandit_delay_immediate": "imediata",
        "bandit_delay_delayed": "atrasada",
        "bandit_baseline_question": "5. Qual referência inicial deve ser usada?",
        "bandit_baseline_label": "Referência",
        "bandit_baseline_fixed": "braço fixo",
        "bandit_baseline_historical": "melhor braço histórico",
        "bandit_baseline_random": "aleatório",
        "bandit_baseline_custom": "personalizado",
    }
}

class UI:
    """Helper for terminal UI, colors, and sections."""
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BOLD = '\033[1m'
    END = '\033[0m'

    @staticmethod
    def use_color() -> bool:
        """Check if colors should be used."""
        if os.getenv("NO_COLOR"):
            return False
        # If we are in a test or piped, isatty() might be False.
        # But for tests we might want to see colors or not.
        if not sys.stdout.isatty():
            return False
        if os.getenv("TERM") == "dumb":
            return False
        return True

    @classmethod
    def color(cls, text: str, color_code: str) -> str:
        if cls.use_color():
            return f"{color_code}{text}{cls.END}"
        return text

    @classmethod
    def section(cls, title: str, number: int) -> None:
        print()
        header = f"--- {number}. {title} ---"
        print(cls.color(header, cls.BLUE + cls.BOLD))

    @classmethod
    def panel(cls, title: str, text: str) -> None:
        print()
        print(cls.color(f"[{title}]", cls.CYAN + cls.BOLD))
        for line in text.strip().split('\n'):
            print(f"  {line.strip()}")

    @classmethod
    def success(cls, text: str) -> None:
        print(cls.color(f"✔ {text}", cls.GREEN))

    @classmethod
    def warning(cls, text: str) -> None:
        print(cls.color(f"⚠ {text}", cls.YELLOW))


def ask(prompt: str, default: str | None = None) -> str:
    suffix = f" [{UI.color(default, UI.CYAN)}]" if default else ""
    full_prompt = f"{prompt}{suffix}: "
    print(full_prompt, end="", flush=True)
    value = input().strip()
    return value or (default or "")


def ask_yes_no(prompt: str, default: bool = True, lang: str = "en") -> bool:
    y_label = "Y" if default else "y"
    n_label = "n" if default else "N"

    if lang == "pt-BR":
        y_label = "S" if default else "s"

    default_label = f"{y_label}/{n_label}"
    colored_label = UI.color(default_label, UI.CYAN)
    full_prompt = f"{prompt} [{colored_label}]: "

    while True:
        print(full_prompt, end="", flush=True)
        value = input().strip().lower()

        if not value:
            return default

        if value in {"y", "yes"}:
            return True
        if value in {"n", "no"}:
            return False

        if lang == "pt-BR":
            if value in {"s", "sim"}:
                return True
            if value in {"não", "nao"}:
                return False

        t = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
        msg = t.get("invalid_option", "Invalid option.")
        print(msg)


def choose_numbered(
    prompt: str,
    options: list[tuple[str, str]],
    default_idx: int = 0,
    t: dict[str, str] | None = None,
    print_options: bool = True
) -> str:
    """Helper for numbered selection menus."""
    if print_options:
        print()
        for i, (_, label) in enumerate(options, 1):
            print(f"{i}. {label}")

    default_val = str(default_idx + 1)

    while True:
        choice = ask(prompt, default_val)

        # Check if it's a number
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(options):
                return options[idx][0]

        # Check if it's the exact value or exact label
        choice_lower = choice.lower()
        for val, label in options:
            if choice_lower == val.lower() or choice_lower == label.lower():
                return val

        msg = t["invalid_option"] if t and "invalid_option" in t else "Invalid option."
        print(msg)


def choose_language() -> str:
    options = [("en", "English"), ("pt-BR", "Português do Brasil")]
    return choose_numbered("Choose language / Escolha o idioma", options, default_idx=0)


def choose_task(t: dict[str, str]) -> str:
    options = [
        ("generic", f"generic       - {t['task_generic']}"),
        ("supervised", f"supervised    - {t['task_supervised']}"),
        ("unsupervised", f"unsupervised  - {t['task_unsupervised']}"),
        ("timeseries", f"timeseries    - {t['task_timeseries']}"),
        ("vision", f"vision        - {t['task_vision']}"),
        ("bandit", f"bandit        - {t['task_bandit']}"),
    ]
    print(f"\n{t['choose_task']}:")
    return choose_numbered(t['choose_option'], options, default_idx=1, t=t)


def choose_experience_mode(t: dict[str, str]) -> str:
    options = [
        ("minimal", f"minimal - {t['mode_minimal']}"),
        ("guided", f"guided  - {t['mode_guided']}"),
    ]
    print(f"\n{t['experience_mode']}:")
    return choose_numbered(t['choose_option'], options, default_idx=0, t=t)


def choose_python_profile(t: dict[str, str]) -> str:
    options = [
        ("3.12", f"safe   - {t['profile_safe']}"),
        ("3.14", f"modern - {t['profile_modern']}"),
    ]
    print(f"\n{t['python_profile']}:")
    return choose_numbered(t['choose_option'], options, default_idx=0, t=t)


def choose_torch_variant(t: dict[str, str]) -> str:
    options = [
        ("none", f"none     - {t['torch_none']}"),
        ("cpu", f"cpu      - {t['torch_cpu']}"),
        ("cu126", f"cuda 12.6  - {t['torch_cuda126']}"),
        ("cu128", f"cuda 12.8  - {t['torch_cuda128']}"),
    ]
    print(f"\n{t['torch_support']}:")
    return choose_numbered(t['choose_option'], options, default_idx=0, t=t)


def choose_optional_profile(t: dict[str, str], experience_mode: str = "minimal") -> str:
    options = [
        ("minimal", f"minimal     - {t['profile_minimal']}"),
        ("recommended", f"recommended - {t['profile_recommended']}"),
        ("full", f"full        - {t['profile_full']}"),
        ("custom", f"custom      - {t['profile_custom']}"),
    ]
    print(f"\n{t['optional_profile']}:")
    default_idx = 0 if experience_mode == "minimal" else 1
    return choose_numbered(t['choose_option'], options, default_idx=default_idx, t=t)


def get_options_by_profile(profile: str) -> dict[str, bool]:
    options = {
        "eda": False,
        "preprocessing": False,
        "metrics": False,
        "optimization": False,
        "feature_measurement": False,
        "visualization": False,
        "notebook_factory": False,
        "model_report": False,
        "experiment_log": False,
        "advisor": False,
        "learning": False,
        "baseline_lab": False,
        "bandit_lab": False,
        "monitoring": False,
        "synthetic_data": False,
    }

    if profile == "minimal":
        return options

    if profile == "recommended":
        options["eda"] = True
        options["preprocessing"] = True
        options["metrics"] = True
        options["visualization"] = True
        options["advisor"] = True
        options["learning"] = True
        options["baseline_lab"] = True
        options["monitoring"] = True
        options["synthetic_data"] = True
        return options

    if profile == "full":
        for key in options:
            options[key] = True
        return options

    return options


def run_problem_framing_wizard(task: str, t: dict[str, str], lang: str) -> dict[str, str]:
    UI.panel(t['problem_framing_panel_title'], t['problem_framing_panel_text'])
    print(t['press_enter_defaults'])

    if task == "bandit":
        # 1. Action?
        print(f"\n{t['bandit_action_question']}")
        action_options = [
            (t['bandit_action_offer'], t['bandit_action_offer']),
            (t['bandit_action_message'], t['bandit_action_message']),
            (t['bandit_action_recommendation'], t['bandit_action_recommendation']),
            ("custom", t['bandit_action_custom']),
        ]
        action = choose_numbered(t["bandit_action_label"], action_options, default_idx=0, t=t)
        if action == "custom":
            action = ask(t["bandit_action_label"], "")

        # 2. Reward?
        print(f"\n{t['bandit_reward_question']}")
        reward_options = [
            (t['bandit_reward_click'], t['bandit_reward_click']),
            (t['bandit_reward_conversion'], t['bandit_reward_conversion']),
            (t['bandit_reward_acceptance'], t['bandit_reward_acceptance']),
            (t['bandit_reward_revenue'], t['bandit_reward_revenue']),
            ("custom", t['bandit_reward_custom']),
        ]
        reward = choose_numbered(t["bandit_reward_label"], reward_options, default_idx=0, t=t)
        if reward == "custom":
            reward = ask(t["bandit_reward_label"], "")

        # 3. Context?
        print(f"\n{t['bandit_context_question']}")
        context_options = [
            (t['bandit_context_simple'], t['bandit_context_simple']),
            (t['bandit_context_contextual'], t['bandit_context_contextual']),
        ]
        context = choose_numbered(t["bandit_context_label"], context_options, default_idx=1, t=t)

        # 4. Delay?
        print(f"\n{t['bandit_delay_question']}")
        delay_options = [
            (t['bandit_delay_immediate'], t['bandit_delay_immediate']),
            (t['bandit_delay_delayed'], t['bandit_delay_delayed']),
        ]
        delay = choose_numbered(t["bandit_delay_label"], delay_options, default_idx=0, t=t)

        # 5. Baseline?
        print(f"\n{t['bandit_baseline_question']}")
        baseline_options = [
            (t['bandit_baseline_fixed'], t['bandit_baseline_fixed']),
            (t['bandit_baseline_historical'], t['bandit_baseline_historical']),
            (t['bandit_baseline_random'], t['bandit_baseline_random']),
            ("custom", t['bandit_baseline_custom']),
        ]
        baseline = choose_numbered(t["bandit_baseline_label"], baseline_options, default_idx=2, t=t)
        if baseline == "custom":
            baseline = ask(t["bandit_baseline_label"], "")

        # 6. Any domain note?
        domain_note = ask(f"\n{t['domain_note_question']}", "")

        return {
            "goal": t["task_bandit"],
            "bandit_action": action,
            "bandit_reward": reward,
            "bandit_context": context,
            "bandit_delay": delay,
            "bandit_baseline": baseline,
            "domain_note": domain_note,
            "language": lang
        }

    # 1. Main goal?
    print(f"\n{t['goal_question']}")
    goal_options = [
        (t["goal_predict_category"], t["goal_predict_category"]),
        (t["goal_predict_number"], t["goal_predict_number"]),
        (t["goal_group_records"], t["goal_group_records"]),
        (t["goal_forecast_values"], t["goal_forecast_values"]),
        (t["goal_work_images_text"], t["goal_work_images_text"]),
    ]
    goals_map = {
        "supervised": t["goal_predict_category"],
        "unsupervised": t["goal_group_records"],
        "timeseries": t["goal_forecast_values"],
        "vision": t["goal_work_images_text"],
        "bandit": t["task_bandit"],
        "generic": t["goal_predict_category"]
    }
    default_goal = goals_map.get(task, t["goal_predict_category"])
    default_idx = 0
    for i, (val, _) in enumerate(goal_options):
        if val == default_goal:
            default_idx = i
            break
    goal = choose_numbered(t["goal_label"], goal_options, default_idx=default_idx, t=t)

    # 2. What matters most?
    print(f"\n{t['priority_question']}")
    priority_options = [
        (t['priority_interpretability'], t['priority_interpretability']),
        (t['priority_performance'], t['priority_performance']),
        (t['priority_speed'], t['priority_speed']),
        (t['priority_imbalanced'], t['priority_imbalanced']),
        (t['priority_learning'], t['priority_learning']),
    ]
    priority = choose_numbered(t["priority_label"], priority_options, default_idx=4, t=t)

    # 3. Which error is more costly?
    print(f"\n{t['error_cost_question']}")
    error_options = [
        (t['error_cost_fp'], t['error_cost_fp']),
        (t['error_cost_fn'], t['error_cost_fn']),
        (t['error_cost_both'], t['error_cost_both']),
        (t['error_cost_not_sure'], t['error_cost_not_sure']),
    ]
    error_cost = choose_numbered(t["error_cost_label"], error_options, default_idx=3, t=t)

    # 4. Expected dataset size?
    print(f"\n{t['size_question']}")
    size_options = [
        (t['size_small'], t['size_small']),
        (t['size_medium'], t['size_medium']),
        (t['size_large'], t['size_large']),
        (t['size_not_sure'], t['size_not_sure']),
    ]
    dataset_size = choose_numbered(t["size_label"], size_options, default_idx=3, t=t)

    # 5. Prefer simple baseline first?
    prefer_baseline = "yes" if ask_yes_no(f"\n{t['baseline_question']}", True, lang=lang) else "no"

    # 6. Any domain note?
    domain_note = ask(f"\n{t['domain_note_question']}", "")

    return {
        "goal": goal,
        "priority": priority,
        "error_cost": error_cost,
        "dataset_size": dataset_size,
        "prefer_baseline": prefer_baseline,
        "domain_note": domain_note,
        "language": lang
    }


def normalize_package_name(value: str) -> str:
    value = value.strip().lower().replace("-", "_").replace(" ", "_")
    value = re.sub(r"[^a-z0-9_]", "", value)
    value = re.sub(r"_+", "_", value).strip("_")

    if not value:
        value = "ml_project"

    if value[0].isdigit():
        value = f"ml_{value}"

    return value


def print_summary(root: Path, values: dict[str, str], t: dict[str, str], include_pyproject: bool) -> None:
    UI.success(t["success_msg"])
    print(f"{t['destination']}: {UI.color(str(root.resolve()), UI.CYAN)}")
    print()

    current_dir = Path.cwd().resolve()
    target_dir = root.resolve()
    steps = []

    # 1. Navigation
    if target_dir == current_dir:
        steps.append(f"1. {t['next_step_already_in']}")
    else:
        try:
            rel_path = target_dir.relative_to(current_dir)
            steps.append(f"1. {t['next_step_cd']}: cd {rel_path}")
        except ValueError:
            steps.append(f"1. {t['next_step_cd']}: cd {target_dir}")

    # 2. Environment/Package Setup
    if include_pyproject:
        python_version = values.get("PYTHON_VERSION", "3.12")
        steps.append(f"2. {t['next_step_setup']}:")
        if sys.platform == "win32":
            steps.append(f"   py -{python_version} -m venv .venv")
            steps.append("   .venv\\Scripts\\activate")
        else:
            steps.append(f"   python{python_version} -m venv .venv")
            steps.append("   source .venv/bin/activate")
        steps.append("   python --version")
        steps.append("   pip install -r requirements.txt")
        steps.append(f"3. {t['next_step_install']}:")
        steps.append("   pip install -e .")
        next_idx = 4
    else:
        steps.append(f"2. {t['next_step_no_setup']}")
        next_idx = 3

    # 3. Data/Config
    steps.append(f"{next_idx}. {t['next_step_1']}: {values['DATASET_PATH']}")
    if values.get("INCLUDE_DEMO") == "true":
        steps.append(f"   - {t['next_step_demo']}")

    steps.append(f"{next_idx+1}. {t['next_step_2']}: configs/config.json")
    steps.append(f"{next_idx+2}. {t['next_step_3']}: src/{values['PACKAGE_NAME']}/features.py")
    steps.append(f"{next_idx+3}. {t['next_step_guide']}: python -m {values['PACKAGE_NAME']}.lab check")

    # 5. Pipeline or Workspace
    run_idx = next_idx + 4
    pkg = values['PACKAGE_NAME']
    if values.get("LEARNING_MODE") == "guided":
        steps.append(f"{run_idx}. {t['next_step_workspace']}:")
        steps.append(f"   python -m {pkg}.lab workspace")
        steps.append(f"   ({t['next_step_eda_first']})")

        steps.append(f"\n   {t['next_step_4']} (CLI):")
        if values.get("GENERATE_EDA") == "true":
            steps.append(f"   - {t['next_step_4_data']}:     python -m {pkg}.lab eda")
        if values.get("GENERATE_ADVISOR") == "true":
            steps.append(f"   - {t['next_step_advisor']}:   python -m {pkg}.lab advisor")
        if values.get("GENERATE_BANDIT") == "true":
            steps.append(f"   - {t['next_step_bandit']}:   python -m {pkg}.lab bandit")
        if values.get("GENERATE_SYNTHETIC") == "true":
            steps.append(f"   - Synthetic Data:  python -m {pkg}.lab synthetic")
        steps.append(f"   - {t['next_step_4_train']}:    python -m {pkg}.lab train")
        steps.append(f"   - {t['next_step_4_eval']}: python -m {pkg}.lab evaluate")
        if values.get("GENERATE_MONITOR") == "true":
            steps.append(f"   - {t['next_step_monitor']}: python -m {pkg}.lab monitor")
    else:
        steps.append(f"{run_idx}. {t['next_step_4']}:")
        if values.get("GENERATE_EDA") == "true":
            steps.append(f"   - {t['next_step_4_data']}:     python -m {pkg}.lab eda")
        steps.append(f"   - {t['next_step_4_train']}:    python -m {pkg}.lab train")
        steps.append(f"   - {t['next_step_4_eval']}: python -m {pkg}.lab evaluate")

        if values.get("GENERATE_ADVISOR") == "true":
            steps.append(f"   - {t['next_step_advisor']}:   python -m {pkg}.lab advisor")
        if values.get("GENERATE_BANDIT") == "true":
            steps.append(f"   - {t['next_step_bandit']}:   python -m {pkg}.lab bandit")
        if values.get("GENERATE_SYNTHETIC") == "true":
            steps.append(f"   - Synthetic Data:  python -m {pkg}.lab synthetic")
        if values.get("GENERATE_MONITOR") == "true":
            steps.append(f"   - {t['next_step_monitor']}: python -m {pkg}.lab monitor")

    UI.panel(t["next_steps"], "\n".join(steps))


def main() -> None:
    print(UI.color("ML Starter Kit Builder", UI.BLUE + UI.BOLD))
    print(UI.color("======================", UI.BLUE + UI.BOLD))

    lang = choose_language()
    t = TRANSLATIONS[lang]

    UI.section(t["project_basics"], 1)
    default_project = Path.cwd().name
    project_name = ask(t["project_name"], default_project)
    package_name = normalize_package_name(
        ask(t["package_name"], normalize_package_name(project_name))
    )
    task = choose_task(t)
    experience_mode = choose_experience_mode(t)
    preset = "none"

    UI.section(t["dataset_target"], 2)
    if task == "supervised":
        UI.panel(t["supervised_panel_title"], t["supervised_panel_text"])
    elif task == "unsupervised":
        UI.panel(t["unsupervised_panel_title"], t["unsupervised_panel_text"])

    dataset_path = ask(t["dataset_path"], "data/raw/dataset.csv")

    if task == "unsupervised":
        target_column = ""
    elif task == "bandit":
        target_column = ask(t["target_column"], "reward")
    else:
        target_column = ask(t["target_column"], "target")

    include_demo = ask_yes_no(t["include_demo"], False, lang=lang)

    UI.section(t["problem_framing"], 3)
    problem_profile = run_problem_framing_wizard(task, t, lang)

    UI.section(t["environment"], 4)
    include_pyproject = ask_yes_no(t["create_env_files"], True, lang=lang)

    python_version = "3.11"
    torch_variant = "none"
    include_ml_basics = False
    include_mlflow = False

    if include_pyproject:
        python_version = choose_python_profile(t)
        if experience_mode == "guided":
            include_ml_basics = True
        else:
            include_ml_basics = ask_yes_no(t["ml_basics"], False, lang=lang)
        include_mlflow = ask_yes_no(t["mlflow_tracking"], False, lang=lang)
        torch_variant = choose_torch_variant(t)

    UI.section(t["optional_tools"], 5)
    if experience_mode == "guided":
        include_docs = True
    else:
        default_docs = (experience_mode != "minimal")
        include_docs = ask_yes_no(t["create_docs"], default_docs, lang=lang)

    print(f"\n{t['optional_files_templates']}")

    if experience_mode == "guided":
        profile = "recommended"
    else:
        profile = choose_optional_profile(t, experience_mode=experience_mode)

    if profile == "custom":
        optional_options = {
            "eda": ask_yes_no(t["include_eda"], False, lang=lang),
            "preprocessing": ask_yes_no(t["include_preprocessing"], False, lang=lang),
            "metrics": ask_yes_no(t["include_metrics"], False, lang=lang),
            "optimization": ask_yes_no(t["include_optimization"], False, lang=lang),
            "feature_measurement": ask_yes_no(t["include_feature_measurement"], False, lang=lang),
            "visualization": ask_yes_no(t["include_visualization"], False, lang=lang),
            "notebook_factory": ask_yes_no(t["include_notebook_factory"], False, lang=lang),
            "model_report": ask_yes_no(t["include_model_report"], False, lang=lang),
            "experiment_log": ask_yes_no(t["include_experiment_log"], False, lang=lang),
            "advisor": ask_yes_no(t["include_advisor"], False, lang=lang),
            "learning": ask_yes_no(t["include_learning"], False, lang=lang),
            "baseline_lab": ask_yes_no(t["include_baseline_lab"], False, lang=lang),
            "bandit_lab": ask_yes_no(t["include_bandit_lab"], False, lang=lang),
            "monitoring": ask_yes_no(t["include_monitoring"], False, lang=lang),
            "synthetic_data": ask_yes_no(t["include_synthetic_data"], False, lang=lang),
        }
    else:
        optional_options = get_options_by_profile(profile)

    if experience_mode == "guided":
        optional_options["eda"] = True
        optional_options["advisor"] = True
        optional_options["learning"] = True
        optional_options["baseline_lab"] = True
        optional_options["monitoring"] = True
        optional_options["synthetic_data"] = True
        optional_options["learning_workspace"] = True

    # P1-D: Gate Bandit Lab.
    # Included only for specific bandit tasks or if explicitly selected in profile.
    is_bandit_task = (task == "bandit" or task == "adaptive")
    if is_bandit_task:
         optional_options["bandit_lab"] = True
         # When task is bandit, we also want the docs and related assets enabled
         # by forcing the GENERATE_BANDIT flag in values later.

    # If bandit lab is enabled, we also need the workspace to view it.
    if optional_options.get("bandit_lab"):
        optional_options["learning_workspace"] = True

    # Explain Synthetic Lab if selected
    if optional_options.get("synthetic_data"):
        UI.panel(t["synthetic_panel_title"], t["synthetic_panel_text"])

    needs_ml_basics = (
        optional_options.get("advisor") or
        optional_options.get("baseline_lab") or
        optional_options.get("synthetic_data")
    )
    if needs_ml_basics and not include_ml_basics:
        if experience_mode != "guided":
            UI.panel(t["dependency_note_title"], t["dependency_note_text"])
            if ask_yes_no(t["enable_ml_basics"], True, lang=lang):
                include_ml_basics = True
        else:
            include_ml_basics = True

    UI.section(t["output_location"], 6)
    sibling_dir = (STARTER_ROOT.parent / package_name).resolve()
    current_dir = Path.cwd().resolve()
    nested_dir = (current_dir / package_name).resolve()

    output_options = [
        ("current", f"{t['dir_current']}: {current_dir}"),
        ("nested", f"{t['dir_nested']}: {nested_dir}"),
        ("sibling", f"{t['dir_sibling']}: {sibling_dir}"),
        ("custom", t["dir_custom"]),
    ]

    while True:
        choice = choose_numbered(t["choose_option"], output_options, default_idx=2, t=t)

        if choice == "current":
            output_dir = current_dir
        elif choice == "nested":
            output_dir = nested_dir
        elif choice == "sibling":
            output_dir = sibling_dir
        elif choice == "custom":
            output_dir = Path(ask(t["enter_custom_path"])).resolve()

        is_inside = False
        try:
            if output_dir == STARTER_ROOT or output_dir.is_relative_to(STARTER_ROOT):
                is_inside = True
        except (ValueError, AttributeError):
            is_inside = False

        if is_inside:
            UI.warning(t["warn_inside_repo"])
            if ask_yes_no(t["continue_anyway"], default=False, lang=lang):
                break
        else:
            break

    force = ask_yes_no(t["overwrite_files"], False, lang=lang)

    python_requires = f">={python_version}"
    if python_version == "3.12":
        python_requires = ">=3.12,<3.13"
    elif python_version == "3.14":
        python_requires = ">=3.14,<3.15"

    advisor_cmd = f"python -m {package_name}.advisor" if optional_options.get("advisor") else ""

    demo_subtype = task
    if task == "supervised":
        goal_lower = problem_profile.get("goal", "").lower()
        # The Problem Framing Wizard might use translated goals.
        # We need to check both English and Portuguese identifiers.
        if any(keyword in goal_lower for keyword in ["number", "número", "2"]):
            demo_subtype = "regression"
        else:
            demo_subtype = "classification"

    values = {
        "PROJECT_NAME": project_name,
        "PACKAGE_NAME": package_name,
        "TASK": task,
        "DEMO_SUBTYPE": demo_subtype,
        "PRESET": preset,
        "DATASET_PATH": dataset_path,
        "TARGET_COLUMN": target_column,
        "INCLUDE_DEMO": "true" if include_demo else "false",
        "PYTHON_REQUIRES": python_requires,
        "PYTHON_VERSION": python_version,
        "ADVISOR_COMMAND": advisor_cmd,
        "LANGUAGE": lang,
        "ENABLE_MLFLOW": "true" if include_mlflow else "false",
        "LEARNING_ENABLED": "true" if experience_mode == "guided" else "false",
        "LEARNING_MODE": experience_mode,
        "GENERATE_EDA": "true" if optional_options.get("eda") else "false",
        "GENERATE_ADVISOR": "true" if optional_options.get("advisor") else "false",
        "GENERATE_LEARNING": "true" if optional_options.get("learning") else "false",
        "GENERATE_BASELINE": "true" if optional_options.get("baseline_lab") else "false",
        "GENERATE_BANDIT": "true" if optional_options.get("bandit_lab") else "false",
        "GENERATE_MONITOR": "true" if optional_options.get("monitoring") else "false",
        "GENERATE_SYNTHETIC": "true" if optional_options.get("synthetic_data") else "false",
    }

    UI.section(t["final_summary"], 7)
    print(f"{t['summary_project_name']}:      {values['PROJECT_NAME']}")
    print(f"{t['summary_package_name']}:      {values['PACKAGE_NAME']}")
    print(f"{t['summary_task']}:           {values['TASK']}")
    print(f"{t['summary_experience_mode']}:   {experience_mode}")
    print(f"{t['summary_dataset_path']}:      {values['DATASET_PATH']}")
    if target_column:
        print(f"{t['summary_target_column']}:     {values['TARGET_COLUMN']}")
    print(f"{t['summary_include_demo']}:      {t['yes'] if include_demo else t['no']}")
    print(f"{t['summary_python_version']}:    {python_version}")
    print(f"{t['summary_torch_variant']}:   {torch_variant}")
    print(f"{t['summary_ml_basics']}: {t['yes'] if include_ml_basics else t['no']}")
    print(f"{t['summary_mlflow']}:       {t['yes'] if include_mlflow else t['no']}")
    print(f"{t['summary_output_dir']}:  {output_dir}")
    print(f"{t['summary_overwrite']}:   {t['yes'] if force else t['no']}")

    print()
    if not ask_yes_no(t["create_project_files"], True, lang=lang):
        print(t["aborted"])
        return

    create_dirs(output_dir, package_name, preset, include_docs)
    create_config(output_dir, values, force=force, problem_profile=problem_profile)
    create_problem_profile(output_dir, problem_profile, force=force)
    create_readme(output_dir, values, force=force)
    create_package_files(output_dir, values, force=force)
    create_optional_files(output_dir, package_name, values, optional_options, force=force)
    create_tests(output_dir, values, force=force)
    create_notebook_placeholder(output_dir, values, force=force)
    create_demo_data(output_dir, values, problem_profile, force=force)

    if include_docs:
        create_docs(output_dir, values, force=force)

    if include_pyproject:
        create_pyproject(output_dir, values, force=force)
        create_env_files(
            output_dir,
            values,
            include_ml_basics,
            torch_variant,
            include_mlflow,
            force=force
        )

    print_summary(output_dir, values, t, include_pyproject)
