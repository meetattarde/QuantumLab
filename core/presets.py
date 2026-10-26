"""Curated parameter sets that support quick demonstrations and comparisons."""

PRESETS = {
    "Double-slit experiment": {
        "Wide fringes": {"wavelength_nm": 650, "slit_separation_um": 15, "screen_distance_m": 2.0, "slit_width_um": 8},
        "Fine fringes": {"wavelength_nm": 420, "slit_separation_um": 80, "screen_distance_m": 1.0, "slit_width_um": 8},
    },
    "Photoelectric effect": {
        "Below threshold": {"frequency_1e14_hz": 4.0, "work_function_ev": 2.3, "intensity": 2.0},
        "Strong emission": {"frequency_1e14_hz": 10.0, "work_function_ev": 2.3, "intensity": 4.0},
    },
    "Quantum tunnelling": {
        "Narrow barrier": {"energy_ev": 2.0, "barrier_ev": 5.0, "width_nm": 0.2},
        "Wide barrier": {"energy_ev": 2.0, "barrier_ev": 5.0, "width_nm": 1.5},
    },
    "Numerical finite well": {
        "Deep ground state": {"well_width_nm": 1.0, "well_depth_ev": 30.0, "state_index": 0},
        "Shallow excited state": {"well_width_nm": 2.0, "well_depth_ev": 8.0, "state_index": 1},
    },
}


def names_for(experiment: str) -> list[str]:
    return list(PRESETS.get(experiment, {}))
