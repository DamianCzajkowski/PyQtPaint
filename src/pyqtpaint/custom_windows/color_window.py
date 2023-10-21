from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QPushButton,
    QColorDialog,
    QLineEdit,
    QFormLayout,
    QHBoxLayout,
    QComboBox,
    QLabel,
)
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt


class ChooseColorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.color = QColor(Qt.GlobalColor.white)

        # Drop down to choose between RGB and CMYK
        self.color_mode_combo = QComboBox()
        self.color_mode_combo.addItems(["RGB", "CMYK"])

        # Labels and LineEdits
        self.rgbEdit = QLineEdit()
        self.cmykEdit = QLineEdit()
        self.cmykEdit.setMinimumWidth(200)

        # Convert button
        self.convertBtn = QPushButton("Convert")
        self.convertBtn.clicked.connect(self.convert)

        # Color preview label
        self.colorLabel = QLabel(self)
        self.colorLabel.setFixedSize(50, 50)
        self.colorLabel.setStyleSheet(f"background-color: {self.color.name()}")

        # Layouts
        layout = QVBoxLayout()

        chooseColorBtn = QPushButton("Choose Color")
        chooseColorBtn.clicked.connect(self.showColorDialog)

        formLayout = QFormLayout()
        formLayout.addRow("Convert:", self.color_mode_combo)
        formLayout.addRow("RGB:", self.rgbEdit)
        formLayout.addRow("CMYK:", self.cmykEdit)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.convertBtn)
        buttonLayout.addWidget(QPushButton("OK", clicked=self.accept))
        buttonLayout.addWidget(QPushButton("Cancel", clicked=self.reject))

        layout.addWidget(self.colorLabel)
        layout.addWidget(chooseColorBtn)
        layout.addLayout(formLayout)
        layout.addLayout(buttonLayout)

        self.setLayout(layout)
        self.setWindowTitle("Choose Color")

    def showColorDialog(self):
        color = QColorDialog.getColor()
        if color.isValid():
            r, g, b, _ = color.getRgb()
            c, m, y, k = self.rgb_to_cmyk(r, g, b)
            self.rgbEdit.setText(f"{r}, {g}, {b}")
            self.cmykEdit.setText(f"{c:.2f}, {m:.2f}, {y:.2f}, {k:.2f}")

            # Update the colorLabel to show the selected color
            self.colorLabel.setStyleSheet(f"background-color: {color.name()}")

    def rgb_to_cmyk(self, r, g, b):
        c = 1 - r / 255.0
        m = 1 - g / 255.0
        y = 1 - b / 255.0
        k = min(c, m, y)
        if k < 1:
            c = (c - k) / (1 - k)
            m = (m - k) / (1 - k)
            y = (y - k) / (1 - k)
        else:
            c = m = y = 0
        self.color = QColor(r, g, b)
        return c * 100, m * 100, y * 100, k * 100

    def cmyk_to_rgb(self, c, m, y, k):
        # Convert percentage values to the range [0, 1]
        c /= 100.0
        m /= 100.0
        y /= 100.0
        k /= 100.0

        r = 255 * (1 - c) * (1 - k)
        g = 255 * (1 - m) * (1 - k)
        b = 255 * (1 - y) * (1 - k)

        # Round the float values to the nearest integers
        r_int = round(r)
        g_int = round(g)
        b_int = round(b)

        self.color = QColor(r_int, g_int, b_int)

        return (r_int, g_int, b_int)

    def convert(self):
        if self.color_mode_combo.currentText() == "RGB" and self.rgbEdit.text():
            try:
                r, g, b = map(int, self.rgbEdit.text().split(","))
            except Exception:
                return
            c, m, y, k = self.rgb_to_cmyk(r, g, b)
            self.cmykEdit.setText(f"{c:.2f}, {m:.2f}, {y:.2f}, {k:.2f}")
            self.colorLabel.setStyleSheet(f"background-color: rgb({r}, {g}, {b});")
        elif self.color_mode_combo.currentText() == "CMYK" and self.cmykEdit.text():
            try:
                c, m, y, k = map(float, self.cmykEdit.text().split(","))
            except Exception:
                return
            r, g, b = self.cmyk_to_rgb(c, m, y, k)
            self.rgbEdit.setText(f"{r}, {g}, {b}")
            self.colorLabel.setStyleSheet(f"background-color: rgb({r}, {g}, {b});")
