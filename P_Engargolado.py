#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: 850 -*-

import sys
import sqlite3 as lite
import MyWindow, AgregarSocio, calWidget
import os
from PyQt4.QtGui import *
from PyQt4.QtCore import *
#import pdb

#import gammu    ##modulo para enviar mensajes

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s
    
try:
    _encoding = QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)

## Variables Globales
#Nutricion, total_extras = 18, 0
#Extras = {'Proteina': 7, 'Fibra': 9, 'Batido': 10, 'Aloe': 5, 'Te': 5, 'LiftOff':20 }
Nutricion, total_extras = 22, 0
Extras = {'Proteina': 9, 'Fibra': 10, 'Batido': 12, 'Aloe': 6, 'Te': 6, 'LiftOff':20 }
FechaHoy = str(QDate.toString(QDate.currentDate(), "yyyy/MM/dd"))
FechaCal = None #fecha escogida en el calendario
Semana = None #nombre del dia de la semana
Mes = None #
Hoy = None #dia en el que empieza tu semana de trabajo
appName = "ENGARGOLADO"
Views_List = list()
colNameIndex = dict()
Fechas_List = list()
font = QFont()
font.setFamily(_fromUtf8("Ubuntu Condensed"))
font.setPointSize(12)
#path = (sys.argv[1] if len(sys.argv) > 1 and
#                    QFile.exists(sys.argv[1]) else os.getcwd())
path = os.getcwd()
print path
Calcular = True # boolean que me permite cargar la tabla de asistencia tal cual esta en la BD
## --------------------

class MainForm(QMainWindow, MyWindow.Ui_MainWindow):
    def __init__(self,parent=None):
        #initialize parent class
        super(MainForm,self).__init__(None)
        self.setupUi(self)
        self.varIniciales()
        self.dibujarTablas()
        self.setCalWidget()
        self.connectActions()
        #self.tbl_Asistencia_ColWith()
        print "hola"
        self.Diccionario()
        print "dic"
        self.dateChanged()
        self.myprint()
    def main(self):
        self.show()

#--------------CONECTANDO EVENTOS CON MIS FUNCIONES----------------
    def connectActions(self):
        
        self.dateEdit.setDate(QDate.currentDate())
        self.btn_Agregar.clicked.connect(self.AddEditBD)
        self.txt_Nombre.textChanged.connect(self.txt_Nombre_textChanged)
        #self.lst_Encontrado.doubleClicked.connect(self.lst_Encontrado_dblClick)
        self.lst_Encontrado.clicked.connect(self.lst_Encontrado_Clicked)
        self.btn_fecha.clicked.connect(self.AbrirCal)
        self.tab_Main.currentChanged.connect(self.dateChanged)
        self.tab_Registro.currentChanged.connect(self.dateChanged)
        self.tab_Reportes.currentChanged.connect(self.dateChanged)
        #self.btn_fecha.clicked.connect(self.myprint)
        #self.lst_Registrado.doubleClicked.connect(self.lst_Registrado_dblClicked)
        self.dateEdit.dateChanged.connect(self.dateChanged)
        self.tbl_Asistencia.doubleClicked.connect(self.tbl_Asistencia_dblClicked)
        self.tbl_Asistencia.cellChanged.connect(self.tbl_Asistencia_cellChanged)
        #self.tbl_Rep_Mensual.cellChanged.connect(self.tbl_Rep_Mensual_cellChanged)
        self.tbl_Rep_Mensual.cellChanged.connect(self.tbl_Asistencia_cellChanged)
        #self.tbl_Asistencia.keyPressEvent.connect(self.myprint)
        #self.tbl_Asistencia.itemChanged.connect(self.myprint)


###------------MIS FUNCIONES --------------------------------------

    def varIniciales(self):
        global BD
        BD = dataBase()
        BD.createCon()

    def probando(self, headers, ancho, filas):
        tabla.setGeometry(QRect(10, 10, 651, 381))
        tabla.setRowCount(filas)
        tabla.setColumnCount(len(headers))
        col = 0
        for head in headers:
            item = QTableWidgetItem()
            tabla.setHorizontalHeaderItem(col, item)
            tabla.setColumnWidth(col, ancho[col])
            head = tabla.horizontalHeaderItem(col)
            head.setText(_translate("MainWindow", headers[col], None))
            col += 1
            
    def dibujarTablas(self):
        global tabla
        #Inicio del codigo que dibuja la tabla Asistencia
        tabla = QTableWidget(self.Asistencia)
        headers = ['Status', 'Nombre', 'Proteina', 'Fibra', 'Batido', 'Te', 'Aloe', 'LiftOff','PrePago', 'Total']
        ancho = [60,170, 60, 50, 50, 50, 60, 60, 60, 50]
        filas = 100
        self.probando(headers, ancho, filas)
