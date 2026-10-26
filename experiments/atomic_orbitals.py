"""Hydrogen-like atomic orbital probability-density cross-sections.

Educational model in Bohr-radius units. The viewer displays 2D slices,
not complete 3D orbital volumes.
"""

import numpy as np
import re

MAX_PRINCIPAL_N = 7


def get_orbital_options():
    """Return (display label, calculation code) for valid orbitals."""
    orientations = {
        0: [("s", "s")],
        1: [("pₓ", "p_x"), ("pᵧ", "p_y"), ("p_z", "p_z")],
        2: [
            ("dₓᵧ", "d_xy"),
            ("dₓ𝑧", "d_xz"),
            ("dᵧ𝑧", "d_yz"),
            ("dₓ²₋ᵧ²", "d_x2_y2"),
            ("d_z²", "d_z2"),
        ],
        3: [
            ("f_xyz", "f_xyz"),
            ("f_z(x²−y²)", "f_z_x2_y2"),
            ("f_x(x²−3y²)", "f_x_x2_3y2"),
            ("f_y(3x²−y²)", "f_y_3x2_y2"),
            ("f_z(5z²−3r²)", "f_z3"),
            ("f_x(5z²−r²)", "f_xz2"),
            ("f_y(5z²−r²)", "f_yz2"),
        ],
    }

    options = []
    for n in range(1, MAX_PRINCIPAL_N + 1):
        for l in range(min(n, 4)):
            for display, suffix in orientations[l]:
                code = f"{n}{suffix}"
                options.append((f"{n}{display}", code))
    return options


def _associated_laguerre(k, alpha, x):
    """Generalized Laguerre polynomial L_k^alpha(x), via recurrence."""
    if k == 0:
        return np.ones_like(x, dtype=float)

    previous = np.ones_like(x, dtype=float)
    current = 1.0 + alpha - x

    if k == 1:
        return current

    for j in range(1, k):
        following = (
            (2 * j + alpha + 1 - x) * current
            - (j + alpha) * previous
        ) / (j + 1)
        previous, current = current, following

    return current


def _cross_section(code, X, Y):
    """Map the plot grid to a representative plane through the orbital."""
    suffix = re.sub(r"^\d+", "", code)

    if suffix in ("p_z", "d_xz", "d_z2", "f_z3",
                 "f_xz2", "f_z_x2_y2"):
        return X, np.zeros_like(X), Y

    if suffix in ("d_yz", "f_yz2"):
        return np.zeros_like(X), X, Y

    if suffix == "f_xyz":
        # An oblique plane avoids the xyz nodal plane.
        return X, Y, (X + Y) / np.sqrt(2.0)

    # xy-plane slices for s, p_x, p_y, d_xy, d_x2_y2,
    # f_x(x²−3y²), and f_y(3x²−y²).
    return X, Y, np.zeros_like(X)


def _angular_factor(code, x, y, z, r):
    """Real spherical-harmonic shape factors, up to constants."""
    suffix = re.sub(r"^\d+", "", code)
    safe_r = np.where(r > 1e-12, r, 1.0)

    xn = x / safe_r
    yn = y / safe_r
    zn = z / safe_r

    if suffix == "s":
        return np.ones_like(r)

    if suffix == "p_x":
        return xn
    if suffix == "p_y":
        return yn
    if suffix == "p_z":
        return zn

    if suffix == "d_xy":
        return xn * yn
    if suffix == "d_xz":
        return xn * zn
    if suffix == "d_yz":
        return yn * zn
    if suffix == "d_x2_y2":
        return xn**2 - yn**2
    if suffix == "d_z2":
        return 3 * zn**2 - 1

    if suffix == "f_xyz":
        return xn * yn * zn
    if suffix == "f_z_x2_y2":
        return zn * (xn**2 - yn**2)
    if suffix == "f_x_x2_3y2":
        return xn * (xn**2 - 3 * yn**2)
    if suffix == "f_y_3x2_y2":
        return yn * (3 * xn**2 - yn**2)
    if suffix == "f_z3":
        return zn * (5 * zn**2 - 3)
    if suffix == "f_xz2":
        return xn * (5 * zn**2 - 1)
    if suffix == "f_yz2":
        return yn * (5 * zn**2 - 1)

    raise ValueError(f"Unsupported orbital: {code}")


def calculate(p):
    code = str(p["orbital"]).strip()
    scale = float(p["scale_bohr"])

    if not np.isfinite(scale) or scale <= 0:
        raise ValueError("View scale must be a positive finite number.")

    valid_codes = {value for _, value in get_orbital_options()}
    if code not in valid_codes:
        raise ValueError(f"Invalid orbital selection: {code}")

    n = int(re.match(r"^\d+", code).group())
    suffix = re.sub(r"^\d+", "", code)

    if suffix == "s":
        l = 0
    elif suffix.startswith("p_"):
        l = 1
    elif suffix.startswith("d_"):
        l = 2
    else:
        l = 3

    if n < l + 1:
        raise ValueError("The selected orbital is not allowed for this n.")

    axis = np.linspace(-scale, scale, 300)
    X, Y = np.meshgrid(axis, axis)
    x, y, z = _cross_section(code, X, Y)
    r = np.sqrt(x**2 + y**2 + z**2)

    # Hydrogenic radial dependence, using a0 = 1 and nuclear charge Z = 1.
    rho = 2.0 * r / n
    laguerre = _associated_laguerre(n - l - 1, 2 * l + 1, rho)
    radial = np.exp(-rho / 2.0) * rho**l * laguerre

    angular = _angular_factor(code, x, y, z, r)
    density = np.square(radial * angular)

    peak = float(np.max(density))
    if peak > 0:
        density /= peak

    label = f"Hydrogen-like {code} orbital — relative probability density"
    summary = (
        f"Orbital {code}: principal quantum number n={n}, "
        f"angular-momentum quantum number l={l}. "
        f"This is a representative 2D cross-section of an idealized "
        f"hydrogen-like probability density, normalized to a displayed "
        f"maximum of 1. The view extends to ±{scale:g} Bohr radii. "
        f"It is not a complete 3D orbital or an electron trajectory."
    )

    headers = (
        "Cross-section coordinate 1 (Bohr radii)",
        "Cross-section coordinate 2 (Bohr radii)",
        "Relative probability density",
    )

    return (
        (X, Y, density),
        None,
        "Cross-section coordinate 1 (Bohr radii)",
        label,
        summary,
        headers,
    )