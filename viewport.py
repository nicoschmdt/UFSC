from dataclasses import astuple
from typing import List

import numpy
from PyQt6.QtGui import QPainter, QColor, QPolygon, QBrush
from PyQt6.QtCore import QPoint

from geometry.clip import clip_point, clip_line
from geometry.clipping.weiler_atherton import polygon_clip
from geometry.transformations import calculate_rotation
from geometry.shapes import Point, Line, Rectangle, Wireframe, WorldItem, BezierCurve


class Viewport:
    viewport_size: Rectangle
    window_size: Rectangle
    window_angle: float = 0.0
    clipping_algorithm: str = 'cohen sutherland'

    def __init__(self, x: int, y: int, width: int, height: int):
        self.viewport_size = Rectangle(
            x=x,
            y=y,
            width=width,
            height=height
        )

    def draw(self, painter: QPainter, items: List[WorldItem]):
        painter.setPen(QColor.fromString('blue'))
        painter.setBrush(QColor.fromString('white'))
        painter.drawRect(self.viewport_size.x, self.viewport_size.y, self.viewport_size.width,
                         self.viewport_size.height)
        for item in items:
            obj = item.graphic
            if isinstance(obj, Line):
                visible, obj = clip_line(obj, self.window_size, self.clipping_algorithm)
                if visible:
                    self.draw_line(obj.start, obj.end, painter)
            elif isinstance(obj, Point):
                visible = clip_point(obj, self.window_size)
                if visible:
                    self.draw_point(obj.x, obj.y, painter)
            elif isinstance(obj, Wireframe):
                visible, obj = polygon_clip(obj, self.window_size)
                if visible:
                    if item.filled:
                        painter.setBrush(QBrush(QColor.fromString('blue')))
                        for wireframe in obj:
                            self.draw_filled_wireframe(wireframe.points, painter)
                    else:
                        for wireframe in obj:
                            self.draw_wireframe(wireframe.points, painter)

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
        point = calculate_rotation([Point(x, y)], Point(0, 0), -self.window_angle)

        self.window_size.x += point[0].x
        self.window_size.y += point[0].y

    def set_window(self, x: int, y: int, width: int, height: int):
        self.window_size = Rectangle(
            x=x,
            y=y,
            width=width,
            height=height
        )

    def set_window_angle(self, angle: float):
        self.window_angle = (self.window_angle + angle) % 360

    def set_line_clipping_algorithm(self, algorithm: str):
        self.clipping_algorithm = algorithm

    def transformada_vp_y(self, y: int):
        y_vp = 1 - ((y - self.window_size.y) / ((self.window_size.height + self.window_size.y) - self.window_size.y))
        y_vp *= (self.viewport_size.y + self.viewport_size.height) - self.viewport_size.y
        return int(y_vp + self.viewport_size.y)

    def transformada_vp_x(self, x: int):
        x_vp = ((x - self.window_size.x) / ((self.window_size.width + self.window_size.x) - self.window_size.x))
        x_vp *= (self.viewport_size.x + self.viewport_size.width) - self.viewport_size.x
        return int(x_vp + self.viewport_size.x)

    def get_window_center(self) -> Point:
        return Point(self.window_size.x + self.window_size.width // 2,
                     self.window_size.y + self.window_size.height // 2)

    def draw_point(self, x: float, y: float, painter: QPainter):
        rotated_point = calculate_rotation([Point(x, y)], self.get_window_center(), self.window_angle)

        x1 = self.transformada_vp_x(rotated_point[0].x)
        y1 = self.transformada_vp_y(rotated_point[0].y)
        painter.drawPoint(x1, y1)

    def draw_line(self, point1: Point, point2: Point, painter: QPainter):
        rotated_points = calculate_rotation([point1, point2], self.get_window_center(), self.window_angle)

        x1 = self.transformada_vp_x(rotated_points[0].x)
        y1 = self.transformada_vp_y(rotated_points[0].y)
        x2 = self.transformada_vp_x(rotated_points[1].x)
        y2 = self.transformada_vp_y(rotated_points[1].y)

        painter.drawLine(x1, y1, x2, y2)

    def draw_wireframe(self, points: List[Point], painter: QPainter):
        first_point = points[0]
        for point in points[1:]:
            self.draw_line(first_point, point, painter)
            first_point = point
        reference = points[0]
        self.draw_line(first_point, reference, painter)

    def draw_filled_wireframe(self, points: List[Point], painter: QPainter):
        polygon = QPolygon()
        for point in points:
            rotated_point = calculate_rotation([point], self.get_window_center(), self.window_angle)
            x = self.transformada_vp_x(rotated_point[0].x)
            y = self.transformada_vp_y(rotated_point[0].y)
            point = QPoint(x, y)
            polygon.append(point)
        painter.drawPolygon(polygon)

    def draw_bezier(self, curve: BezierCurve, painter: QPainter):
        steps = 100
        step_size = 1/steps

        x = list(map(astuple, [curve.p1, curve.p2, curve.p3, curve.p4]))
        points = numpy.array(x)
        bezier_matrix = numpy.array([
            [-1, 3, -3, 1],
            [3, -6, 3, 0],
            [-3, 3, 0, 0],
            [1, 0, 0, 0]])
        first_point = curve.p1

        for i in range(1, steps):
            t = i*step_size
            T = numpy.array([t**3, t**2, t, 1])

            bezier_curve = T @ bezier_matrix @ points
            second_point = Point(bezier_curve[0], bezier_curve[1])
            draw_line, line = clip_line(Line(first_point, second_point), self.window_size, self.clipping_algorithm)
            if draw_line:
                self.draw_line(line.start, line.end, painter)

            first_point = second_point