##        self.tbl_Asistencia.setRowCount(100)
##        self.tbl_Asistencia.setColumnCount(len(headers))
##        col = 0
##        for head in headers:
##            item = QTableWidgetItem()
##            self.tbl_Asistencia.setHorizontalHeaderItem(col, item)
##            self.tbl_Asistencia.setColumnWidth(col, ancho[col])
##            head = self.tbl_Asistencia.horizontalHeaderItem(col)
##            head.setText(_translate("MainWindow", headers[col], None))
##            #stylesheet = "QHeaderView::section{Background-color:rgb(100,100,100);border-radius:14px;}"
##            #self.tbl_Asistencia.horizontalHeader().setStyleSheet(stylesheet)
##            col += 1
        # Fin del codigo que dibuja la tabla Asistencia
        
        #Inicio del codigo que dibuja la tabla Rep_Mensual
        tabla = QTableWidget(self.Mensual)
        headers = ['Semana', 'Invitaciones', 'Entraron', 'NConsumos', 'Referidos', 'TConsumos', 'Ganancia']
        ancho = [80, 80, 80, 80, 80, 80, 80]
        filas = 31
        self.probando(headers, ancho, filas)
##        self.tbl_Rep_Mensual.setRowCount(31)
##        self.tbl_Rep_Mensual.setColumnCount(len(headers))
##        col = 0
##        for head in headers:
##            item = QTableWidgetItem()
##            self.tbl_Rep_Mensual.setHorizontalHeaderItem(col, item)
##            self.tbl_Rep_Mensual.setColumnWidth(col, 80)
##            head = self.tbl_Rep_Mensual.horizontalHeaderItem(col)
##            head.setText(_translate("MainWindow", headers[col], None))
##            col += 1
        # Fin del codigo que dibuja la tabla Rep_Mensual
        
        # Dibuja la Tabla Producto Cerrado (inicio)}
        tabla = QTableWidget(self.ProdCerrado)
        headers = ['Nombre', 'Producto', 'Cantidad', 'Sobre Rojo', 'Sobre Verde']
        ancho = [170, 160, 80, 80, 80]
        filas = 15
        self.probando(headers, ancho, filas)
##        self.tbl_prodCerrado.setRowCount(15)
##        self.tbl_prodCerrado.setColumnCount(len(headers))
##        col = 0
##        for head in headers:
##            item = QTableWidgetItem()
##            self.tbl_prodCerrado.setHorizontalHeaderItem(col, item)
##            self.tbl_prodCerrado.setColumnWidth(col, ancho[col])
##            head = self.tbl_prodCerrado.horizontalHeaderItem(col)
##            head.setText(_translate("MainWindow", headers[col], None))
##            col += 1
        # Dibuja la Tabla Producto Cerrado (fin)
        # Dibuja la Tabla Reporte Semanal (inicio)
        tabla = QTableWidget(self.Semanal)
        headers = ['Desde - Hasta', 'Promedio', 'Ganancia', 'Proyectado']
        ancho = [170, 80, 80, 80]
        filas = 15
        self.probando(headers, ancho, filas)
