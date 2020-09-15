#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: 850 -*-
import os
import sys
import gammu  # modulo para enviar mensajes

from PyQt4.QtGui import *
from PyQt4.QtCore import *

import MyWindow, DB_Class, pyDate, comandacode
from rotated import RotatedHeaderView
# from ExtendedComboBox import ExtendedComboBox
# from qtableview_completion import ItemTableModel
# import serial

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
# Nutricion, total_extras = 18, 0
# Extras = {'Proteina': 7, 'Fibra': 9, 'Batido': 10, 'Aloe': 5, 'Te': 5, 'LiftOff':20 }
Nutricion, total_extras = 22, 0
Extras = {'Proteina': 9, 'Fibra': 10, 'Batido': 12, 'Aloe': 6, 'Te': 6, 'LiftOff': 20}
FechaCal = None  # fecha escogida en el calendario
Semana = None  # nombre del dia de la semana
Mes = None  #
Hoy = None  # dia en el que empieza tu semana de trabajo
appName = "ENGARGOLADO Estamos Probando"
Views_List = list()
colNameIndex = dict()
Fechas_List = list()
query_Dict = dict()
font = QFont()
font.setFamily(_fromUtf8("Ubuntu Condensed"))
font.setPointSize(12)
# path = (sys.argv[1] if len(sys.argv) > 1 and
#                    QFile.exists(sys.argv[1]) else os.getcwd())
path = os.getcwd()
print path
Calcular = True  # boolean que me permite cargar la tabla de asistencia tal cual esta en la BD


## --------------------

