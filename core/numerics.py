"""Reusable, validated numerical tools for one-dimensional quantum models.

The solver deliberately favours transparent finite-difference mathematics over
high-performance production algorithms.  It is suitable for education and for
small exploratory calculations; boundary conditions are Dirichlet (psi=0).
"""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np

HBAR = 1.054_571_817e-34
M_E = 9.109_383_7015e-31
EV = 1.602_176_634e-19


@dataclass(frozen=True)
class EigenSystem:
    """Lowest stationary states of a discretised one-dimensional Hamiltonian."""
    x_m: np.ndarray
    energies_ev: np.ndarray
    states: np.ndarray


def validate_finite(name: str, value: float, *, positive: bool = False) -> float:
    value = float(value)
    if not np.isfinite(value) or (positive and value <= 0):
        qualifier = "a finite positive" if positive else "a finite"
        raise ValueError(f"{name} must be {qualifier} number.")
    return value


def normalize_wavefunction(psi: np.ndarray, x_m: np.ndarray) -> np.ndarray:
    """Return psi normalised so integral |psi|^2 dx is one."""
    norm = float(np.trapezoid(np.abs(psi) ** 2, x_m))
    if norm <= 0 or not np.isfinite(norm):
        raise ValueError("Wavefunction cannot be normalised.")
    return psi / np.sqrt(norm)


def solve_stationary_1d(x_m, potential_ev, *, mass_kg=M_E, states=4) -> EigenSystem:
    """Solve H psi = E psi with a central-difference kinetic operator.

    ``x_m`` must be a uniform one-dimensional grid.  The returned states omit
    the fixed zero-valued edge points and are individually normalised.
    """
    x = np.asarray(x_m, dtype=float)
    potential = np.asarray(potential_ev, dtype=float)
    mass = validate_finite("Mass", mass_kg, positive=True)
    if x.ndim != 1 or potential.shape != x.shape or x.size < 5:
        raise ValueError("Grid and potential must be matching 1D arrays with at least five points.")
    dx = np.diff(x)
    if np.any(dx <= 0) or not np.allclose(dx, dx[0], rtol=1e-8, atol=0.0):
        raise ValueError("The spatial grid must be strictly increasing and uniform.")
    if not np.all(np.isfinite(potential)):
        raise ValueError("Potential must contain only finite values.")
    count = int(states)
    if count < 1 or count > x.size - 2:
        raise ValueError("Requested state count is outside the grid capacity.")

    n = x.size - 2
    coefficient = HBAR ** 2 / (2.0 * mass * dx[0] ** 2) / EV
    diagonal = 2.0 * coefficient + potential[1:-1]
    off_diagonal = np.full(n - 1, -coefficient)
    hamiltonian = np.diag(diagonal) + np.diag(off_diagonal, 1) + np.diag(off_diagonal, -1)
    energies, vectors = np.linalg.eigh(hamiltonian)

    result = np.zeros((count, x.size), dtype=float)
    for index in range(count):
        result[index, 1:-1] = vectors[:, index]
        result[index] = normalize_wavefunction(result[index], x)
    return EigenSystem(x, energies[:count], result)


def crank_nicolson_step(psi, potential_ev, dx_m, dt_s, *, mass_kg=M_E):
    """Advance a wavefunction one stable Crank--Nicolson time step.

    Fixed zero endpoints are imposed.  This routine is intentionally exposed
    for future experiments and benchmark tests.
    """
    psi = np.asarray(psi, dtype=complex)
    potential = np.asarray(potential_ev, dtype=float)
    if psi.ndim != 1 or potential.shape != psi.shape or psi.size < 5:
        raise ValueError("Wavefunction and potential must be matching 1D arrays.")
    dx = validate_finite("Grid spacing", dx_m, positive=True)
    dt = validate_finite("Time step", dt_s, positive=True)
    mass = validate_finite("Mass", mass_kg, positive=True)
    n = psi.size - 2
    kinetic = HBAR ** 2 / (2.0 * mass * dx ** 2) / EV
    h = np.diag(2 * kinetic + potential[1:-1]).astype(complex)
    h += np.diag(np.full(n - 1, -kinetic), 1) + np.diag(np.full(n - 1, -kinetic), -1)
    factor = 1j * dt * EV / (2 * HBAR)
    identity = np.eye(n, dtype=complex)
    next_interior = np.linalg.solve(identity + factor * h, (identity - factor * h) @ psi[1:-1])
    next_psi = np.zeros_like(psi, dtype=complex)
    next_psi[1:-1] = next_interior
    return next_psi
