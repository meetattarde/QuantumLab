import tempfile
import unittest
from pathlib import Path

from core.labbook import curve_metrics, load_session, make_record, save_session
from core.physics import run_experiment
from core.presets import PRESETS, names_for


class TestLabNotebook(unittest.TestCase):
    def test_curve_metrics_known_triangle(self):
        metrics = curve_metrics([0, 1, 2], [0, 1, 0])
        self.assertEqual(metrics["peak_x"], 1.0)
        self.assertEqual(metrics["maximum"], 1.0)
        self.assertAlmostEqual(metrics["area"], 1.0)

    def test_session_round_trip(self):
        params = {"quantum_number": 1, "box_length_nm": 1.0}
        record = make_record("Particle in a box", params, run_experiment("Particle in a box", params))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "session.json"
            save_session(path, [record], "Particle in a box", params)
            records, experiment, restored = load_session(path)
        self.assertEqual(experiment, "Particle in a box")
        self.assertEqual(restored, params)
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].experiment, record.experiment)
        self.assertEqual(records[0].metrics, record.metrics)

    def test_presets_match_their_experiment_controls(self):
        for experiment, choices in PRESETS.items():
            valid = {item["key"] for item in __import__("core.physics", fromlist=["EXPERIMENTS"]).EXPERIMENTS[experiment]["controls"]}
            self.assertEqual(names_for(experiment), list(choices))
            for values in choices.values():
                self.assertTrue(set(values).issubset(valid))


if __name__ == "__main__":
    unittest.main()
