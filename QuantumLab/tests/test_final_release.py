import json
import tempfile
import unittest
from pathlib import Path

import numpy as np

from core.labbook import load_session, make_record, save_session
from core.physics import run_experiment
from core.reporting import format_report


class TestFinalRelease(unittest.TestCase):
    def test_measurement_seed_is_reproducible(self):
        parameters = {"probability": 0.37, "trials": 100, "seed": 123}
        first = run_experiment("Quantum measurement statistics", parameters)
        second = run_experiment("Quantum measurement statistics", parameters)
        self.assertTrue(np.array_equal(first[1], second[1]))
        self.assertIn("Random seed: 123", first[4])

    def test_session_integrity_detects_changes(self):
        parameters = {"quantum_number": 1, "box_length_nm": 1.0}
        record = make_record("Particle in a box", parameters, run_experiment("Particle in a box", parameters))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "session.json"
            save_session(path, [record], "Particle in a box", parameters)
            payload = json.loads(path.read_text(encoding="utf-8"))
            payload["active_parameters"]["box_length_nm"] = 2.0
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "integrity"):
                load_session(path)

    def test_report_contains_recorded_content(self):
        parameters = {"probability": 0.5, "trials": 20, "seed": 7}
        record = make_record("Quantum measurement statistics", parameters, run_experiment("Quantum measurement statistics", parameters))
        report = format_report([record], "Quantum measurement statistics")
        self.assertIn("Session Report", report)
        self.assertIn("Quantum measurement statistics", report)
        self.assertIn("probability", report)


if __name__ == "__main__":
    unittest.main()
