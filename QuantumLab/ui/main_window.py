from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QFrame, QStackedWidget, QMessageBox, QScrollArea, QGridLayout,
    QTextBrowser, QProgressBar
)

from core.physics import EXPERIMENTS
from ui.experiment_widget import ExperimentWidget


STYLE = """
QMainWindow, QWidget {
    background: #080b1b;
    color: #e7eef8;
    font-family: Segoe UI, Arial;
    font-size: 10pt;
}
QFrame#sidebar {
    background: #10132a;
    border: 1px solid #2a315b;
    border-radius: 18px;
}
QFrame#panel, QFrame#experimentCard, QFrame#controlCard, QFrame#visualizationCard, QFrame#demoCard, QFrame#notebookCard {
    background: #12152e;
    border: 1px solid #2a315b;
    border-radius: 18px;
}
QFrame#experimentCard:hover { border: 1px solid #7f72ff; background: #171a38; }
QFrame#visualizationCard { border: 1px solid #4a3f93; background: #0d1025; }
QFrame#demoCard { border: 1px solid #24627a; background: #0c1628; }
QFrame#notebookCard { border: 1px solid #46518b; background: #10142c; }
QLabel#brand {
    font-size: 21pt;
    font-weight: 800;
    color: #f6f5ff;
}
QLabel#tagline, QLabel#muted {
    color: #aeb8d9;
}
QLabel#pageTitle {
    font-size: 22pt;
    font-weight: 750;
    color: #f6f5ff;
}
QLabel#sectionTitle {
    font-size: 12pt;
    font-weight: 700;
    color: #e3e6ff;
    padding-bottom: 4px;
}
QLabel#livePill { background: #0c403d; color: #63e7c9; border: 1px solid #216d64; border-radius: 11px; padding: 5px 10px; font-weight: 700; }
QLabel#resultPanel {
    background: #102c31;
    color: #b8f1df;
    border: 1px solid #24756a;
    border-radius: 10px;
    padding: 12px;
}
QLabel#tutorialHeading {
    font-size: 16pt;
    font-weight: 700;
    padding: 8px;
}
QLabel#tutorialStep {
    background: #181d3d;
    border-radius: 10px;
    padding: 12px;
    margin: 4px;
}
QPushButton {
    background: #1a1e3e;
    color: #eaf2fb;
    border: 1px solid #3c467c;
    border-radius: 10px;
    padding: 9px 12px;
}
QPushButton:hover {
    background: #292d59;
    border-color: #7f72ff;
}
QPushButton:pressed {
    background: #11142e;
}
QPushButton#primary {
    background: #6757e9;
    border-color: #8b7dff;
    font-weight: 700;
}
QPushButton#navButton {
    text-align: left;
    padding: 12px;
}
QComboBox, QSpinBox, QDoubleSpinBox {
    background: #0b0f24;
    color: #edf4ff;
    border: 1px solid #3c467c;
    border-radius: 6px;
    padding: 7px;
}
QComboBox QAbstractItemView {
    background: #171a38;
    selection-background-color: #6757e9;
}
QScrollArea {
    border: none;
}
QProgressBar {
    background: #151936;
    color: #e7eef8;
    border: 1px solid #3c467c;
    border-radius: 6px;
    text-align: center;
    min-height: 15px;
}
QProgressBar::chunk {
    background: #8b7dff;
    border-radius: 5px;
}
QTextBrowser {
    background: transparent;
    border: none;
    color: #e7eef8;
    selection-background-color: #6757e9;
}
"""


