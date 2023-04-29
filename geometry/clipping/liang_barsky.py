from geometry.shapes import Rectangle, Line, Point


def line_clipping(line: Line, window: Rectangle) -> (bool, Line):
    p1 = - (line.end.x - line.start.x)
    p2 = - p1
    p3 = - (line.end.y - line.start.y)
    p4 = - p3

    q1 = line.start.x - window.x
    q2 = (window.x + window.width) - line.start.x
    q3 = line.start.y - window.y
    q4 = (window.y + window.height) - line.start.y

    m = angular_coef(line)

    parameters = [(p1, q1), (p2, q2), (p3, q3), (p4, q4)]

    if (p1 == 0 and q1 < 0) or (p2 == 0 and q2 < 0) or (p3 == 0 and q3 < 0) or (p4 == 0 and q4 < 0):
        return False

    pos = [q/p for (p, q) in parameters if p > 0]
    neg = [q/p for (p, q) in parameters if p < 0]

    rn1 = max(0, max(pos))
    rn2 = min(1, min(neg))

    if rn1 > rn2:
        return False

    xn1 = line.start.x + p2 * rn1
    yn1 = line.start.y + p4 * rn1

    xn2 = line.start.x + p2 * rn2
    yn2 = line.start.y + p4 * rn2

    return True, Line(Point(xn1, yn1), Point(xn2, yn2))


def angular_coef(line: Line) -> float:
    start = line.start
    end = line.end

    if start.y == end.y or start.x == end.x:
        return 0

    return (end.y - start.y) / (end.x - start.x)
