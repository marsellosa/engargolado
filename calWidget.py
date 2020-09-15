# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'calWidget.ui'
#
# Created: Wed Mar 11 19:58:55 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Calendario(object):
    def setupUi(self, Calendario):
        Calendario.setObjectName(_fromUtf8("Calendario"))
        Calendario.resize(295, 457)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu Condensed"))
        font.setPointSize(12)
        Calendario.setFont(font)
        self.calWidget = QtGui.QCalendarWidget(Calendario)
        self.calWidget.setGeometry(QtCore.QRect(20, 60, 261, 201))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu Condensed"))
        self.calWidget.setFont(font)
        self.calWidget.setObjectName(_fromUtf8("calWidget"))
        self.lbl_Titulo = QtGui.QLabel(Calendario)
        self.lbl_Titulo.setGeometry(QtCore.QRect(10, 20, 261, 17))
        self.lbl_Titulo.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_Titulo.setObjectName(_fromUtf8("lbl_Titulo"))
        self.line = QtGui.QFrame(Calendario)
        self.line.setGeometry(QtCore.QRect(7, 40, 281, 20))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.splitter = QtGui.QSplitter(Calendario)
        self.splitter.setGeometry(QtCore.QRect(20, 280, 261, 29))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.lbl_firstDay = QtGui.QLabel(self.splitter)
        self.lbl_firstDay.setObjectName(_fromUtf8("lbl_firstDay"))
        self.cbo_dayOfWeek = QtGui.QComboBox(self.splitter)
        self.cbo_dayOfWeek.setObjectName(_fromUtf8("cbo_dayOfWeek"))
        self.btn_Continuar = QtGui.QPushButton(Calendario)
        self.btn_Continuar.setGeometry(QtCore.QRect(190, 420, 96, 31))
        self.btn_Continuar.setObjectName(_fromUtf8("btn_Continuar"))

        self.retranslateUi(Calendario)
        QtCore.QMetaObject.connectSlotsByName(Calendario)

    def retranslateUi(self, Calendario):
        Calendario.setWindowTitle(_translate("Calendario", "Form", None))
        self.lbl_Titulo.setText(_translate("Calendario", "TextLabel", None))
        self.lbl_firstDay.setText(_translate("Calendario", "Primer día de la Semana:", None))
        self.btn_Continuar.setText(_translate("Calendario", "Continuar", None))