PRESENTATION_SLIDES = [
    {
        "section": "WELCOME",
        "title": "Exploring the Quantum World",
        "body": """
            <h2>Welcome to QUANTUM LAB</h2>
            <p>This virtual laboratory explores the physics of very small
            systems, where particles such as electrons and photons can behave
            in ways that differ from everyday objects.</p>
            <h3>What this presentation covers</h3>
            <ul>
                <li>Wave behaviour and interference</li>
                <li>Light and the photoelectric effect</li>
                <li>Quantized energy levels</li>
                <li>Quantum tunnelling</li>
                <li>Atomic orbitals and probability</li>
            </ul>
            <p>Each experiment connects a physical principle with an
            interactive simulation, adjustable parameters, and graphs.</p>
        """,
        "notes": """
            Opening suggestion:
            “Good morning. My project is QUANTUM LAB, a virtual quantum
            physics laboratory. It demonstrates important quantum concepts
            using interactive simulations. I will explain the scientific
            idea behind each experiment and show how the laboratory helps
            us explore it.”
        """,
    },
    {
        "section": "EXPERIMENT 01 OF 05",
        "title": "Double-Slit Experiment",
        "body": """
            <h2>Can particles produce an interference pattern?</h2>
            <p>When coherent waves pass through two narrow slits, the waves
            overlap. Where they reinforce each other, bright fringes form;
            where they cancel, dark fringes form.</p>
            <h3>Key relationship</h3>
            <p><b>Fringe spacing:</b> &nbsp; β = λL / d</p>
            <ul>
                <li><b>β</b> — distance between adjacent bright fringes</li>
                <li><b>λ</b> — wavelength</li>
                <li><b>L</b> — distance from the slits to the screen</li>
                <li><b>d</b> — separation between the slits</li>
            </ul>
            <h3>What should we observe?</h3>
            <p>Increasing wavelength or screen distance increases fringe
            spacing. Increasing slit separation decreases fringe spacing,
            within the assumptions of this simplified model.</p>
            <h3>Why it matters</h3>
            <p>The experiment illustrates interference and wave-particle
            duality. Quantum experiments can produce interference patterns
            even when particles are sent through the apparatus individually.</p>
        """,
        "notes": """
            Explain that the pattern is caused by the superposition of
            waves. Point to the simulation and change one parameter at a
            time. Ask the audience to predict whether the fringes will
            spread apart or move closer together before you change it.
            Mention that real experiments also depend on coherence and
            the details of the apparatus.
        """,
    },
    {
        "section": "EXPERIMENT 02 OF 05",
        "title": "Photoelectric Effect",
        "body": """
            <h2>How can light release electrons from a material?</h2>
            <p>The photoelectric effect occurs when light transfers energy
            to electrons in a material. Emission requires the light
            frequency to be high enough for the material's work function.</p>
            <h3>Einstein's photoelectric equation</h3>
            <p><b>K<sub>max</sub> = hf − φ</b></p>
            <ul>
                <li><b>K<sub>max</sub></b> — maximum kinetic energy of emitted electrons</li>
                <li><b>h</b> — Planck's constant</li>
                <li><b>f</b> — frequency of incident light</li>
                <li><b>φ</b> — work function of the material</li>
            </ul>
            <p>The threshold frequency is <b>f₀ = φ / h</b>. Below this
            threshold, the idealized model predicts no photoemission.</p>
            <h3>Important distinction</h3>
            <p>Above threshold, increasing frequency raises the maximum
            kinetic energy. Increasing light intensity mainly increases
            the number of incident photons and can increase photocurrent.</p>
            <h3>Applications</h3>
            <p>Related photoelectric principles are used in light sensors,
            photodetectors, and scientific instruments.</p>
        """,
        "notes": """
            Emphasize that frequency and intensity do different jobs.
            Frequency determines the energy per photon; intensity is
            related to how much light arrives. Use the controls to show
            the threshold effect, then compare frequency and intensity.
            The exact displayed values depend on the simulation model.
        """,
    },
    {
        "section": "EXPERIMENT 03 OF 05",
        "title": "Particle in a Box",
        "body": """
            <h2>Why can a confined particle have only certain energies?</h2>
            <p>A particle confined to a small region is described by a
            wavefunction. For an ideal one-dimensional infinite potential
            well, only standing waves that satisfy the boundary conditions
            are allowed.</p>
            <h3>Energy levels</h3>
            <p><b>Eₙ = n²h² / (8mL²)</b>, where n = 1, 2, 3, ...</p>
            <ul>
                <li><b>Eₙ</b> — energy of level n</li>
                <li><b>m</b> — particle mass</li>
                <li><b>L</b> — box length</li>
                <li><b>n</b> — positive integer quantum number</li>
            </ul>
            <p>The energy is quantized: the particle cannot have an
            arbitrary energy in this idealized model. The ground-state
            energy is nonzero.</p>
            <h3>What changes the energy?</h3>
            <p>Higher quantum numbers give higher energy levels.
            Increasing the box length lowers the energy levels; increasing
            the particle mass also lowers them.</p>
            <h3>Why it matters</h3>
            <p>Confinement models help introduce quantization in nanoscale
            systems and quantum structures.</p>
        """,
        "notes": """
            Explain that the allowed wavefunctions must fit the boundary
            conditions. Increase the quantum number and compare the energy
            and wave shape. If the simulation exposes the box size, change
            it and observe how confinement affects the energy.
        """,
    },
    {
        "section": "EXPERIMENT 04 OF 05",
        "title": "Quantum Tunnelling",
        "body": """
            <h2>Can a particle cross a barrier it cannot classically overcome?</h2>
            <p>In quantum mechanics, a particle is described by a
            wavefunction. When it encounters a finite potential barrier,
            the wavefunction can extend into and beyond the barrier,
            giving a nonzero probability of transmission.</p>
            <h3>What influences tunnelling?</h3>
            <ul>
                <li><b>Barrier width:</b> a wider barrier generally reduces
                transmission probability.</li>
                <li><b>Barrier height:</b> a higher barrier generally
                reduces transmission when other conditions are fixed.</li>
                <li><b>Particle energy and mass:</b> these also affect
                the transmission probability.</li>
            </ul>
            <p>For a simple barrier where the particle energy is below the
            barrier, transmission often decreases approximately
            exponentially with barrier width. The exact result depends
            on the potential and energy.</p>
            <h3>Applications</h3>
            <p>Tunnelling is important in scanning tunnelling microscopes,
            tunnel diodes, and some nuclear processes.</p>
            <p><i>Tunnelling is a quantum probability effect, not a
            classical particle simply climbing over the barrier.</i></p>
        """,
        "notes": """
            Start by describing the barrier as a region that a classical
            particle with insufficient energy could not cross. Then explain
            that quantum mechanics predicts a nonzero transmission
            probability for a finite barrier. Adjust the barrier width or
            height and describe the trend rather than promising a specific
            numerical result.
        """,
    },
    {
        "section": "EXPERIMENT 05 OF 05",
        "title": "Atomic Orbitals",
        "body": """
            <h2>Where is an electron likely to be found in an atom?</h2>
            <p>Atomic orbitals are quantum states described by wavefunctions.
            The square magnitude of a wavefunction, |ψ|², gives a
            probability density for position.</p>
            <h3>Important ideas</h3>
            <ul>
                <li>Orbitals are not fixed planetary paths.</li>
                <li>Different quantum states have different energy,
                shapes, and probability distributions.</li>
                <li>Nodes are regions where the wavefunction is zero.</li>
                <li>Visualized orbital surfaces represent a chosen
                probability or density level, not a solid electron shell.</li>
            </ul>
            <h3>Quantum numbers</h3>
            <p>The principal quantum number <b>n</b> relates to energy
            and size; the angular momentum quantum number <b>l</b>
            relates to orbital shape; and the magnetic quantum number
            <b>mₗ</b> specifies an allowed orientation in a chosen basis.</p>
            <h3>Why it matters</h3>
            <p>Orbital models help explain atomic spectra, chemical
            bonding, and the arrangement of electrons in atoms.</p>
        """,
        "notes": """
            Clarify that an orbital is a mathematical quantum state,
            not a track around the nucleus. Point out the regions where
            probability density is higher or lower. If the viewer offers
            multiple orbital states, compare their shapes and nodal
            features.
        """,
    },
    {
        "section": "CONCLUSION",
        "title": "From Quantum Ideas to Real Technology",
        "body": """
            <h2>What have we explored?</h2>
            <ul>
                <li><b>Double slit:</b> interference and wave-particle duality.</li>
                <li><b>Photoelectric effect:</b> photon energy and electron emission.</li>
                <li><b>Particle in a box:</b> confinement and quantized energy.</li>
                <li><b>Quantum tunnelling:</b> probability of transmission through a barrier.</li>
                <li><b>Atomic orbitals:</b> electron states and probability density.</li>
            </ul>
            <h3>Why a virtual laboratory?</h3>
            <p>Interactive simulations make it possible to vary parameters,
            compare predictions with results, visualize abstract ideas,
            and export data for further analysis.</p>
            <h3>Final message</h3>
            <p>Quantum physics is not only a theory of the microscopic
            world. It is also part of the scientific foundation behind
            many modern technologies.</p>
            <h2>Thank you</h2>
            <p>Questions are welcome.</p>
        """,
        "notes": """
            Summarize one main lesson from each experiment. Explain that
            the lab is an educational simulation, and that its predictions
            depend on the assumptions built into each model. Finish by
            inviting the judges to choose an experiment for a live
            demonstration.
        """,
    },
]


