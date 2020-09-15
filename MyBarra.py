#!/usr/bin/env python
import sys
import barra, comandacode, addSocio, ReporteCode
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class MainForm(QMainWindow, barra.Ui_Engargolado):
    def __init__(self, parent=None):
        # initialize parent class
        super(MainForm, self).__init__(None)
        self.setupUi(self)
        self.ValIniciales()
        self.connectActions()

    def ValIniciales(self):
        self.btnComanda.setToolTip('Registro')
        self.btnEstadisticas.setToolTip('Reportes')


    def main(self):
        self.show()

    def connectActions(self):
        self.btnReferidos.clicked.connect(self.on_mainbuttons_clicked)
        self.btnComanda.clicked.connect(self.on_mainbuttons_clicked)
        self.btnEstadisticas.clicked.connect(self.on_mainbuttons_clicked)

    def on_mainbuttons_clicked(self):
        sender = self.sender().objectName()
        if sender == 'btnReferidos':
            # wid = skincode.Registro(self)
            wid = addSocio.AddSocio(self)
        if sender == 'btnComanda':
            wid = comandacode.Registro(self)
        if sender == 'btnEstadisticas':
            wid = ReporteCode.Reporte(self)
        wid.exec_()

app = QApplication(sys.argv)
ui = MainForm()
ui.main()
app.exec_()
