from html import escape

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QWidget,
    QFrame,
)
from PySide6.QtCore import Qt


# Scientific learning content for all five experiments.
# These explanations complement the existing experiment calculations.

SCIENCE_CONTENT = {
    "Double-slit experiment": {
        "aim": "Explore how light passing through two slits produces an interference pattern.",
        "theory": (
            "Waves from the two slits overlap. Where their phase difference "
            "produces constructive interference, bright fringes form; where "
            "it produces destructive interference, dark fringes form. "
            "This experiment demonstrates wave interference and, in quantum "
            "experiments with individual particles, wave-particle duality."
        ),
        "equations": [
            "<b>Fringe spacing:</b> &Delta;y = &lambda;L / d",
            "<b>Approximate intensity:</b> I(y) &prop; cos<sup>2</sup>"
            "(&pi;dy / &lambda;L)",
        ],
        "symbols": (
            "&lambda; = wavelength; L = distance from the slits to the screen; "
            "d = separation between the slits; &Delta;y = spacing between "
            "adjacent bright fringes; y = position on the screen."
        ),
        "observations": [
            "Increasing the wavelength increases fringe spacing.",
            "Increasing the slit separation decreases fringe spacing.",
            "Increasing the screen distance increases fringe spacing.",
            "Real slit widths can produce a diffraction envelope around "
            "the interference fringes."
        ],
        "applications": (
            "Wave optics, interferometry, precision measurements, and "
            "experiments investigating the quantum behaviour of matter."
        ),
        "conclusion": (
            "The pattern results from the superposition of waves. The simple "
            "fringe-spacing equation assumes small angles and an ideal setup."
        ),
    },

    "Photoelectric effect": {
        "aim": (
            "Investigate how the frequency of incident light affects the "
            "emission and maximum kinetic energy of photoelectrons."
        ),
        "theory": (
            "Light transfers energy in packets called photons. An electron "
            "can escape a material if a photon supplies at least the work "
            "function energy. Any energy remaining becomes the electron's "
            "maximum kinetic energy in the basic Einstein model."
        ),
        "equations": [
            "<b>Photon energy:</b> E = hf",
            "<b>Einstein's equation:</b> K<sub>max</sub> = hf &minus; &phi;",
            "<b>Threshold frequency:</b> f<sub>0</sub> = &phi; / h",
        ],
        "symbols": (
            "h = Planck's constant; f = light frequency; &phi; = work function "
            "of the material; K<sub>max</sub> = maximum kinetic energy; "
            "f<sub>0</sub> = threshold frequency."
        ),
        "observations": [
            "Below the threshold frequency, the ideal model predicts no "
            "photoelectron emission, regardless of light intensity.",
            "Above the threshold, increasing frequency increases maximum "
            "kinetic energy.",
            "Increasing intensity mainly increases the number of emitted "
            "electrons when the frequency is above threshold."
        ],
        "applications": (
            "Photodetectors, light sensors, photoelectric measurement "
            "systems, and understanding the particle properties of light."
        ),
        "conclusion": (
            "The photoelectric effect supports the photon model of light. "
            "The result also depends on the material's work function."
        ),
    },

    "Particle in a box": {
        "aim": (
            "Explore how confinement produces discrete energy levels and "
            "position-dependent probability densities."
        ),
        "theory": (
            "A particle confined between two infinitely high potential "
            "walls can occupy only particular stationary quantum states. "
            "The wavefunction must vanish at both walls. Its squared "
            "magnitude gives the probability density for position."
        ),
        "equations": [
            "<b>Allowed energies:</b> "
            "E<sub>n</sub> = n<sup>2</sup>h<sup>2</sup> / (8mL<sup>2</sup>)",
            "<b>Wavefunction:</b> "
            "&psi;<sub>n</sub>(x) = &radic;(2/L) "
            "sin(n&pi;x/L)",
            "<b>Probability density:</b> P(x) = |&psi;<sub>n</sub>(x)|<sup>2</sup>",
        ],
        "symbols": (
            "n = positive integer quantum number; h = Planck's constant; "
            "m = particle mass; L = box length; x = position; "
            "&psi; = wavefunction."
        ),
        "observations": [
            "The energy increases in proportion to n squared.",
            "Increasing box length decreases the energy levels in proportion "
            "to 1/L squared.",
            "Higher quantum numbers produce more nodes inside the box.",
            "The probability density is zero at the infinitely high walls."
        ],
        "applications": (
            "Introductory models of quantum confinement, nanoscale systems, "
            "and the electronic states of simplified molecular systems."
        ),
        "conclusion": (
            "Confinement quantizes energy. This ideal one-dimensional model "
            "assumes perfectly rigid walls and a non-relativistic particle."
        ),
    },

    "Quantum tunnelling": {
        "aim": (
            "Explore how a quantum particle can have a non-zero probability "
            "of crossing a barrier even when its energy is below the barrier."
        ),
        "theory": (
            "A quantum wavefunction can extend into and beyond a finite "
            "potential barrier. Consequently, the transmission probability "
            "can be non-zero even when classical mechanics predicts that "
            "the particle cannot cross. Transmission generally decreases "
            "as the barrier becomes wider or higher."
        ),
        "equations": [
            "<b>Below-barrier decay constant:</b> "
            "&kappa; = &radic;(2m(V<sub>0</sub> &minus; E)) / "
            "&hbar;",
            "<b>Approximate transmission trend:</b> "
            "T &prop; e<sup>&minus;2&kappa;a</sup>",
        ],
        "symbols": (
            "T = transmission probability; m = particle mass; V<sub>0</sub> "
            "= barrier height; E = particle energy; a = barrier width; "
            "&hbar; = reduced Planck's constant. The exponential expression "
            "describes a simplified below-barrier approximation, not the "
            "exact transmission formula for every barrier."
        ),
        "observations": [
            "A wider barrier generally reduces transmission.",
            "A higher barrier generally reduces transmission when particle "
            "energy remains below it.",
            "A particle with energy below the barrier can still have a "
            "non-zero transmission probability."
        ],
        "applications": (
            "Scanning tunnelling microscopes, alpha decay, tunnel diodes, "
            "and quantum devices."
        ),
        "conclusion": (
            "Tunnelling is a quantum phenomenon arising from wavefunction "
            "behaviour. The displayed approximation is intended for learning."
        ),
    },

    "Atomic orbitals": {
        "aim": (
            "Visualize how electron probability density varies with position "
            "for selected atomic orbitals."
        ),
        "theory": (
            "An orbital is a quantum state described by a wavefunction. "
            "The quantity |&psi;| squared represents probability density. "
            "It does not describe a fixed path followed by an electron. "
            "Orbital shape and nodes depend on the quantum state."
        ),
        "equations": [
            "<b>Probability density:</b> &rho; = |&psi;|<sup>2</sup>",
            "<b>Normalization:</b> &int; |&psi;|<sup>2</sup> dV = 1",
        ],
        "symbols": (
            "&psi; = orbital wavefunction; &rho; = probability density; "
            "dV = an element of volume. Normalization means the total "
            "probability over all space is one."
        ),
        "observations": [
            "The 1s orbital has spherical symmetry and no angular node.",
            "The 2p orbital has two principal lobes separated by a nodal plane.",
            "High-density regions indicate a greater probability of finding "
            "an electron in the corresponding volume.",
            "The displayed image is a two-dimensional density cross-section, "
            "not a complete three-dimensional orbital."
        ],
        "applications": (
            "Understanding atomic structure, chemical bonding, spectroscopy, "
            "and the electronic properties of materials."
        ),
        "conclusion": (
            "Orbitals describe quantum states and probability distributions, "
            "not planetary-style electron trajectories."
        ),
    },
}