#        self.tbl_Rep_Semanal = RotatedHeaderView()
#        self.tbl_Rep_Semanal.setGeometry(QtCore.QRect(10, 10, 671, 391))
#        self.tbl_Rep_Semanal.setObjectName(_fromUtf8("tbl_Rep_Semanal"))
#        self.tbl_Rep_Semanal.paintEvent().RotatedHeaderView()
##        self.tbl_Rep_Semanal.setRowCount(15)
##        self.tbl_Rep_Semanal.setColumnCount(len(headers))
##        col = 0
##        for head in headers:
##            item = QTableWidgetItem()
##            self.tbl_Rep_Semanal.setHorizontalHeaderItem(col, item)
##            self.tbl_Rep_Semanal.setColumnWidth(col, ancho[col])
##            head = self.tbl_Rep_Semanal.horizontalHeaderItem(col)
##            head.setText(_translate("MainWindow", headers[col], None))
##            col += 1
        
        # Dibuja la Tabla Reporte Semanal (fin)
        
    def closeEvent(self, event):
        print "Saliendo...."
        Borrar = list(set(Views_List))
        for View in Borrar:
            query = "DROP VIEW %s;" % View
            BD.interAct(query)
        BD.closeCon()

    def dateChanged(self): #pass
        global Calcular
        global FechaCal
        global Semana
        global Mes
        
        FechaCal = str(QDate.toString(self.dateEdit.date(), "yyyy/MM/dd"))
        Semana = QDate.longDayName(QDate.dayOfWeek(self.dateEdit.date()))
        Mes = str(QDate.toString(self.dateEdit.date(), "yyyy/MM/"))
        self.label.setText("Fecha:   " + Semana)
        self.txt_Nombre.clear()
        self.lbl_Total.clear()
        self.lbl_Consumos.clear()
        self.lbl_Rojo.clear()
        self.lbl_Verde.clear()
        self.statusbar.clear()

        if self.tab_Main.tabText(self.tab_Main.currentIndex()) == 'Registro':
            if self.tab_Registro.tabText(self.tab_Registro.currentIndex()) == 'Asistencia':
                View_Name = str(QDate.toString(self.dateEdit.date(), "MMMddyyyy"))
                self.tbl_Asistencia.clearContents()

                if FechaCal <= FechaHoy:
                    query = "CREATE VIEW IF NOT EXISTS %s AS SELECT \
                        Status, \
                        Nombre, \
                        Apellido, \
                        Proteina, \
                        Fibra, \
                        Batido, \
                        Te, \
                        Aloe, \
                        liftOff, \
                        PrePago, \
                        Total \
                        FROM asistencia a, socios s \
                        WHERE s.Id = a.IdSocio \
                        AND a.FechaCal='%s';" \
                        % (View_Name, FechaCal)
                    BD.interAct(query)
                    self.txt_Nombre.setEnabled(True)
                    self.tbl_Asistencia.setEnabled(True)
                    query = "SELECT * FROM %s;" % View_Name
                    Registros = BD.interAct(query)
                    Calcular = False
                    row = 0
                    for Registro in Registros:
                        item = 0
                        fullName = str(Registro[1] + " " + Registro[2])
                        for col in range(self.tbl_Asistencia.columnCount()):
                            if col == 1:
                                self.tbl_Asistencia.setItem(row, col, QTableWidgetItem(fullName))
                                item += 2
                            else:
                                if str(Registro[item]) != "None":
                                    self.tbl_Asistencia.setItem(row, 
                                        col, QTableWidgetItem(str(Registro[item])))
                                item += 1
                        row += 1
                    Views_List.append(View_Name)
                    
                    query = "SELECT TVentas, TConsumos, Capital, Ganancia \
                                FROM reporte WHERE FechaCal='%s'" % FechaCal
                    Registros = BD.interAct(query)

                    for Reg in Registros:
                        self.lbl_Total.setText(str(Reg[0]))
                        self.lbl_Consumos.setText(str(Reg[1]))
                        self.lbl_Rojo.setText(str(Reg[2]))
                        self.lbl_Verde.setText(str(Reg[3]))
                        
                    self.frecuentes()
                    #self.CuentaConsumos(self.tbl_Asistencia.rowCount())
                    Calcular = True
                    
                if FechaCal > FechaHoy:
                    self.statusbar.showMessage("No se puede hacer Registros Posteriores a Hoy...")
                    self.txt_Nombre.setDisabled(True)
                    self.tbl_Asistencia.setDisabled(True)
        if self.tab_Main.tabText(self.tab_Main.currentIndex()) == 'Reportes':
            if self.tab_Reportes.tabText(self.tab_Reportes.currentIndex()) == 'Semanal':
                self.tbl_Rep_Semanal.clearContents()
                query = "SELECT \
                                sum(TVentas), \
                                sum(Capital), \
                                avg(TConsumos), \
                                sum(Ganancia) \
                                FROM reporte WHERE FechaCal >= '2015/09/14' and FechaCal < '2015/09/21';"
                print query
            if self.tab_Reportes.tabText(self.tab_Reportes.currentIndex()) == 'Mensual':
                numDia = int(QDate.toString(self.dateEdit.date(), "d")) - 1
                self.tbl_Rep_Mensual.clearContents()
                query = "SELECT \
                     Semana, \
                     Invitaciones, \
                     Entraron, \
                     NConsumos, \
                     Referidos, \
                     TConsumos, \
                     Ganancia \
                     FROM reporte WHERE FechaCal LIKE '%s%%' ORDER BY FechaCal;" % Mes
                Reporte = BD.interAct(query)
                #Reporte = _fromUtf8(Reporte)
                Calcular = False
                row = 0
                for linea in Reporte:
                    for col in range(self.tbl_Rep_Mensual.columnCount()):
                        if type(linea[col]) is int:
                            self.tbl_Rep_Mensual.setItem(row, col, QTableWidgetItem(str(linea[col])))
                        else:
                            self.tbl_Rep_Mensual.setItem(row, col, QTableWidgetItem(_fromUtf8(linea[col])))
                        #if 'lunes' in linea: self.tbl_Rep_Mensual.item(row, col).setBackground(QColor(100,150,100))
                        if row == numDia: self.tbl_Rep_Mensual.item(row, col).setBackground(QColor(100,150,100))
                    row += 1
                query = "SELECT sum(TVentas), sum(Ganancia), sum(Capital), \
                                sum(TConsumos), avg(TConsumos), avg(Entraron), avg(Invitaciones) \
                                FROM reporte WHERE FechaCal LIKE '" + Mes + "%';"
                Resultados = BD.interAct(query)
                for Resultado in Resultados:
                    self.lbl_Total.setText(str(Resultado[0]))
                    self.lbl_Verde.setText(str(Resultado[1]))
                    self.lbl_Rojo.setText(str(Resultado[2]))
                    self.lbl_Consumos.setText(str(Resultado[3]))
                    print "Rojo: $bs: %s - $us: %.2f  " % (Resultado[2], Resultado[2]/6.96)
                    print "Prom_Consumos/Mes: %.2f " % Resultado[4]
                    print "Prom_Presentaciones/Mes: %.2f" % Resultado[5]
                    print "Prom_Invitaciones/Mes: %.2f" % Resultado[6]
                Calcular = True
        
        
    def tbl_Asistencia_ColWith(self): pass

    def tbl_Asistencia_cellChanged(self,  row, col):
        sender = self.sender().objectName()
        if Calcular:
            if sender == 'tbl_Asistencia':
                #Verificamos que la celda "Nombre" existe y tiene texto
                NameExists = True if self.tbl_Asistencia.item(row, 
                        colNameIndex['Nombre']) and self.tbl_Asistencia.item(row, 
                        colNameIndex['Nombre']).text() != "" else False
                # si existe nombre ya debe registrarse en la bd,
                # si el cambio es de la lista de extras se hace el calculo de precios
                # y despues se registra en la bd.
                if NameExists:
                    colHeaderName = str(self.tbl_Asistencia.horizontalHeaderItem(col).text())
                    #Creamos un diccionario que despues cargamos con los pares 
                    #de nombre de columna y dato introducido.
                    Detalle = dict()
                    for cols in range(self.tbl_Asistencia.columnCount()):
                        item = str(self.tbl_Asistencia.item(row, 
                            cols).text()) if self.tbl_Asistencia.item(row, 
                            cols) and self.tbl_Asistencia.item(row, 
                            cols).text() != "" else 0
                        Detalle[str(self.tbl_Asistencia.horizontalHeaderItem(cols).text())] = item
                    #Capturamos el texto de la celda modificada
                    item = str(self.tbl_Asistencia.item(row, 
                            col).text()) if self.tbl_Asistencia.item(row, 
                            col) and self.tbl_Asistencia.item(row, 
                            col).text() != "" else 'NULL'
                    
                    if colHeaderName in Extras:
                        total_extras = sum(Extras[Extra] * int(Detalle[Extra]) for Extra in Extras) 
                        total = Nutricion + total_extras
                        query = "UPDATE asistencia \
                            SET %s=%s, Total=%s \
                            WHERE Fila=%s \
                            AND FechaCal='%s';" \
                            % (colHeaderName, item, total, row, FechaCal)
                        BD.interAct(query)
                        self.tbl_Asistencia.setItem(row, colNameIndex['Total'], 
                            QTableWidgetItem(str(total)))

                    if colHeaderName == 'Total':
                        query = "UPDATE asistencia \
                            SET %s=%s \
                            WHERE Fila=%s \
                            AND FechaCal='%s';" \
                            % (colHeaderName, item, row, FechaCal)
                        BD.interAct(query)

                    if colHeaderName == 'Status':
                        item = item.upper() if item != "NULL" else ""
                        print item
                        query = "UPDATE asistencia \
                            SET %s='%s' \
                            WHERE Fila=%s \
                            AND FechaCal='%s';" \
                            % (colHeaderName, item, row, FechaCal)
                        BD.interAct(query)
                    self.CuentaConsumos()
                    
                else: 
                    for i in range(self.tbl_Asistencia.columnCount()):
                        self.tbl_Asistencia.takeItem(row, col)
            if sender == 'tbl_Rep_Mensual':
                headers = ['Invitaciones', 'Entraron']
                colHeaderName = str(self.sender().horizontalHeaderItem(col).text())
                #print 'El Nombre de la columna es: %s' % colHeaderName
                #num = self.sender().columnCount()
                #print 'Numero de Columnas: %s' % num
                day = Mes + str(row + 1).zfill(2)
                #print 'La fila es: %s' % day
                item = str(self.sender().item(row, 
                            col).text()) if self.sender().item(row, 
                            col) and self.sender().item(row, 
                            col).text() != "" else 0
                query = "UPDATE reporte \
                            SET %s=%s \
                            WHERE FechaCal='%s';" \
                            % (colHeaderName, item, day)
                print query
                InterAc(query)

    def tbl_Asistencia_dblClicked(self):
        if self.tbl_Asistencia.horizontalHeaderItem(
            self.tbl_Asistencia.currentColumn()).text() == 'Nombre':
            Row = self.tbl_Asistencia.currentRow()
            for col in range(self.tbl_Asistencia.columnCount()):
                self.tbl_Asistencia.takeItem(Row, col)
            query = "DELETE FROM asistencia \
                WHERE Fila='%s' \
                AND FechaCal='%s';" \
                % (Row, FechaCal)
            BD.interAct(query)
            self.CuentaConsumos()
            
    def sendSMS(self): pass
        #sm = gammu.StateMachine()
        #sm.ReadConfig()
        #sm.Init()
        
    def Fecha(self):
        return str(QDate.toString(self.dateEdit.date(), "yyyy/MM/dd"))

    def lst_Registrado_dblClicked(self): pass

    def myprint(self): #pass
    # funcion que llena la tabla de reporte mes a mes
        
        query = "SELECT * FROM reporte WHERE FechaCal = '%s'" % FechaCal
        consulta = BD.interAct(query)
        if not consulta:
            x = 1
            while QDate.isValid(QDate.year(self.dateEdit.date()), QDate.month(self.dateEdit.date()), x):
                Fecha = "%s/%s/%s" % (QDate.year(self.dateEdit.date()), 
                    QDate.toString(self.dateEdit.date(), "MM"),
                    str(x).zfill(2))
                formatFecha = Fecha.replace('/', '')
                Sem = QDate.longDayName(QDate.dayOfWeek(QDate.fromString(formatFecha, "yyyyMMdd")))
                query = "INSERT INTO reporte (FechaCal, Semana) VALUES ('%s', '%s')" % (Fecha, Sem)
                BD.interAct(query)
                x += 1