class MainForm(QMainWindow, MyWindow.Ui_MainWindow):
    def __init__(self, parent=None):
        # initialize parent class
        super(MainForm, self).__init__(None)
        self.setupUi(self)
        self.varIniciales()
        self.setCalWidget()
        self.connectActions()
        self.dibujarTablas()
        self.Diccionario()
        self.dateChanged()
        self.myprint()

    def main(self):
        self.show()

    # --------------CONECTANDO EVENTOS CON MIS FUNCIONES----------------
    def connectActions(self):

        self.btn_Agregar.clicked.connect(self.AddEditBD)
        self.txt_Nombre.textChanged.connect(self.txt_Nombre_textChanged)
        # self.lst_Encontrado.doubleClicked.connect(self.lst_Encontrado_dblClick)
        # self.lst_Encontrado.clicked.connect(self.lst_Encontrado_Clicked)
        # self.btnLlamar.clicked.connect(self.handle_PhonesEvents)
        self.btnSMS.clicked.connect(self.handle_PhonesEvents)
        self.tab_Main.currentChanged.connect(self.dateChanged)
        self.tab_Registro.currentChanged.connect(self.dateChanged)
        self.tab_Reportes.currentChanged.connect(self.dateChanged)
        self.treeEncontrado.clicked.connect(self.treeEncontrado_handleClicked)
        # self.lst_Registrado.doubleClicked.connect(self.lst_Registrado_dblClicked)
        self.dateEdit.dateChanged.connect(self.dateChanged)
        self.tbl_Asistencia.doubleClicked.connect(self.tbl_Asistencia_dblClicked)
        self.tbl_Asistencia.cellChanged.connect(self.tbl_Asistencia_cellChanged)
        # self.tbl_Rep_Mensual.cellChanged.connect(self.tbl_Rep_Mensual_cellChanged)
        self.tbl_Rep_Mensual.cellChanged.connect(self.tbl_Asistencia_cellChanged)
        # self.tbl_Asistencia.keyPressEvent.connect(self.myprint)
        # self.tbl_Asistencia.itemChanged.connect(self.myprint)
        # self.txt_Nombre.completer.connect(self.on_completer_activated)
        # self.txt_Nombre.connect.completer(self.on_completer_activated)
        self.cboEncontrado.activated.connect(self.on_completer_activated)
        # self.cboEncontrado.lineEdit().textEdited[unicode].connect(self.cboEncontrado.pFilterModel.setFilterFixedString)

    ###------------MIS FUNCIONES --------------------------------------

    def varIniciales(self):
        global BD
        global sm
        global model
        global idnombre

        idnombre = dict()

        BD = DB_Class.dataBase()
        BD.createCon()
        query = "CREATE TRIGGER IF NOT EXISTS aft_update_asistencia AFTER UPDATE OF Total ON asistencia " \
                "BEGIN " \
                    "UPDATE reporte_mensual SET TVentas=sum(asistencia.Total)" \
                    "WHERE FechaCal=OLD.FechaCal" \
                "END;"
        # print query
        try:
            sm = gammu.StateMachine()
            # lee el archivo de configuracion
            sm.ReadConfig(Filename='.gammurc')
            sm.Init()
        except:
            error = sys.exc_info()[1]
            self.statusbar.showMessage("Hubo un Error: %s" % error)

        # self.cboCriterioBusqueda = ExtendedComboBox(self.splitter_3)
        # self.tvlRegistroAsistencia.setModel(ItemTableModel(self.tvlRegistroAsistencia))
        # self.tbl_Asistencia.setHorizontalHeader(RotatedHeaderView(self.tbl_Asistencia))
        self.treeEncontrado.setHeaderHidden(True)
        model = QStringListModel()

        completer = QCompleter()
        completer.setModel(model)
        completer.setCaseSensitivity(Qt.CaseInsensitive)

        self.txt_Nombre.setCompleter(completer)

        # self.cboCriterioBusqueda.addItem("SKU")
        # self.cboCriterioBusqueda.addItem("Numero de Serie")
        # self.cboCriterioBusqueda.addItem("Descripcion")
        # self.cboCriterioBusqueda.addItem("Nombre Corto")
        self.setWindowTitle(QApplication.translate("MainWindow", appName, None, QApplication.UnicodeUTF8))

        # scroll area widget contents - layout
        self.scrollLayout = QFormLayout()

        # scroll area widget contents
        self.scrollWidget = QWidget()
        self.scrollWidget.setLayout(self.scrollLayout)

        # scroll area
        self.scrollPhonesArea.setWidget(self.scrollWidget)

    def dibujarTablas(self):
        # Inicio del codigo que dibuja la tabla Asistencia
        headers = ['Status', 'Nombre', 'Proteina', 'Fibra', 'Batido', 'Te', 'Aloe', 'LiftOff', 'PrePago', 'Total']
        ancho = [30, 150, 30, 30, 30, 30, 30, 30, 30, 60]
        #        rotation = RotatedHeaderView()
        self.tbl_Asistencia.setHorizontalHeader(RotatedHeaderView(self.tbl_Asistencia))
        self.tbl_Asistencia.setRowCount(51)
        self.tbl_Asistencia.setColumnCount(len(headers))
        col = 0
        for colname in headers:
            item = QTableWidgetItem()
            self.tbl_Asistencia.setHorizontalHeaderItem(col, item)
            self.tbl_Asistencia.setColumnWidth(col, ancho[col])
            head = self.tbl_Asistencia.horizontalHeaderItem(col)
            head.setText(_translate("MainWindow", colname, None))

            # stylesheet = "QHeaderView::section{Background-color:rgb(100,100,100);border-radius:14px;}"
            # stylesheet = RotatedHeaderView()
            # self.tbl_Asistencia.horizontalHeader().setStyleSheet(stylesheet)
            col += 1
        # Fin del codigo que dibuja la tabla Asistencia

        # Inicio del codigo que dibuja la tabla Rep_Mensual
        headers = ['Semana', 'Invitaciones', 'Entraron', 'NConsumos', 'Referidos', 'TConsumos', 'Ganancia']
        ancho = [70, 30, 30, 30, 30, 30, 30]
        self.tbl_Rep_Mensual.setHorizontalHeader(RotatedHeaderView(self.tbl_Rep_Mensual))
        self.tbl_Rep_Mensual.setRowCount(31)
        self.tbl_Rep_Mensual.setColumnCount(len(headers))
        col = 0
        for head in headers:
            item = QTableWidgetItem()
            self.tbl_Rep_Mensual.setHorizontalHeaderItem(col, item)
            self.tbl_Rep_Mensual.setColumnWidth(col, ancho[col])
            head = self.tbl_Rep_Mensual.horizontalHeaderItem(col)
            head.setText(_translate("MainWindow", headers[col], None))
            col += 1
        # Fin del codigo que dibuja la tabla Rep_Mensual

        # Dibuja la Tabla Producto Cerrado (inicio)
        headers = ['SKU', 'Descripcion', 'Cantidad', 'Sobre Rojo', 'Sobre Verde']
        ancho = [40, 250, 80, 80, 80]
        self.tbl_prodCerrado.setRowCount(15)
        self.tbl_prodCerrado.setColumnCount(len(headers))
        col = 0
        for head in headers:
            item = QTableWidgetItem()
            self.tbl_prodCerrado.setHorizontalHeaderItem(col, item)
            self.tbl_prodCerrado.setColumnWidth(col, ancho[col])
            head = self.tbl_prodCerrado.horizontalHeaderItem(col)
            head.setText(_translate("MainWindow", headers[col], None))
            col += 1
        # Dibuja la Tabla Producto Cerrado (fin)
        # Dibuja la Tabla Reporte Semanal (inicio)
        # headers = ['Desde - Hasta', 'Promedio', 'Ganancia', 'Proyectado']
        # ancho = [170, 80, 80, 80]
        #        self.tbl_Rep_Semanal = RotatedHeaderView()
        #        self.tbl_Rep_Semanal.setGeometry(QtCore.QRect(10, 10, 671, 391))
        #        self.tbl_Rep_Semanal.setObjectName(_fromUtf8("tbl_Rep_Semanal"))
        #        self.tbl_Rep_Semanal.paintEvent().RotatedHeaderView()
        self.tbl_Rep_Semanal.setRowCount(15)
        # self.tbl_Rep_Semanal.setColumnCount(len(headers))
        self.tbl_Rep_Semanal.setColumnCount(4)
        # col = 0
        # for head in headers:
        #     item = QTableWidgetItem()
        #     self.tbl_Rep_Semanal.setHorizontalHeaderItem(col, item)
        #     self.tbl_Rep_Semanal.setColumnWidth(col, ancho[col])
        #     head = self.tbl_Rep_Semanal.horizontalHeaderItem(col)
        #     head.setText(_translate("MainWindow", headers[col], None))
        #     col += 1
        self.tbl_Rep_Semanal.setHorizontalHeaderLabels(QString("Desde - Hasta;Promedio;Ganancia;Proyectado").split(";"))
        texto_1 = QLineEdit()
        texto_2 = QLineEdit()
        self.tbl_Rep_Semanal.setCellWidget(0,1, texto_1)
        self.tbl_Rep_Semanal.setCellWidget(1,1, texto_2)

        # for fila in range(self.tbl_Rep_Semanal.rowCount()):
        #
        #     self.tbl_Rep_Semanal.setItem()
        # self.tbl_Rep_Semanal.setColumnWidth(70,80)
            # Dibuja la Tabla Reporte Semanal (fin)


        # headers = ['Mario Llosa', 'Marcelo Llosa', 'Paola Perez', 'Paola Llosa']
        #
        # for head in headers:
        #     self.cboCriterioBusqueda.addItem(head)
    # on selection of an item from the completer, select the corresponding item from combobox
    def on_completer_activated(self, received):

        if type(received) != int:
            selected = str(received)
            # index = self.findText(received)
            # self.setCurrentIndex(index)
            # print "Es el texto: %s & index: %s" % (self.itemText(index), index)
            # print "Es el texto como viene: %s" % received
            # return received
        else:
            # print "Es el texto extraido del numero enviado: %s " % self.cboCriterioBusqueda.itemText(received)
            # return self.itemText(received)
            selected = str(self.cboEncontrado.itemText(received))
        Nombre = selected[:selected.rfind(' ')]
        IdSocio = selected[selected.rfind(' '):]
        print "Nombre: %s; IdSocio: %s" % (Nombre, IdSocio)

        if self.tab_Registro.tabText(self.tab_Registro.currentIndex()) == 'Asistencia':
            for Row in range(self.tbl_Asistencia.rowCount()):
                if not self.tbl_Asistencia.item(Row,
                        colNameIndex['Nombre']) or self.tbl_Asistencia.item(Row,
                        colNameIndex['Nombre']).text() == "":
                    # insertar en la tabla asistencia el No de Row y el id del socio
                    self.tbl_Asistencia.setItem(Row,colNameIndex['Nombre'], QTableWidgetItem(Nombre))
                    break
            Calcular = True
            self.tbl_Asistencia.setItem(Row,
                        colNameIndex['Total'],
                        QTableWidgetItem(str(Nutricion)))
            query = "INSERT INTO registro_asistencia (\
                FechaCal, \
                UpdatedOn, \
                Fila, \
                IdSocio, \
                Total) VALUES ('%s','%s','%s','%s', %s);" \
                    % (FechaCal, FechaHoy, Row, IdSocio, int(Nutricion))
            BD.interAct(query)

    def verifyitem(self, row, col):
        item = self.tbl_Asistencia.item(row, col)
        if item is not None and item.text() != "":
            existe = True
        else:
            existe = False

        return existe

    def mousePressEvent(self, event):
        print event.type()

    def closeEvent(self, event):
        print "Saliendo...."
        # self.crear_archivo()
        Borrar = list(set(Views_List))
        for View in Borrar:
            query = "DROP VIEW %s;" % View
            BD.interAct(query)
        BD.closeCon()

    def dateChanged(self):
        global Calcular
        global FechaCal
        global Semana
        global Mes
        global FechaHoy

        FechaHoy = str(QDate.toString(QDate.currentDate(), "yyyy-MM-dd"))
        FechaCal = str(QDate.toString(self.dateEdit.date(), "yyyy-MM-dd"))
        Semana = QDate.longDayName(QDate.dayOfWeek(self.dateEdit.date()))
        Mes = str(QDate.toString(self.dateEdit.date(), "yyyy-MM-"))
        self.label.setText("Fecha:   " + Semana)
        self.txt_Nombre.clear()
        self.lbl_Total.clear()
        self.lbl_Consumos.clear()
        self.lbl_Rojo.clear()
        self.lbl_Verde.clear()
        self.statusbar.clear()

        if self.tab_Main.tabText(self.tab_Main.currentIndex()) == 'Registro':
            if self.tab_Registro.tabText(self.tab_Registro.currentIndex()) == 'Asistencia':
                # View_Name = str(QDate.toString(self.dateEdit.date(), "MMMddyyyy"))
                self.tbl_Asistencia.clearContents()

                if FechaCal <= FechaHoy:
                    query = """SELECT
                        registro_asistencia.Status as Status,
                        registro_socios.Nombre as Nombre,
                        registro_socios.Apellido as Apellido,
                        registro_asistencia.Proteina as Proteina,
                        registro_asistencia.Fibra as Fibra,
                        registro_asistencia.Batido as Batido,
                        registro_asistencia.Te as Te,
                        registro_asistencia.Aloe as Aloe,
                        registro_asistencia.LiftOff as LiftOff,
                        registro_asistencia.PrePago as PrePago,
                        registro_asistencia.Total as Total,
                        registro_asistencia.Fila as Fila
                    FROM
                        registro_socios
                        LEFT JOIN registro_asistencia ON registro_asistencia.IdSocio = registro_socios.id
                    WHERE
                        FechaCal='%s';""" % FechaCal
                    self.txt_Nombre.setEnabled(True)
                    self.tbl_Asistencia.setEnabled(True)
                    # query = "SELECT * FROM %s;" % View_Name
                    Registros = BD.interAct(query)
                    Calcular = False
                    # row = 0
                    for Registro in Registros:
                        item = 0
                        row = int(Registro[11])
                        fullName = str(Registro[1] + " " + Registro[2])
                        for col in range(self.tbl_Asistencia.columnCount()):
                            if col == 1:
                                self.tbl_Asistencia.setItem(row, col, QTableWidgetItem(fullName))
                                item += 2
                            else:
                                if col == 9: self.tbl_Asistencia.setItem(row,
                                                                col, QTableWidgetItem(str(Registro[item])))
                                if str(Registro[item]) != "0" and str(Registro[item]) != "None":
                                    self.tbl_Asistencia.setItem(row,
                                                                col, QTableWidgetItem(str(Registro[item])))
                                item += 1
                        # row += 1
                    # Views_List.append(View_Name)
                    query = """SELECT
                                TVentas,
                                TConsumos,
                                Capital,
                                Ganancia
                            FROM
                                reporte_mensual
                            WHERE
                                FechaCal='%s'""" % FechaCal
                    Registros = BD.interAct(query)
                    for Reg in Registros:
                        self.lbl_Total.setText(str(Reg[0]))
                        self.lbl_Consumos.setText(str(Reg[1]))
                        self.lbl_Rojo.setText(str(Reg[2]))
                        self.lbl_Verde.setText(str(Reg[3]))

                    self.frecuentes()
                    Calcular = True

                if FechaCal > FechaHoy:
                    self.statusbar.showMessage("No se puede hacer Registros Posteriores a Hoy...")
                    self.txt_Nombre.setDisabled(True)
                    self.tbl_Asistencia.setDisabled(True)
            if self.tab_Registro.tabText(self.tab_Registro.currentIndex()) == 'Producto Cerrado': pass
                # query = "SELECT SKU, Descripcion FROM productos;"
                # Registros = BD.interAct(query)
                # Calcular = False
                # row = 0
                # for Registro in Registros:
                #     for col in range(2):
                #         self.tbl_prodCerrado.setItem(row, col, QTableWidgetItem(Registro[col]))
                #     row += 1
                # Calcular = True

            if self.tab_Registro.tabText(self.tab_Registro.currentIndex()) == 'Mensajes':
                self.lblNombreCompleto.clear()
                try:
                    self.treeEncontrado_handleClicked()
                except:
                    pass

        if self.tab_Main.tabText(self.tab_Main.currentIndex()) == 'Reportes':
            if self.tab_Reportes.tabText(self.tab_Reportes.currentIndex()) == 'Semanal':
                self.tbl_Rep_Semanal.clearContents()
                query = "SELECT \
                                sum(TVentas), \
                                sum(Capital), \
                                avg(TConsumos), \
                                sum(Ganancia) \
                                FROM reporte_mensual WHERE FechaCal >= '2015-09-14' and FechaCal < '2015-09-21';"
                # print query
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
                     FROM reporte_mensual WHERE FechaCal LIKE '%s%%' ORDER BY FechaCal;" % Mes

                Reporte = BD.interAct(query)
                Calcular = False
                row = 0
                for linea in Reporte:
                    for col in range(self.tbl_Rep_Mensual.columnCount()):
                        if type(linea[col]) is int:
                            self.tbl_Rep_Mensual.setItem(row, col, QTableWidgetItem(str(linea[col])))
                        else:
                            self.tbl_Rep_Mensual.setItem(row, col, QTableWidgetItem(_fromUtf8(linea[col])))
                        # if 'lunes' in linea: self.tbl_Rep_Mensual.item(row, col).setBackground(QColor(100,150,100))
                        if row == numDia: self.tbl_Rep_Mensual.item(row, col).setBackground(QColor(100, 150, 100))
                    row += 1
                query = "SELECT sum(TVentas), sum(Ganancia), sum(Capital), \
                                sum(TConsumos), avg(TConsumos), avg(Entraron), avg(Invitaciones), sum(Promocion) \
                                FROM reporte_mensual WHERE FechaCal LIKE '%s%%';" % Mes
                Resultados = BD.interAct(query)
                for Resultado in Resultados:
                    verdeprom = Resultado[7] / 3
                    rojoprom = Resultado[7] - verdeprom
                    self.lbl_Total.setText(str(Resultado[0]))
                    self.lbl_Verde.setText(str(Resultado[1]))
                    self.lbl_Rojo.setText(str(Resultado[2]))
                    self.lbl_Consumos.setText(str(Resultado[3]))
                    print "Total: $bs: %s - $us: %.2f " % (Resultado[0], Resultado[0] / 6.96)
                    print "Verde: $bs: %s - $us: %.2f  " % (Resultado[1], Resultado[1] / 6.96)
                    print "Rojo: $bs: %s - $us: %.2f  " % (Resultado[2], Resultado[2] / 6.96)
                    print "Promociones: $sbs: %s - $us: %.2f " % (rojoprom, rojoprom / 6.96)
                    print "Prom_Consumos/Mes: %.2f " % Resultado[4]
                    print "Prom_Presentaciones/Mes: %.2f" % Resultado[5]
                    print "Prom_Invitaciones/Mes: %.2f" % Resultado[6]
                    print "Ganancia Real: %s " % (Resultado[1] - rojoprom)
                Calcular = True

    def tbl_Asistencia_cellChanged(self, row, col):
        sender = self.sender().objectName()
        if Calcular:
            if sender == 'tbl_Asistencia':
                # Verificamos que la celda "Nombre" existe y tiene texto
                # NameExists = True if self.tbl_Asistencia.item(row,colNameIndex['Nombre']) is not None else False
                NameExists = self.verifyitem(row, colNameIndex['Nombre'])
                # si el cambio es de la lista de extras se hace el calculo de precios
                if NameExists:
                    colHeaderName = str(self.tbl_Asistencia.horizontalHeaderItem(col).text())
                    # item = self.tbl_Asistencia.item(row, col) if self.tbl_Asistencia.item(row, col).text() is not None else 'NULL'
                    item = str(self.tbl_Asistencia.item(row, col).text()) if self.verifyitem(row, col) else 'NULL'
                    # if colHeaderName == 'Status' or colHeaderName == 'PrePago': pass
                    # if colHeaderName == 'PrePago' and item == '10':
                    #
                    #     Promocion = "SELECT sum(Total) FROM registro_asistencia WHERE FechaCal='%s' AND Prepago=10" % FechaCal
                    #     # if colHeaderName == 'Status':
                    #     #     item = item.upper() if item != "NULL" else ""
                    #     query = "UPDATE reporte_mensual \
                    #         SET Promocion=(%s) \
                    #         WHERE FechaCal='%s';" % (Promocion, FechaCal)
                    #     # print query
                    #     BD.interAct(query)

                    if colHeaderName in Extras:
                        cantidad = str(self.tbl_Asistencia.item(row,col).text())
                        total_extras = Extras[colHeaderName] * int(cantidad) if cantidad.isdigit() else 0
                        if total_extras == 0: total_extras = -Extras[colHeaderName]
                        total = int(self.tbl_Asistencia.item(row,colNameIndex['Total']).text()) + total_extras
                        self.tbl_Asistencia.setItem(row, colNameIndex['Total'],QTableWidgetItem(str(total)))

                    # if colHeaderName == 'Total':
                        # cantidad = int(self.tbl_Asistencia.item(row,col).text())
                    self.CuentaConsumos(row)

                else:
                    for i in range(self.tbl_Asistencia.columnCount()):
                        self.tbl_Asistencia.takeItem(row, col)

            if sender == 'tbl_Rep_Mensual':
                headers = ['Invitaciones', 'Entraron']
                colHeaderName = str(self.sender().horizontalHeaderItem(col).text())
                # num = self.sender().columnCount()
                # print 'Numero de Columnas: %s' % num
                if colHeaderName in headers:
                    print 'El Nombre de la columna es: %s' % colHeaderName
                    day = Mes + str(row + 1).zfill(2)
                    # print 'La fila es: %s' % day
                    item = str(self.sender().item(row,
                        col).text()) if self.sender().item(row,
                        col) and self.sender().item(row,
                        col).text() != "" else 0
                    query = "UPDATE reporte_mensual \
                                SET %s=%s \
                                WHERE FechaCal='%s';" \
                            % (colHeaderName, item, day)
                    print query
                    BD.interAct(query)

    def tbl_Asistencia_dblClicked(self):
        if self.tbl_Asistencia.horizontalHeaderItem(
                self.tbl_Asistencia.currentColumn()).text() == 'Nombre':
            Row = self.tbl_Asistencia.currentRow()
            for col in range(self.tbl_Asistencia.columnCount()):
                self.tbl_Asistencia.takeItem(Row, col)
            query = "DELETE FROM registro_asistencia \
                WHERE Fila='%s' \
                AND FechaCal='%s';" \
                    % (Row, FechaCal)
            BD.interAct(query)
            self.CuentaConsumos(Row)

    def handle_PhonesEvents(self):  # pass

        if self.txtCelPhone:
            cel = str(self.txtCelPhone.text())
            sender = self.sender().objectName()
            if sender == 'btnLlamar':
                try:
                    sm.DialVoice(cel)
                except:
                    error = sys.exc_info()[1]
                    self.statusbar.showMessage("Hubo un Error: %s" % error)
            if sender == 'btnSMS':
                Text = 'SPA Facial. Anita, El Mie-6/Dic a Hrs 19:15 te esperamos en el Edif. Los Jardines \
                    Piso 1 of. G (6 de agosto #2404 entre B.Salinas y P.Salazar) Marcelo.'
                try:
                    message = {
                        'Text': Text,
                        'SMSC': {'Location': 1},
                        'Number': cel,
                    }
                    ##                    # Create SMS info structure
                    ##                    smsinfo = {
                    ##                        'Class': -1,
                    ##                        'Unicode': False,
                    ##                        'Entries':  [
                    ##                            {
                    ##                                'ID': 'ConcatenatedTextLong',
                    ##                                'Buffer':
                    ##                                    'Very long python-gammu testing message '
                    ##                                    'sent from example python script. '
                    ##                                    'Very long python-gammu testing message '
                    ##                                    'sent from example python script. '
                    ##                                    'Very long python-gammu testing message '
                    ##                                    'sent from example python script. '
                    ##                            }
                    ##                        ]}

                    ##                    # Encode messages
                    ##                    encoded = gammu.EncodeSMS(smsinfo)

                    ##                    # Send messages
                    ##                    for message in encoded:
                    ##                        # Fill in numbers
                    ##                        message['SMSC'] = {'Location': 1}
                    ##                        message['Number'] = sys.argv[1]

                    ##                        # Actually send the message
                    sm.SendSMS(message)
                except:
                    error = sys.exc_info()[1]
                    self.statusbar.showMessage("Hubo un Error: %s" % error)
                    # Create object for talking with phone
                    ##        sm = gammu.StateMachine()
                    ##        #lee el archivo de configuracion
                    ##        sm.ReadConfig()
                    ##        # Connect to the phone
                    #
                    # Dial a number
                    #        sm.DialVoice(cel)

                    ##    In my gammu configuration file I changed the port to /dev/phone
                    ##Then I went to /etc/udev/rules/ directory and in it I created a file name 99-phone.rules, then in that file I wrote the following line:
                    ##SUBSYSTEM=="usb", ATTRS{idVendor}=="0421", ATTRS{idProduct}=="006b", MODE="0666" , SYMLINK+="phone"
                    ##Then I rebooted my system and then when I connected my Nokia phone, I was able to run commands on it without using sudo!

    def Fecha(self):
        return str(QDate.toString(self.dateEdit.date(), "yyyy-MM-dd"))

    def myprint(self):  # pass
        # funcion que llena la tabla de reporte mes a mes

        xDia, xMes, xAnho, fechaDesde = 1, QDate.month(self.dateEdit.date()), QDate.year(self.dateEdit.date()), ""
        dicSemana = dict()

        query = "SELECT * FROM reporte_mensual WHERE FechaCal = '%s'" % FechaCal
        if not BD.interAct(query):
            xMez = xMes
            dicSemana.clear()
            for i in range(2):
                for xDia in range(31):
                    xDia += 1
                    if QDate.isValid(xAnho, xMez, xDia):
                        fechaHasta = "%s-%s-%s" % (xAnho,
                                      str(xMez).zfill(2),
                                      str(xDia).zfill(2))
                        formatFecha = fechaHasta.replace('-', '')
                        diaDeSemana = QDate.longDayName(QDate.dayOfWeek(QDate.fromString(formatFecha, "yyyyMMdd")))
                        if diaDeSemana == "lunes":
                            NoSem = QDate.weekNumber(QDate.fromString(formatFecha, "yyyyMMdd"))
                            dicSemana[fechaHasta] = NoSem[0]
                            if fechaDesde:
                                query = """
                                INSERT INTO
                                    reporte_semanal (fechaDesde, fechaHasta, noSem)
                                VALUES
                                    ('%s', '%s', '%s')""" % (fechaDesde, fechaHasta, dicSemana[fechaDesde])
                                print query
                                # BD.interAct(query)
                                if xMes != xMez: break
                            fechaDesde = fechaHasta
                        # if xMes == xMez:
                        #     query = """
                        #     INSERT INTO
                        #         reporte_mensual (FechaCal, Semana)
                        #     VALUES
                        #         ('%s', '%s')""" % (fechaHasta, diaDeSemana)
                        #     BD.interAct(query)
                xMez += 1
    #TODO: agregar la columna numero de semana a la tabla semanal
    #TODO: generar vistas de los promedios de la tabla reporte

    def txt_Nombre_textChanged(self, event):
        # Al escribir en txt_nombre

        if self.txt_Nombre.text():
            query = "SELECT \
                id, \
                Nombre, \
                Apellido \
                FROM registro_socios \
                WHERE Nombre \
                LIKE '%s%%'" % self.txt_Nombre.text()
            rows = BD.interAct(query)
            if rows:
                idnombre.clear()
                self.fillNamesList(rows)
            else:
                nombrecompleto = str(self.txt_Nombre.text())
                try:
                    self.treeEncontrado_handleClicked(nombrecompleto, idnombre[nombrecompleto])
                except:
                    pass
                # print "%s: %s" % (nombrecompleto, idnombre[nombrecompleto])

    def frecuentes(self):
        View_Name = "frecuentes"
        # query = "CREATE VIEW IF NOT EXISTS %s AS SELECT \
        #     IdSocio, \
        #     Nombre, \
        #     Apellido, \
        #     FROM asistencia a, socios s \
        #     WHERE s.Id = a.IdSocio \
        #     GROUP BY IdSocio ORDER BY count(IdSocio) DESC;" \
        #         % View_Name
        query = "SELECT id, Nombre, Apellido FROM registro_socios;"
        rows = BD.interAct(query)
        self.fillNamesList(rows)

    def fillNamesList(self, rows):
        # column = 0
        resultado = list()
        # self.cboEncontrado.clear()
        for row in rows:
            Resultado = "%s %s" % (row[1], row[2])
            idnombre[str(Resultado)] = row[0]
            resultado.append(Resultado)
            model.setStringList(resultado)

            # self.cboEncontrado.addItem(Resultado)

            # data = 'data %s' % Resultado
            # # self.lst_Encontrado.addItem(Resultado)
            # self.treeEncontrado.addTopLevelItem(
            #         self.addParent(self.treeEncontrado.invisibleRootItem(), column, Resultado, data))
            ##            if self.tab_Registro.tabText(self.tab_Registro.currentIndex()) == 'Producto Cerrado':
            ##                print self.tab_Registro.currentTabName()

    def addParent(self, parent, column, title, data):
        item = QTreeWidgetItem(parent, [title])
        item.setData(column, Qt.UserRole, data)
        item.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
        item.setExpanded(True)
        return item

    def treeEncontrado_handleClicked(self, Nombre, IdSocio):
        global Calcular
        global celPhone
        #evitamos que se hagan calculos al modificar la tabla asistencia
        Calcular = False
        #
        if self.tab_Registro.tabText(self.tab_Registro.currentIndex()) == 'Asistencia':
            #hacemos un barrido por todas las filas de la tabla
            for Row in range(self.tbl_Asistencia.rowCount()):
                if not self.tbl_Asistencia.item(Row,
                        colNameIndex['Nombre']) or self.tbl_Asistencia.item(Row,
                        colNameIndex['Nombre']).text() == "":
                    # insertar en la tabla asistencia el No de Row y el id del socio
                    self.tbl_Asistencia.setItem(Row,colNameIndex['Nombre'], QTableWidgetItem(Nombre))
                    break
            Calcular = True
            self.tbl_Asistencia.setItem(Row,
                        colNameIndex['Total'],
                        QTableWidgetItem(str(Nutricion)))
            query = """
            INSERT INTO registro_asistencia (
                FechaCal,
                UpdatedOn,
                Fila,
                IdSocio,
                Total)
            VALUES
                ('%s','%s','%s','%s', %s);""" % (FechaCal, FechaHoy, Row, IdSocio, int(Nutricion))
            BD.interAct(query)
            self.txt_Nombre.selectAll()
        # print self.treeEncontrado.currentItem().text(0)
        if self.tab_Registro.tabText(self.tab_Registro.currentIndex()) == 'Mensajes':
            self.lblNombreCompleto.setText(Nombre)
            for i in reversed(range(self.scrollLayout.count())):
                self.scrollLayout.itemAt(i).widget().deleteLater()
            # rows = BD.interAct(str("SELECT * FROM Socios WHERE Id ='" + IdSocio[:IdSocio.find(' ')] + "'"))
            rows = BD.interAct("SELECT * FROM registro_socios WHERE Id ='%s'" % IdSocio)
            Buscar = False
            for row in rows:
                print row
                ##                self.txt_AddName.setText(row[1])
                ##                self.txt_AddName.setEnabled(False)
                ##                self.txt_AddLName.setText(row[2])
                celPhone = row[3]
                self.scrollLayout.addRow(CelButton())
            Buscar = True

    def Diccionario(self):
        # crea un diccionario con los pares de titulo de columna y el valor de la celda
        # colecta los nombres de columna de la tabla asistencia
        # con sus respectivos numeros de columnas
        for col in range(self.tbl_Asistencia.columnCount()):
            colHeaderName = self.tbl_Asistencia.horizontalHeaderItem(col).text()
            colNameIndex[str(colHeaderName)] = col

    def CuentaConsumos(self, fila):
        TConsumos, TVentas, Promocion = 0, 0, 0
        for Row in range(self.tbl_Asistencia.rowCount()):
            if self.tbl_Asistencia.item(Row, colNameIndex['Total']):
