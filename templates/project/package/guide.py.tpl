from __future__ import annotations

import csv
import sys
from pathlib import Path

from .config import load_config, project_root

def infer_type(values: list[str]) -> str:
    valid_values = [v for v in values if v.strip()]
    if not valid_values:
        return "empty/unknown"

    is_numeric = True
    for v in valid_values:
        try:
            float(v.replace(",", ".")) # handle some european decimals just in case
        except ValueError:
            is_numeric = False
            break
    if is_numeric:
        return "numeric"

    is_date = True
    for v in valid_values:
        # Very simple heuristic: contains - or / and some numbers
        if not (("-" in v or "/" in v) and any(c.isdigit() for c in v)):
            is_date = False
            break
    if is_date:
        return "date-like"

    return "categorical/text"

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

    if not raw_path.exists():
        print(f"\n[!] Dataset NOT FOUND at: {raw_path_str}")
        print("\nNext steps:")
        print(f"  1. Place your CSV file at: {raw_path_str}")
        print("  2. Or update 'data.raw_path' in configs/config.json to point to your file.")
        print("\nOnce the file is in place, run this guide again.")
        return

    # Dataset exists
    print(f"\n[✔] Dataset found at: {raw_path_str}")

    try:
        with open(raw_path, "r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            columns = reader.fieldnames
            if not columns:
                print("[!] The dataset appears to be empty or has no headers.")
                return

            sample_rows = []
            for i, row in enumerate(reader):
                sample_rows.append(row)
                if i >= 100:
                    break
    except Exception as e:
        print(f"\n[ERROR] Could not read dataset: {e}")
        return

    print(f"Sampled {len(sample_rows)} rows for inspection.")
    print("\nColumns found:")

    found_target = False
    target_candidates = []

    for col in columns:
        col_values = [row[col] for row in sample_rows if col in row and row[col] is not None]
        col_type = infer_type(col_values)

        status = ""
        if target_col and col == target_col:
            found_target = True
            status = " [TARGET]"

        print(f"  - {col}: {col_type}{status}")

        if not found_target:
            if col.lower() in ["target", "label", "y", "class", "outcome"]:
                target_candidates.append(col)

    if target_col:
        if found_target:
            print(f"\n[✔] Target column '{target_col}' found in dataset.")
        else:
            print(f"\n[WARNING] Target column '{target_col}' NOT FOUND in dataset.")
            if target_candidates:
                print(f"Suggested candidates: {', '.join(target_candidates)}")
            print("Please update 'target.column' in configs/config.json if needed.")

    print("\nRecommended next commands:")
    print(f"  1. python -m {{PACKAGE_NAME}}.data      (Process your data)")

    advisor_cmd = "{{ADVISOR_COMMAND}}"
    if advisor_cmd:
        print(f"  2. {advisor_cmd}   (Get detailed analysis)")
        print(f"  3. python -m {{PACKAGE_NAME}}.train     (Train baseline model)")
        print(f"  4. python -m {{PACKAGE_NAME}}.evaluate  (Evaluate performance)")
    else:
        print(f"  2. python -m {{PACKAGE_NAME}}.train     (Train baseline model)")
        print(f"  3. python -m {{PACKAGE_NAME}}.evaluate  (Evaluate performance)")

if __name__ == "__main__":
    main()