##al escribir en txt_nombre
    def txt_Nombre_textChanged(self):

        self.lst_Encontrado.clear()
        if self.txt_Nombre.text():
            if self.tab_Registro.tabText(self.tab_Registro.currentIndex()) == 'Asistencia':
                query = "SELECT \
                    Id, \
                    Nombre, \
                    Apellido \
                    FROM Socios \
                    WHERE Nombre \
                    LIKE '%s%%'" % self.txt_Nombre.text()
                rows = BD.interAct(query)
                self.fillNamesList(rows)
        else:
            self.frecuentes()
        

    def frecuentes(self):
        View_Name = "frecuentes"
        query = "CREATE VIEW IF NOT EXISTS %s AS SELECT \
            IdSocio, \
            Nombre, \
            Apellido, \
            FROM asistencia a, socios s \
            WHERE s.Id = a.IdSocio \
            GROUP BY IdSocio ORDER BY count(IdSocio) DESC;" \
            % View_Name
        query = "SELECT * FROM %s;" % View_Name
        rows = BD.interAct(query)
        self.fillNamesList(rows)

    def fillNamesList(self, rows):
        for row in rows:
            Resultado = "%s %s %s" % (row[0], row[1], row[2])
            self.lst_Encontrado.addItem(Resultado)
                    
            if self.tab_Registro.tabText(self.tab_Registro.currentIndex()) == 'Producto Cerrado':
                print self.tab_Registro.currentTabName()

    def lst_Encontrado_Clicked(self, item):
        global Calcular
        Calcular = False

        if self.tab_Registro.tabText(self.tab_Registro.currentIndex()) == 'Asistencia':
            #FechaCal = str(QDate.toString(self.dateEdit.date(), "yyyy/MM/dd"))
            Selected = str(self.lst_Encontrado.currentItem().text())
            Nombre =  QTableWidgetItem(Selected[Selected.find(' '):])
            IdSocio = Selected[:Selected.find(' ')]
            Row = 0
            for Row in range(self.tbl_Asistencia.rowCount()):
                if not self.tbl_Asistencia.item(Row, 
                        colNameIndex['Nombre']) or self.tbl_Asistencia.item(Row, 
                        colNameIndex['Nombre']).text() == "":
                    #insertar en la tabla asistencia el No de Row y el id del socio
                    self.tbl_Asistencia.setItem(Row, 
                        colNameIndex['Nombre'], Nombre)
                    break
            Calcular = True
            self.tbl_Asistencia.setItem(Row, 
                colNameIndex['Total'], 
                QTableWidgetItem(str(Nutricion)))
            query = "INSERT INTO asistencia (\
                FechaCal, \
                UpdatedOn, \
                Fila, \
                IdSocio, \
                Total) VALUES ('%s','%s','%s','%s', %s);" \
                % (FechaCal, FechaHoy, Row, IdSocio, int(Nutricion))
            
            BD.interAct(query)
            

        if self.tab_Registro.tabText(self.tab_Registro.currentIndex()) == 'Producto Cerrado': 
            pass

    # crea un diccionario con los pares de titulo de columna y el valor de la celda
    def Diccionario(self):
        #colecta los nombres de columna de la tabla asistencia
        # con sus respectivos numeros de columnas
        print "Diccionario"
        for col in range(self.tbl_Asistencia.columnCount()):
            colHeaderName = self.tbl_Asistencia.horizontalHeaderItem(col).text()
            colNameIndex[str(colHeaderName)] = col
            print colNameIndex[str(colHeaderName)], col
        
    def CuentaConsumos(self):
        Consumos, total_ventas = 0, 0
        while self.tbl_Asistencia.item(Consumos, int(colNameIndex['Nombre'])) \
        and self.tbl_Asistencia.item(Consumos, int(colNameIndex['Nombre'])).text() != "":
            total_ventas = total_ventas + int(self.tbl_Asistencia.item(Consumos, int(colNameIndex['Total'])).text())
            Consumos +=1
        print "total de ventas: %s" % total_ventas
        sobre_verde = total_ventas / 3
        sobre_rojo = total_ventas - sobre_verde
        self.lbl_Consumos.setText(str(Consumos))
        self.lbl_Total.setText(str(total_ventas))
        self.lbl_Verde.setText(str(sobre_verde))
        self.lbl_Rojo.setText(str(sobre_rojo))
        Id = "SELECT Id FROM reporte WHERE FechaCal='" + FechaCal + "'"
        Invitaciones = "SELECT Invitaciones FROM reporte WHERE FechaCal='" + FechaCal + "'"
        Entraron = "SELECT Entraron FROM reporte WHERE FechaCal='" + FechaCal + "'"
        NConsumos = "SELECT count() FROM asistencia WHERE FechaCal='%s' AND Status='N'" % FechaCal
        Referidos = "SELECT count() FROM asistencia WHERE FechaCal='%s' AND Status='R'" % FechaCal
        query = "INSERT OR REPLACE INTO reporte \
                (Id, Invitaciones, Entraron, NConsumos, Referidos, \
                FechaCal, Semana, TConsumos, Ganancia, TVentas, Capital) \
                VALUES ((%s),(%s),(%s),(%s),(%s),\
                '%s','%s', '%s','%s','%s','%s')" \
                % (Id, Invitaciones, Entraron, NConsumos, Referidos, \
                FechaCal, Semana, Consumos, sobre_verde, total_ventas, sobre_rojo)
        BD.interAct(query)

    def lst_Encontrado_dblClick(self): pass
        ## al hacer doble click en la lista
        #self.tbl_Asistencia.setItem(item.row(), item.column(), item)
        #self.lst_Registrado.addItems(self.lst_wEncontrado.text())
        #Row = item.row()
        #tabName = self.tab_Registro.tabText(self.tab_Registro.currentIndex())
    def mousePressEvent(self, event):
        #super(dateEdit, self).mousePressEvent(event)
        print "Mes: %s" % Mes
        
    def AbrirCal(self):
        cal = pyDate(self)
        cal.exec_()
        
    def AddEditBD(self):
        self.txt_Nombre.clear()
        wid = AddSocio(self)
        wid.exec_()
        
    # partes del formulario
    def setCalWidget(self): #pass
        self.splitter_5 = QSplitter(self.centralwidget)
        self.splitter_5.setGeometry(QRect(55, 30, 131, 51))
        self.splitter_5.setOrientation(Qt.Vertical)
        self.splitter_5.setObjectName(_fromUtf8("splitter_5"))
        self.label = QLabel(self.splitter_5)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.dateEdit = PyDateEdit(self.splitter_5)
        self.dateEdit.setFont(font)
        self.dateEdit.setCursor(QCursor(Qt.ArrowCursor))
        #######
        #self.Rotacion = RotatedHeaderView(self.tbl_Asistencia)

