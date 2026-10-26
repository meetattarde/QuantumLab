import numpy as np

def calculate(p):
    wavelength = p["wavelength_nm"] * 1e-9
    separation = p["slit_separation_um"] * 1e-6
    distance = p["screen_distance_m"]
    width = p["slit_width_um"] * 1e-6
    x = np.linspace(-0.025, 0.025, 1600)
    theta = np.arctan2(x, distance)
    beta = np.pi * width * np.sin(theta) / wavelength
    alpha = np.pi * separation * np.sin(theta) / wavelength
    envelope = np.ones_like(beta)
    mask = np.abs(beta) > 1e-10
    envelope[mask] = (np.sin(beta[mask]) / beta[mask]) ** 2
    interference = np.cos(alpha) ** 2
    y = envelope * interference
    y /= max(float(np.max(y)), 1e-12)
    fringe_spacing = wavelength * distance / separation
    summary = f"Approx. fringe spacing: {fringe_spacing * 1e3:.2f} mm. Intensity is normalized; finite slit width adds a diffraction envelope."
    return x * 1000, y, "Position on screen (mm)", "Normalized intensity", summary, ("Position (mm)", "Normalized intensity")
