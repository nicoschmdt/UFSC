from geometry.shapes import Rectangle, Wireframe, Point, Line
from cohen_sutherland import line_clipping
from geometry.polygon import intersect, get_lines_from_polygon, point_inside_polygon

from typing import List


def polygon_clip(polygon: Wireframe, window: Rectangle) -> (bool, List[Wireframe]):
    intersect_quantity = polygon_position(polygon, window)

    if intersect_quantity == 0:
        # se todos os pontos estão dentro da window e as suas linhas não se intersectam
        if all([True if is_point_inside(point, window) else False for point in polygon.points]):
            return True, [polygon]
        # se todos os pontos da window estão dentro do poligono
        elif all([True if point_inside_polygon(point, polygon) else False for point in window.get_points()]):
            return True, [Wireframe(window.get_points())]
        # como nenhum ponto se intersecta, se não tem nenhum dentro então todos estão fora
        else:
            return False, None

    # agora preciso calcular caso a intersecção aconteça
    # tuplas indicando se o ponto está dentro ou fora da window
    polygon_points = [(point, True) if is_point_inside(point, window) else False for point in polygon.points]
    polygon_points.append(polygon_points[0])

    wireframes = []
    new_polygon_points = []
    # initial_polygon_point,  initial_inside = polygon_points[0]
    outside_in = 0
    inside_out = False
    polygon_point_checked = None
    point_outside = None
    for polygon_point, inside_window in polygon_points:
        if inside_window:
            # primeira iteração
            if point_outside is None:
                point_outside = False
            # ponto de dentro pra dentro
            elif not point_outside:
                new_polygon_points.append(polygon_point)
            # ponto de fora pra dentro
            elif point_outside:
                point_outside = False
                line = Line(polygon_point_checked, polygon_point)
                line = line_clipping(line, window)
                new_polygon_points.append(line.start)
                new_polygon_points.append(line.end)
                outside_in = 1

        # nessa parte o ponto atual está fora
        # de dentro pra fora
        elif not point_outside and point_outside is not None:
            point_outside = True
            line = Line(polygon_point, polygon_point_checked)
            line = line_clipping(line, window)
            new_polygon_points.append(line.end)
            if outside_in == 0:
                inside_out = True
            elif outside_in == 1:
                outside_in = 0
            # ainda preciso ldiar com o preenchimento das quinas mas vejo depois
            wireframes.append(Wireframe(new_polygon_points))
            new_polygon_points = []

        polygon_point_checked = polygon_point

    if inside_out:
        # adicionar pontos restantes no primeiro wireframe da lista
        pass


def polygon_position(polygon: Wireframe, window: Rectangle) -> int:
    intersect_points = 0
    window_lines = get_lines_from_polygon(window.get_points())
    polygon_lines = get_lines_from_polygon(polygon.points)

    for window_line in window_lines:
        for polygon_line in polygon_lines:
            if intersect(window_line, polygon_line):
                intersect_points += 1

    return intersect_points


def is_point_inside(point: Point, window: Rectangle) -> bool:
    if window.x <= point.x <= (window.x + window.width):
        if window.y <= point.y <= (window.y + window.height):
            return True
    return False


