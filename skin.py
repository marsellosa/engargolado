# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'skin.ui'
#
# Created: Sun May 15 23:52:32 2016
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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(400, 464)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu Condensed"))
        Form.setFont(font)
        self.tblReferidos = QtGui.QTableWidget(Form)
        self.tblReferidos.setEnabled(False)
        self.tblReferidos.setGeometry(QtCore.QRect(10, 50, 381, 371))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu Condensed"))
        self.tblReferidos.setFont(font)
        self.tblReferidos.setObjectName(_fromUtf8("tblReferidos"))
        self.tblReferidos.setColumnCount(0)
        self.tblReferidos.setRowCount(0)
        self.btnSalir = QtGui.QPushButton(Form)
        self.btnSalir.setGeometry(QtCore.QRect(10, 430, 96, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu Condensed"))
        self.btnSalir.setFont(font)
        self.btnSalir.setObjectName(_fromUtf8("btnSalir"))
        self.btnGuardar = QtGui.QPushButton(Form)
        self.btnGuardar.setGeometry(QtCore.QRect(300, 430, 96, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu Condensed"))
        self.btnGuardar.setFont(font)
        self.btnGuardar.setObjectName(_fromUtf8("btnGuardar"))
        self.btnAgregar = QtGui.QPushButton(Form)
        self.btnAgregar.setGeometry(QtCore.QRect(360, 10, 31, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu Condensed"))
        self.btnAgregar.setFont(font)
        self.btnAgregar.setObjectName(_fromUtf8("btnAgregar"))
        self.line = QtGui.QFrame(Form)
        self.line.setGeometry(QtCore.QRect(10, 420, 381, 16))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu Condensed"))
        self.line.setFont(font)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.layoutWidget = QtGui.QWidget(Form)
        self.layoutWidget.setGeometry(QtCore.QRect(60, 10, 291, 31))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.layoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.txtReferidor = QtGui.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu Condensed"))
        self.txtReferidor.setFont(font)
        self.txtReferidor.setObjectName(_fromUtf8("txtReferidor"))
        self.horizontalLayout.addWidget(self.txtReferidor)
        self.chksendmail = QtGui.QCheckBox(Form)
        self.chksendmail.setGeometry(QtCore.QRect(170, 430, 121, 26))
        self.chksendmail.setChecked(True)
        self.chksendmail.setObjectName(_fromUtf8("chksendmail"))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.btnSalir.setText(_translate("Form", "&Salir", None))
        self.btnGuardar.setText(_translate("Form", "&Guardar", None))
        self.btnAgregar.setText(_translate("Form", "+", None))
        self.label.setText(_translate("Form", "Invitado por :", None))
        self.chksendmail.setText(_translate("Form", "enviar por correo", None))

