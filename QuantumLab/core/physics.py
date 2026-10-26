"""Numerical models used by QUANTUM LAB. These are educational models, not research software."""
import numpy as np
from experiments.double_slit import calculate as double_slit
from experiments.photoelectric import calculate as photoelectric
from experiments.particle_box import calculate as particle_box
from experiments.tunnelling import calculate as tunnelling
from experiments.atomic_orbitals import calculate as atomic_orbitals
from experiments.atomic_orbitals import get_orbital_options
from experiments.uncertainty_principle import calculate as uncertainty_principle
from experiments.harmonic_oscillator import calculate as harmonic_oscillator
from experiments.numerical_well import calculate as numerical_well
from experiments.measurement_statistics import calculate as measurement_statistics

EXPERIMENTS = {
    "Double-slit experiment": {
        "description": "Explore how two coherent slits produce an interference pattern.",
        "controls": [
            {"key": "wavelength_nm", "label": "Wavelength (nm)", "min": 380, "max": 700, "value": 500, "step": 10},
            {"key": "slit_separation_um", "label": "Slit separation (µm)", "min": 5, "max": 100, "value": 30, "step": 1},
            {"key": "screen_distance_m", "label": "Screen distance (m)", "min": 0.5, "max": 3, "value": 1, "step": 0.1},
            {"key": "slit_width_um", "label": "Slit width (µm)", "min": 1, "max": 30, "value": 8, "step": 1},
        ],
        "calculate": double_slit,
        "tutorial": [
            "A coherent source illuminates two narrow slits.",
            "Waves from the slits overlap. Their phase difference creates bright and dark fringes.",
            "Change wavelength, slit separation, and screen distance. Longer wavelength or greater screen distance increases fringe spacing.",
            "The plotted curve is normalized intensity, including a single-slit diffraction envelope."
        ],
    },
    "Photoelectric effect": {
        "description": "Investigate how light frequency and work function affect emitted electrons.",
        "controls": [
            {"key": "frequency_1e14_hz", "label": "Frequency (×10¹⁴ Hz)", "min": 3, "max": 12, "value": 8, "step": 0.1},
            {"key": "work_function_ev", "label": "Work function (eV)", "min": 1, "max": 5, "value": 2.3, "step": 0.1},
            {"key": "intensity", "label": "Relative intensity", "min": 0.2, "max": 5, "value": 2, "step": 0.1},
        ],
        "calculate": photoelectric,
        "tutorial": [
            "Photons carry energy E = hf. Electrons are emitted only when photon energy is at least the material's work function.",
            "The maximum kinetic energy is Kmax = hf − φ when the result is positive.",
            "Frequency controls photon energy; intensity mainly affects the number of emitted electrons in this simplified model.",
            "Move frequency below the threshold to see emission stop."
        ],
    },
    "Particle in a box": {
        "description": "View stationary-state probability densities for a particle in a one-dimensional infinite well.",
        "controls": [
            {"key": "quantum_number", "label": "Quantum number n", "min": 1, "max": 8, "value": 2, "step": 1},
            {"key": "box_length_nm", "label": "Box length (nm)", "min": 0.2, "max": 3, "value": 1, "step": 0.1},
        ],
        "calculate": particle_box,
        "tutorial": [
            "The particle is confined between two infinitely high potential walls.",
            "Only discrete stationary states are allowed. The quantum number n determines the number of half-wavelengths in the box.",
            "Probability density is |ψ|², so it is never negative and integrates to one.",
            "For an ideal box, energy is proportional to n² and inversely proportional to box length squared."
        ],
    },
    "Quantum tunnelling": {
        "description": "Explore transmission through a rectangular potential barrier in a simplified 1D model.",
        "controls": [
            {"key": "energy_ev", "label": "Particle energy (eV)", "min": 0.1, "max": 8, "value": 2, "step": 0.1},
            {"key": "barrier_ev", "label": "Barrier height (eV)", "min": 0.5, "max": 10, "value": 5, "step": 0.1},
            {"key": "width_nm", "label": "Barrier width (nm)", "min": 0.1, "max": 2, "value": 0.6, "step": 0.1},
        ],
        "calculate": tunnelling,
        "tutorial": [
            "Classically, a particle with energy below a barrier cannot cross it.",
            "Quantum mechanics predicts a wavefunction inside the barrier, allowing a nonzero transmission probability.",
            "For a rectangular barrier, the exact transmission probability depends on particle energy, barrier height, and width.",
            "Below the barrier, transmission generally decreases rapidly as width or height increases.",
            "Above the barrier, wave reflection and interference can also make transmission vary with barrier width.",
            "This is an ideal one-dimensional rectangular-barrier model for an electron, not a complete simulation of every physical barrier.",
        ],
    },
    
    "Heisenberg uncertainty principle": {
        "description": (
            "Explore how position and momentum uncertainties are related "
            "in a minimum-uncertainty Gaussian wave packet."
        ),
        "controls": [
            {
                "key": "sigma_x_nm",
                "label": "Position uncertainty Δx (nm)",
                "min": 0.1,
                "max": 2.0,
                "value": 0.5,
                "step": 0.1,
            },
        ],
        "calculate": uncertainty_principle,
        "tutorial": [
            "Quantum particles cannot have arbitrarily small uncertainties "
            "in both position and momentum.",
            "The Heisenberg uncertainty relation is Δx·Δp ≥ ħ/2.",
            "For this ideal Gaussian wave packet, Δx·Δp = ħ/2.",
            "Reducing the position uncertainty increases the momentum uncertainty.",
            "The plotted curve is a normalized position probability density, "
            "not a particle trajectory.",
        ],
    },
    "Quantum harmonic oscillator": {
        "description": "Explore exact stationary states of a particle in a one-dimensional quadratic potential.",
        "controls": [
            {"key": "quantum_number", "label": "State n", "min": 0, "max": 8, "value": 0, "step": 1},
            {"key": "frequency_thz", "label": "Oscillator frequency (THz)", "min": 1, "max": 100, "value": 20, "step": 1},
        ],
        "calculate": harmonic_oscillator,
        "tutorial": [
            "A harmonic oscillator has a quadratic potential and equally spaced energy levels.",
            "The ground state has nonzero energy: E0 = hbar omega / 2.",
            "Higher states have progressively more nodes in their wavefunction.",
            "This is an exact one-dimensional model for an electron in an ideal quadratic potential.",
        ],
    },
    "Numerical finite well": {
        "description": "Solve stationary states of a finite square well with a finite-difference Schrödinger solver.",
        "controls": [
            {"key": "well_width_nm", "label": "Well width (nm)", "min": 0.2, "max": 5, "value": 1, "step": 0.1},
            {"key": "well_depth_ev", "label": "Well depth (eV)", "min": 1, "max": 50, "value": 15, "step": 1},
            {"key": "state_index", "label": "State index", "min": 0, "max": 3, "value": 0, "step": 1},
        ],
        "calculate": numerical_well,
        "tutorial": [
            "This experiment discretises space and diagonalises a Hamiltonian matrix.",
            "A finite well can support bound states with negative energy and wavefunction tails outside the well.",
            "Use the state control to compare the lowest numerical eigenstates.",
            "The result depends slightly on grid resolution and boundary placement; this is a numerical-model limitation.",
        ],
    },
    "Quantum measurement statistics": {
        "description": "Simulate repeated binary quantum measurements and observe statistical convergence.",
        "controls": [
            {"key": "probability", "label": "Predicted probability", "min": 0, "max": 1, "value": 0.5, "step": 0.05},
            {"key": "trials", "label": "Measurements", "min": 10, "max": 2000, "value": 200, "step": 10},
            {"key": "seed", "label": "Random seed", "min": 0, "max": 9999, "value": 42, "step": 1},
        ],
        "calculate": measurement_statistics,
        "tutorial": [
            "Quantum theory predicts probabilities for individual outcomes, not a deterministic result for each measurement.",
            "This model treats each measurement as an independent binary outcome with the chosen probability.",
            "As the number of measurements grows, the running fraction usually approaches the predicted probability.",
            "Use the random seed to make a particular demonstration repeatable, then change it to compare another sample.",
        ],
    },
    
   "Atomic orbitals": {
    "description": (
        "Explore hydrogen-like s, p, d and f orbitals, their orientations, "
        "radial nodes, and relative probability-density cross-sections."
    ),
    "controls": [
        {
            "key": "orbital",
            "label": "Orbital state",
            "type": "choice",
            "options": get_orbital_options(),
            "value": "1s",
        },
        {
            "key": "scale_bohr",
            "label": "View scale (Bohr radii)",
            "min": 2,
            "max": 12,
            "value": 6,
            "step": 1,
        },
    ],
    "calculate": atomic_orbitals,
    "tutorial": [
        "An orbital is a quantum state, not a fixed path followed by an electron.",
        "Choose an allowed orbital state from the selector. The list includes s, p, d and f orbital families up to n = 7.",
        "The principal quantum number n affects the radial distribution. The angular-momentum quantum number l determines the orbital family.",
        "Radial nodes are spherical regions where the radial wavefunction is zero; angular nodes depend on orbital shape and orientation.",
        "The image is a representative two-dimensional cross-section of relative probability density, not a complete three-dimensional orbital.",
        "The displayed density is scaled for visual comparison and should not be interpreted as an absolute probability."
    ],
    },
}


def run_experiment(name, params):
    """Return x, y, x-axis label, y-axis label, result summary, and CSV column labels."""
    if name not in EXPERIMENTS:
        raise KeyError(f"Unknown experiment: {name}")
    return EXPERIMENTS[name]["calculate"](params)
