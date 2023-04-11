from typing import List

from PyQt6.QtGui import QPainter, QColor

from calculation.transformations import calculate_rotation
from calculation.polygon import is_polygon
from calculation.shapes.line import Line
from calculation.shapes.point import Point
from calculation.shapes.rectangle import Rectangle
from calculation.shapes.wireframe import Wireframe
from common.errors import NotAPolygon
from window import WorldItem


class Viewport:
    viewport_size: Rectangle
    window_size: Rectangle
    window_angle: float = 0.0

    def __init__(self, x: int, y: int, width: int, height: int):
        self.viewport_size = Rectangle(
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

        self.window_size = Rectangle(
            x=int(diff / 2) + self.window_size.x,
            y=int(diff / 2) + self.window_size.y,
            width=new_width,
            height=new_height
        )

    def move_window(self, x: int, y: int):
        self.window_size.x += x
        self.window_size.y += y

    def set_window(self, x: int, y: int, width: int, height: int):
        self.window_size = Rectangle(
            x=x,
            y=y,
            width=width,
            height=height
        )

    def set_window_angle(self, angle: float):
        self.window_angle += angle

    def transformada_vp_y(self, y: int):
        y_vp = 1 - ((y - self.window_size.y) / ((self.window_size.height + self.window_size.y) - self.window_size.y))
        y_vp *= (self.viewport_size.y + self.viewport_size.height) - self.viewport_size.y
        return int(y_vp + self.viewport_size.y)

    def transformada_vp_x(self, x: int):
        x_vp = ((x - self.window_size.x) / ((self.window_size.width + self.window_size.x) - self.window_size.x))
        x_vp *= (self.viewport_size.x + self.viewport_size.width) - self.viewport_size.x
        return int(x_vp + self.viewport_size.x)

    def draw_point(self, x: int, y: int, painter: QPainter):
        painter.drawPoint(x, y)

    def draw_line(self, x1: int, y1: int, x2: int, y2: int, painter: QPainter):
        window_center = Point(self.window_size.x + self.window_size.width // 2,
                              self.window_size.y + self.window_size.height // 2)

        rotated_points = calculate_rotation([Point(x1, y1), Point(x2, y2)], window_center, self.window_angle)

        x1 = self.transformada_vp_x(rotated_points[0].x)
        y1 = self.transformada_vp_y(rotated_points[0].y)
        x2 = self.transformada_vp_x(rotated_points[1].x)
        y2 = self.transformada_vp_y(rotated_points[1].y)

        painter.drawLine(x1, y1, x2, y2)

    def draw_wireframe(self, points: List[Point], painter: QPainter):
        if not is_polygon(points):
            raise NotAPolygon

        first_point = points[0]
        for point in points[1:]:
            self.draw_line(first_point.x, first_point.y, point.x, point.y, painter)
            first_point = point
        reference = points[0]
        self.draw_line(first_point.x, first_point.y, reference.x, reference.y, painter)