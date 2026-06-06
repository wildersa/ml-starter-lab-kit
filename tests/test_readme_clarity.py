import unittest
import shutil
import tempfile
from pathlib import Path
from tests.helpers import run_generator

class TestReadmeClarity(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.project_name = "readme_proj"
        self.package_name = "readme_pkg"

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_readme_contains_p0_explanations_en(self):
        run_generator(
            language="1", # English
            project_name=self.project_name,
            package_name=self.package_name,
            output_dir=self.test_dir,
            optional_profile="3", # full (includes advisor)
        )

        readme_path = self.test_dir / "README.md"
        content = readme_path.read_text(encoding="utf-8")

        # P0.1: Default dataset path
        self.assertIn("data/raw/dataset.csv", content)

        # P0.2: config.json fields
        self.assertIn("data.raw_path", content)
        self.assertIn("data.processed_path", content)
        self.assertIn("target.column", content)

        # P0.3 & P0.4: target vs features and CSV example
        self.assertIn("Target", content)
        self.assertIn("Features", content)
        self.assertIn("feature_1,feature_2,feature_3,target_column", content)
        self.assertIn("one", content.lower())
        self.assertIn("many", content.lower())

        # P0.5: baseline meaning
        self.assertIn("baseline", content.lower())
        self.assertIn("minimum performance to beat", content.lower())

        # P0.6: features.py and existing columns
        self.assertIn("features.py", content)
        self.assertIn("candidate features", content)

        # P0.7: advisor and suggested_pipeline relation
        self.assertIn("Advisor", content)
        self.assertIn("suggested_pipeline.py", content)

    def test_readme_contains_p0_explanations_pt(self):
        run_generator(
            language="2", # pt-BR
            project_name=self.project_name,
            package_name=self.package_name,
            output_dir=self.test_dir,
            optional_profile="3", # full (includes advisor)
        )

        readme_path = self.test_dir / "README.md"
        content = readme_path.read_text(encoding="utf-8")

        # P0.1: Default dataset path
        self.assertIn("data/raw/dataset.csv", content)

        # P0.2: config.json fields
        self.assertIn("data.raw_path", content)
        self.assertIn("data.processed_path", content)
        self.assertIn("target.column", content)

        # P0.3 & P0.4: target vs features and CSV example
        self.assertIn("Alvo", content)
        self.assertIn("Features", content)
        self.assertIn("feature_1,feature_2,feature_3,target_column", content)
        self.assertIn("um", content.lower())
        self.assertIn("muitas", content.lower())

        # P0.5: baseline meaning
        self.assertIn("baseline", content.lower())
        self.assertIn("desempenho mínimo a ser superado", content.lower())

        # P0.6: features.py and existing columns
        self.assertIn("features.py", content)
        self.assertIn("candidatas a features", content)

        # P0.7: advisor and suggested_pipeline relation
        self.assertIn("Advisor", content)
        self.assertIn("suggested_pipeline.py", content)

if __name__ == "__main__":
    unittest.main()
