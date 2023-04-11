from dataclasses import dataclass
from typing import List

from calculation.shapes.point import Point


@dataclass
class Wireframe:
    points: List[Point]
