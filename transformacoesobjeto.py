from typing import Callable

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QWidget

from typing import List, Callable

import window
from calculation.shapes.point import Point
from calculation import transformations


class TransformacoesObjetoUI(QWidget):

    transformationList: List[Callable] = list()
    translationCounter = rotationCounter = scalingCounter = 0

    def setupUi(self):
        self.setObjectName("Form")
        self.setWindowModality(QtCore.Qt.WindowModality.WindowModal)
        self.resize(800, 600)
        self.setMinimumSize(QtCore.QSize(800, 600))
        self.setMaximumSize(QtCore.QSize(800, 600))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.setFont(font)
        self.verticalLayoutWidget = QtWidgets.QWidget(parent=self)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 781, 581))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayoutPrincipal = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayoutPrincipal.setContentsMargins(0, 0, 0, 0)
        self.verticalLayoutPrincipal.setObjectName("verticalLayoutPrincipal")
        self.groupBoxTransformacoes = QtWidgets.QGroupBox(parent=self.verticalLayoutWidget)
        self.groupBoxTransformacoes.setObjectName("groupBoxTransformacoes")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(parent=self.groupBoxTransformacoes)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(-1, 19, 781, 481))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayoutTransformacoes = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayoutTransformacoes.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayoutTransformacoes.setObjectName("horizontalLayoutTransformacoes")
        self.tabWidgetTiposTransformacao = QtWidgets.QTabWidget(parent=self.horizontalLayoutWidget_2)
        self.tabWidgetTiposTransformacao.setObjectName("tabWidgetTiposTransformacao")

        self.tabTranslacao = QtWidgets.QWidget()
        self.tabTranslacao.setObjectName("tabTranslacao")
        self.verticalLayoutWidget_7 = QtWidgets.QWidget(parent=self.tabTranslacao)
        self.verticalLayoutWidget_7.setGeometry(QtCore.QRect(-1, -1, 511, 451))
        self.verticalLayoutWidget_7.setObjectName("verticalLayoutWidget_7")
        self.verticalLayoutParametrosTranslacao = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_7)
        self.verticalLayoutParametrosTranslacao.setContentsMargins(10, 10, 10, 10)
        self.verticalLayoutParametrosTranslacao.setObjectName("verticalLayoutParametrosTranslacao")
        self.groupBoxSelecionarEsqDir = QtWidgets.QGroupBox(parent=self.verticalLayoutWidget_7)
        self.groupBoxSelecionarEsqDir.setObjectName("groupBoxSelecionarEsqDir")
        self.verticalLayoutWidget_8 = QtWidgets.QWidget(parent=self.groupBoxSelecionarEsqDir)
        self.verticalLayoutWidget_8.setGeometry(QtCore.QRect(9, 30, 481, 71))
        self.verticalLayoutWidget_8.setObjectName("verticalLayoutWidget_8")
        self.verticalLayoutSelecionarEsqDir = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_8)
        self.verticalLayoutSelecionarEsqDir.setContentsMargins(10, 0, 0, 0)
        self.verticalLayoutSelecionarEsqDir.setObjectName("verticalLayoutSelecionarEsqDir")
        self.radioButtonEsquerda = QtWidgets.QRadioButton(parent=self.verticalLayoutWidget_8)
        self.radioButtonEsquerda.setObjectName("radioButtonEsquerda")
        self.verticalLayoutSelecionarEsqDir.addWidget(self.radioButtonEsquerda)
        self.radioButtonDireita = QtWidgets.QRadioButton(parent=self.verticalLayoutWidget_8)
        self.radioButtonDireita.setObjectName("radioButtonDireita")
        self.verticalLayoutSelecionarEsqDir.addWidget(self.radioButtonDireita)
        self.verticalLayoutParametrosTranslacao.addWidget(self.groupBoxSelecionarEsqDir)
        self.groupBoxUnidadesEsqDir = QtWidgets.QGroupBox(parent=self.verticalLayoutWidget_7)
        self.groupBoxUnidadesEsqDir.setObjectName("groupBoxUnidadesEsqDir")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBoxUnidadesEsqDir)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayoutUnidadesEsqDir = QtWidgets.QHBoxLayout()
        self.horizontalLayoutUnidadesEsqDir.setContentsMargins(10, -1, -1, -1)
        self.horizontalLayoutUnidadesEsqDir.setObjectName("horizontalLayoutUnidadesEsqDir")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                           QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayoutUnidadesEsqDir.addItem(spacerItem)
        self.labelDeslocamentoHorizontal = QtWidgets.QLabel(parent=self.groupBoxUnidadesEsqDir)
        self.labelDeslocamentoHorizontal.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading | QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.labelDeslocamentoHorizontal.setObjectName("labelDeslocamentoHorizontal")
        self.horizontalLayoutUnidadesEsqDir.addWidget(self.labelDeslocamentoHorizontal)
        self.plainTextEditUnidadesEsqDir = QtWidgets.QPlainTextEdit(parent=self.groupBoxUnidadesEsqDir)
        self.plainTextEditUnidadesEsqDir.setMaximumSize(QtCore.QSize(16777215, 30))
        self.plainTextEditUnidadesEsqDir.setObjectName("plainTextEditUnidadesEsqDir")
        self.horizontalLayoutUnidadesEsqDir.addWidget(self.plainTextEditUnidadesEsqDir)
        self.labelUnidadesEsqDir = QtWidgets.QLabel(parent=self.groupBoxUnidadesEsqDir)
        self.labelUnidadesEsqDir.setObjectName("labelUnidadesEsqDir")
        self.horizontalLayoutUnidadesEsqDir.addWidget(self.labelUnidadesEsqDir)
        self.horizontalLayoutUnidadesEsqDir.setStretch(0, 3)
        self.horizontalLayoutUnidadesEsqDir.setStretch(1, 1)
        self.horizontalLayoutUnidadesEsqDir.setStretch(2, 1)
        self.horizontalLayoutUnidadesEsqDir.setStretch(3, 1)
        self.horizontalLayout_3.addLayout(self.horizontalLayoutUnidadesEsqDir)
        self.verticalLayoutParametrosTranslacao.addWidget(self.groupBoxUnidadesEsqDir)
        self.groupBoxSelecionarCimaBaixo = QtWidgets.QGroupBox(parent=self.verticalLayoutWidget_7)
        self.groupBoxSelecionarCimaBaixo.setObjectName("groupBoxSelecionarCimaBaixo")
        self.verticalLayoutWidget_9 = QtWidgets.QWidget(parent=self.groupBoxSelecionarCimaBaixo)
        self.verticalLayoutWidget_9.setGeometry(QtCore.QRect(10, 30, 481, 71))
        self.verticalLayoutWidget_9.setObjectName("verticalLayoutWidget_9")
        self.verticalLayoutSelecionarCimaBaixo = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_9)
        self.verticalLayoutSelecionarCimaBaixo.setContentsMargins(10, 0, 0, 0)
        self.verticalLayoutSelecionarCimaBaixo.setObjectName("verticalLayoutSelecionarCimaBaixo")
        self.radioButtonCima = QtWidgets.QRadioButton(parent=self.verticalLayoutWidget_9)
        self.radioButtonCima.setObjectName("radioButtonCima")
        self.verticalLayoutSelecionarCimaBaixo.addWidget(self.radioButtonCima)
        self.radioButtonBaixo = QtWidgets.QRadioButton(parent=self.verticalLayoutWidget_9)
        self.radioButtonBaixo.setObjectName("radioButtonBaixo")
        self.verticalLayoutSelecionarCimaBaixo.addWidget(self.radioButtonBaixo)
        self.verticalLayoutParametrosTranslacao.addWidget(self.groupBoxSelecionarCimaBaixo)
        self.groupBoxUnidadesCimaBaixo = QtWidgets.QGroupBox(parent=self.verticalLayoutWidget_7)
        self.groupBoxUnidadesCimaBaixo.setObjectName("groupBoxUnidadesCimaBaixo")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.groupBoxUnidadesCimaBaixo)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayoutUnidadesCimaBaixo = QtWidgets.QHBoxLayout()
        self.horizontalLayoutUnidadesCimaBaixo.setObjectName("horizontalLayoutUnidadesCimaBaixo")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                            QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayoutUnidadesCimaBaixo.addItem(spacerItem1)
        self.labelDeslocamentoVertical = QtWidgets.QLabel(parent=self.groupBoxUnidadesCimaBaixo)
        self.labelDeslocamentoVertical.setObjectName("labelDeslocamentoVertical")
        self.horizontalLayoutUnidadesCimaBaixo.addWidget(self.labelDeslocamentoVertical)
        self.plainTextEditUnidadesCimaBaixo = QtWidgets.QPlainTextEdit(parent=self.groupBoxUnidadesCimaBaixo)
        self.plainTextEditUnidadesCimaBaixo.setMaximumSize(QtCore.QSize(16777215, 30))
        self.plainTextEditUnidadesCimaBaixo.setObjectName("plainTextEditUnidadesCimaBaixo")
        self.horizontalLayoutUnidadesCimaBaixo.addWidget(self.plainTextEditUnidadesCimaBaixo)
        self.labelUnidadesCimaBaixo = QtWidgets.QLabel(parent=self.groupBoxUnidadesCimaBaixo)
        self.labelUnidadesCimaBaixo.setObjectName("labelUnidadesCimaBaixo")
        self.horizontalLayoutUnidadesCimaBaixo.addWidget(self.labelUnidadesCimaBaixo)
        self.horizontalLayoutUnidadesCimaBaixo.setStretch(0, 3)
        self.horizontalLayoutUnidadesCimaBaixo.setStretch(1, 1)
        self.horizontalLayoutUnidadesCimaBaixo.setStretch(2, 1)
        self.horizontalLayoutUnidadesCimaBaixo.setStretch(3, 1)
        self.horizontalLayout_4.addLayout(self.horizontalLayoutUnidadesCimaBaixo)
        self.verticalLayoutParametrosTranslacao.addWidget(self.groupBoxUnidadesCimaBaixo)
        self.verticalLayoutParametrosTranslacao.setStretch(0, 1)
        self.verticalLayoutParametrosTranslacao.setStretch(1, 1)
        self.verticalLayoutParametrosTranslacao.setStretch(2, 1)
        self.verticalLayoutParametrosTranslacao.setStretch(3, 1)
        self.tabWidgetTiposTransformacao.addTab(self.tabTranslacao, "")

        self.tabRotacao = QtWidgets.QWidget()
        self.tabRotacao.setObjectName("tabRotacao")
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(parent=self.tabRotacao)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(10, 10, 491, 431))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayoutRotacao = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayoutRotacao.setContentsMargins(0, 0, 0, 0)
        self.verticalLayoutRotacao.setObjectName("verticalLayoutRotacao")
        self.groupBoxOpcoesRotacao = QtWidgets.QGroupBox(parent=self.verticalLayoutWidget_3)
        self.groupBoxOpcoesRotacao.setObjectName("groupBoxOpcoesRotacao")
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(parent=self.groupBoxOpcoesRotacao)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(10, 29, 471, 141))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.verticalLayoutOpcoesRotacao = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayoutOpcoesRotacao.setContentsMargins(0, 0, 0, 0)
        self.verticalLayoutOpcoesRotacao.setObjectName("verticalLayoutOpcoesRotacao")
        self.radioButtonRotacionarOrigem = QtWidgets.QRadioButton(parent=self.verticalLayoutWidget_4)
        self.radioButtonRotacionarOrigem.setChecked(True)
        self.radioButtonRotacionarOrigem.setObjectName("radioButtonRotacionarOrigem")
        self.verticalLayoutOpcoesRotacao.addWidget(self.radioButtonRotacionarOrigem)
        self.radioButtonRotacionarPonto = QtWidgets.QRadioButton(parent=self.verticalLayoutWidget_4)
        self.radioButtonRotacionarPonto.setObjectName("radioButtonRotacionarPonto")
        self.verticalLayoutOpcoesRotacao.addWidget(self.radioButtonRotacionarPonto)
        self.radioButtonRotacionarCentro = QtWidgets.QRadioButton(parent=self.verticalLayoutWidget_4)
        self.radioButtonRotacionarCentro.setObjectName("radioButtonRotacionarCentro")
        self.verticalLayoutOpcoesRotacao.addWidget(self.radioButtonRotacionarCentro)
        self.verticalLayoutRotacao.addWidget(self.groupBoxOpcoesRotacao)
        self.groupBoxSelecaoTipoRotacao = QtWidgets.QGroupBox(parent=self.verticalLayoutWidget_3)
        self.groupBoxSelecaoTipoRotacao.setObjectName("groupBoxSelecaoTipoRotacao")
        self.verticalLayoutWidget_5 = QtWidgets.QWidget(parent=self.groupBoxSelecaoTipoRotacao)
        self.verticalLayoutWidget_5.setGeometry(QtCore.QRect(10, 30, 471, 201))
        self.verticalLayoutWidget_5.setObjectName("verticalLayoutWidget_5")
        self.verticalLayoutParametrosRotacao = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_5)
        self.verticalLayoutParametrosRotacao.setContentsMargins(0, 0, 0, 0)
        self.verticalLayoutParametrosRotacao.setObjectName("verticalLayoutParametrosRotacao")
        self.groupBoxAnguloRotacao = QtWidgets.QGroupBox(parent=self.verticalLayoutWidget_5)
        self.groupBoxAnguloRotacao.setObjectName("groupBoxAnguloRotacao")
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(parent=self.groupBoxAnguloRotacao)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(9, 30, 451, 51))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout.setContentsMargins(0, 0, 10, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                            QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.labelAngulo = QtWidgets.QLabel(parent=self.horizontalLayoutWidget_3)
        self.labelAngulo.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.labelAngulo.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTrailing | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.labelAngulo.setObjectName("labelAngulo")
        self.horizontalLayout.addWidget(self.labelAngulo)
        self.plainTextEdit = QtWidgets.QPlainTextEdit(parent=self.horizontalLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plainTextEdit.sizePolicy().hasHeightForWidth())
        self.plainTextEdit.setSizePolicy(sizePolicy)
        self.plainTextEdit.setMaximumSize(QtCore.QSize(16777215, 30))
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.horizontalLayout.addWidget(self.plainTextEdit)
        self.label = QtWidgets.QLabel(parent=self.horizontalLayoutWidget_3)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.horizontalLayout.setStretch(0, 2)
        self.horizontalLayout.setStretch(1, 1)
        self.horizontalLayout.setStretch(2, 1)
        self.verticalLayoutParametrosRotacao.addWidget(self.groupBoxAnguloRotacao)
        self.groupBoxPontoRotacao = QtWidgets.QGroupBox(parent=self.verticalLayoutWidget_5)
        self.groupBoxPontoRotacao.setEnabled(False)
        self.groupBoxPontoRotacao.setObjectName("groupBoxPontoRotacao")
        self.horizontalLayoutWidget_4 = QtWidgets.QWidget(parent=self.groupBoxPontoRotacao)
        self.horizontalLayoutWidget_4.setGeometry(QtCore.QRect(9, 30, 451, 51))
        self.horizontalLayoutWidget_4.setObjectName("horizontalLayoutWidget_4")
        self.horizontalLayoutPontoRotacao = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_4)
        self.horizontalLayoutPontoRotacao.setContentsMargins(10, 0, 40, 0)
        self.horizontalLayoutPontoRotacao.setObjectName("horizontalLayoutPontoRotacao")
        self.labelX = QtWidgets.QLabel(parent=self.horizontalLayoutWidget_4)
        self.labelX.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTrailing | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.labelX.setObjectName("labelX")
        self.horizontalLayoutPontoRotacao.addWidget(self.labelX)
        self.plainTextEditX = QtWidgets.QPlainTextEdit(parent=self.horizontalLayoutWidget_4)
        self.plainTextEditX.setMaximumSize(QtCore.QSize(16777215, 30))
        self.plainTextEditX.setObjectName("plainTextEditX")
        self.horizontalLayoutPontoRotacao.addWidget(self.plainTextEditX)
        self.labelY = QtWidgets.QLabel(parent=self.horizontalLayoutWidget_4)
        self.labelY.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTrailing | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.labelY.setObjectName("labelY")
        self.horizontalLayoutPontoRotacao.addWidget(self.labelY)
        self.plainTextEditY = QtWidgets.QPlainTextEdit(parent=self.horizontalLayoutWidget_4)
        self.plainTextEditY.setMaximumSize(QtCore.QSize(16777215, 30))
        self.plainTextEditY.setObjectName("plainTextEditY")
        self.horizontalLayoutPontoRotacao.addWidget(self.plainTextEditY)
        self.labelZ = QtWidgets.QLabel(parent=self.horizontalLayoutWidget_4)
        self.labelZ.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTrailing | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.labelZ.setObjectName("labelZ")
        self.labelZ.setEnabled(False)
        self.horizontalLayoutPontoRotacao.addWidget(self.labelZ)
        self.plainTextEditZ = QtWidgets.QPlainTextEdit(parent=self.horizontalLayoutWidget_4)
        self.plainTextEditZ.setMaximumSize(QtCore.QSize(16777215, 30))
        self.plainTextEditZ.setObjectName("plainTextEditZ")
        self.plainTextEditZ.setEnabled(False)
        self.horizontalLayoutPontoRotacao.addWidget(self.plainTextEditZ)
        self.horizontalLayoutPontoRotacao.setStretch(0, 1)
        self.horizontalLayoutPontoRotacao.setStretch(1, 1)
        self.horizontalLayoutPontoRotacao.setStretch(2, 1)
        self.horizontalLayoutPontoRotacao.setStretch(3, 1)
        self.horizontalLayoutPontoRotacao.setStretch(4, 1)
        self.horizontalLayoutPontoRotacao.setStretch(5, 1)
        self.verticalLayoutParametrosRotacao.addWidget(self.groupBoxPontoRotacao)
        self.verticalLayoutRotacao.addWidget(self.groupBoxSelecaoTipoRotacao)
        self.verticalLayoutRotacao.setStretch(0, 3)
        self.verticalLayoutRotacao.setStretch(1, 4)
        self.tabWidgetTiposTransformacao.addTab(self.tabRotacao, "")

        self.tabEscalonamento = QtWidgets.QWidget()
        self.tabEscalonamento.setObjectName("tabEscalonamento")
        self.verticalLayoutWidget_6 = QtWidgets.QWidget(parent=self.tabEscalonamento)
        self.verticalLayoutWidget_6.setGeometry(QtCore.QRect(-1, -1, 511, 451))
        self.verticalLayoutWidget_6.setObjectName("verticalLayoutWidget_6")
        self.verticalLayoutEscalonamento = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_6)
        self.verticalLayoutEscalonamento.setContentsMargins(10, 10, 10, 10)
        self.verticalLayoutEscalonamento.setObjectName("verticalLayoutEscalonamento")
        self.groupBoxEscalonar = QtWidgets.QGroupBox(parent=self.verticalLayoutWidget_6)
        self.groupBoxEscalonar.setObjectName("groupBoxEscalonar")
        self.horizontalLayoutWidget_5 = QtWidgets.QWidget(parent=self.groupBoxEscalonar)
        self.horizontalLayoutWidget_5.setGeometry(QtCore.QRect(10, 29, 471, 61))
        self.horizontalLayoutWidget_5.setObjectName("horizontalLayoutWidget_5")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_5)
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetFixedSize)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                            QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.labelProporcaoEscalonamento = QtWidgets.QLabel(parent=self.horizontalLayoutWidget_5)
        self.labelProporcaoEscalonamento.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTrailing | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.labelProporcaoEscalonamento.setObjectName("labelProporcaoEscalonamento")
        self.horizontalLayout_2.addWidget(self.labelProporcaoEscalonamento)
        self.plainTextEditPorcentagemEscalonamento = QtWidgets.QPlainTextEdit(parent=self.horizontalLayoutWidget_5)
        self.plainTextEditPorcentagemEscalonamento.setMaximumSize(QtCore.QSize(16777215, 30))
        self.plainTextEditPorcentagemEscalonamento.setObjectName("plainTextEditPorcentagemEscalonamento")
        self.horizontalLayout_2.addWidget(self.plainTextEditPorcentagemEscalonamento)
        self.label_2 = QtWidgets.QLabel(parent=self.horizontalLayoutWidget_5)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.horizontalLayout_2.setStretch(0, 10)
        self.horizontalLayout_2.setStretch(1, 3)
        self.horizontalLayout_2.setStretch(2, 3)
        self.horizontalLayout_2.setStretch(3, 1)
        self.verticalLayoutEscalonamento.addWidget(self.groupBoxEscalonar)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum,
                                            QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayoutEscalonamento.addItem(spacerItem4)
        self.verticalLayoutEscalonamento.setStretch(0, 1)
        self.verticalLayoutEscalonamento.setStretch(1, 3)
        self.tabWidgetTiposTransformacao.addTab(self.tabEscalonamento, "")
        self.horizontalLayoutTransformacoes.addWidget(self.tabWidgetTiposTransformacao)
        self.verticalLayoutListaTransformacoes = QtWidgets.QVBoxLayout()
        self.verticalLayoutListaTransformacoes.setContentsMargins(5, 5, 5, 5)
        self.verticalLayoutListaTransformacoes.setObjectName("verticalLayoutListaTransformacoes")
        self.pushButtonAdiciona = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget_2)
        self.pushButtonAdiciona.setMaximumSize(QtCore.QSize(300, 28))
        self.pushButtonAdiciona.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.pushButtonAdiciona.setObjectName("pushButtonAdiciona")
        self.verticalLayoutListaTransformacoes.addWidget(self.pushButtonAdiciona)
        self.groupBoxListaTransformacoes = QtWidgets.QGroupBox(parent=self.horizontalLayoutWidget_2)
        self.groupBoxListaTransformacoes.setObjectName("groupBoxListaTransformacoes")
        self.listWidgetListaTransformacoes = QtWidgets.QListWidget(parent=self.groupBoxListaTransformacoes)
        self.listWidgetListaTransformacoes.setGeometry(QtCore.QRect(5, 23, 237, 405))
        self.listWidgetListaTransformacoes.setObjectName("listWidgetListaTransformacoes")
        self.verticalLayoutListaTransformacoes.addWidget(self.groupBoxListaTransformacoes)
        self.horizontalLayoutTransformacoes.addLayout(self.verticalLayoutListaTransformacoes)
        self.horizontalLayoutTransformacoes.setStretch(0, 2)
        self.horizontalLayoutTransformacoes.setStretch(1, 1)
        self.verticalLayoutPrincipal.addWidget(self.groupBoxTransformacoes)
        self.horizontalLayoutOKCancel = QtWidgets.QHBoxLayout()
        self.horizontalLayoutOKCancel.setSpacing(5)
        self.horizontalLayoutOKCancel.setObjectName("horizontalLayoutOKCancel")
        self.widgetSpacerOKCancel = QtWidgets.QWidget(parent=self.verticalLayoutWidget)
        self.widgetSpacerOKCancel.setObjectName("widgetSpacerOKCancel")
        self.horizontalLayoutOKCancel.addWidget(self.widgetSpacerOKCancel)
        self.pushButtonCancel = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.horizontalLayoutOKCancel.addWidget(self.pushButtonCancel)
        self.pushButtonOK = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.pushButtonOK.setObjectName("pushButtonOK")
        self.horizontalLayoutOKCancel.addWidget(self.pushButtonOK)
        self.horizontalLayoutOKCancel.setStretch(0, 4)
        self.horizontalLayoutOKCancel.setStretch(1, 1)
        self.horizontalLayoutOKCancel.setStretch(2, 1)
        self.verticalLayoutPrincipal.addLayout(self.horizontalLayoutOKCancel)
        self.verticalLayoutPrincipal.setStretch(0, 7)
        self.verticalLayoutPrincipal.setStretch(1, 1)

        self.retranslateUi()
        self.tabWidgetTiposTransformacao.setCurrentIndex(0)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Transformações Objeto"))
        self.groupBoxTransformacoes.setTitle(_translate("Form", "Transformações"))
        self.groupBoxSelecionarEsqDir.setTitle(_translate("Form", "Selecionar deslocamento horizontal"))
        self.radioButtonEsquerda.setText(_translate("Form", "Mover para a esquerda"))
        self.radioButtonDireita.setText(_translate("Form", "Mover para a direita"))
        self.groupBoxUnidadesEsqDir.setTitle(_translate("Form", "Unidades para deslocar (esquerda ou direita)"))
        self.labelDeslocamentoHorizontal.setText(_translate("Form", "Deslocamento:"))
        self.labelUnidadesEsqDir.setText(_translate("Form", "unidades"))
        self.groupBoxSelecionarCimaBaixo.setTitle(_translate("Form", "Selecionar deslocamento vertical"))
        self.radioButtonCima.setText(_translate("Form", "Mover para cima"))
        self.radioButtonBaixo.setText(_translate("Form", "Mover para baixo"))
        self.groupBoxUnidadesCimaBaixo.setTitle(_translate("Form", "Unidades para deslocar (cima ou baixo)"))
        self.labelDeslocamentoVertical.setText(_translate("Form", "Deslocamento:"))
        self.labelUnidadesCimaBaixo.setText(_translate("Form", "unidades"))
        self.tabWidgetTiposTransformacao.setTabText(self.tabWidgetTiposTransformacao.indexOf(self.tabTranslacao),
                                                    _translate("Form", "Translação"))
        self.groupBoxOpcoesRotacao.setTitle(_translate("Form", "Opções"))
        self.radioButtonRotacionarOrigem.setText(_translate("Form", "Rotacionar sobre a Origem"))
        self.radioButtonRotacionarPonto.setText(_translate("Form", "Rotacionar sobre um Ponto"))
        self.radioButtonRotacionarCentro.setText(_translate("Form", "Rotacionar sobre o Centro do Objeto"))
        self.groupBoxSelecaoTipoRotacao.setTitle(_translate("Form", "Rotacionar sobre a Origem"))
        self.groupBoxAnguloRotacao.setTitle(_translate("Form", "Ângulo de Rotação"))
        self.labelAngulo.setText(_translate("Form", "Ângulo:"))
        self.label.setText(_translate("Form", "°"))
        self.groupBoxPontoRotacao.setTitle(_translate("Form", "Selecionar Ponto"))
        self.labelX.setText(_translate("Form", "X:"))
        self.plainTextEditX.setPlainText(_translate("Form", "0"))
        self.labelY.setText(_translate("Form", "Y:"))
        self.plainTextEditY.setPlainText(_translate("Form", "0"))
        self.labelZ.setText(_translate("Form", "Z:"))
        self.plainTextEditZ.setPlainText(_translate("Form", "0"))
        self.tabWidgetTiposTransformacao.setTabText(self.tabWidgetTiposTransformacao.indexOf(self.tabRotacao),
                                                    _translate("Form", "Rotação"))
        self.groupBoxEscalonar.setTitle(_translate("Form", "Escalonar"))
        self.labelProporcaoEscalonamento.setText(_translate("Form", "Proporção:"))
        self.label_2.setText(_translate("Form", "%"))
        self.tabWidgetTiposTransformacao.setTabText(self.tabWidgetTiposTransformacao.indexOf(self.tabEscalonamento),
                                                    _translate("Form", "Escalonamento"))
        self.pushButtonAdiciona.setText(_translate("Form", "Adiciona"))
        self.groupBoxListaTransformacoes.setTitle(_translate("Form", "Lista de transformações"))
        __sortingEnabled = self.listWidgetListaTransformacoes.isSortingEnabled()
        self.listWidgetListaTransformacoes.setSortingEnabled(False)
        self.listWidgetListaTransformacoes.setSortingEnabled(__sortingEnabled)
        self.pushButtonCancel.setText(_translate("Form", "Cancel"))
        self.pushButtonOK.setText(_translate("Form", "OK"))

    def setupEvents(self):
        self.pushButtonAdiciona.clicked.connect(self.addTransformation)
        self.pushButtonCancel.clicked.connect(self.close)
        self.pushButtonOK.clicked.connect(self.applyTransformations)
        self.radioButtonEsquerda.clicked.connect(self.checkMoveLeft)
        self.radioButtonDireita.clicked.connect(self.checkMoveRight)
        self.radioButtonCima.clicked.connect(self.checkMoveUp)
        self.radioButtonBaixo.clicked.connect(self.checkMoveDown)
        self.radioButtonRotacionarOrigem.clicked.connect(self.checkRotateOnOrigin)
        self.radioButtonRotacionarCentro.clicked.connect(self.checkRotateOnObjectCenter)
        self.radioButtonRotacionarPonto.clicked.connect(self.checkRotateOnPoint)

    def translate(self) -> Callable:
        try:
            x = int(self.plainTextEditUnidadesEsqDir.toPlainText())
            y = int(self.plainTextEditUnidadesCimaBaixo.toPlainText())
        except ValueError:
            return

        if self.radioButtonEsquerda.isChecked():
            x *= -1

        if self.radioButtonBaixo.isChecked():
            y *= -1

        point = Point(x, y)
        return transformations.translate(self.item, point)

    def scaling(self) -> Callable:
        try:
            proportion = int(self.plainTextEditPorcentagemEscalonamento.toPlainText()) / 100
        except ValueError:
            return
        return transformations.scale(self.item.graphic, proportion, self.item.center_point)

    def rotation(self) -> Callable:
        try:
            graus = int(self.plainTextEdit.toPlainText())
        except ValueError:
            return

        if self.radioButtonRotacionarOrigem.isChecked():
            reference_point = Point(0, 0)
        elif self.radioButtonRotacionarPonto.isChecked():
            try:
                x = int(self.plainTextEditX.toPlainText())
                y = int(self.plainTextEditY.toPlainText())
            except ValueError:
                return
            reference_point = Point(x, y)
        else:
            reference_point = self.item.center_point

        return transformations.rotate(self.item, reference_point, graus)

    def addTransformation(self):
        print(self.item)
        index = self.tabWidgetTiposTransformacao.currentIndex()
        # translaçao
        if index == 0:
            self.transformationList.append(self.translate())
            self.translationCounter += 1
            self.listWidgetListaTransformacoes.addItem(f"Translação {self.translationCounter}")
        # rotaçao
        elif index == 1:
            self.transformationList.append(self.rotation())
            self.rotationCounter += 1
            self.listWidgetListaTransformacoes.addItem(f"Rotação {self.rotationCounter}")
        # escalonamento
        else:
            self.transformationList.append(self.scaling())
            self.scalingCounter += 1
            self.listWidgetListaTransformacoes.addItem(f"Escalonamento {self.translationCounter}")

    def applyTransformations(self):

        for transformation in self.transformationList:
            transformation()

        self.on_close()
        self.close()

    def checkMoveLeft(self):
        self.radioButtonEsquerda.setChecked(True)
        self.radioButtonDireita.setChecked(False)

    def checkMoveRight(self):
        self.radioButtonEsquerda.setChecked(False)
        self.radioButtonDireita.setChecked(True)

    def checkMoveUp(self):
        self.radioButtonCima.setChecked(True)
        self.radioButtonBaixo.setChecked(False)

    def checkMoveDown(self):
        self.radioButtonCima.setChecked(False)
        self.radioButtonBaixo.setChecked(True)

    def checkRotateOnOrigin(self):
        self.radioButtonRotacionarOrigem.setChecked(True)
        self.radioButtonRotacionarCentro.setChecked(False)
        self.radioButtonRotacionarPonto.setChecked(False)
        self.groupBoxPontoRotacao.setEnabled(False)
        self.groupBoxSelecaoTipoRotacao.setTitle("Rotacionar sobre a Origem")
        self.plainTextEditX.setPlainText("0")
        self.plainTextEditY.setPlainText("0")
        self.plainTextEditZ.setPlainText("0")

    def checkRotateOnObjectCenter(self):
        self.radioButtonRotacionarOrigem.setChecked(False)
        self.radioButtonRotacionarCentro.setChecked(True)
        self.radioButtonRotacionarPonto.setChecked(False)
        self.groupBoxPontoRotacao.setEnabled(False)
        self.groupBoxSelecaoTipoRotacao.setTitle("Rotacionar sobre o Centro do Objeto")
        # TODO modificar valores para ser igual ao do centro do objeto
        # self.plainTextEditX.setPlainText("")
        # self.plainTextEditY.setPlainText("")
        # self.plainTextEditZ.setPlainText("")

    def checkRotateOnPoint(self):
        self.radioButtonRotacionarOrigem.setChecked(False)
        self.radioButtonRotacionarCentro.setChecked(False)
        self.radioButtonRotacionarPonto.setChecked(True)
        self.groupBoxPontoRotacao.setEnabled(True)
        self.groupBoxSelecaoTipoRotacao.setTitle("Rotacionar sobre um Ponto")
        self.plainTextEditX.setPlainText("")
        self.plainTextEditY.setPlainText("")
        self.plainTextEditZ.setPlainText("")

    def __init__(self, item: window.WorldItem, on_close: Callable):
        super().__init__()
        self.transformationList = list()
        self.setupUi()
        self.setupEvents()
        self.item = item
        self.on_close = on_close
        self.show()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = TransformacoesObjetoUI(None)
    sys.exit(app.exec())
