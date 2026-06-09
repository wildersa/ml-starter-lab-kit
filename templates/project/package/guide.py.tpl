from __future__ import annotations

import sys
from .config import load_config, project_root
from .core.readiness import check_dataset_readiness

def main() -> None:
    print("\n--- Project Guide: Dataset & Configuration Onboarding ---")

    try:
        config = load_config()
    except Exception as e:
        print(f"\n[ERROR] Could not load config: {e}")
        print("Please ensure configs/config.json exists.")
        sys.exit(1)

    data_config = config.get("data", {})
    raw_path_str = data_config.get("raw_path", "data/raw/dataset.csv")
    raw_path = project_root() / raw_path_str

    target_config = config.get("target", {})
    target_col = target_config.get("column")

    print(f"\nConfigured dataset path: {raw_path_str}")
    if target_col:
        print(f"Configured target column: {target_col}")

    readiness = check_dataset_readiness(raw_path)

    if not readiness["exists"]:
        print(f"\n[!] Dataset NOT FOUND at: {raw_path_str}")
        print("\nNext steps:")
        print(f"  1. Place your CSV file at: {raw_path_str}")
        print("  2. Or update 'data.raw_path' in configs/config.json to point to your file.")
        print("\nOnce the file is in place, run this guide again.")
        return

    if readiness.get("error"):
        print(f"\n[ERROR] Could not read dataset: {readiness['error']}")
        return

    if readiness.get("empty"):
        print("[!] The dataset appears to be empty or has no headers.")
        return

    # Dataset exists
    print(f"\n[✔] Dataset found at: {raw_path_str}")
    print(f"Sampled {readiness['sample_count']} rows for inspection.")
    print("\nColumns found:")

    found_target = False
    columns = readiness["columns"]

    for col, info in columns.items():
        col_type = info["type"]
        status = ""
        if target_col and col == target_col:
            found_target = True
            status = " [TARGET]"

        print(f"  - {col}: {col_type}{status}")

    if target_col:
        if found_target:
            print(f"\n[✔] Target column '{target_col}' found in dataset.")
        else:
            print(f"\n[WARNING] Target column '{target_col}' NOT FOUND in dataset.")
            target_candidates = readiness.get("target_candidates", [])
            if target_candidates:
                print(f"Suggested candidates: {', '.join(target_candidates)}")
            print("Please update 'target.column' in configs/config.json if needed.")

    print("\nRecommended next commands:")
    pkg = "{{PACKAGE_NAME}}"
    {% if LEARNING_ENABLED == "true" %}
    print(f"  1. python -m {pkg}.lab workspace (Visual insights)")
    print(f"  2. python -m {pkg}.lab eda       (Generate dataset summary)")
    {% else %}
    {% if GENERATE_EDA == "true" %}
    print(f"  1. python -m {pkg}.lab eda       (Run exploratory analysis)")
    {% else %}
    print(f"  1. python -m {pkg}.lab train     (Train baseline model)")
    {% endif %}
    {% if GENERATE_ADVISOR == "true" %}
    print(f"  2. python -m {pkg}.lab advisor   (Get modeling suggestions)")
    {% endif %}
    {% endif %}

if __name__ == "__main__":
    main()
