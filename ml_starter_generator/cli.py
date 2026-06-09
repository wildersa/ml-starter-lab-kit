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
        "dependency_note_title": "Dependency Note",
        "dependency_note_text": "Dataset Advisor and Baseline Lab require basic ML dependencies (pandas, scikit-learn).",
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
        "next_step_demo": "Check the demo scenario and data dictionary in docs/demo-scenario.md",
        "summary_mlflow": "MLflow Tracking",
        "yes": "yes",
        "no": "no",
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
        "dependency_note_title": "Nota de Dependência",
        "dependency_note_text": "O Dataset Advisor e o Baseline Lab requerem dependências básicas de ML (pandas, scikit-learn).",
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
        "next_step_demo": "Consulte o cenário de demo e o dicionário de dados em docs/demo-scenario.md",
        "summary_mlflow": "Rastreamento MLflow",
        "yes": "sim",
        "no": "não",
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
    print(full_prompt, end="", flush=True)
    value = input().strip().lower()

    if not value:
        return default

    if lang == "pt-BR":
        return value in {"s", "sim", "y", "yes"}

    return value in {"y", "yes"}


def choose_language() -> str:
    print()
    print("1. English")
    print("2. Português do Brasil")

    while True:
        choice = ask("Choose language / Escolha o idioma", "1")
        if choice == "1" or choice.lower() == "en":
            return "en"
        if choice == "2" or choice.lower() == "pt-br":
            return "pt-BR"
        print("Invalid option / Opção inválida.")


def choose_task(t: dict[str, str]) -> str:
    print()
    print(f"{t['choose_task']}:")
    print(f"1. generic       - {t['task_generic']}")
    print(f"2. supervised    - {t['task_supervised']}")
    print(f"3. unsupervised  - {t['task_unsupervised']}")
    print(f"4. timeseries    - {t['task_timeseries']}")
    print(f"5. vision        - {t['task_vision']}")

    while True:
        choice = ask(t['choose_option'], "2")
        if choice in TASKS:
            return TASKS[choice]
        if choice in TASKS.values():
            return choice
        print(t['invalid_option'])


def choose_experience_mode(t: dict[str, str]) -> str:
    print()
    print(f"{t['experience_mode']}:")
    print(f"1. minimal - {t['mode_minimal']}")
    print(f"2. guided  - {t['mode_guided']}")

    while True:
        choice = ask(t['choose_option'], "1")
        if choice == "1" or choice == "minimal":
            return "minimal"
        if choice == "2" or choice == "guided":
            return "guided"
        print(t['invalid_option'])


def choose_python_profile(t: dict[str, str]) -> str:
    print()
    print(f"{t['python_profile']}:")
    print(f"1. safe   - {t['profile_safe']}")
    print(f"2. modern - {t['profile_modern']}")

    while True:
        choice = ask(t['choose_option'], "1")
        if choice == "1" or choice == "safe":
            return "3.12"
        if choice == "2" or choice == "modern":
            return "3.14"
        print(t['invalid_option'])


def choose_torch_variant(t: dict[str, str]) -> str:
    print()
    print(f"{t['torch_support']}:")
    print(f"1. none     - {t['torch_none']}")
    print(f"2. cpu      - {t['torch_cpu']}")
    print(f"3. cuda126  - {t['torch_cuda126']}")
    print(f"4. cuda128  - {t['torch_cuda128']}")

    mapping = {
        "1": "none",
        "2": "cpu",
        "3": "cu126",
        "4": "cu128"
    }

    while True:
        choice = ask(t['choose_option'], "1")
        if choice in mapping:
            return mapping[choice]
        if choice in mapping.values():
            return choice
        print(t['invalid_option'])


def choose_optional_profile(t: dict[str, str], experience_mode: str = "minimal") -> str:
    print()
    print(f"{t['optional_profile']}:")
    print(f"1. minimal     - {t['profile_minimal']}")
    print(f"2. recommended - {t['profile_recommended']}")
    print(f"3. full        - {t['profile_full']}")
    print(f"4. custom      - {t['profile_custom']}")

    default_choice = "1" if experience_mode == "minimal" else "2"

    while True:
        choice = ask(t['choose_option'], default_choice)
        if choice in {"1", "2", "3", "4"}:
            mapping = {"1": "minimal", "2": "recommended", "3": "full", "4": "custom"}
            return mapping[choice]
        if choice in {"minimal", "recommended", "full", "custom"}:
            return choice
        print(t['invalid_option'])


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
        return options

    if profile == "full":
        for key in options:
            options[key] = True
        return options

    return options