#                print "%s; %s" % (Row, self.tbl_Asistencia.item(Row, colNameIndex['Total']).text())
                TVentas = TVentas + int(self.tbl_Asistencia.item(Row, int(colNameIndex['Total'])).text())
                TConsumos += 1

        SVerde = TVentas / 3
        SRojo = TVentas - SVerde
        self.lbl_Consumos.setText(str(TConsumos))
        self.lbl_Total.setText(str(TVentas))
        self.lbl_Verde.setText(str(SVerde))
        self.lbl_Rojo.setText(str(SRojo))
        #verificamos si hay nombre
        if self.tbl_Asistencia.item(fila, 1) is not None:
            instruccion, query = "UPDATE registro_asistencia SET ", ""
            #para cada columna de la fila seleccionada
            for col in range(self.tbl_Asistencia.columnCount()):
                item = self.tbl_Asistencia.item(fila, col)
                if item is not None:
                    colHeaderName = str(self.tbl_Asistencia.horizontalHeaderItem(col).text())
                    # obviamos la columna del Nombre
                    if colHeaderName != "Nombre":
                    # capturamos el item a evaluar
                        valor = str(item.text()) if item.text() != "" else 'NULL'
                        # print "colHeaderName: %s y valor: %s" % (colHeaderName, valor)
                        if colHeaderName == "Status":
                            valor = valor.upper()
                            # print "valor: %s" % valor
                            instruccion = instruccion + "%s='%s', " % (colHeaderName, valor)
                        else:
                            instruccion = instruccion + "%s=%s, " % (colHeaderName, valor)
                        query = instruccion
                        if colHeaderName == "PrePago" and valor == "10":
                            Promocion = "SELECT sum(Total) FROM registro_asistencia WHERE FechaCal='%s' AND Prepago=10" % FechaCal

            if query:
                # quitamos la coma del final
                query = query[:query.rfind(',')]
                # completamos query con las condiciones
                query = query + " WHERE Fila=%s AND FechaCal='%s';" % (fila, FechaCal)
                prev_query = query
                #actualizamos la base de datos
                # query_Dict[0] = query
                # print query
                BD.interAct(query)

        NConsumos = "SELECT count() FROM registro_asistencia WHERE FechaCal='%s' AND Status='N'" % FechaCal
        Referidos = "SELECT count() FROM registro_asistencia WHERE FechaCal='%s' AND Status='R'" % FechaCal

        query = """UPDATE reporte_mensual SET
            NConsumos=(%s),
            Referidos=(%s),
            TConsumos=%s,
            TVentas=%s,
            Capital=%s,
            Ganancia=%s,
            Promocion=(%s)
            WHERE FechaCal='%s'""" \
            % (NConsumos, Referidos, TConsumos,
               TVentas, SRojo, SVerde, Promocion, FechaCal)
        # query_Dict[1] = query
        # print query
        # print query_Dict[0]
        # print query_Dict[1]
        BD.interAct(query)
    #
    def crear_archivo(self):

        for row in range(self.tbl_Asistencia.rowCount()):
            if self.tbl_Asistencia.item(row, 1) is not None:
                query = "UPDATE registro_asistencia SET "
                for col in range(self.tbl_Asistencia.columnCount()):
                    if self.tbl_Asistencia.item(row, col) is not None:
                        colHeaderName = str(self.tbl_Asistencia.horizontalHeaderItem(col).text())
                        if colHeaderName != "Nombre":
                            valor = str(self.tbl_Asistencia.item(row, col).text())
                            query = query + "%s ='%s' " % (colHeaderName, valor)
                query = query + "WHERE Fila=%s AND FechaCal='%s';" % (row, FechaCal)
                print query

    def AbrirCal(self):
        cal = pyDate(self)
        cal.exec_()

    def AddEditBD(self):
        self.txt_Nombre.clear()
        # wid = addSocio.AddSocio(self)
        wid = comandacode.Registro(self)
        wid.exec_()

    def setCalWidget(self):  # pass
        self.splitter_5 = QSplitter(self.centralwidget)
        self.splitter_5.setGeometry(QRect(55, 30, 131, 51))
        self.splitter_5.setOrientation(Qt.Vertical)
        self.splitter_5.setObjectName(_fromUtf8("splitter_5"))
        self.label = QLabel(self.splitter_5)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.dateEdit = pyDate.PyDateEdit(self.splitter_5)
        self.dateEdit.setFont(font)
        self.dateEdit.setCursor(QCursor(Qt.ArrowCursor))
        self.dateEdit.setDate(QDate.currentDate())
        #######
        # self.Rotacion = RotatedHeaderView(self.tbl_Asistenci


class CelButton(QPushButton):
    def __init__(self, parent=None):
        super(CelButton, self).__init__(parent)
        self.setText(celPhone)
        self.clicked.connect(self.CelButton_handleClicked)

    def CelButton_handleClicked(self):
        cel = str(self.text())
        try:
            sm.DialVoice(cel)
        except:
            error = sys.exc_info()[1]
            main = MainForm()
            main.statusbar.showMessage("Hubo un Error: %s" % error)
            print "Error Llamando al %s" % self.text()

app = QApplication(sys.argv)
ui = MainForm()
ui.main()
app.exec_()
