import os
import sys
import argparse
from pathlib import Path

try:
    import pandas as pd
    import numpy as np
except ImportError:
    pd = None
    np = None

def load_config():
    """Loads basic project configuration."""
    # In a real project, this would import from .core.config
    # For this educational stub, we try to be self-contained or import if possible
    try:
        from .core.config import load_config as _load
        return _load()
    except (ImportError, ValueError):
        return {}

def check_drift(reference_df, current_df, target_col=None):
    """
    Performs basic drift checks between reference (train) and current (new) data.
    This is an educational stub showing common patterns.
    """
    report = []
    report.append("# Basic Drift Analysis Report")
    report.append(f"- Reference rows: {len(reference_df)}")
    report.append(f"- Current rows: {len(current_df)}")
    report.append("")

    # 1. Schema Check
    ref_cols = set(reference_df.columns)
    cur_cols = set(current_df.columns)

    missing_cols = ref_cols - cur_cols
    new_cols = cur_cols - ref_cols

    if missing_cols or new_cols:
        report.append("## Schema Changes")
        if missing_cols:
            report.append(f"- [!] Missing columns in new data: {missing_cols}")
        if new_cols:
            report.append(f"- [+] New columns in new data: {new_cols}")
    else:
        report.append("## Schema: OK (Matched)")
    report.append("")

    # 2. Numerical Drift (Simple Statistics)
    # Use 'number' string for compatibility if numpy is not present (though pandas usually has it)
    num_cols = reference_df.select_dtypes(include=['number']).columns
    if not num_cols.empty:
        report.append("## Numerical Feature Statistics (Mean Comparison)")
        report.append("| Feature | Reference Mean | Current Mean | Shift (%) |")
        report.append("|---|---|---|---|")

        for col in num_cols:
            if col in current_df.columns:
                ref_mean = reference_df[col].mean()
                cur_mean = current_df[col].mean()
                shift = 0
                if ref_mean != 0:
                    shift = ((cur_mean - ref_mean) / abs(ref_mean)) * 100

                status = " "
                if abs(shift) > 20: status = "⚠️"

                report.append(f"| {col} | {ref_mean:.4f} | {cur_mean:.4f} | {shift:+.1f}% {status} |")
        report.append("")

    # 3. Categorical Drift (New categories)
    cat_cols = reference_df.select_dtypes(include=['object', 'category']).columns
    if not cat_cols.empty:
        report.append("## Categorical Feature Changes")
        for col in cat_cols:
            if col in current_df.columns:
                ref_cats = set(reference_df[col].unique())
                cur_cats = set(current_df[col].unique())
                new_cats = cur_cats - ref_cats
                if new_cats:
                    report.append(f"- **{col}**: ⚠️ Found {len(new_cats)} new categories: {list(new_cats)[:5]}...")
                else:
                    report.append(f"- **{col}**: OK (No new categories)")
        report.append("")

    return "\n".join(report)

def main():
    if pd is None:
        print("Error: pandas is required for this monitoring stub.")
        print("Install it with: pip install pandas")
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Educational Monitoring/Drift Stub")
    parser.add_argument("--reference", help="Path to reference (training) data")
    parser.add_argument("--current", help="Path to current (new) data")
    parser.add_argument("--output", default="reports/drift-report.md", help="Path to save report")

    # Strip 'monitor' if called via unified CLI
    argv = sys.argv[1:]
    if argv and argv[0] == "monitor":
        argv = argv[1:]

    args, _ = parser.parse_known_args(argv)

    config = load_config()

    # Default paths if not provided
    ref_path = args.reference or config.get("data", {}).get("raw_path", "data/raw/dataset.csv")
    cur_path = args.current

    print(f"Monitoring: Reference={ref_path}")

    if not os.path.exists(ref_path):
        print(f"Error: Reference file not found: {ref_path}")
        return

    if not cur_path:
        print("\n[INFO] No 'current' dataset provided for comparison.")
        print("In a real scenario, you would provide a new file with recent data.")
        print("For this demo, we will compare the reference file with a slightly perturbed version of itself.")

        ref_df = pd.read_csv(ref_path)
        cur_df = ref_df.copy()

        # Simulating some drift for educational purposes
        num_cols = cur_df.select_dtypes(include=[np.number]).columns
        if not num_cols.empty:
            col = num_cols[0]
            cur_df[col] = cur_df[col] * 1.25 # 25% shift
            print(f"Simulating 25% drift in column: {col}")
    else:
        ref_df = pd.read_csv(ref_path)
        cur_df = pd.read_csv(cur_path)

    report_content = check_drift(ref_df, cur_df)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report_content)

    print(f"\n✔ Drift report generated at: {output_path}")
    print("\nEducational Note: Monitoring is not just about tools, it's about asking:")
    print("1. Has my data distribution changed?")
    print("2. Is the model relationship still valid (Concept Drift)?")
    print("3. Are there new categories or missing values?")

if __name__ == "__main__":
    main()
