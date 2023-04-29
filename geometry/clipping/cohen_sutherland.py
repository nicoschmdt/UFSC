from bitarray import bitarray
from dataclasses import dataclass

from geometry.shapes import Rectangle, Point, Line


@dataclass
class RegionCode:
    up: int
    down: int
    left: int
    right: int

    def to_bitarray(self) -> bitarray:
        return bitarray(f'{self.up}{self.down}{self.left}{self.right}')


def get_region_code(point: Point, window: Rectangle) -> RegionCode:
    region_code = RegionCode(0, 0, 0, 0)

    if point.x < window.x:
        region_code.left = 1

    if point.x > (window.x + window.width):
        region_code.right = 1

    if point.y < window.y:
        region_code.down = 1

    if point.y > (window.y + window.height):
        region_code.up = 1

    return region_code


def line_clipping(line: Line, window: Rectangle) -> (bool, Line | None):
    region_start = get_region_code(line.start, window).to_bitarray()
    region_end = get_region_code(line.end, window).to_bitarray()

    if (region_start | region_end) == bitarray('0000'):
        return True, line

    and_result = region_start & region_end
    if and_result != bitarray('0000'):
        return False, None
    elif region_start != region_end and and_result == bitarray('0000'):
        # new_line = clip_line(line, window, region_start, region_end)
        new_line = clip_line_partial(line, window, region_start, region_end)
        if new_line:
            return True, new_line

    return False, None


def clip_line_partial(line: Line, window: Rectangle, region_start: bitarray, region_end: bitarray) -> Line | None:
    coef = angular_coef(line)

    # gotta clip start_point only
    if region_end == bitarray('0000'):
        result, new_start_point = region_clip(line.start, window, region_start, coef)
        if result:
            return Line(new_start_point, line.end)
    # gotta clip end_point only
    elif region_start == bitarray('0000'):
        result, new_end_point = region_clip(line.end, window, region_end, coef)
        if result:
            return Line(line.start, new_end_point)
    # gotta clip both points
    else:
        result_start, new_start_point = region_clip(line.start, window, region_end, coef)
        result_end, new_end_point = region_clip(line.end, window, region_start, coef)
        if result_start and result_end:
            return Line(new_start_point, new_end_point)

    return None


def region_clip(point: Point, window: Rectangle, region: bitarray, angular_coef: float) -> (bool, Point):
    # UP
    if region & bitarray('1000') == bitarray('1000'):
        x = angular_coef * ((window.y + window.height) - point.y) + point.x

        if accept_clipped(x, window.x, (window.x + window.width)):
            return True, Point(x, (window.y + window.height))

    # DOWN
    if region & bitarray('0100') == bitarray('0100'):
        x = point.x + (angular_coef * (window.y - point.y))

        if accept_clipped(x, window.x, (window.x + window.width)):
            return True, Point(x, window.y)

    # LEFT
    if region & bitarray('0010') == bitarray('0010'):
        y = angular_coef * (window.x - point.x) + point.y

        if accept_clipped(y, window.y, (window.y + window.height)):
            return True, Point(window.x, y)

    # RIGHT
    if region & bitarray('0001') == bitarray('0001'):
        y = angular_coef * ((window.x + window.width) - point.x) + point.y

        if accept_clipped(y, window.y, (window.y + window.height)):
            return True, Point((window.x + window.width), y)

    return False, None


def accept_clipped(y: float, down: float, up: float) -> bool:
    if down <= y <= up:
        return True
    return False


def angular_coef(line: Line) -> float:
    start = line.start
    end = line.end

    if start.y == end.y or start.x == end.x:
        return 0

    return (end.y - start.y) / (end.x - start.x)
