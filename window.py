import sys
from dataclasses import dataclass
from pathlib import Path

from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QTabWidget,
    QWidget,
)
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QPalette, QColor, QPainter
from PySide6.QtCore import QObject, Slot
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine, QmlElement
from PySide6.QtQuickControls2 import QQuickStyle

# import style_rc



# [ ] Display file para 2D capaz de representar pontos, segmentos de retas e polígonos (listas de pontos
# interconectados), onde: Cada objeto possui um nome, cada objeto possui um tipo e sua lista de  coordenadas de
# tamanho variável dependendo de seu tipo. Para facilitar a sua vida mais tarde, chame o objeto polígono de
# wireframe;
# [ ] Transformação de viewport em 2D; [ ] Funções de Panning/navegação 2D (movimentação do window);
# [ ] Funções de Zooming (modificação do tamanho do window);

# OBS: Use apenas as diretivas de desenho de pontos e linhas para exibir os objetos no canvas, não use
# drawPolygon;
# A transformada de viewport não deve distorcer os objetos. Ex.: Se um objeto for um quadrado,
# ele deve ser exibido como tal.

@dataclass
class Size:
    x: int
    y: int
    width: int
    height: int


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

    def draw(self, painter: QPainter):
        painter.setPen(QColor.fromString('blue'))
        painter.drawRect(self.viewport_size.x, self.viewport_size.y, self.viewport_size.width,
                         self.viewport_size.height)
        # painter.drawPoint(int((self.viewport_size.x+self.viewport_size.width)/2),int((self.viewport_size.y+self.viewport_size.height)/2))

    def zoom(self, step: int):
        # print(f'x={self.window_size.x}, y={self.window_size.y}, max_x={self.window_size.x + self.window_size.width}, max_y={self.window_size.y + self.window_size.height}')
        new_width = int(self.window_size.width * (1 - (step / 100)))
        new_height = int(self.window_size.height * (1 - (step / 100)))
        diff = self.window_size.width - new_width

        self.window_size = Size(
            x=int(diff / 2) + self.window_size.x,
            y=int(diff / 2) + self.window_size.y,
            width=new_width,
            height=new_height
        )
        # print(f'x={self.window_size.x}, y={self.window_size.y}, max_x={self.window_size.x + self.window_size.width}, max_y={self.window_size.y + self.window_size.height}')

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

    def transformada_vp_x(self, x):
        # print(f'x={self.viewport_size.x}, y={self.viewport_size.y}, max_x={self.viewport_size.x + self.viewport_size.width}, max_y={self.viewport_size.y + self.viewport_size.height}')
        x_vp = ((x - self.window_size.x) / ((self.window_size.width + self.window_size.x) - self.window_size.x))
        x_vp *= (self.viewport_size.x + self.viewport_size.width) - self.viewport_size.x
        return int(x_vp + self.viewport_size.x)

    def transformada_vp_y(self, y):
        # print(f'x={self.window_size.x}, y={self.window_size.y}, max_x={self.window_size.x + self.window_size.width}, max_y={self.window_size.y + self.window_size.height}')
        y_vp = 1 - ((y - self.window_size.y) / ((self.window_size.height + self.window_size.y) - self.window_size.y))
        y_vp *= (self.viewport_size.y + self.viewport_size.height) - self.viewport_size.y
        return int(y_vp + self.viewport_size.y)

    def draw_line(self, x1, y1, x2, y2, painter: QPainter):
        # print(f'x1={x1}, y1={y1}, x2={x2}, y2={y2}')
        x1 = self.transformada_vp_x(x1)
        y1 = self.transformada_vp_y(y1)
        x2 = self.transformada_vp_x(x2)
        y2 = self.transformada_vp_y(y2)
        # print(f'x1={x1}, y1={y1}, x2={x2}, y2={y2}')
        painter.drawLine(x1, y1, x2, y2)


class CustomCanvas(QWidget):
    step = 10

    def __init__(self, color='white', **kwargs):
        super(CustomCanvas, self).__init__(**kwargs)
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)

    def paintEvent(self, event):
        super().paintEvent(event)
        print("paint")
        painter = QPainter(self)
        painter.setPen(QColor.fromString('blue'))

        # draw viewport
        # viewport = Viewport(5, 5, 400, 200)
        viewport = Viewport(0, 0, 515, 680)
        viewport.draw(painter)
        viewport.set_window(0, 0, 200, 200)
        viewport.move_window(50,0)
        # viewport.zoom(0)

        viewport.draw_line(0, 0, 100, 100, painter)
        # viewport.draw_line(100, 0, 400, 100, painter)
        # painter.drawLine(5, 5, 105, 105)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        self.setFixedSize(QSize(450, 450))
        self.setCentralWidget(CustomCanvas("white"))


QML_IMPORT_NAME = "io.qt.textproperties"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class Bridge(QObject):

    @Slot(str, result=str)
    def getColor(self, s):
        if s.lower() == "red":
            return "#ef9a9a"
        elif s.lower() == "green":
            return "#a5d6a7"
        elif s.lower() == "blue":
            return "#90caf9"
        else:
            return "white"

    @Slot(float, result=int)
    def getSize(self, s):
        size = int(s * 34)
        if size <= 0:
            return 1
        else:
            return size

    @Slot(str, result=bool)
    def getItalic(self, s):
        if s.lower() == "italic":
            return True
        else:
            return False

    @Slot(str, result=bool)
    def getBold(self, s):
        if s.lower() == "bold":
            return True
        else:
            return False

    @Slot(str, result=bool)
    def getUnderline(self, s):
        if s.lower() == "underline":
            return True
        else:
            return False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # window = MainWindow()
    #
    # window.show()
    # window.raise_()
    QQuickStyle.setStyle("Material")
    engine = QQmlApplicationEngine()

    # Get the path of the current directory, and then add the name
    # of the QML file, to load it.
    qml_file = Path(__file__).parent / 'test.qml'
    engine.load(qml_file)

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())