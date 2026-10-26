import numpy as np

H_EV_S = 4.135667696e-15
C = 299792458

def calculate(p):
    frequency = p["frequency_1e14_hz"] * 1e14
    work = p["work_function_ev"]
    intensity = p["intensity"]
    threshold = work / H_EV_S
    photon_energy = H_EV_S * frequency
    kmax = max(0.0, photon_energy - work)
    x = np.linspace(2.5, 12.5, 500)
    y = np.maximum(H_EV_S * x * 1e14 - work, 0)
    summary = (
        f"Photon energy: {photon_energy:.2f} eV | Threshold frequency: {threshold / 1e14:.2f} ×10¹⁴ Hz | "
        f"Maximum kinetic energy: {kmax:.2f} eV. "
        + ("Emission predicted." if photon_energy >= work else "Below threshold: no photoelectrons predicted.")
        + f" Relative intensity setting: {intensity:.1f} (qualitative count indicator)."
    )
    return x, y, "Light frequency (×10¹⁴ Hz)", "Maximum kinetic energy (eV)", summary, ("Frequency (×10¹⁴ Hz)", "Maximum kinetic energy (eV)")
