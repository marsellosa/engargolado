# -*- coding: utf-8 -*-

import db_func
import reporte
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from datetime import date


# from db_func import reporte as func

from rotated import RotatedHeaderView
from pyDate import PyDateEdit


class Reporte(QDialog, reporte.Ui_Form):
    def __init__(self, parent=None):
        super(Reporte, self).__init__(parent)
        self.setupUi(self)
        self.ValIniciales()
        self.dibujartablas()
        self.connectActions()
        self.dateChanged()

    def connectActions(self):
        self.dateEdit.dateChanged.connect(self.dateChanged)
        self.tabMain.currentChanged.connect(self.dateChanged)
        self.cboOperador.currentIndexChanged.connect(self.dateChanged)
        self.btnPrint.clicked.connect(self.on_btnPrint_clicked)

    def dateChanged(self):
        self.clear_labels()
        if self.tabMain.tabText(self.tabMain.currentIndex()) == 'Actividad Diaria':
            self.tblDiaria.clearContents()

            xMes, xAnho = QDate.month(
                self.dateEdit.date()), QDate.year(self.dateEdit.date())

            for row in range(31):
                xDia = row + 1
                if QDate.isValid(xAnho, xMes, xDia):

                    fechaActual = date(xAnho, xMes, xDia)
                    nombreDia = fechaActual.strftime('%A')
                    formatFecha = fechaActual.strftime('%Y%m%d')
                    self.tblDiaria.setItem(
                        row, 0, QTableWidgetItem(str(fechaActual)))
                    self.tblDiaria.setItem(row, 1, QTableWidgetItem(nombreDia))

                    if str(self.cboOperador.currentText()) == 'CLUB':
                        datos = func.actividad_diaria_club(fechaActual)
                    else:
                        datos = func.actividad_diaria_personal(
                            fechaActual, esOperador[str(self.cboOperador.currentText())])

                    for dato in datos:
                        # print(dato)
                        for col in range(2, self.tblDiaria.columnCount()):
                            item = col-2
                            if type(dato[item]) is int or type(dato[item]) is float:
                                self.tblDiaria.setItem(
                                    row, col, QTableWidgetItem(str(dato[item])))

            # TODO: SUMATORIA DE LOS DATOS GLOBALES EN LA TABLA REPORTE_MENSUAL
            # xMes = str(QDate.toString(self.dateEdit.date(), "yyyy-MM-"))
            xMes = fechaActual.strftime('%Y-%m-')
            condicion = "" if str(self.cboOperador.currentText(
            )) == 'CLUB' else " AND id_operador=%s" % esOperador[str(self.cboOperador.currentText())]

            for datos in func.reporte_mensual(xMes, condicion):
                self.lblConsumos.setText(str(datos[0]))
                self.lblSobreRojo.setText(str('{:0.1f}'.format(datos[1]))) if type(
                    datos[1]) is float else self.lblSobreRojo.setText(str(datos[1]))
                self.lblSobreVerde.setText(str('{:0.1f}'.format(datos[2]))) if type(
                    datos[2]) is float else self.lblSobreVerde.setText(str(datos[2]))
                self.lblTotalVendido.setText(str('{:0.1f}'.format(datos[3]))) if type(
                    datos[3]) is float else self.lblTotalVendido.setText(str(datos[3]))
                print(
                    f'insumos: {datos[4]}, descuento: {datos[5]}, mayoreo: {datos[6]}')

        if self.tabMain.tabText(self.tabMain.currentIndex()) == 'Semanal':
            dicSemana = dict()
            fechaDesde, xMez, Anho = "", 1, ""

            # fecha_calendario = str(QDate.toString(QDate.currentDate(), "yyyy-MM-dd"))

            var = "n"
            if var == "y":
                # variable que define el año que deseas cargar
                xAnho = 2020  # 2020 ya esta cargado
                # iteracion para cada mes del año
                # el numero de la izquierda define el mes
                for xMes in range(xMez, 14):
                    # iteracion para cada dia del mes
                    for xDia in range(1, 32):
                        # si el mes pasa a 13 cambiamos al primer mes del siguiente año
                        if xMes == 13:
                            xMes = 1  # mes 1
                            xAnho += 1  # siguiente año
                        # si la fecha propuesta es valida
                        if QDate.isValid(xAnho, xMes, xDia):
                            # formateamos la fecha donde ternima la
                            fechaHasta = "%s-%s-%s" % (xAnho,
                                                       str(xMes).zfill(2), str(xDia).zfill(2))
                            # formateamos la fecha para obtener el nombre del dia
                            formatFecha = fechaHasta.replace('-', '')
                            # obtenemos el nombre del dia
                            nombreDia = QDate.longDayName(
                                QDate.dayOfWeek(
                                    QDate.fromString(
                                        formatFecha, "yyyyMMdd")))
                            # si el nombre del dia es lunes
                            if nombreDia == 'lunes':
                                # obtenemos el numero de semana
                                noSem = QDate.weekNumber(
                                    QDate.fromString(
                                        formatFecha, "yyyyMMdd"))
                                # insertamos en un diccionario
                                # el numero de semana con la fecha de inicio
                                dicSemana[fechaHasta] = noSem[0]
                                # si existe la fecha desde que empieza la semana
                                if fechaDesde:
                                    # llamamos a la funcion para insertar en la tabla
                                    func.llenar_tbl_reporte_semanal(
                                        fechaDesde, fechaHasta, dicSemana[fechaDesde])
                                    # print(fechaDesde, fechaHasta, dicSemana[fechaDesde])
                                # asignamos fecha hasta a la fecha inicial
                                fechaDesde = fechaHasta
                                # si el año esta vacio y ya no es igual al anterior año
                                # se corta el loop
                                if Anho != "" and Anho != xAnho:
                                    break
                    Anho = xAnho
