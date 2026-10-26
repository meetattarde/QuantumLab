"""Heisenberg uncertainty principle simulation for QUANTUM LAB.

Uses a normalized Gaussian position probability density and a
minimum-uncertainty Gaussian wave packet.
"""

import numpy as np

HBAR = 1.054571817e-34


def calculate(p):
    """Return data in QUANTUM LAB's standard six-value format."""

    # Standard deviation of position, converted from nm to metres.
    sigma_x_nm = float(p["sigma_x_nm"])
    sigma_x_m = sigma_x_nm * 1e-9

    if sigma_x_m <= 0:
        raise ValueError("Position uncertainty must be greater than zero.")

    # A minimum-uncertainty Gaussian wave packet satisfies:
    # Δx Δp = ħ/2.
    delta_x = sigma_x_m
    delta_p = HBAR / (2.0 * delta_x)
    uncertainty_product = delta_x * delta_p
    lower_bound = HBAR / 2.0

    # Position coordinate in nm.
    x = np.linspace(-5.0 * sigma_x_nm, 5.0 * sigma_x_nm, 501)

    # Normalized Gaussian probability density per nanometre.
    # Its integral over position is approximately 1.
    y = (
        np.exp(-0.5 * (x / sigma_x_nm) ** 2)
        / (np.sqrt(2.0 * np.pi) * sigma_x_nm)
    )

    ratio = uncertainty_product / lower_bound

    summary = (
        "Gaussian wave packet — minimum-uncertainty state\n"
        f"Position uncertainty Δx: {delta_x:.4e} m "
        f"({sigma_x_nm:.4f} nm)\n"
        f"Momentum uncertainty Δp: {delta_p:.4e} kg·m/s\n"
        f"Uncertainty product Δx·Δp: {uncertainty_product:.4e} J·s\n"
        f"Heisenberg lower bound ħ/2: {lower_bound:.4e} J·s\n"
        f"Product / lower bound: {ratio:.6f}\n"
        "Interpretation: this ideal Gaussian reaches the minimum "
        "uncertainty allowed by the Heisenberg relation. Reducing "
        "Δx increases Δp."
    )

    return (
        x,
        y,
        "Position (nm)",
        "Probability density (nm⁻¹)",
        summary,
        ("Position (nm)", "Probability density (nm^-1)"),
    )