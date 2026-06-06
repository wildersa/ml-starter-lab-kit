from __future__ import annotations

import re
from pathlib import Path
from .constants import STARTER_ROOT, TASKS
from .config import create_config, create_problem_profile
from .scaffold import (
    create_dirs,
    create_readme,
    create_package_files,
    create_optional_files,
    create_tests,
    create_notebook_placeholder,
    create_docs,
    create_pyproject,
    create_env_files,
)

def ask(prompt: str, default: str | None = None) -> str:
    suffix = f" [{default}]" if default else ""
    full_prompt = f"{prompt}{suffix}: "
    print(full_prompt, end="", flush=True)
    value = input().strip()
    return value or (default or "")


TRANSLATIONS = {
    "en": {
        "project_type": "Project Type (ML Task):",
        "choose_option": "Choose an option",
        "invalid_option": "Invalid option.",
        "python_profile": "Python Profile:",
        "pytorch_support": "PyTorch Support:",
        "optional_profile": "Optional Template Profile:",
        "problem_framing_title": "Problem Framing Wizard (Optional)",
        "press_enter_defaults": "Press Enter to use defaults.",
        "goal_q": "1. Main goal?",
        "priority_q": "2. What matters most?",
        "error_cost_q": "3. Which error is more costly?",
        "size_q": "4. Expected dataset size?",
        "baseline_q": "5. Prefer simple baseline first?",
        "domain_note_q": "6. Any domain note? (optional)",
        "project_name": "Project name",
        "package_name_q": "Python package name",
        "dataset_path_q": "Dataset path",
        "target_column_q": "Target column name",
        "output_dir_q": "Directory to create the structure",
        "warning_inside_repo": "WARNING: The target directory is inside the starter kit repository.",
        "continue_anyway": "Do you want to continue anyway?",
        "create_docs_q": "Create documentation files?",
        "create_env_q": "Create pyproject.toml and environment files?",
        "include_ml_basics_q": "Include basic ML dependencies (pandas, numpy, scikit-learn, matplotlib, seaborn)?",
        "optional_files_title": "Optional files (templates):",
        "overwrite_q": "Overwrite existing files if there is a conflict?",
        "summary_title": "Starter-kit created.",
        "summary_dest": "Destination",
        "summary_project": "Project",
        "summary_package": "Package",
        "summary_type": "Type",
        "next_steps_title": "Next steps:",
        "step_config": "Adjust configs/config.json",
        "step_data": "Place your dataset in data/raw/",
        "step_features": "Edit src/{}/features.py",
        "step_run": "Run:",
        "advisor_note": "NOTE: Dataset Advisor requires basic ML dependencies (pandas, scikit-learn).",
        "enable_ml_now": "Enable basic ML dependencies now?",
        "goal_predict_category": "predict a category",
        "goal_predict_number": "predict a number",
        "goal_group_records": "group similar records",
        "goal_forecast_values": "forecast future values",
        "goal_work_images": "work with images/text",
        "priority_interpretability": "interpretability",
        "priority_performance": "predictive performance",
        "priority_simplicity": "speed/simplicity",
        "priority_imbalanced": "handling imbalanced classes",
        "priority_learning": "learning/experimentation",
        "error_fp": "false positive",
        "error_fn": "false negative",
        "error_both": "both similar",
        "error_not_sure": "not sure",
        "size_small": "small",
        "size_medium": "medium",
        "size_large": "large",
        "size_not_sure": "not sure",
        "opt_eda": "Include EDA support?",
        "opt_preprocessing": "Include preprocessing support?",
        "opt_metrics": "Include custom metrics?",
        "opt_optimization": "Include optimization scaffolding?",
        "opt_features": "Include feature measurement?",
        "opt_visualization": "Include visualization support?",
        "opt_notebook": "Include notebook factory?",
        "opt_report": "Include model report template?",
        "opt_log": "Include experiment log template?",
        "opt_advisor": "Include explainable Dataset Advisor?",
    },
    "pt-BR": {
        "project_type": "Tipo de Projeto (Tarefa de ML):",
        "choose_option": "Escolha uma opção",
        "invalid_option": "Opção inválida.",
        "python_profile": "Perfil do Python:",
        "pytorch_support": "Suporte ao PyTorch:",
        "optional_profile": "Perfil de Templates Opcionais:",
        "problem_framing_title": "Assistente de Definição do Problema (Opcional)",
        "press_enter_defaults": "Pressione Enter para usar os padrões.",
        "goal_q": "1. Objetivo principal?",
        "priority_q": "2. O que é mais importante?",
        "error_cost_q": "3. Qual erro é mais caro?",
        "size_q": "4. Tamanho esperado do dataset?",
        "baseline_q": "5. Prefere um baseline simples primeiro?",
        "domain_note_q": "6. Alguma nota de domínio? (opcional)",
        "project_name": "Nome do projeto",
        "package_name_q": "Nome do pacote Python",
        "dataset_path_q": "Caminho do dataset",
        "target_column_q": "Nome da coluna alvo",
        "output_dir_q": "Diretório para criar a estrutura",
        "warning_inside_repo": "AVISO: O diretório de destino está dentro do repositório do starter kit.",
        "continue_anyway": "Deseja continuar de qualquer forma?",
        "create_docs_q": "Criar arquivos de documentação?",
        "create_env_q": "Criar pyproject.toml e arquivos de ambiente?",
        "include_ml_basics_q": "Incluir dependências básicas de ML (pandas, numpy, scikit-learn, matplotlib, seaborn)?",
        "optional_files_title": "Arquivos opcionais (templates):",
        "overwrite_q": "Sobrescrever arquivos existentes se houver conflito?",
        "summary_title": "Starter-kit criado.",
        "summary_dest": "Destino",
        "summary_project": "Projeto",
        "summary_package": "Pacote",
        "summary_type": "Tipo",
        "next_steps_title": "Próximos passos:",
        "step_config": "Ajuste configs/config.json",
        "step_data": "Coloque seu dataset em data/raw/",
        "step_features": "Edite src/{}/features.py",
        "step_run": "Execute:",
        "advisor_note": "NOTA: O Dataset Advisor requer dependências básicas de ML (pandas, scikit-learn).",
        "enable_ml_now": "Ativar dependências básicas de ML agora?",
        "goal_predict_category": "prever uma categoria",
        "goal_predict_number": "prever um número",
        "goal_group_records": "agrupar registros semelhantes",
        "goal_forecast_values": "prever valores futuros (forecast)",
        "goal_work_images": "trabalhar com imagens/texto",
        "priority_interpretability": "interpretabilidade",
        "priority_performance": "performance preditiva",
        "priority_simplicity": "velocidade/simplicidade",
        "priority_imbalanced": "lidar com classes desbalanceadas",
        "priority_learning": "aprendizado/experimentação",
        "error_fp": "falso positivo",
        "error_fn": "falso negativo",
        "error_both": "ambos similares",
        "error_not_sure": "não tenho certeza",
        "size_small": "pequeno",
        "size_medium": "médio",
        "size_large": "grande",
        "size_not_sure": "não tenho certeza",
        "opt_eda": "Incluir suporte a EDA?",
        "opt_preprocessing": "Incluir suporte a pré-processamento?",
        "opt_metrics": "Incluir métricas customizadas?",
        "opt_optimization": "Incluir estrutura de otimização?",
        "opt_features": "Incluir medição de features?",
        "opt_visualization": "Incluir suporte a visualização?",
        "opt_notebook": "Incluir fábrica de notebooks?",
        "opt_report": "Incluir template de relatório do modelo?",
        "opt_log": "Incluir template de log de experimentos?",
        "opt_advisor": "Incluir Dataset Advisor explicável?",
    }
}


