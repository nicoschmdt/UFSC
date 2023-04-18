from geometry.shapes import Point, Line


def is_polygon(points: list[Point]) -> bool:
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
