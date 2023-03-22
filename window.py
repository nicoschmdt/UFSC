from dataclasses import dataclass
from PyQt6.QtWidgets import QMainWindow,QWidget
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QPalette, QColor, QPainter


@dataclass
class Size:
    x: int
    y: int
    width: int
    height: int


@dataclass
class Point:
    x: int
    y: int


@dataclass
class Line:
    start: Point
    end: Point


@dataclass
class Wireframe:
    points: list[Point]


@dataclass
class WorldItem:
    name: str
    graphic: Point | Line | Wireframe


class Viewport:
    viewport_size: Size
    window_size: Size

    def __init__(self, x: int, y: int, width: int, height: int):
        self.viewport_size = Size(
            x=x,
            y=y,
            width=width,
            height=height
        )

    def draw(self, painter: QPainter, items: list[WorldItem]):
        painter.setPen(QColor.fromString('blue'))
        painter.drawRect(self.viewport_size.x, self.viewport_size.y, self.viewport_size.width,
                         self.viewport_size.height)
        for item in items:
            obj = item.graphic
            if isinstance(obj, Line):
                self.draw_line(obj.start.x, obj.start.y, obj.end.x, obj.end.y, painter)
            elif isinstance(obj, Point):
                self.draw_point(obj.x, obj.y, painter)
            elif isinstance(obj, Wireframe):
                self.draw_wireframe(obj.points)

    def zoom(self, step: int):
        new_width = int(self.window_size.width * (1 - (step / 100)))
        new_height = int(self.window_size.height * (1 - (step / 100)))
        diff = self.window_size.width - new_width

        self.window_size = Size(
            x=int(diff / 2) + self.window_size.x,
            y=int(diff / 2) + self.window_size.y,
            width=new_width,
            height=new_height
        )

    def move_window(self, x: int, y: int):
        self.window_size.x += x
        self.window_size.y += y

    def set_window(self, x: int, y: int, width: int, height: int):
        self.window_size = Size(
            x=x,
            y=y,
            width=width,
            height=height
        )

    def transformada_vp_y(self, y):
        y_vp = 1 - ((y - self.window_size.y) / ((self.window_size.height + self.window_size.y) - self.window_size.y))
        y_vp *= (self.viewport_size.y + self.viewport_size.height) - self.viewport_size.y
        return int(y_vp + self.viewport_size.y)

    def transformada_vp_x(self, x):
        x_vp = ((x - self.window_size.x) / ((self.window_size.width + self.window_size.x) - self.window_size.x))
        x_vp *= (self.viewport_size.x + self.viewport_size.width) - self.viewport_size.x
        return int(x_vp + self.viewport_size.x)

    def draw_point(self, x: int, y: int, painter: QPainter):
        painter.drawPoint(
            int((self.viewport_size.x + self.viewport_size.width) / 2),
            int((self.viewport_size.y + self.viewport_size.height) / 2)
        )

    def draw_line(self, x1, y1, x2, y2, painter: QPainter):
        # print(f'x1={x1}, y1={y1}, x2={x2}, y2={y2}')
        x1 = self.transformada_vp_x(x1)
        y1 = self.transformada_vp_y(y1)
        x2 = self.transformada_vp_x(x2)
        y2 = self.transformada_vp_y(y2)
        # print(f'x1={x1}, y1={y1}, x2={x2}, y2={y2}')
        painter.drawLine(x1, y1, x2, y2)

    def draw_wireframe(self, points: list[Point]):
        pass


class CustomCanvas(QWidget):
    step: int
    viewport: Viewport
    world_items: list[WorldItem]

    def __init__(self, color='white', **kwargs):
        super(CustomCanvas, self).__init__(**kwargs)
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)

        self.step = 10
        self.viewport = Viewport(0, 0, 515, 680)
        self.viewport.set_window(0, 0, 200, 200)

        self.world_items = []

    def paintEvent(self, event):
        super().paintEvent(event)
        print("paint")
        painter = QPainter(self)
        painter.setPen(QColor.fromString('blue'))

        self.viewport.draw(painter, self.world_items)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        self.setFixedSize(QSize(450, 450))
        self.setCentralWidget(CustomCanvas("white"))
