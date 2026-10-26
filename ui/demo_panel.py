"""Offline animated concept demonstrations for exhibition use.

These compact looping drawings are intentionally labelled as educational
animations, so they improve explanation without pretending to be laboratory
footage or depending on an internet connection.
"""
import math

from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QColor, QFont, QPainter, QPen
from PySide6.QtWidgets import QWidget


class DemonstrationPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.experiment = "Double-slit experiment"
        self.phase = 0
        self.setMinimumWidth(270)
        self.setMinimumHeight(280)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        self.timer.start(60)

    def set_experiment(self, name):
        self.experiment = name
        self.phase = 0
        self.update()

    def _tick(self):
        self.phase = (self.phase + 1) % 360
        self.update()

    def _pen(self, color, width=2):
        return QPen(QColor(color), width, Qt.PenStyle.SolidLine)

    def _title(self, painter):
        painter.setPen(QColor("#b8f1df"))
        painter.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        painter.drawText(12, 23, "LIVE CONCEPT DEMO")
        painter.setPen(QColor("#a8b8cd"))
        painter.setFont(QFont("Segoe UI", 8))
        painter.drawText(12, self.height() - 12, "Offline educational animation")

    def paintEvent(self, _event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor("#0e1828"))
        self._title(painter)
        area_top, area_bottom = 38, self.height() - 30
        width, height = self.width(), area_bottom - area_top
        name = self.experiment
        if name == "Double-slit experiment":
            self._double_slit(painter, width, area_top, height)
        elif name == "Photoelectric effect":
            self._photoelectric(painter, width, area_top, height)
        elif name == "Quantum tunnelling":
            self._tunnelling(painter, width, area_top, height)
        elif name == "Particle in a box":
            self._box(painter, width, area_top, height)
        elif name == "Atomic orbitals":
            self._orbital(painter, width, area_top, height)
        elif name == "Heisenberg uncertainty principle":
            self._uncertainty(painter, width, area_top, height)
        elif name == "Quantum harmonic oscillator":
            self._oscillator(painter, width, area_top, height)
        elif name == "Numerical finite well":
            self._well(painter, width, area_top, height)
        else:
            self._measurements(painter, width, area_top, height)
        painter.end()

    def _double_slit(self, p, w, top, h):
        p.setPen(self._pen("#526176", 5))
        x = w * 0.38
        p.drawLine(int(x), top, int(x), top + int(h * .35))
        p.drawLine(int(x), top + int(h * .45), int(x), top + int(h * .55))
        p.drawLine(int(x), top + int(h * .65), int(x), top + h)
        p.setPen(self._pen("#64d8ff", 2))
        for offset in (-h * .1, h * .1):
            for radius in range(10, int(w * .55), 22):
                p.drawArc(int(x - radius), int(top + h * .5 + offset - radius), radius * 2, radius * 2, -65 * 16, 130 * 16)
        p.setPen(self._pen("#41b8a6", 2))
        screen = int(w * .82)
        for y in range(top + 8, top + h - 8, 12):
            intensity = (math.cos((y + self.phase * 2) / 13) + 1) / 2
            p.setPen(self._pen("#41b8a6", max(1, int(1 + intensity * 5))))
            p.drawPoint(screen, y)

    def _photoelectric(self, p, w, top, h):
        p.setPen(self._pen("#e0a04b", 3))
        metal_x = int(w * .6)
        p.drawLine(metal_x, top + 20, metal_x, top + h - 20)
        p.setPen(self._pen("#64d8ff", 2))
        for index in range(5):
            y = top + 35 + index * int((h - 70) / 4)
            x = (self.phase * 2 + index * 55) % int(w * .5)
            p.drawLine(x, y, min(x + 25, metal_x - 4), y)
        p.setBrush(QColor("#b8f1df"))
        p.setPen(Qt.PenStyle.NoPen)
        for index in range(5):
            x = metal_x + ((self.phase * 3 + index * 37) % int(w * .3))
            y = top + 35 + index * int((h - 70) / 4)
            p.drawEllipse(int(x), int(y - 4), 8, 8)

    def _tunnelling(self, p, w, top, h):
        barrier_x = int(w * .52)
        p.fillRect(barrier_x, top + 25, 36, h - 50, QColor("#5e435d"))
        p.setPen(self._pen("#a98bb8", 1))
        p.drawText(barrier_x - 2, top + 18, "barrier")
        particle_x = int((self.phase * 2) % (w * .95))
        y = top + h // 2 + int(math.sin(self.phase / 15) * 18)
        p.setBrush(QColor("#41b8a6" if particle_x > barrier_x + 36 else "#64d8ff"))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawEllipse(particle_x, y, 14, 14)
        p.setPen(self._pen("#526176", 1))
        p.drawLine(12, top + h // 2 + 28, w - 12, top + h // 2 + 28)

    def _box(self, p, w, top, h):
        left, right = 35, w - 35
        baseline = top + h // 2
        p.setPen(self._pen("#526176", 4))
        p.drawLine(left, top + 20, left, top + h - 20)
        p.drawLine(right, top + 20, right, top + h - 20)
        p.setPen(self._pen("#41b8a6", 2))
        points = []
        for x in range(left, right + 1, 3):
            normalized = (x - left) / (right - left)
            y = baseline - math.sin(3 * math.pi * normalized + self.phase / 30) * h * .28
            points.append((x, int(y)))
        for first, second in zip(points, points[1:]):
            p.drawLine(*first, *second)

    def _orbital(self, p, w, top, h):
        cx, cy = w // 2, top + h // 2
        stretch = int(35 + 8 * math.sin(self.phase / 24))
        p.setBrush(QColor("#9b6bd1"))
        p.setPen(self._pen("#d9b7ff", 1))
        p.drawEllipse(cx - stretch - 10, cy - 34, stretch, 68)
        p.setBrush(QColor("#41b8a6"))
        p.drawEllipse(cx + 10, cy - 34, stretch, 68)
        p.setBrush(QColor("#f0c45c"))
        p.drawEllipse(cx - 7, cy - 7, 14, 14)

    def _uncertainty(self, p, w, top, h):
        cx = w // 2 + int(math.sin(self.phase / 20) * 25)
        spread = 20 + int((math.sin(self.phase / 35) + 1) * 30)
        p.setPen(self._pen("#64d8ff", 2))
        last = None
        for x in range(20, w - 20, 2):
            y = top + h - 30 - int((h * .6) * math.exp(-((x - cx) / spread) ** 2))
            if last:
                p.drawLine(*last, x, y)
            last = (x, y)
        p.setPen(QColor("#a8b8cd"))
        p.drawText(20, top + 20, "narrower position → broader momentum")

    def _oscillator(self, p, w, top, h):
        cx, baseline = w // 2, top + h // 2
        p.setPen(self._pen("#526176", 1))
        for x in range(18, w - 18, 2):
            y = baseline - int(.005 * (x - cx) ** 2) + 55
            p.drawPoint(x, y)
        p.setPen(self._pen("#41b8a6", 2))
        last = None
        for x in range(25, w - 25, 2):
            z = (x - cx) / 45
            y = baseline - int(42 * math.exp(-z * z / 2) * math.cos(2 * z + self.phase / 28))
            if last:
                p.drawLine(*last, x, y)
            last = (x, y)

    def _well(self, p, w, top, h):
        left, right = int(w * .28), int(w * .72)
        base, depth = top + int(h * .3), int(h * .45)
        p.setPen(self._pen("#a98bb8", 3))
        p.drawLine(18, base, left, base)
        p.drawLine(left, base, left, base + depth)
        p.drawLine(left, base + depth, right, base + depth)
        p.drawLine(right, base + depth, right, base)
        p.drawLine(right, base, w - 18, base)
        p.setPen(self._pen("#41b8a6", 2))
        last = None
        for x in range(left + 2, right - 1, 2):
            y = base + depth - 25 - int(25 * math.sin((x - left) / 20 + self.phase / 30))
            if last:
                p.drawLine(*last, x, y)
            last = (x, y)

    def _measurements(self, p, w, top, h):
        p.setPen(self._pen("#526176", 1))
        p.drawLine(20, top + h - 35, w - 15, top + h - 35)
        p.drawLine(20, top + 20, 20, top + h - 35)
        p.setPen(self._pen("#41b8a6", 2))
        last = None
        for x in range(22, w - 15, 5):
            noise = math.sin(x * .33 + self.phase / 14) * 24 / math.sqrt(max(1, (x - 20) / 5))
            y = top + int(h * .45 + noise)
            if last:
                p.drawLine(*last, x, y)
            last = (x, y)
        p.setPen(QColor("#a8b8cd"))
        p.drawText(28, top + 20, "running measurement probability")
