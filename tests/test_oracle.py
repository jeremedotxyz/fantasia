import unittest
from fantasia.oracle import SouthernOracle


class TestOracle(unittest.TestCase):
    def test_synthetic_oracle_fallback(self):
        oracle = SouthernOracle()
        # Force offline/synthetic
        res = oracle._synthetic_oracle("How do we fix this bug in production?")
        self.assertEqual(res["provider"], "synthetic-sphinx")
        self.assertIn("Sphinxes", res["verdict"])
        self.assertGreater(res["confidence"], 0.9)

    def test_consult_what_am_i(self):
        oracle = SouthernOracle()
        res = oracle.consult("What is this world?")
        self.assertIn("Fantasia", res["verdict"])


if __name__ == "__main__":
    unittest.main()
