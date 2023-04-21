from geometry.shapes import Rectangle, Point, Line


def clip_point(point: Point, window: Rectangle) -> bool:
    """
    verifica se o ponto deve ser desenhado ou não
    """

    if window.x <= point.x <= (window.x + window.width):
        if window.y <= point.y <= (window.y + window.height):
            return True
    return False


def angular_coef(line: Line) -> float:
    start = line.start
    end = line.end

    return (end.y - start.y) / (end.x - start.x)