def polygon_clipping(polygon: Wireframe, window: Rectangle):
    window_points = window.get_points()
    polygon_coordinates = [(point.x, point.x) for point in polygon.points]

    # 0 = original
    # 1 = enter
    # 2 = exit

    # First step: build two lists of vertices
    window_vertices = [((window_points[0].x, window_points[0].y), 0), ((window_points[1].x, window_points[1].y), 0),
                       ((window_points[2].x, window_points[2].y), 0), ((window_points[3].x, window_points[3].y), 0)]
    object_vertices = [(coordinate, 0) for coordinate in polygon_coordinates]

    number_points = len(object_vertices)
    enter_points = []
    # Second step: calculate intersections
    for index in range(number_points):
        p0 = polygon_coordinates[index]
        p1 = polygon_coordinates[(index + 1) % number_points]

        line = Line(Point(p0[0], p0[1]), Point(p1[0], p1[1]))

        (is_visible, new_line) = line_clipping(line, window)

        new_p0 = (new_line.start.x, new_line.start.y)
        new_p1 = (new_line.end.x, new_line.end.y)

        if is_visible:
            if new_p1 != p1:
                # Exit point
                point_index = object_vertices.index((p0, 0)) + 1
                # Append new point right after the original
                object_vertices.insert(point_index, (new_p1, 2))
                window_vertices = get_window_index(window_vertices, new_p1, 2)

            if new_p0 != p0:
                # Enter point
                point_index = object_vertices.index((p0, 0)) + 1
                # Append new point right after the original
                object_vertices.insert(point_index, (new_p0, 1))
                enter_points.append((new_p0, 1))
                window_vertices = get_window_index(window_vertices, new_p0, 1)

    new_polygons = []
    new_points = []
    # If enter points is empty, return the own coordinates
    if enter_points != []:
        # Repeat until empty enter points
        while enter_points != []:
            # Get first point from enter
            reference_point = enter_points.pop(0)
            rf_p, _ = reference_point
            inside_points = [rf_p]
            point_index = object_vertices.index(reference_point) + 1
            new_points.append(reference_point)

            obj_len = len(object_vertices)
            for aux_index in range(obj_len):
                (p, c) = object_vertices[(point_index + aux_index) % obj_len]
                new_points.append((p, c))
                inside_points.append(p)
                if c != 0:
                    break

            last_point = new_points[-1]
            point_index = window_vertices.index(last_point)
            window_len = len(window_vertices)
            for aux_index in range(window_len):
                (p, c) = window_vertices[(point_index + aux_index) % window_len]
                new_points.append((p, c))
                inside_points.append(p)
                if c != 0:
                    break

            new_polygons.append(inside_points)
        coordinates = new_polygons
    else:
        coordinates = [polygon_coordinates]

    # print(f"Coordinates after weiler_atherton={coordinates}")
    return True, coordinates


def get_window_index(window_vertices, point, code):
    x, y = point
    # The index from window vertices list must be the
    # right before the next window vertice
    if x == 1:
        # Right, so right bottom
        index = window_vertices.index(((1, -1), 0))
        window_vertices.insert(index, (point, code))
    if x == -1:
        # Left, so left top
        index = window_vertices.index(((-1, 1), 0))

        window_vertices.insert(index, (point, code))
    if y == 1:
        # Top, so right top
        index = window_vertices.index(((1, 1), 0))
        window_vertices.insert(index, (point, code))
    if y == -1:
        # Bottom, so left bottom
        index = window_vertices.index(((-1, -1), 0))
        window_vertices.insert(index, (point, code))
    return window_vertices


def get_lines_from_polygon(polygon: List[Point]) -> List[Line]:
    lines = []
    initial_point = polygon[0]
    for point in polygon[1:]:
        lines.append(Line(initial_point, point))
        initial_point = point
    lines.append(Line(initial_point, polygon[0]))
    return lines

# algorithm: Given polygon A(window) as the clipping region and polygon B as the subject polygon to be clipped,
# the algorithm consists of the following steps:
#
# [x] List the vertices of the clipping-region polygon A and those of the subject polygon B.
# Label the listed vertices of subject polygon B as either inside or outside of clipping region A.
# Find all the polygon intersections and insert them into both lists, linking the lists at the intersections.
# Generate a list of "inbound" intersections – the intersections where the vector from the intersection to the subsequent
# vertex of subject polygon B begins inside the clipping region.
# Follow each intersection clockwise around the linked lists until the start position is found.
#
# If there are no intersections then one of three conditions must be true:
#
#     A is inside B – return A for clipping, B for merging.
#     B is inside A – return B for clipping, A for merging.
#     A and B do not overlap – return None for clipping or A & B for merging
