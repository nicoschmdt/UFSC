from dataclasses import dataclass

from calculation.shapes.point import Point


@dataclass
class Line:
    start: Point
    end: Point
