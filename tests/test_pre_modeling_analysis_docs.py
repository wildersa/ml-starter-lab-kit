import unittest
import os

class TestPreModelingAnalysisDocs(unittest.TestCase):
    def setUp(self):
        self.en_path = "docs/workflows/pre-modeling-analysis.md"
        self.pt_path = "docs/workflows/pre-modeling-analysis.pt-BR.md"

    def test_files_exist(self):
        self.assertTrue(os.path.exists(self.en_path))
        self.assertTrue(os.path.exists(self.pt_path))

    def test_bilingual_parity(self):
        with open(self.en_path, "r", encoding="utf-8") as f:
            en_content = f.read()
        with open(self.pt_path, "r", encoding="utf-8") as f:
            pt_content = f.read()

        # Check for similar headers/sections
        en_headers = [line for line in en_content.splitlines() if line.startswith("## ")]
        pt_headers = [line for line in pt_content.splitlines() if line.startswith("## ")]
        self.assertEqual(len(en_headers), len(pt_headers))

        # Check for analysis families (10 in each)
        self.assertIn("### 10.", en_content)
        self.assertIn("### 10.", pt_content)

    def test_taxonomy_content(self):
        required_terms_en = [
            "Data Profiling", "Structural Integrity", "Distribution Analysis",
            "Visual Relationship Checks", "Correlation & Redundancy",
            "Leakage & Availability", "Univariate Predictive Screening",
            "Quick Baseline", "Segment-Level Checks", "Temporal Consistency"
        ]

        with open(self.en_path, "r", encoding="utf-8") as f:
            content = f.read()

        for term in required_terms_en:
            self.assertIn(term, content)

        # Check for problem-specific table
        self.assertIn("| Analysis Family |", content)
        self.assertIn("Supervised Tabular", content)
        self.assertIn("Bandit / RL", content)

    def test_vendor_neutrality(self):
        forbidden_terms = ["Pandas Profiling", "Sweetviz", "ydata-profiling", "Facets", "Great Expectations"]

        for path in [self.en_path, self.pt_path]:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read().lower()
                for term in forbidden_terms:
                    self.assertNotIn(term.lower(), content)

    def test_learning_rules(self):
        # Every document must include a "Limitations" note
        for path in [self.en_path, self.pt_path]:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                self.assertTrue("Limitations" in content or "Limitações" in content)
                self.assertTrue("Learn More" in content or "Saiba Mais" in content)

if __name__ == "__main__":
    unittest.main()