def choose_language() -> str:
    print()
    print("Choose Language / Escolha o idioma:")
    print("1. en    - English")
    print("2. pt-BR - Português do Brasil")

    while True:
        choice = ask("Choose an option / Escolha uma opção", "1")
        if choice == "1" or choice == "en":
            return "en"
        if choice == "2" or choice == "pt-BR":
            return "pt-BR"
        print("Invalid option / Opção inválida.")


def ask_yes_no(prompt: str, default: bool = True) -> bool:
    default_label = "Y/n" if default else "y/N"
    full_prompt = f"{prompt} [{default_label}]: "
    print(full_prompt, end="", flush=True)
    value = input().strip().lower()

    if not value:
        return default

    return value in {"y", "yes"}


def choose_task(lang: str = "en") -> str:
    t = TRANSLATIONS[lang]
    print()
    print(t["project_type"])
    print("1. generic       - generic ML structure")
    print("2. supervised    - classification/regression")
    print("3. unsupervised  - PCA/K-Means/clustering")
    print("4. timeseries    - time series/LSTM")
    print("5. vision        - image classification/detection")

    while True:
        choice = ask(t["choose_option"], "2")
        if choice in TASKS:
            return TASKS[choice]
        if choice in TASKS.values():
            return choice
        print(t["invalid_option"])