def run_problem_framing_wizard(task: str, t: dict[str, str], lang: str) -> dict[str, str]:
    UI.panel(t['problem_framing_panel_title'], t['problem_framing_panel_text'])
    print(t['press_enter_defaults'])

    # 1. Main goal?
    print(f"\n{t['goal_question']}")
    goals = {
        "supervised": t["goal_predict_category"],
        "unsupervised": t["goal_group_records"],
        "timeseries": t["goal_forecast_values"],
        "vision": t["goal_work_images_text"],
        "generic": t["goal_predict_category"]
    }
    default_goal = goals.get(task, t["goal_predict_category"])
    print(f"   - {t['goal_predict_category']}")
    print(f"   - {t['goal_predict_number']}")
    print(f"   - {t['goal_group_records']}")
    print(f"   - {t['goal_forecast_values']}")
    print(f"   - {t['goal_work_images_text']}")
    goal = ask(t["goal_label"], default_goal)

    # 2. What matters most?
    print(f"\n{t['priority_question']}")
    print(f"   - {t['priority_interpretability']}")
    print(f"   - {t['priority_performance']}")
    print(f"   - {t['priority_speed']}")
    print(f"   - {t['priority_imbalanced']}")
    print(f"   - {t['priority_learning']}")
    priority = ask(t["priority_label"], t["priority_learning"])

    # 3. Which error is more costly?
    print(f"\n{t['error_cost_question']}")
    print(f"   - {t['error_cost_fp']}")
    print(f"   - {t['error_cost_fn']}")
    print(f"   - {t['error_cost_both']}")
    print(f"   - {t['error_cost_not_sure']}")
    error_cost = ask(t["error_cost_label"], t["error_cost_not_sure"])

    # 4. Expected dataset size?
    print(f"\n{t['size_question']}")
    print(f"   - {t['size_small']}")
    print(f"   - {t['size_medium']}")
    print(f"   - {t['size_large']}")
    print(f"   - {t['size_not_sure']}")
    dataset_size = ask(t["size_label"], t["size_not_sure"])

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
        steps.append(f"2. {t['next_step_setup']}:")
        steps.append("   python -m venv .venv")
        if sys.platform == "win32":
            steps.append("   .venv\\Scripts\\activate")
        else:
            steps.append("   source .venv/bin/activate")
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
    if values.get("LEARNING_MODE") == "guided":
        steps.append(f"{run_idx}. {t['next_step_workspace']}:")
        steps.append(f"   python -m {values['PACKAGE_NAME']}.lab workspace")
        steps.append(f"   ({t['next_step_eda_first']})")

        steps.append(f"\n   {t['next_step_4']} (CLI):")
        steps.append(f"   - {t['next_step_4_data']}:     python -m {values['PACKAGE_NAME']}.lab eda")
        steps.append(f"   - {t['next_step_advisor']}:   python -m {values['PACKAGE_NAME']}.lab advisor")
        steps.append(f"   - {t['next_step_4_train']}:    python -m {values['PACKAGE_NAME']}.lab train")
        steps.append(f"   - {t['next_step_4_eval']}: python -m {values['PACKAGE_NAME']}.lab evaluate")
    else:
        steps.append(f"{run_idx}. {t['next_step_4']}:")
        steps.append(f"   - {t['next_step_4_data']}:     python -m {values['PACKAGE_NAME']}.lab eda")
        steps.append(f"   - {t['next_step_4_train']}:    python -m {values['PACKAGE_NAME']}.lab train")
        steps.append(f"   - {t['next_step_4_eval']}: python -m {values['PACKAGE_NAME']}.lab evaluate")

        if values.get("ADVISOR_COMMAND"):
            steps.append(f"   - {t['next_step_advisor']}:   python -m {values['PACKAGE_NAME']}.lab advisor")

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
        }
    else:
        optional_options = get_options_by_profile(profile)

    if experience_mode == "guided":
        optional_options["eda"] = True
        optional_options["advisor"] = True
        optional_options["learning"] = True
        optional_options["baseline_lab"] = True
        optional_options["learning_workspace"] = True

    needs_ml_basics = (optional_options.get("advisor") or optional_options.get("baseline_lab"))
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

    print(f"1. {t['dir_current']}: {current_dir}")
    print(f"2. {t['dir_nested']}: {nested_dir}")
    print(f"3. {t['dir_sibling']}: {sibling_dir}")
    print(f"4. {t['dir_custom']}")

    while True:
        choice = ask(t["choose_option"], "3")
        if choice == "1":
            output_dir = current_dir
        elif choice == "2":
            output_dir = nested_dir
        elif choice == "3":
            output_dir = sibling_dir
        elif choice == "4":
            output_dir = Path(ask(t["enter_custom_path"])).resolve()
        else:
            print(t["invalid_option"])
            continue

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
        "ADVISOR_COMMAND": advisor_cmd,
        "LANGUAGE": lang,
        "ENABLE_MLFLOW": "true" if include_mlflow else "false",
        "LEARNING_ENABLED": "true" if experience_mode == "guided" else "false",
        "LEARNING_MODE": experience_mode,
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