Buscar = True

class AddSocio(QDialog, AgregarSocio.Ui_Form):
    def __init__(self, parent=None):
        super(AddSocio, self).__init__(parent)
        self.setupUi(self)
        self.connectActions()
        #self.show()
        
    def connectActions(self):
        self.txt_AddName.textChanged.connect(self.txt_textChanged)
        self.txt_AddLName.textChanged.connect(self.txt_textChanged)
        self.txt_AddCel1.textChanged.connect(self.txt_textChanged)
        self.btn_Guardar.clicked.connect(self.btn_Guardar_Clicked)
        self.lst_Socios.clicked.connect(self.lst_Socios_Clicked)
        
    def txt_textChanged(self):
        sender = self.sender().objectName()
        criterio = self.sender().text()
        #print criterio
        if Buscar:
            if sender == "txt_AddName": condicion = "Nombre"
            if sender == "txt_AddLName": condicion = "Apellido"
            if sender == "txt_AddCel1": condicion = "Cel1"
            self.lst_Socios.clear()
            state = False if self.txt_AddName.text() == '' \
                or self.txt_AddLName.text() == '' else True
            self.btn_Guardar.setEnabled(state)
            if criterio:
                rows = InterActBD(str(
                    "SELECT Id, Nombre, Apellido \
                    FROM Socios \
                    WHERE " + condicion + " LIKE '" + criterio + "%'"))
                for row in rows:
                    Resultado = "%s %s %s" % (row[0], row[1], row[2])
                    self.lst_Socios.addItem(Resultado)

    def lst_Socios_Clicked(self):
        global Buscar
        IdSocio = str(self.lst_Socios.currentItem().text())
        Id = IdSocio[:IdSocio.find(' ')]
        rows = InterActBD(str("SELECT * FROM Socios WHERE Id ='" + IdSocio[:IdSocio.find(' ')] + "'"))
        #print Id
        Buscar = False
        for row in rows:
            self.txt_AddName.setText(row[1])
            self.txt_AddLName.setText(row[2])
            self.txt_AddCel1.setText(row[3])
        Buscar = True

    def btn_Guardar_Clicked(self):
        nombre = self.txt_AddName.text().toUpper()
        apellido = self.txt_AddLName.text().toUpper()
        celular = str(self.txt_AddCel1.text())
        mail = str(self.txt_AddCel2.text())
        query = "INSERT INTO Socios (\
            Nombre, \
            Apellido, \
            Cel1, \
            Cumple,\
            InsertedOn) \
            VALUES ('%s','%s','%s','%s', '%s');" % \
            (nombre, apellido, celular, mail, FechaHoy)