class TutorialDialog(QDialog):
    def __init__(self, title, steps, parent=None):
        super().__init__(parent)

        self.setWindowTitle(f"Guided tutorial — {title}")
        self.resize(680, 680)
        self.setMinimumSize(500, 450)

        outer = QVBoxLayout(self)

        heading = QLabel(escape(title))
        heading.setObjectName("tutorialHeading")
        heading.setWordWrap(True)
        outer.addWidget(heading)

        subtitle = QLabel(
            "SCIENTIFIC GUIDE  |  Theory, equations, observations "
            "and applications"
        )
        subtitle.setObjectName("muted")
        subtitle.setWordWrap(True)
        outer.addWidget(subtitle)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(12)

        science = SCIENCE_CONTENT.get(title)

        if science:
            self._add_section(
                content_layout, "1. Aim", science["aim"]
            )
            self._add_section(
                content_layout, "2. Theory", science["theory"]
            )

            equations = "<br>".join(science["equations"])
            self._add_section(
                content_layout, "3. Key equations", equations,
                rich=True
            )
            self._add_section(
                content_layout, "Symbols and variables",
                science["symbols"], rich=True
            )

            observation_text = "<br>".join(
                f"&#8226; {escape(item)}"
                for item in science["observations"]
            )
            self._add_section(
                content_layout, "4. Expected observations",
                observation_text, rich=True
            )
            self._add_section(
                content_layout, "5. Real-world applications",
                science["applications"]
            )
            self._add_section(
                content_layout, "6. Conclusion",
                science["conclusion"]
            )

        # Preserve the experiment-specific steps already in core/physics.py.
        if steps:
            step_html = "<br><br>".join(
                f"<b>Step {i}.</b> {escape(str(step))}"
                for i, step in enumerate(steps, 1)
            )
            self._add_section(
                content_layout,
                "7. Guided procedure",
                step_html,
                rich=True
            )

        content_layout.addStretch(1)
        scroll.setWidget(content)
        outer.addWidget(scroll, 1)

        close_button = QPushButton("Got it")
        close_button.clicked.connect(self.accept)
        outer.addWidget(close_button)

    @staticmethod
    def _add_section(layout, heading, body, rich=False):
        card = QFrame()
        card.setObjectName("panel")

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(14, 12, 14, 12)
        card_layout.setSpacing(7)

        title_label = QLabel(escape(heading))
        title_label.setObjectName("sectionTitle")
        title_label.setWordWrap(True)
        card_layout.addWidget(title_label)

        body_label = QLabel(body if rich else escape(body))
        body_label.setObjectName("tutorialStep")
        body_label.setWordWrap(True)
        body_label.setTextFormat(
            Qt.TextFormat.RichText if rich else Qt.TextFormat.PlainText
        )
        body_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        body_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        card_layout.addWidget(body_label)

        layout.addWidget(card)