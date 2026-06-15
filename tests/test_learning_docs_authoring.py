import os
import unittest

class TestLearningDocsAuthoring(unittest.TestCase):
    def test_authoring_guides_exist(self):
        """Verify that the authoring guides exist in both EN and PT-BR."""
        self.assertTrue(os.path.exists("docs/authoring/learning-docs.md"))
        self.assertTrue(os.path.exists("docs/authoring/learning-docs.pt-BR.md"))

    def test_authoring_guide_content_en(self):
        """Verify that the English authoring guide contains the required rules."""
        with open("docs/authoring/learning-docs.md", "r", encoding="utf-8") as f:
            content = f.read()

        # Required source roles
        self.assertIn("scikit-learn", content)
        self.assertIn("Slivkins", content)
        self.assertIn("Sutton & Barto", content)

        # Required rules
        self.assertIn("No Direct Copying", content)
        self.assertIn("No Independent Research", content)
        self.assertIn("Conciseness over Academic Depth", content)
        self.assertIn("Limitation Notes", content)

    def test_authoring_guide_content_pt_br(self):
        """Verify that the Portuguese authoring guide contains the required rules."""
        with open("docs/authoring/learning-docs.pt-BR.md", "r", encoding="utf-8") as f:
            content = f.read()

        # Required source roles (names should stay the same)
        self.assertIn("scikit-learn", content)
        self.assertIn("Slivkins", content)
        self.assertIn("Sutton & Barto", content)

        # Required rules (translated)
        self.assertIn("Sem Cópia Direta", content)
        self.assertIn("Sem Pesquisa Independente", content)
        self.assertIn("Concisão sobre Profundidade Acadêmica", content)
        self.assertIn("Notas de Limitação", content)

    def test_readme_links(self):
        """Verify that the READMEs link to the authoring guides."""
        with open("docs/README.md", "r", encoding="utf-8") as f:
            self.assertIn("authoring/learning-docs.md", f.read())

        with open("docs/README.pt-BR.md", "r", encoding="utf-8") as f:
            self.assertIn("authoring/learning-docs.pt-BR.md", f.read())
