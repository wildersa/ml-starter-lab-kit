import unittest
import shutil
import tempfile
from pathlib import Path
import json
import csv

from tests.helpers import run_generator

class TestDemoData(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_p0_1_demo_defaults_off(self):
        # P0.1: demo option exists and defaults off
        run_generator(
            task="2",
            output_dir=self.test_dir,
            include_demo="n"
        )
        demo_file = self.test_dir / "data/raw/demo_dataset.csv"
        self.assertFalse(demo_file.exists())

    def test_p0_2_disabled_behavior_unchanged(self):
        # P0.2: disabled behavior unchanged
        custom_path = "data/raw/custom.csv"
        run_generator(
            task="2",
            dataset_path=custom_path,
            output_dir=self.test_dir,
            include_demo="n"
        )

        with open(self.test_dir / "configs/config.json") as f:
            config = json.load(f)
            self.assertEqual(config["data"]["raw_path"], custom_path)

        self.assertFalse((self.test_dir / "data/raw/demo_dataset.csv").exists())

    def test_p0_3_supervised_classification_demo(self):
        # P0.3: supervised/classification demo CSV generated
        # Choosing "predict a category" (default for supervised)
        run_generator(
            task="2",
            output_dir=self.test_dir,
            include_demo="y",
            problem_goal="predict a category"
        )

        demo_file = self.test_dir / "data/raw/demo_dataset.csv"
        self.assertTrue(demo_file.exists())

        with open(demo_file, newline="") as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames
            self.assertIn("subscribed", headers)
            rows = list(reader)
            self.assertTrue(len(rows) > 0)

    def test_p0_4_supervised_regression_demo(self):
        # P0.4: regression demo behavior defined
        # Choosing "predict a number"
        run_generator(
            task="2",
            output_dir=self.test_dir,
            include_demo="y",
            problem_goal="predict a number"
        )

        demo_file = self.test_dir / "data/raw/demo_dataset.csv"
        self.assertTrue(demo_file.exists())

        with open(demo_file, newline="") as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames
            self.assertIn("price", headers)

    def test_p0_5_unsupervised_demo_no_target(self):
        # P0.5: unsupervised demo has no target
        run_generator(
            task="3", # unsupervised
            output_dir=self.test_dir,
            include_demo="y"
        )

        demo_file = self.test_dir / "data/raw/demo_dataset.csv"
        self.assertTrue(demo_file.exists())

        with open(self.test_dir / "configs/config.json") as f:
            config = json.load(f)
            self.assertEqual(config["target"]["column"], "")

        with open(demo_file, newline="") as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames
            # It should have some feature columns but no "target" or "subscribed"
            self.assertNotIn("target", headers)
            self.assertNotIn("subscribed", headers)

    def test_p0_6_timeseries_demo(self):
        # P0.6: timeseries demo generated
        run_generator(
            task="4", # timeseries
            output_dir=self.test_dir,
            include_demo="y"
        )

        demo_file = self.test_dir / "data/raw/demo_dataset.csv"
        self.assertTrue(demo_file.exists())

        with open(demo_file, newline="") as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames
            self.assertIn("date", headers)
            self.assertIn("sales", headers)

    def test_p0_7_vision_demo_metadata(self):
        # P0.7: vision demo is metadata-only
        run_generator(
            task="5", # vision
            output_dir=self.test_dir,
            include_demo="y"
        )

        demo_file = self.test_dir / "data/raw/demo_dataset.csv"
        self.assertTrue(demo_file.exists())

        # Verify no fake binaries were created in data/raw (should only be the CSV and .gitkeep)
        files = list((self.test_dir / "data/raw").iterdir())
        for f in files:
            if f.is_file() and f.name != ".gitkeep":
                self.assertEqual(f.name, "demo_dataset.csv")

    def test_p0_8_config_points_to_demo(self):
        # P0.8: config points to demo path
        tasks = ["2", "3", "4", "5"]
        for task in tasks:
            shutil.rmtree(self.test_dir)
            self.test_dir.mkdir()
            run_generator(
                task=task,
                output_dir=self.test_dir,
                include_demo="y"
            )
            with open(self.test_dir / "configs/config.json") as f:
                config = json.load(f)
                self.assertEqual(config["data"]["raw_path"], "data/raw/demo_dataset.csv")

    def test_p0_9_deterministic_and_small(self):
        # P0.9: demo is deterministic and small
        run_generator(
            task="2",
            output_dir=self.test_dir,
            include_demo="y"
        )
        demo_path = self.test_dir / "data/raw/demo_dataset.csv"
        with open(demo_path) as f:
            content1 = f.read()
            rows1 = len(content1.splitlines())

        shutil.rmtree(self.test_dir)
        self.test_dir.mkdir()

        run_generator(
            task="2",
            output_dir=self.test_dir,
            include_demo="y"
        )
        with open(demo_path) as f:
            content2 = f.read()
            rows2 = len(content2.splitlines())

        self.assertEqual(content1, content2)
        self.assertTrue(rows1 < 100) # Small

if __name__ == "__main__":
    unittest.main()