#            (str(nombre.upper()), str(apellido.upper()), str(celular.upper()), str(mail.upper()), FechaHoy)
        InterActBD(str(query))
        self.btn_Limpiar.click()
        
        
class RotatedHeaderView( QHeaderView ):
    def __init__(self, orientation, parent=None ):
        super(RotatedHeaderView, self).__init__(orientation, parent)
        self.setMinimumSectionSize(20)

    def paintSection(self, painter, rect, logicalIndex ):
        painter.save()
        # translate the painter such that rotate will rotate around the correct point
        painter.translate(rect.x()+rect.width(), rect.y())
        painter.rotate(90)
        # and have parent code paint at this location
        newrect = QtCore.QRect(0,0,rect.height(),rect.width())
        super(RotatedHeaderView, self).paintSection(painter, newrect, logicalIndex)
        painter.restore()

    def minimumSizeHint(self):
        size = super(RotatedHeaderView, self).minimumSizeHint()
        size.transpose()
        return size

    def sectionSizeFromContents(self, logicalIndex):
        size = super(RotatedHeaderView, self).sectionSizeFromContents(logicalIndex)
        size.transpose()
        return size
        

class pyDate(QDialog, calWidget.Ui_Calendario):
    def __init__(self, parent=None):
        super(pyDate, self).__init__(parent)
        self.setupUi(self)
        self.setDefaults()
        self.connectActions()


    def connectActions(self):
