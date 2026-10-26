import math
import unittest
import numpy as np

from core.numerics import HBAR, M_E, EV, crank_nicolson_step, solve_stationary_1d
from core.physics import EXPERIMENTS, run_experiment
from experiments.tunnelling import transmission_probability


class TestScientificBenchmarks(unittest.TestCase):
    def test_all_experiments_return_finite_curves(self):
        for name, metadata in EXPERIMENTS.items():
            params = {item["key"]: item["value"] for item in metadata["controls"]}
            x, y, xlabel, ylabel, summary, headers = run_experiment(name, params)
            if name == "Atomic orbitals":
                _, _, density = x
                values = density
            else:
                values = y
            self.assertTrue(np.all(np.isfinite(values)), name)
            self.assertTrue(str(xlabel) and str(ylabel) and str(summary), name)
            self.assertEqual(len(headers), 2 if name != "Atomic orbitals" else 3)

    def test_rectangular_barrier_limits(self):
        self.assertEqual(transmission_probability(1, 5, 0), 1.0)
        self.assertEqual(transmission_probability(1, 0, 1), 1.0)
        self.assertGreater(transmission_probability(1, 5, 0.1), transmission_probability(1, 5, 1.0))

    def test_box_energy_scaling(self):
        params = {"quantum_number": 1, "box_length_nm": 1}
        _, _, _, _, one, _ = run_experiment("Particle in a box", params)
        params["quantum_number"] = 2
        _, _, _, _, two, _ = run_experiment("Particle in a box", params)
        e1 = float(one.split("Energy: ")[1].split(" eV")[0])
        e2 = float(two.split("Energy: ")[1].split(" eV")[0])
        self.assertAlmostEqual(e2 / e1, 4.0, places=3)

    def test_uncertainty_gaussian_saturates_bound(self):
        _, _, _, _, summary, _ = run_experiment("Heisenberg uncertainty principle", {"sigma_x_nm": 0.5})
        self.assertIn("Product / lower bound: 1.000000", summary)

    def test_finite_difference_box_benchmark(self):
        length = 1e-9
        x = np.linspace(0, length, 301)
        solution = solve_stationary_1d(x, np.zeros_like(x), states=1)
        expected = math.pi**2 * HBAR**2 / (2 * M_E * length**2) / EV
        self.assertLess(abs(solution.energies_ev[0] - expected) / expected, 0.002)
        self.assertAlmostEqual(float(np.trapezoid(solution.states[0] ** 2, x)), 1.0, places=8)

    def test_crank_nicolson_preserves_norm(self):
        x = np.linspace(-2e-9, 2e-9, 101)
        psi = np.exp(-(x / 0.5e-9) ** 2).astype(complex)
        psi /= math.sqrt(float(np.trapezoid(abs(psi) ** 2, x)))
        advanced = crank_nicolson_step(psi, np.zeros_like(x), x[1] - x[0], 1e-18)
        self.assertAlmostEqual(float(np.trapezoid(abs(advanced) ** 2, x)), 1.0, places=8)


if __name__ == "__main__":
    unittest.main()
