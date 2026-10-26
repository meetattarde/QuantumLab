import numpy as np

HBAR = 1.054571817e-34
M_E = 9.1093837e-31
EV = 1.602176634e-19

def calculate(p):
    n = int(round(p["quantum_number"]))
    length_nm = p["box_length_nm"]
    length = length_nm * 1e-9
    x_nm = np.linspace(0, length_nm, 800)
    x = x_nm * 1e-9
    psi = np.sqrt(2 / length) * np.sin(n * np.pi * x / length)
    prob = psi ** 2
    energy = (n**2 * np.pi**2 * HBAR**2) / (2 * M_E * length**2) / EV
    summary = f"State n={n} | Energy: {energy:.4f} eV | Number of internal nodes: {n-1}. Energy assumes an electron in an ideal 1D infinite well."
    return x_nm, prob / max(float(np.max(prob)), 1e-12), "Position in box (nm)", "Relative probability density", summary, ("Position (nm)", "Relative probability density")
