import unittest
from pathlib import Path

class TestReferencesDocs(unittest.TestCase):
    def setUp(self):
        self.en_file = Path("docs/references.md")
        self.pt_file = Path("docs/references.pt-BR.md")
        self.en_readme = Path("docs/README.md")
        self.pt_readme = Path("docs/README.pt-BR.md")

    def test_files_exist(self):
        self.assertTrue(self.en_file.exists(), "docs/references.md missing")
        self.assertTrue(self.pt_file.exists(), "docs/references.pt-BR.md missing")

    def test_allowed_urls_present(self):
        urls = [
            "https://scikit-learn.org/stable/user_guide.html",
            "https://scikit-learn.org/stable/modules/model_evaluation.html",
            "https://scikit-learn.org/stable/datasets/sample_generators.html",
            "https://arxiv.org/abs/1904.07272",
            "http://incompleteideas.net/book/the-book-2nd.html"
        ]

        for filepath in [self.en_file, self.pt_file]:
            content = filepath.read_text(encoding="utf-8")
            for url in urls:
                self.assertIn(url, content, f"URL {url} missing in {filepath}")

    def test_required_sections_present(self):
        # Using English markers for simplicity in en_file, and translated equivalents for pt_file
        en_markers = ["What it supports", "Where it applies", "Beginner note", "Limitation"]
        pt_markers = ["O que suporta", "Onde se aplica", "Nota para iniciantes", "Limitação"]

        en_content = self.en_file.read_text(encoding="utf-8")
        for marker in en_markers:
            self.assertIn(marker, en_content, f"Marker '{marker}' missing in {self.en_file}")

        pt_content = self.pt_file.read_text(encoding="utf-8")
        for marker in pt_markers:
            self.assertIn(marker, pt_content, f"Marker '{marker}' missing in {self.pt_file}")

    def test_readme_links(self):
        self.assertIn("references.md", self.en_readme.read_text(encoding="utf-8"))
        self.assertIn("references.pt-BR.md", self.pt_readme.read_text(encoding="utf-8"))

if __name__ == "__main__":
    unittest.main()
