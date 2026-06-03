
from __future__ import annotations

import csv
from pathlib import Path

from .config import load_config, project_root


def load_csv(path: str | Path) -> list[dict[str, str]]:
    file_path = project_root() / path

    if not file_path.exists():
        raise FileNotFoundError(f"Dataset não encontrado: {file_path}")

    with file_path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def save_csv(rows: list[dict[str, object]], path: str | Path) -> None:
    if not rows:
        raise ValueError("Nenhuma linha para salvar.")

    file_path = project_root() / path
    file_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = list(rows[0].keys())

    with file_path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    config = load_config()
    raw_path = config["data"]["raw_path"]
    processed_path = config["data"]["processed_path"]

    rows = load_csv(raw_path)
    print(f"Linhas carregadas: {len(rows)}")

    if rows:
        print(f"Colunas: {list(rows[0].keys())}")

    save_csv(rows, processed_path)
    print(f"Arquivo processado salvo em: {processed_path}")


if __name__ == "__main__":
    main()
