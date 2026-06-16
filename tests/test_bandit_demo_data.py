import unittest
import csv
import io
from ml_starter_generator.demo_data import get_demo_data

class TestBanditDemoData(unittest.TestCase):
    def test_get_demo_data_bandit_richness(self):
        """
        Verify P0.1: Bandit demo CSV richness and mandatory columns.
        """
        csv_content = get_demo_data("bandit")
        f = io.StringIO(csv_content)
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        rows = list(reader)

        # 1. get_demo_data("bandit") returns 100 lines + header.
        self.assertEqual(len(rows), 100)

        # 2. O CSV Bandit contém as colunas obrigatórias.
        required_columns = [
            "event_id", "timestamp", "customer_id", "age", "balance", "job",
            "segment", "channel_preference", "previous_contacts", "arm_name",
            "action_probability", "policy_name", "reward", "conversion",
            "revenue", "delay_days"
        ]
        for col in required_columns:
            self.assertIn(col, headers, f"Column {col} missing from Bandit demo")

        # 3. Existem 4 braços distintos no dataset.
        arms = set(row["arm_name"] for row in rows)
        expected_arms = {
            "term_deposit_email",
            "term_deposit_phone",
            "investment_advisor_call",
            "credit_card_push"
        }
        self.assertEqual(arms, expected_arms)

        # 4. reward e conversion são binários.
        for row in rows:
            self.assertIn(row["reward"], ["0", "1"])
            self.assertIn(row["conversion"], ["0", "1"])
            # verify policy name update
            self.assertEqual(row["policy_name"], "deterministic_uniform_logging_policy")

    def test_demo_data_regression_non_bandit(self):
        """
        Verify P0.4: regression testing for other tasks.
        """
        tasks = {
            "supervised": ["id", "age", "job", "balance", "subscribed"],
            "unsupervised": ["customer_id", "age", "annual_income", "spend_score"],
            "timeseries": ["date", "sales", "on_promotion"],
            "vision": ["image_path", "label", "width", "height"]
        }

        for task, expected_headers in tasks.items():
            csv_content = get_demo_data(task)
            f = io.StringIO(csv_content)
            reader = csv.DictReader(f)
            headers = reader.fieldnames
            self.assertEqual(headers, expected_headers, f"Headers for task {task} changed unexpectedly")
            rows = list(reader)
            self.assertEqual(len(rows), 10, f"Row count for task {task} changed unexpectedly")

if __name__ == "__main__":
    unittest.main()
