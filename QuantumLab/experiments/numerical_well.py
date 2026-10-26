"""Finite-difference eigenstates of a finite one-dimensional square well."""
import numpy as np

from core.numerics import solve_stationary_1d, validate_finite


def calculate(p):
    width_nm = validate_finite("Well width", p["well_width_nm"], positive=True)
    depth_ev = validate_finite("Well depth", p["well_depth_ev"], positive=True)
    state = int(round(float(p["state_index"])))
    if state < 0 or state > 3:
        raise ValueError("State index must be between 0 and 3.")
    extent_nm = max(5.0, 3.0 * width_nm)
    x_nm = np.linspace(-extent_nm, extent_nm, 401)
    potential = np.where(np.abs(x_nm) <= width_nm / 2, -depth_ev, 0.0)
    solution = solve_stationary_1d(x_nm * 1e-9, potential, states=4)
    density = solution.states[state] ** 2
    energy = solution.energies_ev[state]
    bound = "bound" if energy < 0 else "box-discretised continuum-like"
    summary = (f"Numerical state {state} | Energy: {energy:.6g} eV ({bound})\n"
               f"Well width: {width_nm:g} nm | Well depth: {depth_ev:g} eV\n"
               "Method: central finite-difference Hamiltonian with fixed zero boundaries. Results converge as the grid is refined.")
    return x_nm, density * 1e-9, "Position (nm)", "Probability density (nm⁻¹)", summary, ("Position (nm)", "Probability density (nm^-1)")
