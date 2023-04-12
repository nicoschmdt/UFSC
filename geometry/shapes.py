from dataclasses import dataclass
from typing import List


@dataclass
class Point:
    x: int
    y: int


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


@dataclass
class Wireframe:
    points: List[Point]


GraphicObject = Point | Line | Wireframe


@dataclass
class WorldItem:
    name: str
    center_point: Point
    graphic: GraphicObject
