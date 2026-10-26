# Scientific scope, validation, and numerical methods

QUANTUM LAB is an educational simulation. Values are calculated in SI units internally unless an axis explicitly says otherwise. The models intentionally trade experimental detail for transparent, inspectable equations.

## Model catalogue

| Experiment | Model | Main limitations |
|---|---|---|
| Double slit | Far-field two-slit interference with a single-slit envelope | Assumes coherent monochromatic light and neglects detector geometry. |
| Photoelectric effect | Einstein relation `Kmax = hf - phi` | Intensity is qualitative; no material band structure or collection voltage. |
| Particle in a box | Electron in a 1D infinite well | Infinite walls and a single non-interacting particle. |
| Tunnelling | Exact 1D rectangular barrier transmission | Electron, stationary plane waves, equal exterior potentials. |
| Atomic orbitals | Hydrogen-like relative 2D density slices | One-electron model; images are not 3D probability volumes. |
| Uncertainty | Minimum-uncertainty Gaussian packet | Saturates the bound; general states need not. |
| Harmonic oscillator | Exact 1D electron oscillator | Ideal quadratic potential. |
| Numerical finite well | Finite-difference stationary Schrödinger equation | Fixed boundaries and a finite grid create discretisation error. |

## Numerical solver

`core.numerics.solve_stationary_1d` constructs a central-difference Hamiltonian and diagonalises it with NumPy. `crank_nicolson_step` provides a norm-preserving time-step foundation. Tests include normalisation, a square-well energy benchmark, and a Crank–Nicolson norm check.

## Validation practice

Run `python -m unittest discover -s tests -v`. The tests cover known limits (zero-width barrier, photoelectric threshold, box energy scaling, Gaussian uncertainty bound), probability normalisation, solver accuracy, and every experiment's public calculation contract.
