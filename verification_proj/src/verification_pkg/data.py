from __future__ import annotations

from .core.config import load_config, project_root
from .core.data import load_csv, save_csv

def main() -> None:
    config = load_config()
    raw_path = config["data"]["raw_path"]
    processed_path = config["data"]["processed_path"]

    rows = load_csv(raw_path)
    print(f"Rows loaded: {len(rows)}")

    if rows:
        print(f"Columns: {list(rows[0].keys())}")

    save_csv(rows, processed_path)
    print(f"Processed file saved at: {processed_path}")

if __name__ == "__main__":
    main()
