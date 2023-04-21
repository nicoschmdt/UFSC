from geometry.polygon import polygon_intersect
from geometry.shapes import Rectangle, Wireframe, Point, Line


def polygon_clipping(polygon: Wireframe, window: Rectangle):
    window_lines = get_lines_from_polygon(window.get_points())
    polygon_lines = get_lines_from_polygon(polygon.points)

    intersect, intersect_lines = polygon_intersect(window_lines, polygon_lines)
    # intersect_lines = (windowLine, polygonLine)
    if not intersect:
        # então ou o polygono está totalmente dentro ou totalmente fora
        # ou está longe e não será desenhado
        return

    # então existe alguma intersecção
    for window_line, polygon_line in intersect_lines:




def get_lines_from_polygon(polygon: [Point]) -> [Line]:
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
