from PyQt6.QtWidgets import (
    QGraphicsRectItem,
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


class ResizableRectangle(QGraphicsRectItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAcceptHoverEvents(True)
        self.setFlag(
            QGraphicsItem.GraphicsItemFlag.ItemIsMovable
            | QGraphicsItem.GraphicsItemFlag.ItemIsSelectable
        )
        self._resize_direction = None

    def hoverMoveEvent(self, event):
        if (
            abs(event.pos().x() - self.rect().left()) < 5
            and abs(event.pos().y() - self.rect().top()) < 5
        ):
            self.setCursor(Qt.CursorShape.SizeFDiagCursor)
            self._resize_direction = "TL"
        elif (
            abs(event.pos().x() - self.rect().right()) < 5
            and abs(event.pos().y() - self.rect().top()) < 5
        ):
            self.setCursor(Qt.CursorShape.SizeBDiagCursor)
            self._resize_direction = "TR"
        elif (
            abs(event.pos().x() - self.rect().right()) < 5
            and abs(event.pos().y() - self.rect().bottom()) < 5
        ):
            self.setCursor(Qt.CursorShape.SizeFDiagCursor)
            self._resize_direction = "BR"
        elif (
            abs(event.pos().x() - self.rect().left()) < 5
            and abs(event.pos().y() - self.rect().bottom()) < 5
        ):
            self.setCursor(Qt.CursorShape.SizeBDiagCursor)
            self._resize_direction = "BL"
        elif abs(event.pos().x() - self.rect().left()) < 5:
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
        if self._resize_direction == "L":
            self.setRect(
                event.pos().x(),
                rect.top(),
                rect.width() - (event.pos().x() - rect.left()),
                rect.height(),
            )
        elif self._resize_direction == "R":
            self.setRect(
                rect.left(), rect.top(), event.pos().x() - rect.left(), rect.height()
            )
        elif self._resize_direction == "T":
            self.setRect(
                rect.left(),
                event.pos().y(),
                rect.width(),
                rect.height() - (event.pos().y() - rect.top()),
            )
        elif self._resize_direction == "B":
            self.setRect(
                rect.left(), rect.top(), rect.width(), event.pos().y() - rect.top()
            )
        elif self._resize_direction == "TL":
            self.setRect(
                event.pos().x(),
                event.pos().y(),
                rect.width() + (rect.left() - event.pos().x()),
                rect.height() + (rect.top() - event.pos().y()),
            )
        elif self._resize_direction == "TR":
            self.setRect(
                rect.left(),
                event.pos().y(),
                event.pos().x() - rect.left(),
                rect.height() - (event.pos().y() - rect.top()),
            )
        elif self._resize_direction == "BR":
            self.setRect(
                rect.left(),
                rect.top(),
                event.pos().x() - rect.left(),
                event.pos().y() - rect.top(),
            )
        elif self._resize_direction == "BL":
            self.setRect(
                event.pos().x(),
                rect.top(),
                rect.width() - (event.pos().x() - rect.left()),
                event.pos().y() - rect.top(),
            )
        else:
            return super().mouseMoveEvent(event)

    def mouseDoubleClickEvent(self, event: QGraphicsSceneMouseEvent | None) -> None:
        dialog = TextInputRectangleEditDialog()
        if dialog.exec():
            width, height = dialog.getValues()
            self.setRect(event.pos().x(), event.pos().y(), width, height)
        return super().mouseDoubleClickEvent(event)


class TextInputRectangleDialog(QDialog):
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
        self.setWindowTitle("Rectangle Input")

    def getValues(self):
        start_x = float(self.startXLineEdit.text())
        start_y = float(self.startYLineEdit.text())
        width = float(self.widthLineEdit.text())
        height = float(self.heightLineEdit.text())
        return start_x, start_y, width, height


class TextInputRectangleEditDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Labels and LineEdits
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

        hLayout = QHBoxLayout()
        hLayout.addWidget(self.widthLabel)
        hLayout.addWidget(self.widthLineEdit)
        hLayout.addWidget(self.heightLabel)
        hLayout.addWidget(self.heightLineEdit)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.okButton)
        buttonLayout.addWidget(self.cancelButton)

        layout.addLayout(hLayout)
        layout.addLayout(buttonLayout)

        self.setLayout(layout)
        self.setWindowTitle("Rectangle Edit")

    def getValues(self):
        width = float(self.widthLineEdit.text())
        height = float(self.heightLineEdit.text())
        return width, height
