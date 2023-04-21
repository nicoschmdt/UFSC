from dataclasses import dataclass
from typing import List


@dataclass
class Point:
    x: float
    y: float


@dataclass
class Line:
    start: Point
    end: Point


@dataclass
class Rectangle:
    x: int
    y: int
    width: int
    height: int

    def get_points(self) -> [Point]:
        return [Point(self.x, self.y), Point((self.x + self.width), self.y),
                Point((self.x + self.width), (self.y + self.height)), Point(self.x, (self.y + self.width))]


@dataclass
class Wireframe:
    points: List[Point]


GraphicObject = Point | Line | Wireframe


@dataclass
class WorldItem:
    name: str
    center_point: Point
    graphic: GraphicObject
    filled: bool = False