class ExhibitionPresentation(QWidget):
    """A self-contained, navigable presentation for the science exhibition."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_slide = 0
        self.exit_requested = lambda: None
        self._build_ui()
        self.show_slide(0)

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(14)

        top = QHBoxLayout()
        brand = QLabel("QUANTUM LAB  /  EXHIBITION PRESENTATION")
        brand.setStyleSheet(
            "font-size: 12pt; font-weight: 800; color: #7f72ff;"
        )
        top.addWidget(brand)
        top.addStretch(1)

        self.fullscreen_button = QPushButton("⛶  Toggle full screen")
        self.fullscreen_button.clicked.connect(self.toggle_fullscreen)
        top.addWidget(self.fullscreen_button)

        self.exit_button = QPushButton("Exit presentation  ✕")
        self.exit_button.clicked.connect(self.exit_requested)
        top.addWidget(self.exit_button)
        layout.addLayout(top)

        self.progress = QProgressBar()
        self.progress.setTextVisible(False)
        self.progress.setRange(0, len(PRESENTATION_SLIDES))
        layout.addWidget(self.progress)

        slide_panel = QFrame()
        slide_panel.setObjectName("panel")
        panel_layout = QVBoxLayout(slide_panel)
        panel_layout.setContentsMargins(28, 24, 28, 24)
        panel_layout.setSpacing(12)

        self.section_label = QLabel()
        self.section_label.setStyleSheet(
            "color: #7f72ff; font-size: 10pt; font-weight: 800;"
        )
        panel_layout.addWidget(self.section_label)

        self.title_label = QLabel()
        self.title_label.setWordWrap(True)
        self.title_label.setStyleSheet(
            "font-size: 25pt; font-weight: 800; color: #f6f5ff;"
        )
        panel_layout.addWidget(self.title_label)

        self.body = QTextBrowser()
        self.body.setOpenExternalLinks(False)
        self.body.setStyleSheet("""
            QTextBrowser {
                background: #0e1828;
                border: 1px solid #2a315b;
                border-radius: 10px;
                padding: 16px;
                font-size: 12pt;
                color: #e7eef8;
            }
        """)
        self.body.setHtml("")
        panel_layout.addWidget(self.body, 1)

        layout.addWidget(slide_panel, 5)

        notes_panel = QFrame()
        notes_panel.setObjectName("panel")
        notes_layout = QVBoxLayout(notes_panel)
        notes_layout.setContentsMargins(18, 12, 18, 12)
        notes_layout.setSpacing(6)

        notes_heading = QLabel("SPEAKER NOTES  ·  FOR THE PRESENTER")
        notes_heading.setStyleSheet(
            "color: #7f72ff; font-weight: 800;"
        )
        notes_layout.addWidget(notes_heading)

        self.notes_label = QLabel()
        self.notes_label.setWordWrap(True)
        self.notes_label.setStyleSheet(
            "color: #bdcce0; font-size: 10pt;"
        )
        notes_layout.addWidget(self.notes_label)
        layout.addWidget(notes_panel, 2)

        bottom = QHBoxLayout()
        self.previous_button = QPushButton("←  Previous")
        self.previous_button.clicked.connect(self.previous_slide)
        bottom.addWidget(self.previous_button)

        self.counter_label = QLabel()
        self.counter_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.counter_label.setStyleSheet(
            "font-size: 10pt; font-weight: 700; color: #aeb8d9;"
        )
        bottom.addWidget(self.counter_label, 1)

        self.next_button = QPushButton("Next  →")
        self.next_button.setObjectName("primary")
        self.next_button.clicked.connect(self.next_slide)
        bottom.addWidget(self.next_button)

        layout.addLayout(bottom)

    def show_slide(self, index):
        index = max(0, min(index, len(PRESENTATION_SLIDES) - 1))
        self.current_slide = index
        slide = PRESENTATION_SLIDES[index]

        self.section_label.setText(slide["section"])
        self.title_label.setText(slide["title"])
        self.body.setHtml(slide["body"])
        self.notes_label.setText(slide["notes"].strip())

        self.counter_label.setText(
            f"SLIDE {index + 1} OF {len(PRESENTATION_SLIDES)}"
        )
        self.progress.setValue(index + 1)
        self.previous_button.setEnabled(index > 0)

        if index == len(PRESENTATION_SLIDES) - 1:
            self.next_button.setText("Finish  ✓")
        else:
            self.next_button.setText("Next  →")

    def next_slide(self):
        if self.current_slide < len(PRESENTATION_SLIDES) - 1:
            self.show_slide(self.current_slide + 1)
        else:
            self.exit_requested()

    def previous_slide(self):
        if self.current_slide > 0:
            self.show_slide(self.current_slide - 1)

    def toggle_fullscreen(self):
        window = self.window()
        if window.isFullScreen():
            window.showNormal()
        else:
            window.showFullScreen()

    # Set by QuantumLabWindow when this page is created.
    def set_exit_callback(self, callback):
        self.exit_requested = callback


class QuantumLabWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QUANTUM LAB — Virtual Quantum Physics Laboratory")
        self.resize(1440, 900)
        self.setMinimumSize(1050, 680)
        self.setStyleSheet(STYLE)

        self.exhibition_mode = False
        self._presentation_return_widget = None
        self._presentation_active = False

        self._build_ui()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        root = QHBoxLayout(central)
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(16)

        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(245)

        side = QVBoxLayout(self.sidebar)
        side.setContentsMargins(16, 20, 16, 16)
        side.setSpacing(12)

        brand = QLabel("⚛  QUANTUM LAB")
        brand.setObjectName("brand")

        tagline = QLabel("INTERACTIVE QUANTUM SIMULATOR")
        tagline.setObjectName("tagline")

        side.addWidget(brand)
        side.addWidget(tagline)
        side.addSpacing(18)

        self.home_button = QPushButton("⌂   Dashboard")
        self.home_button.setObjectName("navButton")
        self.home_button.clicked.connect(self.show_dashboard)
        side.addWidget(self.home_button)

        self.experiment_combo = QComboBox()
        self.experiment_combo.addItems(list(EXPERIMENTS.keys()))
        self.experiment_combo.currentTextChanged.connect(
            self.select_experiment
        )

        side.addWidget(QLabel("EXPERIMENT LIBRARY"))
        side.addWidget(self.experiment_combo)

        self.experiment_button = QPushButton("⚛   Open experiment")
        self.experiment_button.setObjectName("primary")
        self.experiment_button.clicked.connect(
            lambda: self.select_experiment(
                self.experiment_combo.currentText()
            )
        )
        side.addWidget(self.experiment_button)

        side.addStretch(1)

        presentation_button = QPushButton("▶   Start presentation")
        presentation_button.setObjectName("primary")
        presentation_button.clicked.connect(self.start_presentation)
        side.addWidget(presentation_button)

        exhibition_button = QPushButton("⛶   Exhibition mode")
        exhibition_button.clicked.connect(self.toggle_exhibition_mode)
        side.addWidget(exhibition_button)

        help_button = QPushButton("?   About / How to use")
        help_button.clicked.connect(self.show_help)
        side.addWidget(help_button)

        footer = QLabel("EDUCATION • SIMULATION • DISCOVERY\nFINAL EXHIBITION EDITION")
        footer.setObjectName("tagline")
        side.addWidget(footer)

        root.addWidget(self.sidebar)

        self.stack = QStackedWidget()
        root.addWidget(self.stack, 1)

        self.dashboard = self._build_dashboard()
        self.stack.addWidget(self.dashboard)

        self.experiment_page = ExperimentWidget()
        self.stack.addWidget(self.experiment_page)

        self.presentation_page = ExhibitionPresentation()
        self.presentation_page.set_exit_callback(self.exit_presentation)
        self.stack.addWidget(self.presentation_page)

        self.show_dashboard()

    def _build_dashboard(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(6, 4, 6, 4)

        hero = QFrame()
        hero.setObjectName("panel")
        hero_layout = QVBoxLayout(hero)
        hero_layout.setContentsMargins(28, 28, 28, 28)

        eyebrow = QLabel("●  LIVE INTERACTIVE SCIENCE EXHIBITION")
        eyebrow.setObjectName("tagline")

        title = QLabel("Explore quantum physics.\nSee the invisible.")
        title.setObjectName("pageTitle")

        subtitle = QLabel(
            "A virtual laboratory for visualizing fundamental quantum "
            "physics through interactive experiments."
        )
        subtitle.setWordWrap(True)
        subtitle.setObjectName("muted")

        hero_layout.addWidget(eyebrow)
        hero_layout.addWidget(title)
        hero_layout.addWidget(subtitle)

        start = QPushButton("Start exploring  →")
        start.setObjectName("primary")
        start.clicked.connect(
            lambda: self.select_experiment(
                self.experiment_combo.currentText()
            )
        )
        hero_layout.addWidget(start, 0, Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(hero)

        section = QLabel("EXPERIMENT COLLECTION")
        section.setObjectName("sectionTitle")
        layout.addWidget(section)

        cards = QGridLayout()
        cards.setSpacing(12)

        descriptions = [
            ("01", "Double-slit experiment", "Interference and diffraction"),
            ("02", "Photoelectric effect", "Photons and electron energy"),
            ("03", "Particle in a box", "Quantized energy states"),
            ("04", "Quantum tunnelling", "Transmission through barriers"),
            ("05", "Atomic orbitals", "Probability-density cross-sections"),
            (
                "06",
                "Heisenberg uncertainty principle",
                "Position and momentum uncertainty",
            ),
            ("07", "Quantum harmonic oscillator", "Exact stationary states"),
            ("08", "Numerical finite well", "Finite-difference solver"),
            ("09", "Quantum measurement statistics", "Probability and repeated measurements"),
        ]
       
        for index, (number, name, desc) in enumerate(descriptions):
            card = QFrame()
            card.setObjectName("experimentCard")
            card_layout = QVBoxLayout(card)

            num = QLabel(number)
            num.setStyleSheet(
                "font-size: 21pt; font-weight: 800; color: #7f72ff;"
            )

            heading = QLabel(name)
            heading.setStyleSheet("font-weight: 700;")

            description = QLabel(desc)
            description.setObjectName("muted")
            description.setWordWrap(True)

            button = QPushButton("Open")
            button.clicked.connect(
                lambda checked=False, n=name: self.open_by_short_name(n)
            )

            card_layout.addWidget(num)
            card_layout.addWidget(heading)
            card_layout.addWidget(description, 1)
            card_layout.addWidget(button)
            cards.addWidget(card, index // 4, index % 4)

        layout.addLayout(cards)

        info = QFrame()
        info.setObjectName("panel")
        info_layout = QVBoxLayout(info)
        info_layout.addWidget(QLabel("HOW TO USE THE LAB"))

        info_text = QLabel(
            "1. Choose an experiment from the library.  "
            "2. Adjust the controls.  "
            "3. Watch the graph update live.  "
            "4. Open the guided tutorial.  "
            "5. Export data as CSV.  "
            "Use Start presentation for the guided exhibition slideshow."
        )
        info_text.setWordWrap(True)
        info_text.setObjectName("muted")
        info_layout.addWidget(info_text)

        layout.addWidget(info)
        layout.addStretch(1)
        return page

    def open_by_short_name(self, experiment_name):
        if experiment_name not in EXPERIMENTS:
            QMessageBox.warning(
                self,
                "Experiment unavailable",
                f"Experiment not found: {experiment_name}",
            )
            return

        index = self.experiment_combo.findText(experiment_name)
        if index >= 0:
            self.experiment_combo.setCurrentIndex(index)

        self.select_experiment(experiment_name)
        
    def select_experiment(self, name):
        if name not in EXPERIMENTS:
            return

        self.experiment_page.load_experiment(name)
        self.stack.setCurrentWidget(self.experiment_page)

    def show_dashboard(self):
        self.stack.setCurrentWidget(self.dashboard)

    def start_presentation(self):
        if self._presentation_active:
            return

        self._presentation_return_widget = self.stack.currentWidget()
        self._presentation_active = True
        self.exhibition_mode = False

        self.presentation_page.show_slide(0)
        self.stack.setCurrentWidget(self.presentation_page)
        self.sidebar.hide()
        self.showFullScreen()

    def exit_presentation(self):
        if not self._presentation_active:
            return

        self._presentation_active = False
        self.showNormal()
        self.sidebar.show()

        return_widget = self._presentation_return_widget
        if return_widget is not None:
            self.stack.setCurrentWidget(return_widget)
        else:
            self.show_dashboard()

        self._presentation_return_widget = None

    def toggle_exhibition_mode(self):
        if self._presentation_active:
            return

        self.exhibition_mode = not self.exhibition_mode
        self.sidebar.setVisible(not self.exhibition_mode)

        if self.exhibition_mode:
            self.showFullScreen()
        else:
            self.showNormal()

    def show_help(self):
        QMessageBox.information(
            self,
            "About QUANTUM LAB",
            "QUANTUM LAB is an educational quantum-physics simulation "
            "for a science exhibition.\n\n"
            "HOW TO OPERATE\n"
            "• Select an experiment in the left-side library.\n"
            "• Change parameters to update the visualization.\n"
            "• Select Guided tutorial to explore key concepts.\n"
            "• Select Export CSV to save plotted data and parameters.\n"
            "• Start presentation opens the guided exhibition slideshow.\n"
            "• During the presentation, use Previous and Next to navigate.\n"
            "• Press Esc to exit presentation or exhibition mode.\n\n"
            "Note: models are simplified for learning and should not be "
            "treated as precision research software."
        )

    def keyPressEvent(self, event):
        if self._presentation_active:
            if event.key() == Qt.Key.Key_Escape:
                self.exit_presentation()
                event.accept()
                return

            if event.key() in (
                Qt.Key.Key_Right,
                Qt.Key.Key_PageDown,
                Qt.Key.Key_Space,
            ):
                self.presentation_page.next_slide()
                event.accept()
                return

            if event.key() in (
                Qt.Key.Key_Left,
                Qt.Key.Key_PageUp,
            ):
                self.presentation_page.previous_slide()
                event.accept()
                return

        elif (
            event.key() == Qt.Key.Key_Escape
            and self.exhibition_mode
        ):
            self.toggle_exhibition_mode()
            event.accept()
            return

        super().keyPressEvent(event)