#        self.cbo_dayOfWeek.changeEvent.connect(self.firstDayChanged)
        self.cbo_dayOfWeek.activated.connect(self.firstDayChanged)
        self.btn_Continuar.clicked.connect(self.Continuar)
        self.calWidget.clicked.connect(self.myPrint)
        #self.cbo_dayOfWeek.currentIndex.connect(self.firstDayChanged)

        
    def setDefaults(self):
        self.cbo_dayOfWeek.addItem("Domingo", Qt.Sunday)
        self.cbo_dayOfWeek.addItem("Lunes", Qt.Monday)
        self.cbo_dayOfWeek.addItem("Martes", Qt.Tuesday)
        self.cbo_dayOfWeek.addItem("Miercoles", Qt.Wednesday)
        self.cbo_dayOfWeek.addItem("Jueves", Qt.Thursday)
        self.cbo_dayOfWeek.addItem("Viernes", Qt.Friday)
        self.cbo_dayOfWeek.addItem("Sabado", Qt.Saturday)

        
    def firstDayChanged(self, index):
        #print Qt.DayOfWeek(index)
        print QDate.dayOfWeek(index)
        self.lbl_Titulo.setText(QDate.longDayName(index))
        self.calWidget.setFirstDayOfWeek(Qt.DayOfWeek(index))
        
    def Continuar(self):
        #print "boton continuar"
        printText = MainForm()
        printText.color = "amarillo"
        printText.myprint()
        #printText.label.setText("Hola:")
        self.close()
        
    def myPrint(self, selDate):
        dia = QDate.dayOfWeek(selDate)
        self.lbl_Titulo.setText(QDate.longDayName(dia))
        #FechaCal1 = str(QDate.toString(selDate, "MMM d yyyy"))
        #print "Ha cambiado la fecha %s" % FechaCal1

class PyDateEdit(QDateEdit):
    #
    # Initialize base class
    # Force use of the calendar popup
    # Set default values for calendar properties
    #
    def __init__(self, parent=None):
        super(PyDateEdit, self).__init__(parent)

        # Main values for initials settings
