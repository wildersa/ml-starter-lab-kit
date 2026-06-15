import os
import pytest

def test_authoring_guides_exist():
    """Verify that the authoring guides exist in both EN and PT-BR."""
    assert os.path.exists("docs/authoring/learning-docs.md")
    assert os.path.exists("docs/authoring/learning-docs.pt-BR.md")

def test_authoring_guide_content_en():
    """Verify that the English authoring guide contains the required rules."""
    with open("docs/authoring/learning-docs.md", "r", encoding="utf-8") as f:
        content = f.read()

    # Required source roles
    assert "scikit-learn" in content
    assert "Slivkins" in content
    assert "Sutton & Barto" in content

    # Required rules
    assert "No Direct Copying" in content
    assert "No Independent Research" in content
    assert "Conciseness over Academic Depth" in content
    assert "Limitation Notes" in content

def test_authoring_guide_content_pt_br():
    """Verify that the Portuguese authoring guide contains the required rules."""
    with open("docs/authoring/learning-docs.pt-BR.md", "r", encoding="utf-8") as f:
        content = f.read()

    # Required source roles (names should stay the same)
    assert "scikit-learn" in content
    assert "Slivkins" in content
    assert "Sutton & Barto" in content

    # Required rules (translated)
    assert "Sem Cópia Direta" in content
    assert "Sem Pesquisa Independente" in content
    assert "Concisão sobre Profundidade Acadêmica" in content
    assert "Notas de Limitação" in content

def test_readme_links():
    """Verify that the READMEs link to the authoring guides."""
    with open("docs/README.md", "r", encoding="utf-8") as f:
        assert "authoring/learning-docs.md" in f.read()

    with open("docs/README.pt-BR.md", "r", encoding="utf-8") as f:
        assert "authoring/learning-docs.pt-BR.md" in f.read()
