from math import sqrt
from PyQt6.QtWidgets import (
    QGraphicsEllipseItem,
    QGraphicsItem,
    QDialog,
    QGraphicsSceneMouseEvent,
    QHBoxLayout,
    QLineEdit,
    QVBoxLayout,
    QPushButton,
    QLabel,
)
from PyQt6.QtCore import Qt


class ResizableCircle(QGraphicsEllipseItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAcceptHoverEvents(True)
        self.setFlag(
            QGraphicsItem.GraphicsItemFlag.ItemIsMovable
            | QGraphicsItem.GraphicsItemFlag.ItemIsSelectable
        )
        self._resize_direction = None

    def hoverMoveEvent(self, event):
        if abs(event.pos().x() - self.rect().left()) < 5:
            self.setCursor(Qt.CursorShape.SizeHorCursor)
            self._resize_direction = "L"
        elif abs(event.pos().x() - self.rect().right()) < 5:
            self.setCursor(Qt.CursorShape.SizeHorCursor)
            self._resize_direction = "R"
        elif abs(event.pos().y() - self.rect().top()) < 5:
            self.setCursor(Qt.CursorShape.SizeVerCursor)
            self._resize_direction = "T"
        elif abs(event.pos().y() - self.rect().bottom()) < 5:
            self.setCursor(Qt.CursorShape.SizeVerCursor)
            self._resize_direction = "B"
        else:
            self.unsetCursor()
            self._resize_direction = None

    def mouseMoveEvent(self, event):
        rect = self.rect()
        if self._resize_direction:
            diff_x = event.pos().x() - rect.center().x()
            diff_y = event.pos().y() - rect.center().y()
            radius = sqrt(diff_x**2 + diff_y**2)

            # Ustaw nowe koło
            self.setRect(
                rect.center().x() - radius,
                rect.center().y() - radius,
                2 * radius,
                2 * radius,
            )
        else:
            super().mouseMoveEvent(event)

    def mouseDoubleClickEvent(self, event: QGraphicsSceneMouseEvent | None) -> None:
        dialog = TextInputCircleEditDialog()
        if dialog.exec():
            radius = dialog.getValues()
            self.setRect(
                event.pos().x() - radius,
                event.pos().y() - radius,
                2 * radius,
                2 * radius,
            )
        return super().mouseDoubleClickEvent(event)


class TextInputCircleDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Labels and LineEdits
        self.startXLabel = QLabel("Start X:")
        self.startXLineEdit = QLineEdit()
        self.startYLabel = QLabel("Start Y:")
        self.startYLineEdit = QLineEdit()

        self.widthLabel = QLabel("Width:")
        self.widthLineEdit = QLineEdit()
        self.heightLabel = QLabel("Height:")
        self.heightLineEdit = QLineEdit()

        # Buttons
        self.okButton = QPushButton("OK")
        self.okButton.clicked.connect(self.accept)
        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.clicked.connect(self.reject)

        # Layouts
        layout = QVBoxLayout()

        hLayout1 = QHBoxLayout()
        hLayout1.addWidget(self.startXLabel)
        hLayout1.addWidget(self.startXLineEdit)
        hLayout1.addWidget(self.startYLabel)
        hLayout1.addWidget(self.startYLineEdit)

        hLayout2 = QHBoxLayout()
        hLayout2.addWidget(self.widthLabel)
        hLayout2.addWidget(self.widthLineEdit)
        hLayout2.addWidget(self.heightLabel)
        hLayout2.addWidget(self.heightLineEdit)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.okButton)
        buttonLayout.addWidget(self.cancelButton)

        layout.addLayout(hLayout1)
        layout.addLayout(hLayout2)
        layout.addLayout(buttonLayout)

        self.setLayout(layout)
        self.setWindowTitle("Circle Input")

    def getValues(self):
        start_x = float(self.startXLineEdit.text())
        start_y = float(self.startYLineEdit.text())
        width = float(self.widthLineEdit.text())
        height = float(self.heightLineEdit.text())
        return start_x, start_y, width, height


class TextInputCircleEditDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Labels and LineEdits
        self.radiusLabel = QLabel("Radius:")
        self.radiusLineEdit = QLineEdit()

        # Buttons
        self.okButton = QPushButton("OK")
        self.okButton.clicked.connect(self.accept)
        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.clicked.connect(self.reject)

        # Layouts
        layout = QVBoxLayout()

        hLayout = QHBoxLayout()
        hLayout.addWidget(self.radiusLabel)
        hLayout.addWidget(self.radiusLineEdit)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.okButton)
        buttonLayout.addWidget(self.cancelButton)

        layout.addLayout(hLayout)
        layout.addLayout(buttonLayout)

        self.setLayout(layout)
        self.setWindowTitle("Circle Edit")

    def getValues(self):
        radius = float(self.radiusLineEdit.text())
        return radius
