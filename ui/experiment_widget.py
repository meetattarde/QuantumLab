import csv

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QSpinBox, QDoubleSpinBox, QComboBox, QFormLayout, QFrame,
    QFileDialog, QMessageBox, QSizePolicy, QScrollArea
)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from core.physics import EXPERIMENTS, run_experiment
from core.labbook import load_session, make_record, save_session
from core.presets import PRESETS, names_for
from core.reporting import save_report
from ui.tutorial_dialog import TutorialDialog
from ui.demo_panel import DemonstrationPanel


class ExperimentWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_name = "Double-slit experiment"
        self.controls = {}
        self.last_result = None
        self.records = []
        self._build_ui()
        self.load_experiment(self.current_name)

    def _build_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        self.content_scroll = QScrollArea()
        self.content_scroll.setWidgetResizable(True)
        self.content_scroll.setFrameShape(QFrame.Shape.NoFrame)
        outer.addWidget(self.content_scroll)

        content = QWidget()
        self.content_scroll.setWidget(content)

        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(12)

        header = QHBoxLayout()

        self.title = QLabel("Double-slit experiment")
        self.title.setObjectName("pageTitle")

        self.tutorial_button = QPushButton("◈ Tutorial")
        self.tutorial_button.clicked.connect(self.show_tutorial)

        self.export_button = QPushButton("⇩ CSV")
        self.export_button.clicked.connect(self.export_csv)

        self.record_button = QPushButton("● Record")
        self.record_button.clicked.connect(self.record_run)
        self.session_button = QPushButton("Save")
        self.session_button.clicked.connect(self.save_lab_session)
        self.load_button = QPushButton("Load")
        self.load_button.clicked.connect(self.load_lab_session)
        self.report_button = QPushButton("Report")
        self.report_button.clicked.connect(self.export_report)

        header.addWidget(self.title)
        header.addStretch(1)
        self.status_pill = QLabel("● RUNNING")
        self.status_pill.setObjectName("livePill")
        header.addWidget(self.status_pill)
        header.addWidget(self.tutorial_button)
        header.addWidget(self.export_button)
        header.addWidget(self.record_button)
        header.addWidget(self.session_button)
        header.addWidget(self.load_button)
        header.addWidget(self.report_button)
        content_layout.addLayout(header)

        self.description = QLabel()
        self.description.setWordWrap(True)
        self.description.setObjectName("muted")
        content_layout.addWidget(self.description)

        notebook = QFrame()
        notebook.setObjectName("notebookCard")
        notebook_layout = QVBoxLayout(notebook)
        notebook_layout.setContentsMargins(14, 10, 14, 10)
        notebook_heading = QLabel("▣  LAB NOTEBOOK & COMPARISON")
        notebook_heading.setObjectName("sectionTitle")
        notebook_layout.addWidget(notebook_heading)
        preset_row = QHBoxLayout()
        preset_row.addWidget(QLabel("Demonstration preset:"))
        self.preset_combo = QComboBox()
        self.preset_combo.currentIndexChanged.connect(self.apply_preset)
        preset_row.addWidget(self.preset_combo, 1)
        notebook_layout.addLayout(preset_row)
        self.metrics_label = QLabel("Run a model to view curve metrics.")
        self.metrics_label.setWordWrap(True)
        self.metrics_label.setObjectName("muted")
        notebook_layout.addWidget(self.metrics_label)
        self.history_label = QLabel("No recorded runs in this session.")
        self.history_label.setWordWrap(True)
        self.history_label.setObjectName("tutorialStep")
        notebook_layout.addWidget(self.history_label)


        body = QHBoxLayout()
        body.setSpacing(16)

        controls_card = QFrame()
        controls_card.setObjectName("controlCard")
        controls_card.setMinimumWidth(255)
        controls_card.setMaximumWidth(285)

        control_layout = QVBoxLayout(controls_card)

        control_heading = QLabel("⚙  EXPERIMENT CONTROLS")
        control_heading.setObjectName("sectionTitle")
        control_layout.addWidget(control_heading)

        self.form = QFormLayout()
        self.form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        self.form.setFormAlignment(Qt.AlignmentFlag.AlignTop)
        self.form.setVerticalSpacing(14)
        control_layout.addLayout(self.form)

        self.reset_button = QPushButton("Reset parameters")
        self.reset_button.clicked.connect(
            lambda: self.load_experiment(self.current_name, reset=True)
        )
        control_layout.addWidget(self.reset_button)
        control_layout.addStretch(1)

        body.addWidget(controls_card)

        plot_card = QFrame()
        plot_card.setObjectName("visualizationCard")
        plot_layout = QVBoxLayout(plot_card)

        plot_heading = QLabel("◉  QUANTUM VISUALIZATION")
        plot_heading.setObjectName("sectionTitle")
        plot_layout.addWidget(plot_heading)

        self.figure = Figure(figsize=(7, 5), tight_layout=True)
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        plot_layout.addWidget(self.canvas, 1)

        body.addWidget(plot_card, 1)

        demo_card = QFrame()
        demo_card.setObjectName("demoCard")
        demo_layout = QVBoxLayout(demo_card)
        demo_heading = QLabel("✦  CONCEPT DEMONSTRATION")
        demo_heading.setObjectName("sectionTitle")
        demo_layout.addWidget(demo_heading)
        self.demo_panel = DemonstrationPanel()
        demo_layout.addWidget(self.demo_panel, 1)
        demo_card.setMinimumWidth(285)
        demo_card.setMaximumWidth(330)
        right_column = QVBoxLayout()
        right_column.setSpacing(12)
        right_column.addWidget(demo_card, 1)
        right_column.addWidget(notebook, 1)
        body.addLayout(right_column)
        content_layout.addLayout(body, 1)

        self.result_label = QLabel()
        self.result_label.setWordWrap(True)
        self.result_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        self.result_label.setObjectName("resultPanel")
        content_layout.addWidget(self.result_label)

        self.analysis_card = QFrame()
        self.analysis_card.setObjectName("panel")
        analysis_layout = QVBoxLayout(self.analysis_card)

        analysis_heading = QLabel("Scientific analysis")
        analysis_heading.setObjectName("sectionTitle")
        analysis_layout.addWidget(analysis_heading)

        self.analysis_label = QLabel()
        self.analysis_label.setWordWrap(True)
        self.analysis_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        self.analysis_label.setObjectName("tutorialStep")
        analysis_layout.addWidget(self.analysis_label)

        self.takeaway_label = QLabel()
        self.takeaway_label.setWordWrap(True)
        self.takeaway_label.setObjectName("resultPanel")
        analysis_layout.addWidget(self.takeaway_label)

        content_layout.addWidget(self.analysis_card)

    def load_experiment(self, name, reset=False):
        self.current_name = name
        data = EXPERIMENTS[name]

        self.title.setText(name)
        self.description.setText(data["description"])
        self.demo_panel.set_experiment(name)
        self._refresh_presets()

        while self.form.rowCount():
            self.form.removeRow(0)

        self.controls = {}

        for item in data["controls"]:
            key = item["key"]

            if item.get("type") == "choice":
                widget = QComboBox()

                for display, stored_value in item["options"]:
                    widget.addItem(display, stored_value)

                default_index = widget.findData(item["value"])
                if default_index >= 0:
                    widget.setCurrentIndex(default_index)

                widget.currentIndexChanged.connect(self.update_plot)

            elif (
                isinstance(item["value"], int)
                and isinstance(item["step"], int)
            ):
                widget = QSpinBox()
                widget.setRange(int(item["min"]), int(item["max"]))
                widget.setSingleStep(int(item["step"]))
                widget.setValue(int(item["value"]))
                widget.setKeyboardTracking(False)
                widget.valueChanged.connect(self.update_plot)

            else:
                widget = QDoubleSpinBox()
                widget.setRange(float(item["min"]), float(item["max"]))
                widget.setSingleStep(float(item["step"]))
                widget.setDecimals(
                    2 if float(item["step"]) < 1 else 1
                )
                widget.setValue(float(item["value"]))
                widget.setKeyboardTracking(False)
                widget.valueChanged.connect(self.update_plot)

            self.controls[key] = widget
            self.form.addRow(item["label"], widget)

        self.update_plot()

    def _refresh_presets(self):
        self.preset_combo.blockSignals(True)
        self.preset_combo.clear()
        self.preset_combo.addItem("Custom settings", None)
        for preset_name in names_for(self.current_name):
            self.preset_combo.addItem(preset_name, preset_name)
        self.preset_combo.blockSignals(False)

    def apply_preset(self, _index):
        preset_name = self.preset_combo.currentData()
        if not preset_name:
            return
        for key, value in PRESETS[self.current_name][preset_name].items():
            widget = self.controls.get(key)
            if isinstance(widget, QComboBox):
                index = widget.findData(value)
                if index >= 0:
                    widget.setCurrentIndex(index)
            elif widget is not None:
                widget.setValue(value)
        self.update_plot()

    def get_params(self):
        params = {}

        for key, widget in self.controls.items():
            if isinstance(widget, QComboBox):
                params[key] = widget.currentData()
            else:
                params[key] = widget.value()

        return params

    def update_plot(self, *_):
        if not self.controls:
            return

        try:
            params = self.get_params()
            result = run_experiment(self.current_name, params)
            self.last_result = result

            x, y, xlabel, ylabel, summary, csv_headers = result
            self.figure.clear()

            if self.current_name == "Atomic orbitals":
                ax = self.figure.add_subplot(111)
                X, Y, density = x

                image = ax.imshow(
                    density,
                    extent=[X.min(), X.max(), Y.min(), Y.max()],
                    origin="lower",
                    cmap="magma",
                    aspect="equal",
                    interpolation="bilinear"
                )
                ax.set_xlabel("Cross-section coordinate 1 (Bohr radii)")
                ax.set_ylabel("Cross-section coordinate 2 (Bohr radii)")
                ax.set_title(ylabel)
                self.figure.colorbar(
                    image,
                    ax=ax,
                    label="Relative probability density",
                    shrink=0.82
                )

            else:
                ax = self.figure.add_subplot(111)
                ax.plot(x, y, linewidth=2.2, color="#7f72ff")
                ax.fill_between(x, y, alpha=0.14, color="#7f72ff")
                ax.set_xlabel(xlabel)
                ax.set_ylabel(ylabel)
                ax.set_title(self.current_name)

                if self.current_name == "Photoelectric effect":
                    ax.axvline(
                        params["frequency_1e14_hz"],
                        linestyle="--",
                        linewidth=1.3,
                        color="#ffb64c",
                        label="Selected frequency"
                    )
                    ax.legend()

                elif self.current_name == "Particle in a box":
                    ax.set_title(
                        "Probability density — n = "
                        f"{int(params['quantum_number'])}"
                    )

            self.figure.patch.set_facecolor("#0d1025")

            for axis in self.figure.axes:
                axis.set_facecolor("#0d1025")
                axis.tick_params(colors="#dce6f2")
                axis.xaxis.label.set_color("#dce6f2")
                axis.yaxis.label.set_color("#dce6f2")
                axis.title.set_color("#f2f6fb")

                for spine in axis.spines.values():
                    spine.set_color("#46518b")

                axis.grid(True, alpha=0.18)

            self.canvas.draw_idle()
            self.result_label.setText("RESULT  ·  " + summary)
            self._update_metrics(result)

            analysis, takeaway = self._build_analysis(params, summary)
            self.analysis_label.setText(analysis)
            self.takeaway_label.setText("KEY TAKEAWAY  ·  " + takeaway)

        except Exception as exc:
            self.result_label.setText(f"Calculation error: {exc}")
            self.analysis_label.setText(
                "Analysis is unavailable until the calculation succeeds."
            )
            self.takeaway_label.clear()

    def _update_metrics(self, result):
        try:
            record = make_record(self.current_name, self.get_params(), result)
            metrics = record.metrics
            if "peak_x" in metrics:
                text = ("Live curve metrics — "
                        f"min: {metrics['minimum']:.4g}; max: {metrics['maximum']:.4g}; "
                        f"peak x: {metrics['peak_x']:.4g}; area: {metrics['area']:.4g}.")
            else:
                text = ("Density metrics — "
                        f"min: {metrics['minimum']:.4g}; max: {metrics['maximum']:.4g}; "
                        f"mean: {metrics['mean']:.4g}.")
            self.metrics_label.setText(text)
        except (TypeError, ValueError) as exc:
            self.metrics_label.setText(f"Metrics unavailable: {exc}")

    def _refresh_history(self):
        if not self.records:
            self.history_label.setText("No recorded runs in this session.")
            return
        lines = ["Recent recorded runs:"]
        for record in self.records[-5:][::-1]:
            metrics = ", ".join(f"{key}={value:.4g}" for key, value in record.metrics.items())
            lines.append(f"• {record.experiment} — {record.created_utc} — {metrics}")
        self.history_label.setText("\n".join(lines))

    def _build_analysis(self, params, summary):
        if self.current_name == "Double-slit experiment":
            values = ", ".join(
                f"{key.replace('_', ' ')} = {value:g}"
                for key, value in params.items()
            )
            analysis = (
                f"Current settings: {values}.\n\n"
                "The interference pattern comes from superposition of "
                "waves from the two slits. Fringe spacing increases with "
                "wavelength and screen distance, and decreases with slit "
                "separation, assuming the small-angle approximation."
            )
            takeaway = (
                "Change one parameter at a time to identify its effect "
                "on the interference pattern."
            )

        elif self.current_name == "Photoelectric effect":
            frequency = params.get("frequency_1e14_hz", 0)
            analysis = (
                f"Selected frequency: {frequency:g} × 10¹⁴ Hz.\n\n"
                "Photon energy is proportional to frequency: E = hf. "
                "Electron emission also depends on the material's work "
                "function. Above threshold, higher frequency increases "
                "the maximum kinetic energy in Einstein's model."
            )
            takeaway = (
                "Frequency controls energy per photon; intensity and "
                "frequency play different roles."
            )

        elif self.current_name == "Particle in a box":
            n = int(params.get("quantum_number", 1))
            analysis = (
                f"Selected quantum number: n = {n}.\n\n"
                "For a one-dimensional infinite well, allowed energies "
                "are proportional to n². Probability density is the "
                "squared magnitude of the wavefunction, with nodes where "
                "the density is zero."
            )
            takeaway = (
                "Quantum confinement allows discrete energy levels."
            )

        elif self.current_name == "Quantum tunnelling":
            values = ", ".join(
                f"{key.replace('_', ' ')} = {value:g}"
                for key, value in params.items()
            )
            analysis = (
                f"Current settings: {values}.\n\n"
                "A quantum wavefunction can extend into a classically "
                "forbidden region. Transmission generally decreases as "
                "barrier width or height increases, with other conditions "
                "held fixed. This app uses a simplified educational model."
            )
            takeaway = (
                "A particle below a finite barrier can still have a "
                "non-zero transmission probability."
            )

        elif self.current_name == "Atomic orbitals":
            orbital = str(params.get("orbital", "1s"))
            scale = float(params.get("scale_bohr", 6))
            analysis = (
                f"Selected orbital: {orbital}.\n"
                f"View extends to ±{scale:g} Bohr radii.\n\n"
                "The principal quantum number n describes the energy "
                "level in the hydrogen atom; the angular-momentum quantum "
                "number l identifies the s, p, d or f family. The shape "
                "also depends on the orbital orientation. Radial and "
                "angular nodes are regions where the wavefunction, and "
                "therefore its probability density, vanishes.\n\n"
                "This display shows relative density in a representative "
                "2D slice. It is not a complete 3D orbital, and the colors "
                "do not represent absolute probabilities."
            )
            takeaway = (
                "Orbital shape and nodes arise from the quantum "
                "wavefunction—not from a fixed electron path."
            )

        else:
            analysis = "Current experiment result:\n" + str(summary)
            takeaway = (
                "Change one parameter at a time and observe the result."
            )

        return analysis, takeaway

    def record_run(self):
        if self.last_result is None:
            QMessageBox.warning(self, "Nothing to record", "Run an experiment before recording it.")
            return
        try:
            self.records.append(make_record(self.current_name, self.get_params(), self.last_result))
            self._refresh_history()
            QMessageBox.information(self, "Run recorded", "This run was added to the current lab notebook session.")
        except (TypeError, ValueError) as exc:
            QMessageBox.warning(self, "Record failed", str(exc))

    def save_lab_session(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save lab session", "quantum_lab_session.json", "JSON files (*.json)")
        if not path:
            return
        try:
            save_session(path, self.records, self.current_name, self.get_params())
            QMessageBox.information(self, "Session saved", f"Lab notebook saved to:\n{path}")
        except (OSError, ValueError) as exc:
            QMessageBox.critical(self, "Save failed", str(exc))

    def load_lab_session(self):
        path, _ = QFileDialog.getOpenFileName(self, "Load lab session", "", "JSON files (*.json)")
        if not path:
            return
        try:
            records, experiment, parameters = load_session(path)
            if experiment not in EXPERIMENTS:
                raise ValueError(f"Session refers to an unavailable experiment: {experiment}")
            self.records = records
            self.load_experiment(experiment)
            for key, value in parameters.items():
                widget = self.controls.get(key)
                if isinstance(widget, QComboBox):
                    index = widget.findData(value)
                    if index >= 0:
                        widget.setCurrentIndex(index)
                elif widget is not None:
                    widget.setValue(value)
            self.update_plot()
            self._refresh_history()
            QMessageBox.information(self, "Session loaded", f"Loaded {len(records)} recorded run(s).")
        except (OSError, ValueError) as exc:
            QMessageBox.critical(self, "Load failed", str(exc))

    def export_report(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Export session report", "quantum_lab_report.md", "Markdown files (*.md)"
        )
        if not path:
            return
        try:
            records = list(self.records)
            if not records and self.last_result is not None:
                records.append(make_record(self.current_name, self.get_params(), self.last_result))
            save_report(path, records, self.current_name)
            QMessageBox.information(self, "Report exported", f"Research report saved to:\n{path}")
        except (OSError, ValueError) as exc:
            QMessageBox.critical(self, "Report failed", str(exc))

    def show_tutorial(self):
        TutorialDialog(
            self.current_name,
            EXPERIMENTS[self.current_name]["tutorial"],
            self
        ).exec()

    def export_csv(self):
        if self.last_result is None:
            QMessageBox.warning(
                self,
                "Nothing to export",
                "Run an experiment before exporting."
            )
            return

        path, _ = QFileDialog.getSaveFileName(
            self,
            "Export experiment data",
            f"{self.current_name.lower().replace(' ', '_').replace('-', '_')}.csv",
            "CSV files (*.csv)"
        )

        if not path:
            return

        try:
            x, y, _, _, summary, headers = self.last_result

            with open(path, "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow([f"QUANTUM LAB — {self.current_name}"])
                writer.writerow(["Parameters", repr(self.get_params())])
                writer.writerow(["Interpretation", summary])
                writer.writerow([])

                if self.current_name == "Atomic orbitals":
                    X, Y, density = x
                    writer.writerow(list(headers))

                    for i in range(X.shape[0]):
                        for j in range(X.shape[1]):
                            writer.writerow([
                                X[i, j], Y[i, j], density[i, j]
                            ])
                else:
                    writer.writerow(list(headers))

                    for xv, yv in zip(x, y):
                        writer.writerow([xv, yv])

            QMessageBox.information(
                self,
                "Export complete",
                f"Data saved to:\n{path}"
            )

        except (OSError, csv.Error) as exc:
            QMessageBox.critical(self, "Export failed", str(exc))