#                                print fechaHasta, noSem[0]
#                                 print "%s-%s-%s" % (xAnho, xMes, xDia)
#                         func.update_tabla_reporte(3, fecha_calendario, nombreDia, 1, "operador_marse")
#                         print "Fecha: %s, Dia: %s" % (fecha_calendario, nombreDia)

    def clear_labels(self):
        self.lblConsumos.clear()
        self.lblSobreRojo.clear()
        self.lblSobreVerde.clear()
        self.lblSobreRojoReal.clear()

    def dibujartablas(self):
        nombre_col = ['Fecha', 'Semana', 'Encuestas', 'Entraron', 'Nuevos',
                      'Referidos', 'Consumos', 'Costo', 'Ganancia', 'RojoReal', 'VerdeReal']
        ancho = [70, 70, 30, 30, 30, 30, 30, 50, 50, 40, 40]
        self.tblDiaria.setHorizontalHeader(RotatedHeaderView(self.tblDiaria))
        self.tblDiaria.setRowCount(31)
        self.tblDiaria.setColumnCount(len(nombre_col))

        for nombre in nombre_col:
            col_index = nombre_col.index(nombre)
            self.tblDiaria.setHorizontalHeaderItem(
                col_index, QTableWidgetItem(nombre))
            self.tblDiaria.setColumnWidth(col_index, ancho[col_index])

    def ValIniciales(self):
        global func
        global esOperador

        func = db_func.reporte()

        # codigo que carga el combo operador
        esOperador = dict()
        self.cboOperador.addItem('CLUB')
        esOperador['CLUB'] = 0
        for row in func.operadores_club():
            fullName = "%s %s" % (row[1], row[2])
            esOperador[str(fullName)] = row[0]
            self.cboOperador.addItem(fullName)
        ###

        self.lblMensaje.clear()
        self.lblConsumos.clear()
        self.lblSobreRojo.clear()
        self.lblSobreVerde.clear()
        self.lblSobreRojoReal.clear()

        self.dateEdit = PyDateEdit(self.layoutWidget)
        self.dateEdit.setDate(QDate.currentDate())
        self.LayOutFecha.setWidget(0, QFormLayout.FieldRole, self.dateEdit)

    def on_btnPrint_clicked(self): pass
    # xDia, xMes, xAnho, fechaDesde = 1, QDate.month(self.dateEdit.date()), QDate.year(self.dateEdit.date()), ""
    # dicSemana = dict()

    # query = "SELECT * FROM reporte_mensual WHERE fecha_calendario = '%s'" % FechaCal
    # if not BD.interAct(query):
    #     xMez = xMes
    #     dicSemana.clear()
    #     for i in range(2):
    #         for xDia in range(31):
    #             xDia += 1
    #             if QDate.isValid(xAnho, xMez, xDia):
    #                 fechaHasta = "%s-%s-%s" % (xAnho,
    #                                            str(xMez).zfill(2),
    #                                            str(xDia).zfill(2))
    #                 formatFecha = fechaHasta.replace('-', '')
    #                 diaDeSemana = QDate.longDayName(QDate.dayOfWeek(QDate.fromString(formatFecha, "yyyyMMdd")))
    #                 if diaDeSemana == "lunes":
    #                     NoSem = QDate.weekNumber(QDate.fromString(formatFecha, "yyyyMMdd"))
    #                     dicSemana[fechaHasta] = NoSem[0]
    #                     if fechaDesde:
    #                         query = """
    #                                 INSERT INTO
    #                                     reporte_semanal (fechaDesde, fechaHasta, noSem)
    #                                 VALUES
    #                                     ('%s', '%s', '%s')""" % (fechaDesde, fechaHasta, dicSemana[fechaDesde])
    #                         print query
    #                         # BD.interAct(query)
    #                         if xMes != xMez: break
    # print "btnPrint_clicked"
    # dialog = QPrintPreviewDialog()
    # dialog.paintRequested.connect(self.handlePaintRequest)
    # dialog.exec_()

    def handlePaintRequest(self, printer):
        document = self.makeTableDocument()
        document.print_(printer)

    def makeTableDocument(self):
        document = QTextDocument()
        cursor = QTextCursor(document)
        font = QFont('ubuntu condensed')

        rows = self.tblDiaria.rowCount()
        # rows = self.table.rowCount()
        # columns = self.table.columnCount()
        columns = self.tblDiaria.columnCount()

        table = cursor.insertTable(rows + 1, columns)
        format = table.format()
        format.setHeaderRowCount(1)
        table.setFormat(format)
        format = cursor.blockCharFormat()
        format.setFontWeight(QFont.Bold)
        for column in range(columns):
            cursor.setCharFormat(format)
            cursor.insertText(
                self.tblDiaria.horizontalHeaderItem(column).text())
            cursor.movePosition(QTextCursor.NextCell)
        for row in range(rows):
            for column in range(columns):
                try:
                    cursor.insertText(self.tblDiaria.item(row, column).text())
                except:
                    cursor.insertText("0")
                cursor.movePosition(QTextCursor.NextCell)
        return document

        # print "hola"
        # document = QTextDocument()
        # cursor = QTextCursor(document)
        # model = self.tblDiaria.model()
        # # model = self.table.model()
        # table = cursor.insertTable(
        #     model.rowCount(), model.columnCount())
        # for column in range(table.columns()):
        #     cursor.insertText(self.tblDiaria.horizontalHeaderItem(column).text())
        #     cursor.movePosition(QTextCursor.NextRow)
        #     QTextCursor.
        #     for row in range(table.rows()):
        #         print "row:%s, col:%s" % (row, column)
        #     # for column in range(table.columns()):
        #         try:
        #             # print "(%s)" % (self.tblDiaria.item(row, column).text())
        #             cursor.insertText(self.tblDiaria.item(row, column).text())
        #             # cursor.movePosition(QTextCursor.NextCell)
        #         except:
        #             # pass
        #             cursor.insertText("0")
        # #         cursor.insertText(model.item(row, column).text())
        #         cursor.movePosition(QTextCursor.NextRow)
        #     cursor.movePosition(QTextCursor.NextCell)
        #
        # document.print_(printer)

    def on_btnSalir_clicked(self):
        self.close()
