"""A reproducible Bernoulli-measurement simulation for quantum probabilities."""
import numpy as np


def calculate(p):
    probability = float(p["probability"])
    trials = int(round(float(p["trials"])))
    seed = int(round(float(p["seed"])))
    if not 0.0 <= probability <= 1.0:
        raise ValueError("Measurement probability must be between 0 and 1.")
    if trials < 10 or trials > 2000:
        raise ValueError("Number of trials must be between 10 and 2000.")
    rng = np.random.default_rng(seed)
    outcomes = rng.random(trials) < probability
    running_mean = np.cumsum(outcomes, dtype=float) / np.arange(1, trials + 1)
    measured = float(running_mean[-1])
    standard_error = float(np.sqrt(max(probability * (1 - probability), 0.0) / trials))
    summary = (
        f"Predicted probability: {probability:.4g}\n"
        f"Measured fraction after {trials} trials: {measured:.4g}\n"
        f"Binomial standard error (using predicted probability): {standard_error:.4g}\n"
        f"Random seed: {seed}\n"
        "Model: independent binary quantum-measurement outcomes. The seed is included so this demonstration is reproducible."
    )
    return (
        np.arange(1, trials + 1), running_mean, "Measurement number",
        "Running measured probability", summary,
        ("Measurement number", "Running measured probability"),
    )
