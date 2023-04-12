from PyQt6 import QtCore, QtGui, QtWidgets

from geometry.shapes import Point, Line, WorldItem
from window import Canvas
import incluirobjeto
from transformacoesobjeto import TransformacoesObjetoUI


class MainWindow:
    objectCreationWindow = None

    def setupUi(self):
        main_window = self.main_window
        main_window.setObjectName("MainWindow")
        main_window.resize(1000, 800)
        main_window.setMaximumSize(QtCore.QSize(1000, 784))
        main_window.setBaseSize(QtCore.QSize(1000, 784))
        self.centralwidget = QtWidgets.QWidget(parent=main_window)
        self.centralwidget.setMaximumSize(QtCore.QSize(1000, 784))
        self.centralwidget.setBaseSize(QtCore.QSize(1000, 784))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.centralwidget.setFont(font)
        self.centralwidget.setObjectName("centralwidget")

        self.toolbar = QtWidgets.QToolBar("Main toolbar", parent=self.main_window)
        self.toolbar.setFixedHeight(30)
        self.toolbar.setFixedWidth(1000)
        saveAction = QtGui.QAction("Salvar", self.toolbar)
        saveAction.setStatusTip("Salvar objetos criados")
        saveAction.triggered.connect(self.saveObjects)
        self.toolbar.addAction(saveAction)
        loadAction = QtGui.QAction("Carregar", self.toolbar)
        loadAction.setStatusTip("Carregar objetos salvos")
        loadAction.triggered.connect(self.loadObjects)
        self.toolbar.addAction(loadAction)

        self.horizontalLayoutWidget = QtWidgets.QWidget(parent=self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(9, 39, 1000, 711))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayoutCentral = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayoutCentral.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayoutCentral.setObjectName("horizontalLayoutCentral")
        self.groupBoxMenuFuncoes = QtWidgets.QGroupBox(parent=self.horizontalLayoutWidget)
        self.groupBoxMenuFuncoes.setObjectName("groupBoxMenuFuncoes")
        self.verticalLayoutMenuFuncoes = QtWidgets.QVBoxLayout(self.groupBoxMenuFuncoes)
        self.verticalLayoutMenuFuncoes.setObjectName("verticalLayoutMenuFuncoes")
        self.verticalLayoutMenuFuncoes_2 = QtWidgets.QVBoxLayout()
        self.verticalLayoutMenuFuncoes_2.setObjectName("verticalLayoutMenuFuncoes_2")

        self.groupBoxObjetos = QtWidgets.QGroupBox(parent=self.groupBoxMenuFuncoes)
        self.groupBoxObjetos.setObjectName("groupBoxObjetos")
        self.listWidget = QtWidgets.QListWidget(parent=self.groupBoxObjetos)
        self.listWidget.setGeometry(QtCore.QRect(0, 21, 231, 141))
        self.listWidget.setObjectName("listWidget")
        self.listWidget.itemDoubleClicked.connect(self.openTransformacoesObjeto)

        self.pushButtonAddObject = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButtonAddObject.setGeometry(QtCore.QRect(160, 31, 50, 30))
        self.pushButtonAddObject.setObjectName("pushButtonAddObject")
        self.pushButtonAddObject.clicked.connect(self.openObjectCreationWindow)
        self.pushButtonAddObject.setAutoDefault(False)

        self.verticalLayoutMenuFuncoes_2.addWidget(self.groupBoxObjetos)
        self.groupBoxWindow = QtWidgets.QGroupBox(parent=self.groupBoxMenuFuncoes)
        self.groupBoxWindow.setObjectName("groupBoxWindow")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(parent=self.groupBoxWindow)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(0, 19, 231, 471))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayoutWindow = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayoutWindow.setContentsMargins(0, 0, 0, 0)
        self.verticalLayoutWindow.setObjectName("verticalLayoutWindow")
        self.widgetPasso = QtWidgets.QWidget(parent=self.verticalLayoutWidget_2)
        self.widgetPasso.setMaximumSize(QtCore.QSize(16777215, 60))
        self.widgetPasso.setObjectName("widgetPasso")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(parent=self.widgetPasso)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(0, 10, 221, 42))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayoutPasso = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayoutPasso.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMinimumSize)
        self.horizontalLayoutPasso.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayoutPasso.setObjectName("horizontalLayoutPasso")
        self.label = QtWidgets.QLabel(parent=self.horizontalLayoutWidget_2)
        self.label.setMaximumSize(QtCore.QSize(16777215, 40))
        self.label.setObjectName("label")
        self.horizontalLayoutPasso.addWidget(self.label)
        self.plainTextEdit = QtWidgets.QPlainTextEdit(parent=self.horizontalLayoutWidget_2)
        self.plainTextEdit.setMaximumSize(QtCore.QSize(16777215, 40))
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.horizontalLayoutPasso.addWidget(self.plainTextEdit)
        self.label_2 = QtWidgets.QLabel(parent=self.horizontalLayoutWidget_2)
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 40))
        self.label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayoutPasso.addWidget(self.label_2)
        self.horizontalLayoutPasso.setStretch(0, 2)
        self.horizontalLayoutPasso.setStretch(1, 3)
        self.horizontalLayoutPasso.setStretch(2, 1)
        self.verticalLayoutWindow.addWidget(self.widgetPasso)
        self.widgetBotoesMovimentacao = QtWidgets.QWidget(parent=self.verticalLayoutWidget_2)
        self.widgetBotoesMovimentacao.setObjectName("widgetBotoesMovimentacao")
        self.gridLayoutWidget = QtWidgets.QWidget(parent=self.widgetBotoesMovimentacao)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 10, 221, 81))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayoutMovimentacao = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayoutMovimentacao.setContentsMargins(0, 0, 0, 0)
        self.gridLayoutMovimentacao.setObjectName("gridLayoutMovimentacao")

        # setas
        self.pushButtonUp = QtWidgets.QPushButton(parent=self.gridLayoutWidget)
        self.pushButtonUp.setMaximumSize(QtCore.QSize(40, 16777215))
        self.pushButtonUp.setObjectName("pushButtonUp")
        self.pushButtonUp.clicked.connect(self.panUp)
        self.gridLayoutMovimentacao.addWidget(self.pushButtonUp, 0, 0, 1, 1)
        self.pushButtonDown = QtWidgets.QPushButton(parent=self.gridLayoutWidget)
        self.pushButtonDown.setMinimumSize(QtCore.QSize(0, 0))
        self.pushButtonDown.setMaximumSize(QtCore.QSize(40, 16777215))
        self.pushButtonDown.setObjectName("pushButtonDown")
        self.pushButtonDown.clicked.connect(self.panDown)
        self.gridLayoutMovimentacao.addWidget(self.pushButtonDown, 1, 0, 1, 1)
        self.pushButtonLeft = QtWidgets.QPushButton(parent=self.gridLayoutWidget)
        self.pushButtonLeft.setMaximumSize(QtCore.QSize(40, 16777215))
        self.pushButtonLeft.setObjectName("pushButtonLeft")
        self.pushButtonLeft.clicked.connect(self.panLeft)
        self.gridLayoutMovimentacao.addWidget(self.pushButtonLeft, 0, 1, 1, 1)
        self.pushButtonRight = QtWidgets.QPushButton(parent=self.gridLayoutWidget)
        self.pushButtonRight.setMaximumSize(QtCore.QSize(40, 16777215))
        self.pushButtonRight.setObjectName("pushButtonRight")
        self.pushButtonRight.clicked.connect(self.panRight)
        self.gridLayoutMovimentacao.addWidget(self.pushButtonRight, 1, 1, 1, 1)

        #
        self.pushButtonIn = QtWidgets.QPushButton(parent=self.gridLayoutWidget)
        self.pushButtonIn.setMaximumSize(QtCore.QSize(40, 16777215))
        self.pushButtonIn.setObjectName("pushButtonIn")
        self.gridLayoutMovimentacao.addWidget(self.pushButtonIn, 0, 2, 1, 1)
        self.pushButtonOut = QtWidgets.QPushButton(parent=self.gridLayoutWidget)
        self.pushButtonOut.setMaximumSize(QtCore.QSize(40, 16777215))
        self.pushButtonOut.setObjectName("pushButtonOut")
        self.gridLayoutMovimentacao.addWidget(self.pushButtonOut, 1, 2, 1, 1)
        self.verticalLayoutWindow.addWidget(self.widgetBotoesMovimentacao)
        self.widgetRotacao = QtWidgets.QWidget(parent=self.verticalLayoutWidget_2)
        self.widgetRotacao.setObjectName("widgetRotacao")
        self.groupBoxRotacao = QtWidgets.QGroupBox(parent=self.widgetRotacao)
        self.groupBoxRotacao.setGeometry(QtCore.QRect(9, -1, 211, 101))
        self.groupBoxRotacao.setObjectName("groupBoxRotacao")
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(parent=self.groupBoxRotacao)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(10, 19, 191, 81))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.verticalLayoutRotacao = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayoutRotacao.setContentsMargins(0, 0, 0, 0)
        self.verticalLayoutRotacao.setObjectName("verticalLayoutRotacao")
        self.horizontalLayoutGraus = QtWidgets.QHBoxLayout()
        self.horizontalLayoutGraus.setObjectName("horizontalLayoutGraus")
        self.labelGraus = QtWidgets.QLabel(parent=self.verticalLayoutWidget_4)
        self.labelGraus.setMaximumSize(QtCore.QSize(16777215, 40))
        self.labelGraus.setObjectName("labelGraus")
        self.horizontalLayoutGraus.addWidget(self.labelGraus)
        self.plainTextEditGraus = QtWidgets.QPlainTextEdit(parent=self.verticalLayoutWidget_4)
        self.plainTextEditGraus.setMaximumSize(QtCore.QSize(16777215, 40))
        self.plainTextEditGraus.setObjectName("plainTextEditGraus")
        self.horizontalLayoutGraus.addWidget(self.plainTextEditGraus)
        self.labelGrausSimbolo = QtWidgets.QLabel(parent=self.verticalLayoutWidget_4)
        self.labelGrausSimbolo.setMaximumSize(QtCore.QSize(16777215, 40))
        self.labelGrausSimbolo.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.labelGrausSimbolo.setObjectName("labelGrausSimbolo")
        self.horizontalLayoutGraus.addWidget(self.labelGrausSimbolo)
        self.horizontalLayoutGraus.setStretch(0, 2)
        self.horizontalLayoutGraus.setStretch(1, 3)
        self.horizontalLayoutGraus.setStretch(2, 1)
        self.verticalLayoutRotacao.addLayout(self.horizontalLayoutGraus)
        self.horizontalLayoutXYZ = QtWidgets.QHBoxLayout()
        self.horizontalLayoutXYZ.setObjectName("horizontalLayoutXYZ")
        self.pushButton_2 = QtWidgets.QPushButton(parent=self.verticalLayoutWidget_4)
        self.pushButton_2.setMaximumSize(QtCore.QSize(40, 40))
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayoutXYZ.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(parent=self.verticalLayoutWidget_4)
        self.pushButton_3.setMaximumSize(QtCore.QSize(40, 40))
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayoutXYZ.addWidget(self.pushButton_3)
        self.pushButton_4 = QtWidgets.QPushButton(parent=self.verticalLayoutWidget_4)
        self.pushButton_4.setMaximumSize(QtCore.QSize(40, 40))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.windowRotationZ)
        self.horizontalLayoutXYZ.addWidget(self.pushButton_4)
        self.verticalLayoutRotacao.addLayout(self.horizontalLayoutXYZ)
        self.verticalLayoutRotacao.setStretch(0, 1)
        self.verticalLayoutRotacao.setStretch(1, 1)
        self.verticalLayoutWindow.addWidget(self.widgetRotacao)
        self.widgetZoom = QtWidgets.QWidget(parent=self.verticalLayoutWidget_2)
        self.widgetZoom.setObjectName("widgetZoom")
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(parent=self.widgetZoom)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(0, 10, 221, 81))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayoutZoom = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayoutZoom.setContentsMargins(0, 0, 0, 0)
        self.verticalLayoutZoom.setObjectName("verticalLayoutZoom")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, -1, 0, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")

        # Zoom
        self.labelZoom = QtWidgets.QLabel(parent=self.verticalLayoutWidget_3)
        self.labelZoom.setMaximumSize(QtCore.QSize(50, 16777215))
        self.labelZoom.setObjectName("labelZoom")
        self.horizontalLayout.addWidget(self.labelZoom)
        self.pushButtonPlus = QtWidgets.QPushButton(parent=self.verticalLayoutWidget_3)
        self.pushButtonPlus.setMaximumSize(QtCore.QSize(40, 40))
        self.pushButtonPlus.setObjectName("pushButtonPlus")
        self.pushButtonPlus.clicked.connect(self.zoomIn)
        self.horizontalLayout.addWidget(self.pushButtonPlus)
        self.pushButtonMinus = QtWidgets.QPushButton(parent=self.verticalLayoutWidget_3)
        self.pushButtonMinus.setMaximumSize(QtCore.QSize(40, 40))
        self.pushButtonMinus.setObjectName("pushButtonMinus")
        self.pushButtonMinus.clicked.connect(self.zoomOut)
        self.horizontalLayout.addWidget(self.pushButtonMinus)
        self.actionZoomPlus = QtGui.QAction(parent=main_window)
        self.actionZoomPlus.setObjectName("actionZoomPlus")
        self.actionZoomPlus.triggered.connect(self.zoomIn)
        self.actionZoomMinus = QtGui.QAction(parent=main_window)
        self.actionZoomMinus.setObjectName("actionZoomMinus")
        self.actionZoomMinus.triggered.connect(self.zoomOut)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 1)
        self.horizontalLayout.setStretch(2, 1)
        self.verticalLayoutZoom.addLayout(self.horizontalLayout)
        self.pushButtonSetWindow = QtWidgets.QPushButton(parent=self.verticalLayoutWidget_3)
        self.pushButtonSetWindow.setObjectName("pushButtonSetWindow")
        self.verticalLayoutZoom.addWidget(self.pushButtonSetWindow)
        self.verticalLayoutWindow.addWidget(self.widgetZoom)
        self.widgetProjecao = QtWidgets.QWidget(parent=self.verticalLayoutWidget_2)
        self.widgetProjecao.setObjectName("widgetProjecao")
        self.groupBoxProjecao = QtWidgets.QGroupBox(parent=self.widgetProjecao)
        self.groupBoxProjecao.setGeometry(QtCore.QRect(-1, -1, 221, 81))
        self.groupBoxProjecao.setObjectName("groupBoxProjecao")
        self.verticalLayoutWidget_5 = QtWidgets.QWidget(parent=self.groupBoxProjecao)
        self.verticalLayoutWidget_5.setGeometry(QtCore.QRect(0, 19, 221, 61))
        self.verticalLayoutWidget_5.setObjectName("verticalLayoutWidget_5")
        self.verticalLayoutProjecao = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_5)
        self.verticalLayoutProjecao.setContentsMargins(0, 0, 0, 0)
        self.verticalLayoutProjecao.setObjectName("verticalLayoutProjecao")
        self.radioButtonParalela = QtWidgets.QRadioButton(parent=self.verticalLayoutWidget_5)
        self.radioButtonParalela.setObjectName("radioButtonParalela")
        self.verticalLayoutProjecao.addWidget(self.radioButtonParalela)
        self.radioButtonPerspectiva = QtWidgets.QRadioButton(parent=self.verticalLayoutWidget_5)
        self.radioButtonPerspectiva.setObjectName("radioButtonPerspectiva")
        self.verticalLayoutProjecao.addWidget(self.radioButtonPerspectiva)
        self.verticalLayoutWindow.addWidget(self.widgetProjecao)
        self.verticalLayoutWindow.setStretch(0, 3)
        self.verticalLayoutWindow.setStretch(1, 4)
        self.verticalLayoutWindow.setStretch(2, 4)
        self.verticalLayoutWindow.setStretch(3, 4)
        self.verticalLayoutWindow.setStretch(4, 4)
        self.verticalLayoutMenuFuncoes_2.addWidget(self.groupBoxWindow)
        self.verticalLayoutMenuFuncoes_2.setStretch(0, 1)
        self.verticalLayoutMenuFuncoes_2.setStretch(1, 3)
        self.verticalLayoutMenuFuncoes.addLayout(self.verticalLayoutMenuFuncoes_2)
        self.horizontalLayoutCentral.addWidget(self.groupBoxMenuFuncoes)
        self.groupBoxViewPort = QtWidgets.QGroupBox(parent=self.horizontalLayoutWidget)
        self.groupBoxViewPort.setObjectName("groupBoxViewPort")
        self.graphicsViewViewport = Canvas(parent=self.groupBoxViewPort)
        self.graphicsViewViewport.setGeometry(QtCore.QRect(0, 20, 690, 700))
        self.graphicsViewViewport.setObjectName("graphicsViewViewport")

        self.horizontalLayoutCentral.addWidget(self.groupBoxViewPort)
        self.horizontalLayoutCentral.setStretch(0, 1)
        self.horizontalLayoutCentral.setStretch(1, 3)
        main_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=main_window)
        self.statusbar.setObjectName("statusbar")
        main_window.setStatusBar(self.statusbar)

        self.retranslate(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslate(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBoxMenuFuncoes.setTitle(_translate("MainWindow", "Menu de Funções"))
        self.groupBoxObjetos.setTitle(_translate("MainWindow", "Objetos"))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        # adiciona items existentes na barra de objetos
        for item in self.graphicsViewViewport.world_items:
            widget = QtWidgets.QListWidgetItem()
            widget.setText(_translate("MainWindow", item.name))
            self.listWidget.addItem(widget)

        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.groupBoxWindow.setTitle(_translate("MainWindow", "Window"))
        self.label.setText(_translate("MainWindow", "Passo:"))
        self.label_2.setText(_translate("MainWindow", "%"))
        self.pushButtonUp.setText(_translate("MainWindow", "Up"))
        self.pushButtonDown.setText(_translate("MainWindow", "Down"))
        self.pushButtonLeft.setText(_translate("MainWindow", "Left"))
        self.pushButtonRight.setText(_translate("MainWindow", "Right"))
        self.pushButtonIn.setText(_translate("MainWindow", "In"))
        self.pushButtonOut.setText(_translate("MainWindow", "Out"))
        self.groupBoxRotacao.setTitle(_translate("MainWindow", "Rotação"))
        self.labelGraus.setText(_translate("MainWindow", "Graus:"))
        self.labelGrausSimbolo.setText(_translate("MainWindow", "°"))
        self.pushButton_2.setText(_translate("MainWindow", "X"))
        self.pushButton_3.setText(_translate("MainWindow", "Y"))
        self.pushButton_4.setText(_translate("MainWindow", "Z"))
        self.labelZoom.setText(_translate("MainWindow", "Zoom"))
        self.pushButtonPlus.setText(_translate("MainWindow", "+"))
        self.pushButtonMinus.setText(_translate("MainWindow", "-"))
        self.pushButtonSetWindow.setText(_translate("MainWindow", "Set Window"))
        self.groupBoxProjecao.setTitle(_translate("MainWindow", "Projeção"))
        self.radioButtonParalela.setText(_translate("MainWindow", "Paralela"))
        self.radioButtonPerspectiva.setText(_translate("MainWindow", "Perspectiva"))
        self.groupBoxViewPort.setTitle(_translate("MainWindow", "Viewport"))
        self.actionZoomPlus.setText(_translate("MainWindow", "ZoomPlus"))
        self.actionZoomPlus.setShortcut(_translate("MainWindow", "+"))
        self.actionZoomMinus.setText(_translate("MainWindow", "ZoomMinus"))
        self.actionZoomMinus.setShortcut(_translate("MainWindow", "-"))
        self.pushButtonAddObject.setText(_translate("MainWindow", "+"))

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setupUi()
        self.main_window.show()

    def add_item_to_world(self, item: WorldItem):
        if item.name == "":
            if isinstance(item.graphic, Point):
                item.name = "Ponto Sem Nome"
            elif isinstance(item.graphic, Line):
                item.name = "Reta Sem Nome"
            else:
                item.name = "Poligono Sem Nome"
        self.graphicsViewViewport.world_items.append(item)

        widget = QtWidgets.QListWidgetItem()
        widget.setText(item.name)
        self.listWidget.addItem(widget)
        self.graphicsViewViewport.repaint()

    def zoomIn(self):
        text = self.plainTextEdit.toPlainText()
        if text == "":
            step = 10
        else:
            step = int(text)
        self.graphicsViewViewport.viewport.zoom(step)
        self.graphicsViewViewport.repaint()

    def zoomOut(self):
        text = self.plainTextEdit.toPlainText()
        if text == "":
            step = 10
        else:
            step = int(text)
        self.graphicsViewViewport.viewport.zoom(-step)
        self.graphicsViewViewport.repaint()

    def panUp(self):
        self.graphicsViewViewport.viewport.move_window(0, -10)
        self.graphicsViewViewport.repaint()

    def panDown(self):
        self.graphicsViewViewport.viewport.move_window(0, 10)
        self.graphicsViewViewport.repaint()

    def panLeft(self):
        self.graphicsViewViewport.viewport.move_window(10, 0)
        self.graphicsViewViewport.repaint()

    def panRight(self):
        self.graphicsViewViewport.viewport.move_window(-10, 0)
        self.graphicsViewViewport.repaint()

    def windowRotationZ(self):
        try:
            angle = float(self.plainTextEditGraus.toPlainText())
        except ValueError:
            return

        self.graphicsViewViewport.viewport.set_window_angle(angle)
        self.graphicsViewViewport.repaint()

    def openObjectCreationWindow(self):
        self.objectCreationWindow = incluirobjeto.IncluirObjeto(self.add_item_to_world)
        object: WorldItem = self.objectCreationWindow.getLastAddedObject()
        if object is not None:
            self.add_item_to_world(object)

    def openTransformacoesObjeto(self, item):
        item_index = self.listWidget.indexFromItem(item).row()
        object = self.graphicsViewViewport.world_items[item_index]
        self.transformacoesObjeto = TransformacoesObjetoUI(object, on_close=self.graphicsViewViewport.repaint)

    def saveObjects(self):
        pass

    def loadObjects(self):
        pass


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    ui = MainWindow(main_window)
    sys.exit(app.exec())