def choose_python_profile(lang: str = "en") -> str:
    t = TRANSLATIONS[lang]
    print()
    print(t["python_profile"])
    print("1. safe   - Python 3.12 (stable)")
    print("2. modern - Python 3.14 (experimental/recent)")

    while True:
        choice = ask(t["choose_option"], "1")
        if choice == "1" or choice == "safe":
            return "3.12"
        if choice == "2" or choice == "modern":
            return "3.14"
        print(t["invalid_option"])


def choose_torch_variant(lang: str = "en") -> str:
    t = TRANSLATIONS[lang]
    print()
    print(t["pytorch_support"])
    print("1. none     - Do not include Torch")
    print("2. cpu      - Torch for CPU")
    print("3. cuda126  - Torch for CUDA 12.6")
    print("4. cuda128  - Torch for CUDA 12.8")

    mapping = {
        "1": "none",
        "2": "cpu",
        "3": "cu126",
        "4": "cu128"
    }

    while True:
        choice = ask(t["choose_option"], "1")
        if choice in mapping:
            return mapping[choice]
        if choice in mapping.values():
            return choice
        print(t["invalid_option"])


def choose_optional_profile(lang: str = "en") -> str:
    t = TRANSLATIONS[lang]
    print()
    print(t["optional_profile"])
    print("1. minimal     - no optional templates")
    print("2. recommended - eda, preprocessing, metrics, visualization")
    print("3. full        - all optional templates")
    print("4. custom      - select templates individually")

    while True:
        choice = ask(t["choose_option"], "2")
        if choice in {"1", "2", "3", "4"}:
            mapping = {"1": "minimal", "2": "recommended", "3": "full", "4": "custom"}
            return mapping[choice]
        if choice in {"minimal", "recommended", "full", "custom"}:
            return choice
        print(t["invalid_option"])


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
    }

    if profile == "minimal":
        return options

    if profile == "recommended":
        options["eda"] = True
        options["preprocessing"] = True
        options["metrics"] = True
        options["visualization"] = True
        options["advisor"] = True
        return options

    if profile == "full":
        for key in options:
            options[key] = True
        return options

    return options


