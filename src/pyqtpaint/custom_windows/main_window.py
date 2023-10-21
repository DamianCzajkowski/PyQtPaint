from PyQt6.QtWidgets import QGraphicsScene, QMainWindow, QToolBar, QDialog
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor, QIcon, QAction, QPixmap
from pyqtpaint.custom_windows.color_window import ChooseColorDialog

from pyqtpaint.views.custom_view import CustomGraphicsView


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.scene = QGraphicsScene(0, 0, 500, 500)
        self.view = CustomGraphicsView(self.scene, self)
        self.input_type = "mouse"

        # Toolbar setup
        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)

        # Selection select mode
        self.select_action = QAction(QIcon.fromTheme("edit-select"), "Select Mode")
        self.select_action.setCheckable(True)
        self.select_action.triggered.connect(self.enableSelectionMode)
        self.toolbar.addAction(self.select_action)

        # Selection mouse input mode
        self.mouse_input_mode = QAction(
            QIcon.fromTheme("edit-select"), "Mouse input Mode"
        )
        self.mouse_input_mode.setCheckable(True)
        self.mouse_input_mode.triggered.connect(self.enableMouseInputMode)
        self.toolbar.addAction(self.mouse_input_mode)

        # # Selection text input mode
        self.text_input_mode = QAction(
            QIcon.fromTheme("edit-select"), "Text input Mode"
        )
        self.text_input_mode.setCheckable(True)
        self.text_input_mode.triggered.connect(self.enableTextInputMode)
        self.toolbar.addAction(self.text_input_mode)

        # Drawing line
        self.draw_line = QAction(QIcon.fromTheme("document-new"), "Draw Line")
        self.draw_line.setCheckable(True)
        self.draw_line.triggered.connect(lambda: self.enableDrawingMode("line"))
        self.toolbar.addAction(self.draw_line)

        # Drawing rectangle
        self.draw_rectangle = QAction(QIcon.fromTheme("document-new"), "Draw Rectangle")
        self.draw_rectangle.setCheckable(True)
        self.draw_rectangle.triggered.connect(
            lambda: self.enableDrawingMode("rectangle")
        )
        self.toolbar.addAction(self.draw_rectangle)

        # Drawing circle
        self.draw_circle = QAction(QIcon.fromTheme("document-new"), "Draw circle")
        self.draw_circle.setCheckable(True)
        self.draw_circle.triggered.connect(lambda: self.enableDrawingMode("circle"))
        self.toolbar.addAction(self.draw_circle)

        # Choose color
        self.choose_color = QAction(QIcon.fromTheme("document-new"), "Choose color")
        self.choose_color.setCheckable(True)
        self.choose_color.triggered.connect(self.chooseColor)
        self.toolbar.addAction(self.choose_color)

        self.setCentralWidget(self.view)

    def resetActions(self):
        self.select_action.setChecked(False)
        self.mouse_input_mode.setChecked(False)
        self.text_input_mode.setChecked(False)
        self.draw_line.setChecked(False)
        self.draw_rectangle.setChecked(False)
        self.draw_circle.setChecked(False)
        self.choose_color.setChecked(False)

    def enableDrawingMode(self, shape):
        if self.input_type == "mouse":
            self.resetActions()
            self.mouse_input_mode.setChecked(True)
            getattr(self, f"draw_{shape}").setChecked(True)
            self.view.setCursor(QCursor(Qt.CursorShape.CrossCursor))
            self.view.enableDrawingMode(shape, True)
        elif self.input_type == "text":
            self.view.enableTextMode(shape, False)

    def enableSelectionMode(self):
        self.resetActions()
        self.select_action.setChecked(True)
        self.view.unsetCursor()
        self.view.enableDrawingMode(None, False)

    def enableMouseInputMode(self):
        self.resetActions()
        self.mouse_input_mode.setChecked(True)
        self.view.unsetCursor()
        self.input_type = "mouse"

    def enableTextInputMode(self):
        self.resetActions()
        self.text_input_mode.setChecked(True)
        self.view.unsetCursor()
        self.input_type = "text"

    def chooseColor(self):
        color_converter_dialog = ChooseColorDialog()
        result = color_converter_dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            self.chosen_color = color_converter_dialog.color
            self.view.setCurrentColor(self.chosen_color)
