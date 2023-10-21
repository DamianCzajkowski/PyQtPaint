from PyQt6.QtWidgets import QGraphicsView
from PyQt6.QtGui import QPen, QBrush
from PyQt6.QtCore import Qt, QRectF, QLineF, QPointF
from pyqtpaint.shapes.circle import ResizableCircle, TextInputCircleDialog
from pyqtpaint.shapes.line import ResizableLine, TextInputLineDialog
from pyqtpaint.shapes.rectangle import ResizableRectangle, TextInputRectangleDialog


class CustomGraphicsView(QGraphicsView):
    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)
        self.startPoint = None
        self.currentItem = None
        self.drawing_mode = False
        self.shape = "rectangle"
        self.pen = QPen(Qt.GlobalColor.white)
        self.brush = QBrush(Qt.GlobalColor.white)

    def enableDrawingMode(self, shape, enabled=True):
        self.drawing_mode = enabled
        self.shape = shape

    def enableTextMode(self, shape, enabled=True):
        self.drawing_mode = enabled
        self.shape = shape
        if self.shape == "rectangle":
            dialog = TextInputRectangleDialog(self)
            if dialog.exec():
                start_x, start_y, width, height = dialog.getValues()
                self.currentItem = ResizableRectangle(start_x, start_y, width, height)
        elif self.shape == "circle":
            dialog = TextInputCircleDialog(self)
            if dialog.exec():
                start_x, start_y, width, height = dialog.getValues()
                self.currentItem = ResizableCircle(start_x, start_y, width, height)
        elif self.shape == "line":
            dialog = TextInputLineDialog(self)
            if dialog.exec():
                (x1, y1, x2, y2) = dialog.getValues()
                self.currentItem = ResizableLine(x1, y1, x2, y2)
        if self.currentItem:
            self.currentItem.setPen(self.pen)
            if self.shape != "line":
                self.currentItem.setBrush(self.brush)
            self.scene().addItem(self.currentItem)

    def mousePressEvent(self, event):
        if self.drawing_mode:
            self.startPoint = event.pos()
            if self.shape == "rectangle":
                self.currentItem = ResizableRectangle()
                self.currentItem.setBrush(self.brush)
            elif self.shape == "circle":
                self.currentItem = ResizableCircle()
                self.currentItem.setBrush(self.brush)
            elif self.shape == "line":
                self.currentItem = ResizableLine()
            self.currentItem.setPen(self.pen)
            self.scene().addItem(self.currentItem)
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.startPoint and self.drawing_mode:
            end = self.mapToScene(event.pos())
            start = self.mapToScene(self.startPoint)
            if self.shape == "line":
                line = QLineF(start, end)
                self.currentItem.setLine(line)
            elif self.shape == "circle":
                # Oblicz odległość między punktami
                distance = (start - end).manhattanLength()

                # Ustal środek kwadratu
                center = QPointF((start.x() + end.x()) / 2, (start.y() + end.y()) / 2)

                # Ustal punkty początkowy i końcowy dla kwadratu
                square_start = QPointF(
                    center.x() - distance / 2, center.y() - distance / 2
                )
                square_end = QPointF(
                    center.x() + distance / 2, center.y() + distance / 2
                )

                # Stwórz kwadrat, w którym zawarte będzie koło
                rect = QRectF(square_start, square_end)

                self.currentItem.setRect(rect)
            else:
                rect = QRectF(start, end)
                self.currentItem.setRect(rect)
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.drawing_mode:
            self.startPoint = None
        else:
            super().mouseReleaseEvent(event)

    def setCurrentColor(self, color):
        self.pen.setColor(color)
        self.brush.setColor(color)

    def keyPressEvent(self, event):
        if event.key() in [Qt.Key.Key_Backspace, Qt.Key.Key_Delete]:
            for item in self.scene().selectedItems():
                self.scene().removeItem(item)
                del item
        return super().keyPressEvent(event)