def run_problem_framing_wizard(task: str, lang: str = "en") -> dict[str, str]:
    t = TRANSLATIONS[lang]
    print(f"\n{t['problem_framing_title']}")
    print("-" * len(t['problem_framing_title']))
    print(t["press_enter_defaults"])

    # 1. Main goal?
    goal_options = {
        "1": "predict a category",
        "2": "predict a number",
        "3": "group similar records",
        "4": "forecast future values",
        "5": "work with images/text"
    }
    print(f"\n{t['goal_q']}")
    print(f"   1. {t['goal_predict_category']}")
    print(f"   2. {t['goal_predict_number']}")
    print(f"   3. {t['goal_group_records']}")
    print(f"   4. {t['goal_forecast_values']}")
    print(f"   5. {t['goal_work_images']}")

    default_goal_map = {"supervised": "1", "unsupervised": "3", "timeseries": "4", "vision": "5"}
    default_goal_key = default_goal_map.get(task, "1")

    goal_choice = ask("Goal", default_goal_key)
    goal = goal_options.get(goal_choice, goal_choice)

    # 2. What matters most?
    priority_options = {
        "1": "interpretability",
        "2": "predictive performance",
        "3": "speed/simplicity",
        "4": "handling imbalanced classes",
        "5": "learning/experimentation"
    }
    print(f"\n{t['priority_q']}")
    print(f"   1. {t['priority_interpretability']}")
    print(f"   2. {t['priority_performance']}")
    print(f"   3. {t['priority_simplicity']}")
    print(f"   4. {t['priority_imbalanced']}")
    print(f"   5. {t['priority_learning']}")
    priority_choice = ask("Priority", "5")
    priority = priority_options.get(priority_choice, priority_choice)

    # 3. Which error is more costly?
    error_options = {
        "1": "false positive",
        "2": "false negative",
        "3": "both similar",
        "4": "not sure"
    }
    print(f"\n{t['error_cost_q']}")
    print(f"   1. {t['error_fp']}")
    print(f"   2. {t['error_fn']}")
    print(f"   3. {t['error_both']}")
    print(f"   4. {t['error_not_sure']}")
    error_choice = ask("Error cost", "4")
    error_cost = error_options.get(error_choice, error_choice)

    # 4. Expected dataset size?
    size_options = {
        "1": "small",
        "2": "medium",
        "3": "large",
        "4": "not sure"
    }
    print(f"\n{t['size_q']}")
    print(f"   1. {t['size_small']}")
    print(f"   2. {t['size_medium']}")
    print(f"   3. {t['size_large']}")
    print(f"   4. {t['size_not_sure']}")
    size_choice = ask("Size", "4")
    dataset_size = size_options.get(size_choice, size_choice)

    # 5. Prefer simple baseline first?
    prefer_baseline = "yes" if ask_yes_no(f"\n{t['baseline_q']}", True) else "no"

    # 6. Any domain note?
    domain_note = ask(f"\n{t['domain_note_q']}", "")

    return {
        "goal": goal,
        "priority": priority,
        "error_cost": error_cost,
        "dataset_size": dataset_size,
        "prefer_baseline": prefer_baseline,
        "domain_note": domain_note
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


def print_summary(root: Path, values: dict[str, str]) -> None:
    lang = values.get("LANGUAGE", "en")
    t = TRANSLATIONS[lang]
    print()
    print(t["summary_title"])
    print(f"{t['summary_dest']}: {root.resolve()}")
    print(f"{t['summary_project']}: {values['PROJECT_NAME']}")
    print(f"{t['summary_package']}: {values['PACKAGE_NAME']}")
    print(f"{t['summary_type']}: {values['TASK']}")
    print()
    print(t["next_steps_title"])
    print(f"1. {t['step_config']}")
    print(f"2. {t['step_data']}")
    print(f"3. {t['step_features'].format(values['PACKAGE_NAME'])}")
    print(f"4. {t['step_run']}")
    print(f"   python -m {values['PACKAGE_NAME']}.data")
    print(f"   python -m {values['PACKAGE_NAME']}.train")
    print(f"   python -m {values['PACKAGE_NAME']}.evaluate")


def main() -> None:
    lang = choose_language()
    t = TRANSLATIONS[lang]

    print("\nML Starter Kit Builder")
    print("======================")

    default_project = Path.cwd().name
    project_name = ask(t["project_name"], default_project)
    package_name = normalize_package_name(
        ask(t["package_name_q"], normalize_package_name(project_name))
    )
    task = choose_task(lang)
    preset = "none"

    dataset_path = ask(t["dataset_path_q"], "data/raw/dataset.csv")

    if task == "unsupervised":
        target_column = ""
    else:
        target_column = ask(t["target_column_q"], "target")

    problem_profile = run_problem_framing_wizard(task, lang)
    problem_profile["language"] = lang

    default_output_dir = STARTER_ROOT.parent / package_name
    while True:
        output_dir = Path(ask(t["output_dir_q"], str(default_output_dir))).resolve()

        is_inside = False
        try:
            if output_dir == STARTER_ROOT or output_dir.is_relative_to(STARTER_ROOT):
                is_inside = True
        except (ValueError, AttributeError):
            is_inside = False

        if is_inside:
            print(f"\n{t['warning_inside_repo']}")
            print("Warning: The selected output directory is inside the starter repository.")
            if ask_yes_no(t["continue_anyway"], default=False):
                break
        else:
            break

    include_docs = ask_yes_no(t["create_docs_q"], True)
    include_pyproject = ask_yes_no(t["create_env_q"], True)

    python_version = "3.11"
    torch_variant = "none"
    include_ml_basics = False

    if include_pyproject:
        python_version = choose_python_profile(lang)
        include_ml_basics = ask_yes_no(t["include_ml_basics_q"], False)
        torch_variant = choose_torch_variant(lang)

    print(f"\n{t['optional_files_title']}")
    profile = choose_optional_profile(lang)
    if profile == "custom":
        optional_options = {
            "eda": ask_yes_no(t["opt_eda"], False),
            "preprocessing": ask_yes_no(t["opt_preprocessing"], False),
            "metrics": ask_yes_no(t["opt_metrics"], False),
            "optimization": ask_yes_no(t["opt_optimization"], False),
            "feature_measurement": ask_yes_no(t["opt_features"], False),
            "visualization": ask_yes_no(t["opt_visualization"], False),
            "notebook_factory": ask_yes_no(t["opt_notebook"], False),
            "model_report": ask_yes_no(t["opt_report"], False),
            "experiment_log": ask_yes_no(t["opt_log"], False),
            "advisor": ask_yes_no(t["opt_advisor"], False),
        }
    else:
        optional_options = get_options_by_profile(profile)

    if optional_options.get("advisor") and not include_ml_basics:
        print(f"\n{t['advisor_note']}")
        if ask_yes_no(t["enable_ml_now"], True):
            include_ml_basics = True

    force = ask_yes_no(t["overwrite_q"], False)

    python_requires = f">={python_version}"
    if python_version == "3.12":
        python_requires = ">=3.12,<3.13"
    elif python_version == "3.14":
        python_requires = ">=3.14,<3.15"

    advisor_cmd = f"python -m {package_name}.advisor" if optional_options.get("advisor") else ""

    values = {
        "PROJECT_NAME": project_name,
        "PACKAGE_NAME": package_name,
        "TASK": task,
        "PRESET": preset,
        "DATASET_PATH": dataset_path,
        "TARGET_COLUMN": target_column,
        "PYTHON_REQUIRES": python_requires,
        "ADVISOR_COMMAND": advisor_cmd,
        "LANGUAGE": lang,
    }

    create_dirs(output_dir, package_name, preset, include_docs)
    create_config(output_dir, values, force=force)
    create_problem_profile(output_dir, problem_profile, force=force)
    create_readme(output_dir, values, force=force)
    create_package_files(output_dir, values, force=force)
    create_optional_files(output_dir, package_name, values, optional_options, force=force)
    create_tests(output_dir, values, force=force)
    create_notebook_placeholder(output_dir, values, force=force)

    if include_docs:
        create_docs(output_dir, values, force=force)

    if include_pyproject:
        create_pyproject(output_dir, values, force=force)
        create_env_files(
            output_dir,
            values,
            include_ml_basics,
            torch_variant,
            force=force
        )

    print_summary(output_dir, values)
