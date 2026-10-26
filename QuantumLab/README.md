# QUANTUM LAB — Virtual Quantum Physics Laboratory

An educational desktop application for a science exhibition, built with Python, PySide6, NumPy, and Matplotlib.

## Features
- Double-slit interference and diffraction model
- Photoelectric-effect model
- Particle in a one-dimensional infinite box
- Exact 1D rectangular-barrier quantum tunnelling model
- Hydrogen-like orbital probability-density cross-sections
- Harmonic-oscillator stationary states
- Numerical finite-well eigenstates using a finite-difference Schrödinger solver
- Live graphs/visualizations
- Guided tutorials
- CSV export
- Full-screen exhibition mode
- Dashboard and in-app operating guide
- Scientific assumptions/limitations documentation and analytical benchmark tests
- Lab notebook: record runs, save/load portable JSON sessions, and compare scalar curve metrics
- Repeatable quantum-measurement statistics experiment and Markdown session reports
- Offline animated concept demonstrations for every experiment; no video downloads or internet connection required

## Requirements
- Python 3.10 or newer
- Windows, macOS, or Linux with a graphical desktop
- Packages listed in `requirements.txt`

## Setup on Windows PowerShell
Open PowerShell in the `QUANTUM_LAB` folder.

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python main.py
```

If your virtual environment already exists and imports have been verified, do not recreate it; activate it and install requirements with `python -m pip`.

## How to operate
1. Start the app with `python main.py`.
2. Select an experiment in the left-side experiment library, or click an experiment card on the dashboard.
3. Adjust the parameters. Graphs update automatically.
4. Use **Guided tutorial** to read the experiment steps and physics concepts.
5. Use **Export CSV** to save the plotted data, parameters, and result interpretation.
6. Use **Exhibition mode** for a full-screen demonstration. Press Escape to exit.

## Project layout
- `main.py`: application entry point
- `core/physics.py`: experiment metadata and calculation routing
- `experiments/`: separate numerical models for each experiment
- `ui/main_window.py`: dashboard, navigation, help, and exhibition mode
- `ui/experiment_widget.py`: parameter controls, live plots, and CSV export
- `ui/tutorial_dialog.py`: guided tutorial window
- `assets/`: reserved for optional application icons and media

## Scientific scope and limitations
These are simplified educational models. The double-slit plot is a normalized far-field-style approximation with a single-slit envelope. The photoelectric plot uses Einstein's photon-energy relation. The particle-in-a-box model is a 1D infinite well for an electron. Tunnelling uses exact stationary transmission through a rectangular barrier. Orbital plots show relative hydrogen probability-density cross-sections. The numerical finite-well solver uses a fixed finite-difference grid and fixed boundary conditions. The app is intended for teaching and exhibition, not precision research. Read `SCIENTIFIC_NOTES.md` for assumptions, equations, and numerical limitations.

## Validation

After installing the requirements, run:

```powershell
python -m unittest discover -s tests -v
```

The validation suite checks physical limiting cases, probability normalisation, known analytical energy relationships, the finite-difference solver, and the public output contract of every experiment.

## Lab notebook (Phases 10–15)

Use **Record run** to add the current model configuration to the temporary notebook. **Save session** writes the recorded settings, summaries, timestamps, and scalar metrics to a portable JSON file; **Load session** restores the notebook and active experiment settings. The notebook has curated presets for selected experiments, intended for clear side-by-side demonstrations. See `PHASES_10_TO_15.md` for scope and limitations.

## Final release features (Phases 16–21)

The final release adds a seeded quantum-measurement statistics demonstration, SHA-256 integrity checking for newly saved sessions, and **Export report** for a readable Markdown summary of the recorded session. Read `PHASES_16_TO_21.md` for the final scope and scientific limitations.

## Troubleshooting
- If `ModuleNotFoundError` appears, activate `.venv` and run `python -m pip install -r requirements.txt`.
- If the app cannot open, check that the command is run from the project folder and that the Python environment is activated.
