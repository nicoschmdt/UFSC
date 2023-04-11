import PyQt6
from typing import List
from PyQt6 import QtCore, QtGui
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPalette, QColor, QPainter

from calculation.shapes.worldItem import WorldItem
from viewport import Viewport


class Canvas(QWidget):
    step: int
    viewport: Viewport
    world_items: List[WorldItem]

    def __init__(self, color='white', **kwargs):
        super(Canvas, self).__init__(**kwargs)
        self.setAutoFillBackground(True)
        self.setFocusPolicy(PyQt6.QtCore.Qt.FocusPolicy.ClickFocus)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)

        self.step = 10
        self.viewport = Viewport(10, 10, 670, 670)
        self.viewport.set_window(0, 0, 200, 200)

        self.world_items = []

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setPen(QColor.fromString('blue'))

        self.viewport.draw(painter, self.world_items)
        self.viewport.draw_line(-1000, 0, 1000, 0, painter)
        self.viewport.draw_line(0, -1000, 0, 1000, painter)
        # self.viewport.draw_line(30, 30, 90, 90, painter)

    # TODO: pegar o valor do step ao inves de usar algo fixo
    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        if event.key() == QtCore.Qt.Key.Key_Left:
            self.viewport.move_window(10, 0)
        elif event.key() == QtCore.Qt.Key.Key_Right:
            self.viewport.move_window(-10, 0)
        elif event.key() == QtCore.Qt.Key.Key_Up:
            self.viewport.move_window(0, -10)
        elif event.key() == QtCore.Qt.Key.Key_Down:
            self.viewport.move_window(0, 10)
        elif event.key() == QtCore.Qt.Key.Key_Plus:
            self.viewport.zoom(10)
        elif event.key() == QtCore.Qt.Key.Key_Minus:
            self.viewport.zoom(-10)
        else:
            super().keyPressEvent(event)

        self.repaint()
