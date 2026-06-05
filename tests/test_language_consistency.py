import unittest
from pathlib import Path
import re

class TestLanguageConsistency(unittest.TestCase):
    FORBIDDEN_TERMS = [
        "dados", "modelo", "treinamento", "avaliação", "relatório",
        "execução", "projeto", "exemplo", "configuração", "saída",
        "entrada", "observabilidade", "métricas", "pacote", "inválida",
        "escolha", "opção", "caminho", "sobrescrever", "diretório"
    ]

    def test_sample_project_is_english_only(self):
        """
        Scan the generated project sample for Portuguese terms.
        """
        sample_path = Path(__file__).resolve().parents[1] / "examples" / "generated-project-sample"

        if not sample_path.exists():
            self.fail(f"Sample project path not found: {sample_path}")

        files_with_forbidden_terms = []

        # Iterate over all files in the sample project
        for path in sample_path.rglob("*"):
            if path.is_file() and not path.name.endswith(".gitkeep"):
                try:
                    content = path.read_text(encoding="utf-8").lower()
                    for term in self.FORBIDDEN_TERMS:
                        if term in content:
                            files_with_forbidden_terms.append(f"{path.relative_to(sample_path)}: found '{term}'")
                            break
                except UnicodeDecodeError:
                    # Skip binary files if any
                    continue

        if files_with_forbidden_terms:
            msg = "Found Portuguese terms in the following files:\n" + "\n".join(files_with_forbidden_terms)
            self.fail(msg)

if __name__ == "__main__":
    unittest.main()
