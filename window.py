from dataclasses import dataclass

import PyQt6
from typing import List
from PyQt6 import QtCore, QtGui
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPalette, QColor, QPainter


@dataclass
class Size:
    x: int
    y: int
    width: int
    height: int


@dataclass
class Point:
    x: int
    y: int


@dataclass
class Line:
    start: Point
    end: Point


@dataclass
class Wireframe:
    points: List[Point]


GraphicObject = Point | Line | Wireframe


@dataclass
class WorldItem:
    name: str
    graphic: GraphicObject


class Viewport:
    viewport_size: Size
    window_size: Size

    def __init__(self, x: int, y: int, width: int, height: int):
        self.viewport_size = Size(
            x=x,
            y=y,
            width=width,
            height=height
        )

    def draw(self, painter: QPainter, items: List[WorldItem]):
        painter.setPen(QColor.fromString('blue'))
        painter.drawRect(self.viewport_size.x, self.viewport_size.y, self.viewport_size.width,
                         self.viewport_size.height)
        for item in items:
            obj = item.graphic
            if isinstance(obj, Line):
                self.draw_line(obj.start.x, obj.start.y, obj.end.x, obj.end.y, painter)
            elif isinstance(obj, Point):
                self.draw_point(obj.x, obj.y, painter)
            elif isinstance(obj, Wireframe):
                self.draw_wireframe(obj.points, painter)

    def zoom(self, step: int):
        new_width = int(self.window_size.width * (1 - (step / 100)))
        new_height = int(self.window_size.height * (1 - (step / 100)))
        diff = self.window_size.width - new_width

        self.window_size = Size(
            x=int(diff / 2) + self.window_size.x,
            y=int(diff / 2) + self.window_size.y,
            width=new_width,
            height=new_height
        )

    def move_window(self, x: int, y: int):
        self.window_size.x += x
        self.window_size.y += y

    def set_window(self, x: int, y: int, width: int, height: int):
        self.window_size = Size(
            x=x,
            y=y,
            width=width,
            height=height
        )

    def transformada_vp_y(self, y: int):
        y_vp = 1 - ((y - self.window_size.y) / ((self.window_size.height + self.window_size.y) - self.window_size.y))
        y_vp *= (self.viewport_size.y + self.viewport_size.height) - self.viewport_size.y
        return int(y_vp + self.viewport_size.y)

    def transformada_vp_x(self, x: int):
        x_vp = ((x - self.window_size.x) / ((self.window_size.width + self.window_size.x) - self.window_size.x))
        x_vp *= (self.viewport_size.x + self.viewport_size.width) - self.viewport_size.x
        return int(x_vp + self.viewport_size.x)

    def draw_point(self, x: int, y: int, painter: QPainter):
        painter.drawPoint(
            int((self.viewport_size.x + self.viewport_size.width) / 2),
            int((self.viewport_size.y + self.viewport_size.height) / 2)
        )

    def draw_line(self, x1: int, y1: int, x2: int, y2: int, painter: QPainter):
        x1 = self.transformada_vp_x(x1)
        y1 = self.transformada_vp_y(y1)
        x2 = self.transformada_vp_x(x2)
        y2 = self.transformada_vp_y(y2)
        painter.drawLine(x1, y1, x2, y2)

    def draw_wireframe(self, points: List[Point], painter: QPainter):
        iterator_points = iter(points)
        first_point = next(iterator_points)
        previous_point = first_point
        for point in iterator_points:
            self.draw_line(previous_point.x, previous_point.y, point.x, point.y, painter)
            previous_point = point
        self.draw_line(previous_point.x, previous_point.y, point.x, point.y, painter)


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


def translate_points(points: list[Point], offset: Point):
    translated_points = []
    for point in points:
        new_point = Point(
            x=point.x + offset.x,
            y=point.y + offset.y
        )
        translated_points.append(new_point)

    return translated_points


def translacao(object: GraphicObject, offset: Point):
    if isinstance(object, Point):
        translated = translate_points([object], offset)[0]
        object.x = translated.x
        object.y = translated.y
    elif isinstance(object, Line):
        start, end = translate_points([object.start, object.end], offset)
        object.start = start
        object.end = end
    else:
        object.points = translate_points(object.points, offset)


# falta deixar o escalonamento em torno do centro do objeto
def scaling_points(points: list[Point], scaling):
    translated_points = []
    for point in points:
        new_point = Point(
            x=point.x * scaling,
            y=point.y * scaling
        )
        translated_points.append(new_point)

    return translated_points


def escalonamento(object: GraphicObject, scaling):
    if isinstance(object, Point):
        translated = scaling_points([object], scaling)[0]
        object.x = translated.x
        object.y = translated.y
    elif isinstance(object, Line):
        start, end = scaling_points([object.start, object.end], scaling)
        object.start = start
        object.end = end
    else:
        object.points = scaling_points(object.points, scaling)


def rotacao():
    pass
