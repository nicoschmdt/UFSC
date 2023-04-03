from dataclasses import dataclass

import PyQt6
from typing import List, Callable
from PyQt6 import QtCore, QtGui
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPalette, QColor, QPainter
import numpy
import math


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
    center_point: Point
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
        first_point = points[0]
        for point in points[1:]:
            self.draw_line(first_point.x, first_point.y, point.x, point.y, painter)
            first_point = point
        reference = points[0]
        self.draw_line(first_point.x, first_point.y, reference.x, reference.y, painter)


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


def calculate_object_center(points: list[Point]):
    new_point_x = 0
    new_point_y = 0
    for point in points:
        new_point_x += point.x
        new_point_y += point.y
    x = int(new_point_x / len(points))
    y = int(new_point_y / len(points))
    return Point(x=x, y=y)


def determine_object_center(item: WorldItem):
    object = item.graphic
    if isinstance(object, Point):
        item.center_point = object
    elif isinstance(object, Line):
        item.center_point = calculate_object_center([object.start, object.end])
    else:
        item.center_point = calculate_object_center(object.points)


def translate_points(points: list[Point], offset: Point):
    translated_points = []
    for point in points:
        new_point = Point(
            x=point.x + offset.x,
            y=point.y + offset.y
        )
        translated_points.append(new_point)

    return translated_points


def translacao(object: GraphicObject, offset: Point) -> Callable:
    def funcao_translacao():
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

    return funcao_translacao


def scaling_points(points: list[Point], scaling, center_point: Point):
    matrix_center_neg = [[1, 0, 0], [0, 1, 0], [-center_point.x, -center_point.y, 1]]
    matrix_scaling = [[scaling, 0, 0], [0, scaling, 0], [0, 0, 1]]
    matrix_center_pos = [[1, 0, 0], [0, 1, 0], [center_point.x, center_point.y, 1]]

    scaled_points = []
    for point in points:
        matrix_point = [point.x, point.y, 1]
        first = numpy.matmul(matrix_point, matrix_center_neg)
        second = numpy.matmul(first, matrix_scaling)
        result = numpy.matmul(second, matrix_center_pos)

        new_point = Point(
            x=result[0],
            y=result[1]
        )
        scaled_points.append(new_point)

    return scaled_points


def escalonamento(object: GraphicObject, scaling, center_point: Point) -> Callable:
    def funcao_escalonamento():
        if isinstance(object, Point):
            translated = scaling_points([object], scaling, center_point)[0]
            object.x = translated.x
            object.y = translated.y
        elif isinstance(object, Line):
            start, end = scaling_points([object.start, object.end], scaling, center_point)
            object.start = start
            object.end = end
        else:
            object.points = scaling_points(object.points, scaling, center_point)

    return funcao_escalonamento


def calculate_rotation(points: list[Point], reference: Point, graus):
    # cos = numpy.cos(graus)
    # sin = numpy.sin(graus)
    cos = math.cos(graus * math.pi / 180)
    sin = math.sin(graus * math.pi / 180)
    # print(graus)
    matrix_center_neg = [[1, 0, 0], [0, 1, 0], [-reference.x, -reference.y, 1]]
    matrix_scaling = [[cos, -sin, 0], [sin, cos, 0], [0, 0, 1]]
    matrix_center_pos = [[1, 0, 0], [0, 1, 0], [reference.x, reference.y, 1]]

    rotated_points = []
    for point in points:
        matrix_point = [point.x, point.y, 1]
        first = numpy.matmul(matrix_point, matrix_center_neg)
        second = numpy.matmul(first, matrix_scaling)
        result = numpy.matmul(second, matrix_center_pos)

        new_point = Point(
            x=result[0],
            y=result[1]
        )
        rotated_points.append(new_point)

    return rotated_points


def rotacao(object: GraphicObject, reference: Point, graus) -> Callable:
    def funcao_rotacao():
        if isinstance(object, Point):
            translated = calculate_rotation([object], reference, graus)[0]
            object.x = translated.x
            object.y = translated.y
        elif isinstance(object, Line):
            start, end = calculate_rotation([object.start, object.end], reference, graus)
            object.start = start
            object.end = end
        else:
            object.points = calculate_rotation(object.points, reference, graus)

    return funcao_rotacao
