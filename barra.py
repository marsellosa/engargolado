# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created: Tue Oct  4 02:00:57 2016
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)

class Ui_Engargolado(object):
    def setupUi(self, Engargolado):
        Engargolado.setObjectName(_fromUtf8("Engargolado"))
        Engargolado.resize(452, 127)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu Condensed"))
        Engargolado.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("images/Main/arrows.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Engargolado.setWindowIcon(icon)
        self.centralwidget = QWidget(Engargolado)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.widget = QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 0, 251, 81))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout = QHBoxLayout(self.widget)
        # self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.btnComanda = QPushButton(self.widget)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnComanda.sizePolicy().hasHeightForWidth())
        self.btnComanda.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu Condensed"))
        self.btnComanda.setFont(font)
        self.btnComanda.setText(_fromUtf8(""))
        self.btnComanda.setIcon(icon)
        self.btnComanda.setIconSize(QtCore.QSize(48, 48))
        self.btnComanda.setObjectName(_fromUtf8("btnComanda"))
        self.horizontalLayout.addWidget(self.btnComanda)
        self.btnEstadisticas = QPushButton(self.widget)
        self.btnEstadisticas.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8("images/Main/1473586024_vector_65_14.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnEstadisticas.setIcon(icon1)
        self.btnEstadisticas.setIconSize(QtCore.QSize(48, 48))
        self.btnEstadisticas.setObjectName(_fromUtf8("btnEstadisticas"))
        self.horizontalLayout.addWidget(self.btnEstadisticas)
        self.btnReferidos = QPushButton(self.widget)
        self.btnReferidos.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8("images/Main/Add User Group Woman Man-48.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnReferidos.setIcon(icon2)
        self.btnReferidos.setIconSize(QtCore.QSize(48, 48))
        self.btnReferidos.setObjectName(_fromUtf8("btnReferidos"))
        self.horizontalLayout.addWidget(self.btnReferidos)
        Engargolado.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(Engargolado)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 452, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuPreferencias = QMenu(self.menubar)
        self.menuPreferencias.setObjectName(_fromUtf8("menuPreferencias"))
        Engargolado.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(Engargolado)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        Engargolado.setStatusBar(self.statusbar)
        self.actionAjustes = QAction(Engargolado)
        self.actionAjustes.setObjectName(_fromUtf8("actionAjustes"))
        self.action_Salir = QAction(Engargolado)
        self.action_Salir.setObjectName(_fromUtf8("action_Salir"))
        self.menuPreferencias.addAction(self.actionAjustes)
        self.menuPreferencias.addSeparator()
        self.menuPreferencias.addAction(self.action_Salir)
        self.menubar.addAction(self.menuPreferencias.menuAction())

        self.retranslateUi(Engargolado)
        QtCore.QMetaObject.connectSlotsByName(Engargolado)

    def retranslateUi(self, Engargolado):
        Engargolado.setWindowTitle(_translate("Engargolado", "Engargolado", None))
        self.menuPreferencias.setTitle(_translate("Engargolado", "Editar", None))
        self.actionAjustes.setText(_translate("Engargolado", "&Preferencias", None))
        self.action_Salir.setText(_translate("Engargolado", "&Salir", None))

