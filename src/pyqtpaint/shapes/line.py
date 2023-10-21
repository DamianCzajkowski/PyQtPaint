from PyQt6.QtWidgets import (
    QGraphicsLineItem,
    QGraphicsItem,
    QDialog,
    QGraphicsSceneMouseEvent,
    QHBoxLayout,
    QLineEdit,
    QVBoxLayout,
    QPushButton,
    QLabel,
)
from PyQt6.QtCore import Qt, QLineF


class ResizableLine(QGraphicsLineItem):
    def __init__(self, *args):
        super().__init__(*args)
        self.setAcceptHoverEvents(True)
        self.setFlag(
            QGraphicsItem.GraphicsItemFlag.ItemIsMovable
            | QGraphicsItem.GraphicsItemFlag.ItemIsSelectable
        )
        self._resize_direction = None

    def hoverMoveEvent(self, event):
        if (self.line().p1() - event.pos()).manhattanLength() < 10:
            self._resize_direction = "L"
            self.setCursor(Qt.CursorShape.PointingHandCursor)
        elif (self.line().p2() - event.pos()).manhattanLength() < 10:
            self._resize_direction = "R"
            self.setCursor(Qt.CursorShape.PointingHandCursor)
        else:
            self.unsetCursor()
            self._resize_direction = None

    def mouseMoveEvent(self, event):
        if self._resize_direction == "L":
            self.setLine(QLineF(event.pos(), self.line().p2()))
        elif self._resize_direction == "R":
            self.setLine(QLineF(self.line().p1(), event.pos()))
        else:
            super().mouseMoveEvent(event)

    def mouseDoubleClickEvent(self, event: QGraphicsSceneMouseEvent | None) -> None:
        dialog = TextInputLineEditDialog()
        if dialog.exec():
            start_x, start_y, end_x, end_y = dialog.getValues()
            self.setLine(start_x, start_y, end_x, end_y)
        return super().mouseDoubleClickEvent(event)


class TextInputLineDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Labels and LineEdits
        self.startXLabel = QLabel("Start X:")
        self.startXLineEdit = QLineEdit()
        self.startYLabel = QLabel("Start Y:")
        self.startYLineEdit = QLineEdit()

        self.endXLabel = QLabel("End X:")
        self.endtXLineEdit = QLineEdit()
        self.endYLabel = QLabel("End Y:")
        self.endYLineEdit = QLineEdit()
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
        hLayout2.addWidget(self.endXLabel)
        hLayout2.addWidget(self.endtXLineEdit)
        hLayout2.addWidget(self.endYLabel)
        hLayout2.addWidget(self.endYLineEdit)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.okButton)
        buttonLayout.addWidget(self.cancelButton)

        layout.addLayout(hLayout1)
        layout.addLayout(hLayout2)
        layout.addLayout(buttonLayout)

        self.setLayout(layout)
        self.setWindowTitle("Line Input")

    def getValues(self):
        start_x = float(self.startXLineEdit.text())
        start_y = float(self.startYLineEdit.text())
        end_x = float(self.endtXLineEdit.text())
        end_y = float(self.endYLineEdit.text())
        return start_x, start_y, end_x, end_y


class TextInputLineEditDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Labels and LineEdits
        self.startXLabel = QLabel("Start X:")
        self.startXLineEdit = QLineEdit()
        self.startYLabel = QLabel("Start Y:")
        self.startYLineEdit = QLineEdit()

        self.endXLabel = QLabel("End X:")
        self.endtXLineEdit = QLineEdit()
        self.endYLabel = QLabel("End Y:")
        self.endYLineEdit = QLineEdit()
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
        hLayout2.addWidget(self.endXLabel)
        hLayout2.addWidget(self.endtXLineEdit)
        hLayout2.addWidget(self.endYLabel)
        hLayout2.addWidget(self.endYLineEdit)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.okButton)
        buttonLayout.addWidget(self.cancelButton)

        layout.addLayout(hLayout1)
        layout.addLayout(hLayout2)
        layout.addLayout(buttonLayout)

        self.setLayout(layout)
        self.setWindowTitle("Line Edit")

    def getValues(self):
        start_x = float(self.startXLineEdit.text())
        start_y = float(self.startYLineEdit.text())
        end_x = float(self.endtXLineEdit.text())
        end_y = float(self.endYLineEdit.text())
        return start_x, start_y, end_x, end_y
