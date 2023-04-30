from geometry.shapes import Point, Line, Wireframe
from typing import List
import numpy

def is_polygon(points: List[Point]) -> bool:
    size = len(points)
    if size == 3:
        return True

    lines = []

    ref_point = points[0]
    for point in points[1:]:
        line = Line(ref_point, point)
        lines.append(line)
        ref_point = point
    lines.append(Line(ref_point, points[0]))

    consider = len(points) - 3
    for i, line in enumerate(lines):
        index = (i + 2) % size
        while consider > 0:
            if intersect(line, lines[index]):
                return False
            consider -= 1
            index = (index + 1) % size

    return True


def intersect(line1: Line, line2: Line) -> bool:
    o1 = orientation(line1.start, line1.end, line2.start)
    o2 = orientation(line1.start, line1.end, line2.end)
    o3 = orientation(line2.start, line2.end, line1.start)
    o4 = orientation(line2.start, line2.end, line1.end)

    if o1 != o2 and o3 != o4:
        return True

    if o1 == 0 and on_segment(line1, line2.start):
        return True
    elif o2 == 0 and on_segment(line1, line2.end):
        return True
    elif o3 == 0 and on_segment(line2, line1.start):
        return True
    elif o4 == 0 and on_segment(line2, line1.end):
        return True

    return False


def on_segment(line: Line, point: Point) -> bool:
    """
    Verifica se um ponto está em uma linha
    """
    point_a = line.start
    point_b = line.end
    if point.x <= max(point_a.x, point_b.x) and (point.x >= min(point_a.x, point_b.x)):
        if point.y <= max(point_a.y, point_b.y) and (point.y >= min(point_a.y, point_b.y)):
            return True
    return False


def orientation(point1: Point, point2: Point, point3: Point) -> int:
    """
    Retorna 0 para colinear, 1 para sentido horário e 2 para sentido anti-horário
    """

    signal = (point2.y - point1.y) * (point3.x - point2.x)
    signal -= (point3.y - point2.y) * (point2.x - point1.x)

    if signal > 0:
        return 1
    elif signal < 0:
        return 2

    return 0

def get_concave_edges(polygon: Wireframe) -> List[List[Point]]:
    vertices = polygon.points
    concave_edges = list()
    if orientation(polygon.points[0], polygon.points[1], polygon.points[2]) == 1:
        vertices = vertices.reverse()
    for i in range(len(vertices)-1):
        first_vector = numpy.array([vertices[i].x, vertices[i].y, 0])
        second_vector = numpy.array([vertices[i+1].x, vertices[i+1].y, 0])
        result = numpy.cross(first_vector, second_vector)
        if result[2] < 0:
            concave_edges.append([vertices[i], vertices[i+1]])
    first_vector = numpy.array([vertices[-1].x, vertices[-1].y, 0])
    second_vector = numpy.array([vertices[0].x, vertices[0].y, 0])
    result = numpy.cross(first_vector, second_vector)
    if result[2] < 0:
        concave_edges.append([vertices[-1], vertices[0]])
    return concave_edges

def split_polygon(polygon: Wireframe) -> List[Wireframe]:
    concave_edges = get_concave_edges(polygon)
    if len(concave_edges) == 0:
        return [polygon]
    vertices = polygon.points
    convex_polygons = list()
    concave_edge = concave_edges.pop(0)
    pass

def split_concave_polygon(polygon: Wireframe, concave_edge: List[Point]) -> List[Wireframe]:
    pass

# ax + by + c = 0 -> y = (a/b)x + (c/b)
def get_general_equation_coeffs_of_line(point1: Point, point2: Point):
    a = (point1.y - point1.y)
    b = (point2.x - point1.x)
    c = (point1.x * point2.y) - (point2.x * point1.y)
    return [(a/b), (c/b)]
