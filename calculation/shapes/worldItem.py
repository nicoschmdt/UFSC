from dataclasses import dataclass

from calculation.shapes.line import Line
from calculation.shapes.point import Point
from calculation.shapes.wireframe import Wireframe

GraphicObject = Point | Line | Wireframe


@dataclass
class WorldItem:
    name: str
    center_point: Point
    graphic: GraphicObject
