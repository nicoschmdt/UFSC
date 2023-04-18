import math
from typing import Callable, List

import numpy
from geometry.shapes import Point, Line, WorldItem, GraphicObject


def translate_points(points: list[Point], offset: Point) -> List:
    translated_points = []
    for point in points:
        new_point = Point(
            x=point.x + offset.x,
            y=point.y + offset.y
        )
        translated_points.append(new_point)

    return translated_points


def translate(item: WorldItem, offset: Point) -> Callable:
    def funcao_translacao():
        shape_item = item.graphic
        if isinstance(shape_item, Point):
            translated = translate_points([shape_item], offset)[0]
            shape_item.x = translated.x
            shape_item.y = translated.y
            points = [Point(shape_item.x, shape_item.y)]
        elif isinstance(shape_item, Line):
            start, end = translate_points([shape_item.start, shape_item.end], offset)
            shape_item.start = start
            shape_item.end = end
            points = [shape_item.start, shape_item.end]
        else:
            shape_item.points = translate_points(shape_item.points, offset)
            points = shape_item.points
        item.center_point = calculate_object_center(points)

    return funcao_translacao


def scaling_points(points: list[Point], scaling, center_point: Point) -> List:
    matrix_center_neg = numpy.array([[1, 0, 0], [0, 1, 0], [-center_point.x, -center_point.y, 1]])
    matrix_scaling = numpy.array([[scaling, 0, 0], [0, scaling, 0], [0, 0, 1]])
    matrix_center_pos = numpy.array([[1, 0, 0], [0, 1, 0], [center_point.x, center_point.y, 1]])

    scale_matrix = matrix_center_neg @ matrix_scaling @ matrix_center_pos

    scaled_points = []
    for point in points:
        matrix_point = [point.x, point.y, 1]
        result = numpy.matmul(matrix_point, scale_matrix)

        new_point = Point(
            x=result[0],
            y=result[1]
        )
        scaled_points.append(new_point)

    return scaled_points


def scale(shape_item: GraphicObject, scaling, center_point: Point) -> Callable:
    def funcao_escalonamento():
        if isinstance(shape_item, Point):
            translated = scaling_points([shape_item], scaling, center_point)[0]
            shape_item.x = translated.x
            shape_item.y = translated.y
        elif isinstance(shape_item, Line):
            start, end = scaling_points([shape_item.start, shape_item.end], scaling, center_point)
            shape_item.start = start
            shape_item.end = end
        else:
            shape_item.points = scaling_points(shape_item.points, scaling, center_point)

    return funcao_escalonamento


def calculate_rotation(points: list[Point], reference: Point, degrees) -> List:
    cos = math.cos(degrees * math.pi / 180)
    sin = math.sin(degrees * math.pi / 180)
    matrix_center_neg = numpy.array([[1, 0, 0], [0, 1, 0], [-reference.x, -reference.y, 1]])
    matrix_scaling = numpy.array([[cos, -sin, 0], [sin, cos, 0], [0, 0, 1]])
    matrix_center_pos = numpy.array([[1, 0, 0], [0, 1, 0], [reference.x, reference.y, 1]])

    rotation_matrix = matrix_center_neg @ matrix_scaling @ matrix_center_pos

    rotated_points = []
    for point in points:
        matrix_point = [point.x, point.y, 1]
        result = numpy.matmul(matrix_point, rotation_matrix)

        new_point = Point(
            x=result[0],
            y=result[1]
        )
        rotated_points.append(new_point)

    return rotated_points


def rotate(item: WorldItem, reference: Point, graus) -> Callable:
    def funcao_rotacao():
        shape_item = item.graphic
        if isinstance(shape_item, Point):
            translated = calculate_rotation([shape_item], reference, graus)[0]
            shape_item.x = translated.x
            shape_item.y = translated.y
            points = [Point(shape_item.x, shape_item.y)]
        elif isinstance(shape_item, Line):
            start, end = calculate_rotation([shape_item.start, shape_item.end], reference, graus)
            shape_item.start = start
            shape_item.end = end
            points = [start, end]
        else:
            shape_item.points = calculate_rotation(shape_item.points, reference, graus)
            points = shape_item.points
        item.center_point = calculate_object_center(points)

    return funcao_rotacao


def calculate_object_center(points: list[Point]) -> Point:
    new_point_x = 0
    new_point_y = 0
    for point in points:
        new_point_x += point.x
        new_point_y += point.y
    x = int(new_point_x / len(points))
    y = int(new_point_y / len(points))
    return Point(x, y)


def determine_object_center(item: WorldItem):
    shape_item = item.graphic
    if isinstance(shape_item, Point):
        item.center_point = shape_item
    elif isinstance(shape_item, Line):
        item.center_point = calculate_object_center([shape_item.start, shape_item.end])
    else:
        item.center_point = calculate_object_center(shape_item.points)
