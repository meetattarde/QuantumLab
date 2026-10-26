import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import QuantumLabWindow


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("QUANTUM LAB")
    app.setOrganizationName("Quantum Lab Science Exhibition")
    app.setStyle("Fusion")
    window = QuantumLabWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
