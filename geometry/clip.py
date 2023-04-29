from geometry.clipping.cohen_sutherland import line_clipping as cs_clipping
from geometry.clipping.liang_barsky import line_clipping as lb_clipping
from geometry.shapes import Rectangle, Point, Line


def clip_point(point: Point, window: Rectangle) -> bool:
    """
    verifica se o ponto deve ser desenhado ou não
    """

    if window.x <= point.x <= (window.x + window.width):
        if window.y <= point.y <= (window.y + window.height):
            return True
    return False


def clip_line(line: Line, window: Rectangle, algorithm: str) -> (bool, Line):
    if algorithm == 'cohen sutherland':
        return cs_clipping(line, window)
    elif algorithm == 'liang_barsky':
        return lb_clipping(line, window)

    return None, None
