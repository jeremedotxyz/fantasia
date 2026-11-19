import unittest
from fantasia.nothing import NothingGauge


class TestNothing(unittest.TestCase):
    def test_initial_state(self):
        gauge = NothingGauge(context_limit=100_000)
        state = gauge.assess()
        self.assertEqual(state.threat_level, "QUIET")
        self.assertEqual(state.ratio, 0.0)

    def test_progressive_entropy(self):
        gauge = NothingGauge(context_limit=100_000)
        gauge.record_usage(50_000)
        state = gauge.assess()
        self.assertEqual(state.threat_level, "RESTLESS")
        self.assertEqual(state.ratio, 0.5)

        gauge.record_usage(40_000)
        state_crit = gauge.assess()
        self.assertEqual(state_crit.threat_level, "CRITICAL")
        self.assertEqual(state_crit.ratio, 0.9)

    def test_radar_output(self):
        gauge = NothingGauge(context_limit=100_000)
        gauge.record_usage(25_000)
        radar = gauge.ascii_radar(width=20)
        self.assertIn("25.0% VOID", radar)
        self.assertTrue(radar.startswith("["))


if __name__ == "__main__":
    unittest.main()
