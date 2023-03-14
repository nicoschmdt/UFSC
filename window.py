import sys

from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QTabWidget,
    QWidget,
)
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QPalette, QColor

class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)
        
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        button = QPushButton("Press Me!")

        self.setFixedSize(QSize(400, 300))
        # window.setGeometry(100, 100, 280, 80)

        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.TabPosition.North)
        tabs.setMovable(True)

        for n, color in enumerate(["red", "green", "blue", "yellow"]):
            tabs.addTab(Color(color), color)

        self.setCentralWidget(tabs)
        
        # Set the central widget of the Window.
        # self.setCentralWidget(button)
        
        helloMsg = QLabel("<h1>Hello, World!</h1>", parent=self)
        helloMsg.move(60, 15)


app = QApplication(sys.argv)
window = MainWindow()

window.show()
window.raise_()
sys.exit(app.exec())