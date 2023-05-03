from geometry.clipping.cohen_sutherland import line_clipping as cs_clipping
from geometry.clipping.liang_barsky import line_clipping as lb_clipping
from geometry.clipping.weiler_atherton import is_point_inside
from geometry.shapes import Rectangle, Point, Line


def clip_point(point: Point, window: Rectangle) -> bool:
    """
    verifica se o ponto deve ser desenhado ou não
    """

    return is_point_inside(point, window)


def clip_line(line: Line, window: Rectangle, algorithm: str) -> (bool, Line):
    if algorithm == 'cohen sutherland':
        return cs_clipping(line, window)
    elif algorithm == 'liang barsky':
        return lb_clipping(line, window)

    return None, None
