"""Quantum tunnelling through a rectangular potential barrier.

Educational model using the exact transmission probability for a
one-dimensional rectangular barrier with equal potential on both sides.
"""

import numpy as np

HBAR = 1.054571817e-34
M_E = 9.1093837e-31
EV = 1.602176634e-19


def transmission_probability(energy_ev, barrier_ev, width_nm):
    """Calculate transmission probability for a rectangular barrier."""

    energy = float(energy_ev) * EV
    barrier = float(barrier_ev) * EV
    width = float(width_nm) * 1e-9

    if energy <= 0 or barrier < 0 or width < 0:
        raise ValueError(
            "Energy must be positive; barrier height and width "
            "must be non-negative."
        )

    if width == 0 or barrier == 0:
        return 1.0

    # At exactly the barrier height, use the analytic limiting expression.
    if np.isclose(energy, barrier, rtol=1e-12, atol=0.0):
        denominator = 1.0 + (
            M_E * barrier * width**2 / (2.0 * HBAR**2)
        )
        return float(1.0 / denominator)

    if energy < barrier:
        # Below-barrier tunnelling.
        kappa = np.sqrt(2.0 * M_E * (barrier - energy)) / HBAR
        argument = kappa * width

        factor = barrier**2 / (
            4.0 * energy * (barrier - energy)
        )

        # T = 1 / [1 + factor * sinh(argument)^2]
        denominator = 1.0 + factor * np.sinh(argument)**2
        result = 1.0 / denominator

    else:
        # Above-barrier transmission with wave interference.
        wave_number = np.sqrt(
            2.0 * M_E * (energy - barrier)
        ) / HBAR

        argument = wave_number * width

        factor = barrier**2 / (
            4.0 * energy * (energy - barrier)
        )

        # T = 1 / [1 + factor * sin(argument)^2]
        denominator = 1.0 + factor * np.sin(argument)**2
        result = 1.0 / denominator

    return float(np.clip(result, 0.0, 1.0))


def calculate(p):
    """Return the standard six-value QUANTUM LAB result."""

    energy_ev = float(p["energy_ev"])
    barrier_ev = float(p["barrier_ev"])
    width_nm = float(p["width_nm"])

    if energy_ev <= 0:
        raise ValueError("Particle energy must be greater than zero.")
    if barrier_ev < 0:
        raise ValueError("Barrier height cannot be negative.")
    if width_nm < 0:
        raise ValueError("Barrier width cannot be negative.")

    transmission = transmission_probability(
        energy_ev, barrier_ev, width_nm
    )

    widths = np.linspace(0.0, 2.0, 401)

    curve = np.array([
        transmission_probability(energy_ev, barrier_ev, w)
        for w in widths
    ])

    if energy_ev < barrier_ev:
        regime = "Below barrier: quantum tunnelling."
        explanation = (
            "Transmission decreases as the barrier becomes wider. "
            "A finite barrier can have nonzero transmission even when "
            "the particle energy is below its height."
        )
    elif energy_ev > barrier_ev:
        regime = "Above barrier: wave transmission."
        explanation = (
            "The particle energy exceeds the barrier height. "
            "The transmission can still vary with width because of "
            "wave reflection and interference at the barrier boundaries."
        )
    else:
        regime = "At the barrier height."
        explanation = (
            "The transmission is calculated using the limiting "
            "rectangular-barrier expression at E = V₀."
        )

    summary = (
        f"{regime}\n"
        f"Particle energy: {energy_ev:.4g} eV\n"
        f"Barrier height: {barrier_ev:.4g} eV\n"
        f"Barrier width: {width_nm:.4g} nm\n"
        f"Transmission probability: {transmission:.6g}\n"
        f"Transmission percentage: {transmission * 100:.6g}%\n"
        f"{explanation}\n"
        "Model: exact transmission for an ideal 1D rectangular "
        "barrier, assuming an electron and equal potentials outside "
        "the barrier."
    )

    return (
        widths,
        curve,
        "Barrier width (nm)",
        "Transmission probability",
        summary,
        ("Barrier width (nm)", "Transmission probability"),
    )