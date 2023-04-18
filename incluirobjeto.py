from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QWidget, QMessageBox, QDialog, QPushButton

from geometry.polygon import is_polygon
from geometry.shapes import Point, Line, WorldItem, Wireframe
from geometry.transformations import determine_object_center
from common.notapolygon import NotAPolygonDialog


class IncluirObjeto(QWidget):
    vertixCounter: int = 1
    lastAddedObject: WorldItem = None

    def setupUi(self):
        self.setObjectName("IncluirObjeto")
        self.resize(737, 812)
        self.setGeometry(QtCore.QRect(10, 10, 737, 812))
        self.verticalLayoutWidget = QtWidgets.QWidget(parent=self)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 691, 781))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayoutPrincipal = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayoutPrincipal.setContentsMargins(20, 20, 20, 20)
        self.verticalLayoutPrincipal.setSpacing(19)
        self.verticalLayoutPrincipal.setObjectName("verticalLayoutPrincipal")
        self.NomeHorizontalLayout = QtWidgets.QHBoxLayout()
        self.NomeHorizontalLayout.setContentsMargins(20, 0, 20, 0)
        self.NomeHorizontalLayout.setSpacing(10)
        self.NomeHorizontalLayout.setObjectName("NomeHorizontalLayout")
        self.labelNome = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelNome.sizePolicy().hasHeightForWidth())
        self.labelNome.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelNome.setFont(font)
        self.labelNome.setScaledContents(False)
        self.labelNome.setObjectName("labelNome")
        self.NomeHorizontalLayout.addWidget(self.labelNome)
        self.textEditInserirNome = QtWidgets.QTextEdit(parent=self.verticalLayoutWidget)
        self.textEditInserirNome.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEditInserirNome.sizePolicy().hasHeightForWidth())
        self.textEditInserirNome.setSizePolicy(sizePolicy)
        self.textEditInserirNome.setMaximumSize(QtCore.QSize(16777215, 30))
        self.textEditInserirNome.setObjectName("textEditInserirNome")
        self.NomeHorizontalLayout.addWidget(self.textEditInserirNome)
        self.NomeHorizontalLayout.setStretch(0, 1)
        self.NomeHorizontalLayout.setStretch(1, 6)
        self.verticalLayoutPrincipal.addLayout(self.NomeHorizontalLayout)
        self.tabWidget = QtWidgets.QTabWidget(parent=self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                                           QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.tabWidget.setFont(font)
        self.tabWidget.setObjectName("tabWidget")

        # Aba p/ adicionar pontos
        self.PontoTab = QtWidgets.QWidget()
        self.PontoTab.setObjectName("PontoTab")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(parent=self.PontoTab)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(19, 19, 611, 491))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayoutPonto = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayoutPonto.setContentsMargins(0, 0, 0, 0)
        self.verticalLayoutPonto.setObjectName("verticalLayoutPonto")
        self.groupBoxCoordenadasPonto = QtWidgets.QGroupBox(parent=self.verticalLayoutWidget_2)
        self.groupBoxCoordenadasPonto.setObjectName("groupBoxCoordenadasPonto")
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(parent=self.groupBoxCoordenadasPonto)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(10, 30, 591, 89))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.horizontalLayoutXYPonto = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayoutXYPonto.setContentsMargins(50, 0, 50, 0)
        self.horizontalLayoutXYPonto.setSpacing(20)
        self.horizontalLayoutXYPonto.setObjectName("horizontalLayoutXYPonto")
        self.labelXPonto = QtWidgets.QLabel(parent=self.horizontalLayoutWidget_3)
        self.labelXPonto.setObjectName("labelXPonto")
        self.horizontalLayoutXYPonto.addWidget(self.labelXPonto)
        self.plainTextEditXPonto = QtWidgets.QPlainTextEdit(parent=self.horizontalLayoutWidget_3)
        self.plainTextEditXPonto.setMaximumSize(QtCore.QSize(16777215, 50))
        self.plainTextEditXPonto.setObjectName("plainTextEditXPonto")
        self.horizontalLayoutXYPonto.addWidget(self.plainTextEditXPonto)
        spacerItem = QtWidgets.QSpacerItem(200, 0, QtWidgets.QSizePolicy.Policy.Expanding,
                                           QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayoutXYPonto.addItem(spacerItem)
        self.labelYPonto = QtWidgets.QLabel(parent=self.horizontalLayoutWidget_3)
        self.labelYPonto.setObjectName("labelYPonto")
        self.horizontalLayoutXYPonto.addWidget(self.labelYPonto)
        self.plainTextEditYPonto = QtWidgets.QPlainTextEdit(parent=self.horizontalLayoutWidget_3)
        self.plainTextEditYPonto.setMaximumSize(QtCore.QSize(16777215, 50))
        self.plainTextEditYPonto.setObjectName("plainTextEditYPonto")
        self.horizontalLayoutXYPonto.addWidget(self.plainTextEditYPonto)
        spacerItem1 = QtWidgets.QSpacerItem(200, 0, QtWidgets.QSizePolicy.Policy.Expanding,
                                            QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayoutXYPonto.addItem(spacerItem1)
        self.label = QtWidgets.QLabel(parent=self.horizontalLayoutWidget_3)
        self.label.setEnabled(False)
        self.label.setObjectName("label")
        self.horizontalLayoutXYPonto.addWidget(self.label)
        self.plainTextEdit = QtWidgets.QPlainTextEdit(parent=self.horizontalLayoutWidget_3)
        self.plainTextEdit.setEnabled(False)
        self.plainTextEdit.setMaximumSize(QtCore.QSize(16777215, 50))
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.horizontalLayoutXYPonto.addWidget(self.plainTextEdit)
        self.verticalLayoutPonto.addWidget(self.groupBoxCoordenadasPonto)
        self.widget = QtWidgets.QWidget(parent=self.verticalLayoutWidget_2)
        self.widget.setEnabled(False)
        self.widget.setObjectName("widget")
        self.verticalLayoutPonto.addWidget(self.widget)
        self.verticalLayoutPonto.setStretch(0, 1)
        self.verticalLayoutPonto.setStretch(1, 3)
        self.tabWidget.addTab(self.PontoTab, "")

        # Aba p/ adicionar retas
        self.RetaTab = QtWidgets.QWidget()
        self.RetaTab.setObjectName("RetaTab")
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(parent=self.RetaTab)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(10, 10, 611, 491))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayoutReta = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayoutReta.setContentsMargins(20, 50, 20, 50)
        self.verticalLayoutReta.setObjectName("verticalLayoutReta")
        self.groupBoxCoordenadasPontoInicialReta = QtWidgets.QGroupBox(parent=self.verticalLayoutWidget_3)
        self.groupBoxCoordenadasPontoInicialReta.setGeometry(QtCore.QRect(0, 0, 609, 111))
        self.groupBoxCoordenadasPontoInicialReta.setObjectName("groupBoxCoordenadasPontoInicialReta")
        self.horizontalLayoutWidget_8 = QtWidgets.QWidget(parent=self.groupBoxCoordenadasPontoInicialReta)
        self.horizontalLayoutWidget_8.setGeometry(QtCore.QRect(10, 30, 561, 89))
        self.horizontalLayoutWidget_8.setObjectName("horizontalLayoutWidget_8")
        self.horizontalLayoutPontoInicialReta = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_8)
        self.horizontalLayoutPontoInicialReta.setContentsMargins(50, 0, 50, 0)
        self.horizontalLayoutPontoInicialReta.setSpacing(20)
        self.horizontalLayoutPontoInicialReta.setObjectName("horizontalLayoutPontoInicialReta")
        self.labelXPontoInicialReta = QtWidgets.QLabel(parent=self.horizontalLayoutWidget_8)
        self.labelXPontoInicialReta.setObjectName("labelXPontoInicialReta")
        self.horizontalLayoutPontoInicialReta.addWidget(self.labelXPontoInicialReta)
        self.plainTextEditXPontoInicialReta = QtWidgets.QPlainTextEdit(parent=self.horizontalLayoutWidget_8)
        self.plainTextEditXPontoInicialReta.setMaximumSize(QtCore.QSize(16777215, 50))
        self.plainTextEditXPontoInicialReta.setObjectName("plainTextEditXPontoInicialReta")
        self.horizontalLayoutPontoInicialReta.addWidget(self.plainTextEditXPontoInicialReta)
        self.labelYPontoInicialReta = QtWidgets.QLabel(parent=self.horizontalLayoutWidget_8)
        self.labelYPontoInicialReta.setObjectName("labelYPontoInicialReta")
        self.horizontalLayoutPontoInicialReta.addWidget(self.labelYPontoInicialReta)
        self.plainTextEditYPontoInicialReta = QtWidgets.QPlainTextEdit(parent=self.horizontalLayoutWidget_8)
        self.plainTextEditYPontoInicialReta.setMaximumSize(QtCore.QSize(16777215, 50))
        self.plainTextEditYPontoInicialReta.setObjectName("plainTextEditYPontoInicialReta")
        self.horizontalLayoutPontoInicialReta.addWidget(self.plainTextEditYPontoInicialReta)
        self.labelZPontoInicialReta = QtWidgets.QLabel(parent=self.horizontalLayoutWidget_8)
        self.labelZPontoInicialReta.setEnabled(False)
        self.labelZPontoInicialReta.setObjectName("labelZPontoInicialReta")
        self.horizontalLayoutPontoInicialReta.addWidget(self.labelZPontoInicialReta)
        self.plainTextEditZPontoInicialReta = QtWidgets.QPlainTextEdit(parent=self.horizontalLayoutWidget_8)
        self.plainTextEditZPontoInicialReta.setEnabled(False)
        self.plainTextEditZPontoInicialReta.setMaximumSize(QtCore.QSize(16777215, 50))
        self.plainTextEditZPontoInicialReta.setObjectName("plainTextEditZPontoInicialReta")
        self.horizontalLayoutPontoInicialReta.addWidget(self.plainTextEditZPontoInicialReta)
        self.verticalLayoutReta.addWidget(self.groupBoxCoordenadasPontoInicialReta)
        self.groupBoxCoordenadasPontoFinalReta = QtWidgets.QGroupBox(parent=self.verticalLayoutWidget_3)
        self.groupBoxCoordenadasPontoFinalReta.setObjectName("groupBoxCoordenadasPontoFinalReta")
        self.horizontalLayoutWidget_4 = QtWidgets.QWidget(parent=self.groupBoxCoordenadasPontoFinalReta)
        self.horizontalLayoutWidget_4.setGeometry(QtCore.QRect(10, 30, 561, 89))
        self.horizontalLayoutWidget_4.setObjectName("horizontalLayoutWidget_4")
        self.horizontalLayoutPontoFinalReta = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_4)
        self.horizontalLayoutPontoFinalReta.setContentsMargins(50, 0, 50, 0)
        self.horizontalLayoutPontoFinalReta.setSpacing(20)
        self.horizontalLayoutPontoFinalReta.setObjectName("horizontalLayoutPontoFinalReta")
        self.labelXPontoFinalReta = QtWidgets.QLabel(parent=self.horizontalLayoutWidget_4)
        self.labelXPontoFinalReta.setObjectName("labelXPontoFinalReta")
        self.horizontalLayoutPontoFinalReta.addWidget(self.labelXPontoFinalReta)
        self.plainTextEditXPontoFinalReta = QtWidgets.QPlainTextEdit(parent=self.horizontalLayoutWidget_4)
        self.plainTextEditXPontoFinalReta.setMaximumSize(QtCore.QSize(16777215, 50))
        self.plainTextEditXPontoFinalReta.setObjectName("plainTextEditXPontoFinalReta")
        self.horizontalLayoutPontoFinalReta.addWidget(self.plainTextEditXPontoFinalReta)
        self.labelYPontoFinalReta = QtWidgets.QLabel(parent=self.horizontalLayoutWidget_4)
        self.labelYPontoFinalReta.setObjectName("labelYPontoFinalReta")
        self.horizontalLayoutPontoFinalReta.addWidget(self.labelYPontoFinalReta)
        self.plainTextEditYPontoFinalReta = QtWidgets.QPlainTextEdit(parent=self.horizontalLayoutWidget_4)
        self.plainTextEditYPontoFinalReta.setMaximumSize(QtCore.QSize(16777215, 50))
        self.plainTextEditYPontoFinalReta.setObjectName("plainTextEditYPontoFinalReta")
        self.horizontalLayoutPontoFinalReta.addWidget(self.plainTextEditYPontoFinalReta)
        self.labelZPontoFinalReta = QtWidgets.QLabel(parent=self.horizontalLayoutWidget_4)
        self.labelZPontoFinalReta.setEnabled(False)
        self.labelZPontoFinalReta.setObjectName("labelZPontoFinalReta")
        self.horizontalLayoutPontoFinalReta.addWidget(self.labelZPontoFinalReta)
        self.plainTextEditZPontoFinalReta = QtWidgets.QPlainTextEdit(parent=self.horizontalLayoutWidget_4)
        self.plainTextEditZPontoFinalReta.setEnabled(False)
        self.plainTextEditZPontoFinalReta.setMaximumSize(QtCore.QSize(16777215, 50))
        self.plainTextEditZPontoFinalReta.setObjectName("plainTextEditZPontoFinalReta")
        self.horizontalLayoutPontoFinalReta.addWidget(self.plainTextEditZPontoFinalReta)
        self.verticalLayoutReta.addWidget(self.groupBoxCoordenadasPontoFinalReta)
        self.widgetReta = QtWidgets.QWidget(parent=self.verticalLayoutWidget_2)
        self.widgetReta.setEnabled(False)
        self.widgetReta.setObjectName("widgetReta")
        self.verticalLayoutReta.addWidget(self.widgetReta)
        self.verticalLayoutReta.setStretch(0, 1)
        self.verticalLayoutReta.setStretch(1, 1)
        self.tabWidget.addTab(self.RetaTab, "")

        # Aba p/ adicionar wireframes
        self.WireframeTab = QtWidgets.QWidget()
        self.WireframeTab.setObjectName("WireframeTab")
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(parent=self.WireframeTab)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(9, 9, 631, 600))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.verticalLayoutWireframe = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayoutWireframe.setContentsMargins(20, 0, 20, 0)
        self.verticalLayoutWireframe.setObjectName("verticalLayoutWireframe")

        self.verticalLayoutWidget_5 = QtWidgets.QWidget(parent=self.WireframeTab)
        self.verticalLayoutWidget_5.setGeometry(QtCore.QRect(9, 9, 631, 560))
        self.verticalLayoutWidget_5.setObjectName("verticalLayoutWidget_5")
        self.verticalLayoutPontosWireframe = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_5)
        self.verticalLayoutPontosWireframe.setContentsMargins(0, 0, 0, 0)
        self.verticalLayoutPontosWireframe.setObjectName("verticalLayoutPontosWireframe")

        self.groupBoxVertice1 = QtWidgets.QGroupBox(parent=self.verticalLayoutWidget_5)
        self.groupBoxVertice1.setMaximumSize(QtCore.QSize(16777215, 81))
        self.groupBoxVertice1.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading | QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop)
        self.groupBoxVertice1.setObjectName("groupBoxVertice1")
        self.horizontalLayoutWidget = QtWidgets.QWidget(parent=self.groupBoxVertice1)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 611, 81))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayoutVertice1 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayoutVertice1.setContentsMargins(50, 10, 50, 10)
        self.horizontalLayoutVertice1.setSpacing(20)
        self.horizontalLayoutVertice1.setObjectName("horizontalLayoutVertice1")
        self.labelXVertice1 = QtWidgets.QLabel(parent=self.horizontalLayoutWidget)
        self.labelXVertice1.setObjectName("labelXVertice1")
        self.horizontalLayoutVertice1.addWidget(self.labelXVertice1)
        self.textEditWireframeX1 = QtWidgets.QPlainTextEdit(parent=self.horizontalLayoutWidget)
        self.textEditWireframeX1.setObjectName("plainTextEditXVertice1")
        self.textEditWireframeX1.setMaximumSize(QtCore.QSize(16777215, 30))
        self.horizontalLayoutVertice1.addWidget(self.textEditWireframeX1)
        self.labelYVertice1 = QtWidgets.QLabel(parent=self.horizontalLayoutWidget)
        self.labelYVertice1.setObjectName("labelYVertice1")
        self.horizontalLayoutVertice1.addWidget(self.labelYVertice1)
        self.textEditWireframeY1 = QtWidgets.QPlainTextEdit(parent=self.horizontalLayoutWidget)
        self.textEditWireframeY1.setMaximumSize(QtCore.QSize(16777215, 30))
        self.textEditWireframeY1.setObjectName("plainTextEditYVertice1")
        self.horizontalLayoutVertice1.addWidget(self.textEditWireframeY1)
        self.labelZVertice1 = QtWidgets.QLabel(parent=self.horizontalLayoutWidget)
        self.labelZVertice1.setEnabled(False)
        self.labelZVertice1.setObjectName("labelZVertice1")
        self.horizontalLayoutVertice1.addWidget(self.labelZVertice1)
        self.textEditWireframeZ1 = QtWidgets.QPlainTextEdit(parent=self.horizontalLayoutWidget)
        self.textEditWireframeZ1.setEnabled(False)
        self.textEditWireframeZ1.setMaximumSize(QtCore.QSize(16777215, 30))
        self.textEditWireframeZ1.setObjectName("plainTextEditZVertice1")
        self.horizontalLayoutVertice1.addWidget(self.textEditWireframeZ1)

        self.verticalLayoutPontosWireframe.addWidget(self.groupBoxVertice1)
        self.pushButtonAdicionarVertice = QtWidgets.QPushButton(parent=self.verticalLayoutWidget_4)
        self.pushButtonAdicionarVertice.setObjectName("pushButtonAdicionarVertice")
        self.pushButtonAdicionarVertice.setFixedWidth(200)
        self.pushButtonAdicionarVertice.setFixedHeight(25)
        self.pushButtonAdicionarVertice.clicked.connect(self.addVertix)
        self.verticalLayoutWireframe.addWidget(self.verticalLayoutWidget_5)
        self.verticalLayoutWireframe.addWidget(self.pushButtonAdicionarVertice, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        self.checkBoxPreencherWireframe = QtWidgets.QRadioButton(self.verticalLayoutWidget_4)
        self.checkBoxPreencherWireframe.setChecked(False)
        self.checkBoxPreencherWireframe.setText("Preencher polígono")
        self.verticalLayoutWireframe.addWidget(self.checkBoxPreencherWireframe)
        self.verticalLayoutWireframe.setStretch(0,20)
        self.verticalLayoutWireframe.setStretch(1,1)
        self.verticalLayoutWireframe.setStretch(2,1)

        self.addVertix()
        self.addVertix()

        self.tabWidget.addTab(self.WireframeTab, "")

        # Aba p/ adicionar curvas
        self.CurvasTab = QtWidgets.QWidget()
        self.CurvasTab.setEnabled(False)
        self.CurvasTab.setObjectName("CurvasTab")
        self.tabWidget.addTab(self.CurvasTab, "")

        #
        self.verticalLayoutPrincipal.addWidget(self.tabWidget)
        self.horizontalLayoutCancelOk_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayoutCancelOk_6.setContentsMargins(50, -1, 50, -1)
        self.horizontalLayoutCancelOk_6.setSpacing(50)
        self.horizontalLayoutCancelOk_6.setObjectName("horizontalLayoutCancelOk_6")
        self.pushButtonCancel_6 = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.pushButtonCancel_6.clicked.connect(self.close)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButtonCancel_6.setFont(font)
        self.pushButtonCancel_6.setObjectName("pushButtonCancel_6")
        self.horizontalLayoutCancelOk_6.addWidget(self.pushButtonCancel_6)
        self.pushButtonOK = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.pushButtonOK.clicked.connect(self.createObject)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButtonOK.setFont(font)
        self.pushButtonOK.setObjectName("pushButtonOK")
        self.horizontalLayoutCancelOk_6.addWidget(self.pushButtonOK)

        self.verticalLayoutPrincipal.addLayout(self.horizontalLayoutCancelOk_6)
        self.verticalLayoutPrincipal.setStretch(0, 1)
        self.verticalLayoutPrincipal.setStretch(1, 8)
        self.verticalLayoutPrincipal.setStretch(2, 1)

        self.retranslateUi()
        self.tabWidget.setCurrentIndex(0)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("IncluirObjeto", "Incluir Objeto"))
        self.labelNome.setText(_translate("IncluirObjeto", "Nome:"))
        self.groupBoxCoordenadasPonto.setTitle(_translate("IncluirObjeto", "Coordenadas do Ponto"))
        self.labelXPonto.setText(_translate("IncluirObjeto", "x:"))
        self.labelYPonto.setText(_translate("IncluirObjeto", "y:"))
        self.label.setText(_translate("IncluirObjeto", "z:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.PontoTab), _translate("IncluirObjeto", "Ponto"))
        self.groupBoxCoordenadasPontoInicialReta.setTitle(_translate("IncluirObjeto", "Coordenadas do Ponto Inicial"))
        self.labelXPontoInicialReta.setText(_translate("IncluirObjeto", "x1:"))
        self.labelYPontoInicialReta.setText(_translate("IncluirObjeto", "y1:"))
        self.labelZPontoInicialReta.setText(_translate("IncluirObjeto", "z1:"))
        self.groupBoxCoordenadasPontoFinalReta.setTitle(_translate("IncluirObjeto", "Coordenadas do Ponto Final"))
        self.labelXPontoFinalReta.setText(_translate("IncluirObjeto", "x2:"))
        self.labelYPontoFinalReta.setText(_translate("IncluirObjeto", "y2:"))
        self.labelZPontoFinalReta.setText(_translate("IncluirObjeto", "z2:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.RetaTab), _translate("IncluirObjeto", "Reta"))
        self.groupBoxVertice1.setTitle(_translate("IncluirObjeto", "Vértice 1"))
        self.labelXVertice1.setText(_translate("IncluirObjeto", "x1:"))
        self.labelYVertice1.setText(_translate("IncluirObjeto", "y1:"))
        self.labelZVertice1.setText(_translate("IncluirObjeto", "z1:"))
        self.pushButtonAdicionarVertice.setText(_translate("IncluirObjeto", "Adicionar vértice"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.WireframeTab), _translate("IncluirObjeto", "Wireframe"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.CurvasTab), _translate("IncluirObjeto", "Curvas"))
        self.pushButtonCancel_6.setText(_translate("IncluirObjeto", "Cancel"))
        self.pushButtonOK.setText(_translate("IncluirObjeto", "OK"))

    def addVertix(self):
        self.vertixCounter += 1

        self.groupBoxVertice2 = QtWidgets.QGroupBox(parent=self.verticalLayoutWidget_5)
        self.groupBoxVertice2.setMaximumSize(QtCore.QSize(16777215, 81))
        self.groupBoxVertice2.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading | QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop)
        self.groupBoxVertice2.setObjectName(f"groupBoxVertice{self.vertixCounter}")

        self.horizontalLayoutWidget2 = QtWidgets.QWidget(parent=self.groupBoxVertice2)
        self.horizontalLayoutWidget2.setGeometry(QtCore.QRect(10, 10, 611, 81))
        self.horizontalLayoutVertice2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget2)
        self.horizontalLayoutVertice2.setContentsMargins(50, 10, 50, 10)
        self.horizontalLayoutVertice2.setSpacing(20)

        self.labelXVertice2 = QtWidgets.QLabel(parent=self.horizontalLayoutWidget2)
        self.labelXVertice2 = QtWidgets.QLabel(parent=self.horizontalLayoutWidget2)

        self.textEditsWireframeX2 = QtWidgets.QPlainTextEdit(parent=self.horizontalLayoutWidget2)
        self.textEditsWireframeX2.setMaximumSize(QtCore.QSize(16777215, 30))
        self.textEditsWireframeX2.setObjectName(f"plainTextEditXVertice{self.vertixCounter}")

        self.labelYVertice2 = QtWidgets.QLabel(parent=self.horizontalLayoutWidget2)

        self.textEditsWireframeY2 = QtWidgets.QPlainTextEdit(parent=self.horizontalLayoutWidget2)
        self.textEditsWireframeY2.setMaximumSize(QtCore.QSize(4987648, 30))
        self.textEditsWireframeY2.setObjectName(f"plainTextEditYVertice{self.vertixCounter}")

        self.labelZVertice2 = QtWidgets.QLabel(parent=self.horizontalLayoutWidget2)
        self.labelZVertice2.setEnabled(False)

        self.textEditsWireframeZ2 = QtWidgets.QPlainTextEdit(parent=self.horizontalLayoutWidget2)
        self.textEditsWireframeZ2.setEnabled(False)
        self.textEditsWireframeZ2.setMaximumSize(QtCore.QSize(16777215, 30))
        self.textEditsWireframeZ2.setObjectName(f"plainTextEditZVertice{self.vertixCounter}")

        self.groupBoxVertice2.setTitle(f"Vértice {self.vertixCounter}")
        self.labelXVertice2.setText(f"x{self.vertixCounter}:")
        self.labelYVertice2.setText(f"y{self.vertixCounter}:")
        self.labelZVertice2.setText(f"z{self.vertixCounter}:")

        self.horizontalLayoutVertice2.addWidget(self.labelXVertice2)
        self.horizontalLayoutVertice2.addWidget(self.textEditsWireframeX2)
        self.horizontalLayoutVertice2.addWidget(self.labelYVertice2)
        self.horizontalLayoutVertice2.addWidget(self.textEditsWireframeY2)
        self.horizontalLayoutVertice2.addWidget(self.labelZVertice2)
        self.horizontalLayoutVertice2.addWidget(self.textEditsWireframeZ2)

        self.verticalLayoutPontosWireframe.addWidget(self.groupBoxVertice2)

    def createObject(self):
        index = self.tabWidget.currentIndex()
        newObject: WorldItem = None
        if index == 0:
            newObject = WorldItem(
                name=self.textEditInserirNome.toPlainText(),
                center_point=Point(0,0),
                graphic=Point(int(self.plainTextEditXPonto.toPlainText()),
                                     int(self.plainTextEditYPonto.toPlainText()))
            )
        elif index == 1:
            newObject = WorldItem(
                name=self.textEditInserirNome.toPlainText(),
                center_point=Point(0,0),
                graphic=Line(
                    start=Point(int(self.plainTextEditXPontoInicialReta.toPlainText()),
                                       int(self.plainTextEditYPontoInicialReta.toPlainText())),
                    end=Point(int(self.plainTextEditXPontoFinalReta.toPlainText()),
                                     int(self.plainTextEditYPontoFinalReta.toPlainText()))
                )
            )
        elif index == 2:
            pontosWireframe = self.verticalLayoutWidget_5.findChild(QtWidgets.QVBoxLayout)
            vertixList = list()
            for i in range(pontosWireframe.count()):
                groupBox = pontosWireframe.itemAt(i).widget()
                horizontalLayout = groupBox.findChild(QWidget)
                xValue = horizontalLayout.findChild(QtWidgets.QPlainTextEdit,
                                                    f"plainTextEditXVertice{i + 1}").toPlainText()
                yValue = horizontalLayout.findChild(QtWidgets.QPlainTextEdit,
                                                    f"plainTextEditYVertice{i + 1}").toPlainText()
                vertixList.append(Point(int(xValue), int(yValue)))
            if not is_polygon(vertixList):
                warning = NotAPolygonDialog()
                warning.exec()
                self.close()
                return

            newObject = WorldItem(
                name=self.textEditInserirNome.toPlainText(),
                center_point=Point(0, 0),
                graphic=Wireframe(vertixList)
            )
        else:
            pass

        determine_object_center(newObject)
        self.on_ok(newObject)
        self.lastAddedObject = newObject

        self.close()

    def getLastAddedObject(self):
        return self.lastAddedObject

    def __init__(self, on_ok):
        super().__init__()
        self.setupUi()
        self.on_ok = on_ok
        self.show()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    incluir_objeto = QtWidgets.QWidget()
    ui = IncluirObjeto(None)
    sys.exit(app.exec())