#        font = QFont()
#        font.setFamily(_fromUtf8("Ubuntu Condensed"))
        self.setFont(font)
        self.setCalendarPopup(True)
        self.setDate(QDate.currentDate())
        self.setDisplayFormat('d/MMMM/yyyy')
        self.setObjectName(_fromUtf8("dateEdit"))
        #self.dateChanged.connect(self.dateChange)
        #
        self.__cw = None
        self.__currentDate = QDate.currentDate()
        self.__firstDayOfWeek = Qt.Monday
        self.__gridVisible = True
        self.__horizontalHeaderFormat = QCalendarWidget.ShortDayNames
        self.__verticalHeaderFormat = QCalendarWidget.ISOWeekNumbers
        self.__navigationBarVisible = True

    def dateChange(self):
        FechaCal = str(QDate.toString(self.date(), "yyyy/MM/dd"))
        self.tbl_Asistencia.clearContents()
        if FechaCal <= FechaHoy:
            print FechaCal

    #
    # Call event handler of base class
    # Get the calendar widget, if not already done
    # Set the calendar properties
    #
    def mousePressEvent(self, event):
        super(PyDateEdit, self).mousePressEvent(event)

        if not self.__cw:
            self.__cw = self.findChild(QCalendarWidget)
            if self.__cw:
                self.__cw.setFirstDayOfWeek(self.__firstDayOfWeek)
                self.__cw.setGridVisible(self.__gridVisible)
                self.__cw.setHorizontalHeaderFormat(self.__horizontalHeaderFormat)
                self.__cw.setVerticalHeaderFormat(self.__verticalHeaderFormat)
                self.__cw.setNavigationBarVisible(self.__navigationBarVisible)
                #self.__cw.setSelectedDate(self.__currentDate)

    #
    # Make sure, the calendarPopup property is invisible in Designer
    #
    def getCalendarPopup(self):
        return True
    calendarPopup = pyqtProperty(bool, fget=getCalendarPopup)
    
    def getCurrentDate(self):
        return self.__currentDate
    currentDate = pyqtProperty(bool, fget=getCurrentDate)
    #
    # Property firstDayOfWeek: Qt::DayOfWeek
    # Get: getFirstDayOfWeek()
    # Set: setFirstDayOfWeek()
    # Reset: resetFirstDayOfWeek()
    #
    def getFirstDayOfWeek(self):
        return self.__firstDayOfWeek
    def setFirstDayOfWeek(self, dayOfWeek):
        if dayOfWeek != self.__firstDayOfWeek:
            self.__firstDayOfWeek = dayOfWeek
            if self.__cw:
                self.__cw.setFirstDayOfWeek(dayOfWeek)
    def resetFirstDayOfWeek(self):
        if self.__firstDayOfWeek != Qt.Monday:
            self.__firstDayOfWeek = Qt.Monday
            if self.__cw:
                self.__cw.setFirstDayOfWeek(Qt.Monday)
    firstDayOfWeek = pyqtProperty(Qt.DayOfWeek,
                                         fget=getFirstDayOfWeek,
                                         fset=setFirstDayOfWeek,
                                         freset=resetFirstDayOfWeek)
  
    #
    # Property gridVisible: bool
    # Get: isGridVisible()
    # Set: setGridVisible()
    # Reset: resetGridVisible()
    #
    def isGridVisible(self):
        return self.__gridVisible
    def setGridVisible(self, show):
        if show != self.__gridVisible:
            self.__gridVisible = show
            if self.__cw:
                self.__cw.setGridVisible(show)
    def resetGridVisible(self):
        if self.__gridVisible != False:
            self.__gridVisible = False
            if self.__cw:
                self.__cw.setGridVisible(False)
    gridVisible = pyqtProperty(bool,
                                      fget=isGridVisible,
                                      fset=setGridVisible,
                                      freset=resetGridVisible)
  
    #
    # Property horizontalHeaderFormat: QCalendarWidget::HorizontalHeaderFormat
    # Get: getHorizontalHeaderFormat()
    # Set: setHorizontalHeaderFormat()
    # Reset: resetHorizontalHeaderFormat()
    #
    def getHorizontalHeaderFormat(self):
        return self.__horizontalHeaderFormat
    def setHorizontalHeaderFormat(self, format):
        if format != self.__horizontalHeaderFormat:
            self.__horizontalHeaderFormat = format
            if self.__cw:
                self.__cw.setHorizontalHeaderFormat(format)
    def resetHorizontalHeaderFormat(self):
        if self.__horizontalHeaderFormat != QCalendarWidget.ShortDayNames:
            self.__horizontalHeaderFormat = QCalendarWidget.ShortDayNames
            if self.__cw:
                self.__cw.setHorizontalHeaderFormat(QCalendarWidget.ShortDayNames)
    horizontalHeaderFormat = pyqtProperty(QCalendarWidget.HorizontalHeaderFormat,
                                                 fget=getHorizontalHeaderFormat,
                                                 fset=setHorizontalHeaderFormat,
                                                 freset=resetHorizontalHeaderFormat)
  
    #
    # Property verticalHeaderFormat: QCalendarWidget::VerticalHeaderFormat
    # Get: getVerticalHeaderFormat()
    # Set: setVerticalHeaderFormat()
    # Reset: resetVerticalHeaderFormat()
    #
    def getVerticalHeaderFormat(self):
        return self.__verticalHeaderFormat
    def setVerticalHeaderFormat(self, format):
        if format != self.__verticalHeaderFormat:
            self.__verticalHeaderFormat = format
            if self.__cw:
                self.__cw.setVerticalHeaderFormat(format)
    def resetVerticalHeaderFormat(self):
        if self.__verticalHeaderFormat != QCalendarWidget.ISOWeekNumbers:
            self.__verticalHeaderFormat = QCalendarWidget.ISOWeekNumbers
            if self.__cw:
                self.__cw.setVerticalHeaderFormat(QCalendarWidget.ISOWeekNumbers)
    verticalHeaderFormat = pyqtProperty(QCalendarWidget.VerticalHeaderFormat,
                                               fget=getVerticalHeaderFormat,
                                               fset=setVerticalHeaderFormat,
                                               freset=resetVerticalHeaderFormat)
  
    #
    # Property navigationBarVisible: bool
    # Get: isNavigationBarVisible()
    # Set: setNavigationBarVisible()
    # Reset: resetNavigationBarVisible()
    #
    def isNavigationBarVisible(self):
        return self.__navigationBarVisible
    def setNavigationBarVisible(self, visible):
        if visible != self.__navigationBarVisible:
            self.__navigationBarVisible = visible
            if self.__cw:
                self.__cw.setNavigationBarVisible(visble)
    def resetNavigationBarVisible(self):
        if self.__navigationBarVisible != True:
            self.__navigationBarVisible = True
            if self.__cw:
                self.__cw.setNavigationBarVisible(True)
    navigationBarVisible = pyqtProperty(bool,
                                               fget=isNavigationBarVisible,
                                               fset=setNavigationBarVisible,
                                               freset=resetNavigationBarVisible)

class dataBase():
## Clase que interactua con la base de datos

    def createCon(self):
        global con
        con = lite.connect('ClubMarsellosa.db')
    def interAct(self, query):
        with con:
            cur = con.cursor()
            cur.execute(query)
            rows = cur.fetchall()
        return rows
        
    def closeCon(self):
        if con: 
            con.close()

    def crearTablas(self): pass
        #codigo para crear o formatear tablas en la bd
        
    def fillTables(self): pass
        
    
def InterActBD(query):
    con = lite.connect('ClubMarsellosa.db')
    with con:
        cur = con.cursor()
        cur.execute(query)
        rows = cur.fetchall()
    if con:
        con.close()
    return rows


BDColNames = list()
rows = InterActBD("PRAGMA table_info(asistencia);")
for row in rows:
    BDColNames.append(str(row[1]))
#print BDColNames


app = QApplication(sys.argv)
ui = MainForm()
ui.main()
app.exec_()

