"""Analytic stationary states of the one-dimensional quantum oscillator."""
import math
import numpy as np

from core.numerics import HBAR, M_E, EV, validate_finite


def calculate(p):
    n = int(round(float(p["quantum_number"])))
    frequency_thz = validate_finite("Frequency", p["frequency_thz"], positive=True)
    if n < 0 or n > 8:
        raise ValueError("Quantum number must be between 0 and 8.")
    omega = 2 * np.pi * frequency_thz * 1e12
    scale = math.sqrt(HBAR / (M_E * omega))
    x = np.linspace(-5.5 * scale, 5.5 * scale, 800)
    xi = x / scale
    coefficients = [0.0] * n + [1.0]
    hermite = np.polynomial.hermite.hermval(xi, coefficients)
    psi = (np.exp(-xi**2 / 2) * hermite /
           (np.sqrt(scale) * np.pi**0.25 * math.sqrt(2**n * math.factorial(n))))
    density = psi**2
    energy_ev = HBAR * omega * (n + 0.5) / EV
    summary = (f"State n = {n} | Energy: {energy_ev:.6g} eV\n"
               f"Oscillator frequency: {frequency_thz:.4g} THz\n"
               "Model: exact 1D harmonic-oscillator stationary state for an electron; the curve is a normalised probability density.")
    return x * 1e9, density * 1e-9, "Position (nm)", "Probability density (nm⁻¹)", summary, ("Position (nm)", "Probability density (nm^-1)")
