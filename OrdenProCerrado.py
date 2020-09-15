# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import comanda
import DB_Class
import addSocio
# from rotated import RotatedHeaderView
from pyDate import PyDateEdit
try:
    _encoding = QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)


class Registro(QDialog, comanda.Ui_Form):
    def __init__(self, parent=None):
        super(Registro, self).__init__(parent)
        self.setupUi(self)
        self.valIniciales()
        self.dibujartablas()
        self.clearform()
        self.connectActions()
        self.on_calFecha_changed()

    def dibujartablas(self):
        headers = ['Producto', 'PV', '25%', '35%', '42%', '50%', 'Cliente']
        ancho = [140, 40, 40, 40, 40, 40, 50]
        # self.tblAsistencia.setHorizontalHeader(RotatedHeaderView(self.tblAsistencia))
        self.tblAsistencia.setRowCount(10)
        self.tblAsistencia.setColumnCount(len(headers))
        col = 0
        for colname in headers:
            item = QTableWidgetItem()
            self.tblAsistencia.setHorizontalHeaderItem(col, item)
            self.tblAsistencia.setColumnWidth(col, ancho[col])
            head = self.tblAsistencia.horizontalHeaderItem(col)
            head.setText(_translate("MainWindow", colname, None))
            col += 1

    def valIniciales(self):
        global BD
        global model
        global dicPares
        global Extras
        global dicoperador
        #
        Extras = {'Proteina': 9, 'Fibra': 10, 'Batido': 12, 'Aloe': 6, 'Te': 6, 'LiftOff': 20}
        # dicoperador = {'Club': 0, 'MLlosa': 1, 'WQuiroga': 2}
        dicoperador = {'MLlosa': 1, 'WQuiroga': 2}
        dicPares = dict()
        #
        BD = DB_Class.dataBase()
        BD.createCon()
        model = QStringListModel()
        #dibujar el calendario del formulario
        self.calFecha = PyDateEdit(self.layoutWidget3)
        self.calFecha.setCursor(QCursor(Qt.ArrowCursor))
        self.calFecha.setDate(QDate.currentDate())
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.calFecha)

        #
        completer = QCompleter()
        completer.setModel(model)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        #
        self.txtNombre.setCompleter(completer)
        #
        self.cboOperador.addItem("Cliente")
        self.cboOperador.addItem("25%")
        self.cboOperador.addItem("35%")
        self.cboOperador.addItem("42%")
        self.cboOperador.addItem("50%")



    def connectActions(self):
        self.btnNombre.clicked.connect(self.agregar_nombre)
        self.btnSalir.clicked.connect(self.on_commandButtons_clicked)
        self.btnGuardar.clicked.connect(self.on_commandButtons_clicked)
        self.btnLimpiar.clicked.connect(self.clearform)
        self.calFecha.dateChanged.connect(self.on_calFecha_changed)
        self.tblAsistencia.doubleClicked.connect(self.on_tblAsistencia_dblClicked)

        self.chkPrePago.stateChanged.connect(self.on_chkPrePago_changeEvent)
        self.txtPrePago.textChanged.connect(self.on_cboPrePago_changed)
        self.txtNombre.textChanged.connect(self.on_txtNombre_text_changed)


        self.btnProteina.clicked.connect(self.on_extraButtons_clicked)
        self.btnFibra.clicked.connect(self.on_extraButtons_clicked)
        self.btnAloe.clicked.connect(self.on_extraButtons_clicked)
        self.btnTe.clicked.connect(self.on_extraButtons_clicked)
        self.btnBatido.clicked.connect(self.on_extraButtons_clicked)
        self.btnLiftOff.clicked.connect(self.on_extraButtons_clicked)
        self.lstExtras.doubleClicked.connect(self.on_lstExtra_doubleClicked)
        self.cboPrePago.currentIndexChanged.connect(self.on_cboPrePago_changed)
        # self.cboOperador.currentIndexChanged.connect(self.on_cbooperador_changed)

    def on_calFecha_changed(self):
        global fechacal
        fechacal = str(QDate.toString(self.calFecha.date(), "yyyy-MM-dd"))
        # self.filltable(str(self.cboOperador.currentText()))
        # self.fillstatics(str(self.cboOperador.currentText()))

    def on_cbooperador_changed(self):
        if self.cboOperador.currentText() == 'Club':
            state = True
        else:
            state = False
        self.txtNombre.setEnabled(state)
        self.btnGuardar.setEnabled(state)
        self.clearform()
        # self.filltable(str(self.cboOperador.currentText()))
        # self.fillstatics(str(self.cboOperador.currentText()))

    def on_cboPrePago_changed(self):
        if self.txtTotal.text(): self.txtTotal.setText(str(self.sumatoria()))

    def on_lstExtra_change(self, event):
        print "el evento: %s" % event

    def on_lstExtra_doubleClicked(self, index):
        # print "%s, %s" % (self.lstExtras.currentRow(), index)
        self.lstExtras.takeItem(self.lstExtras.currentRow())
        self.txtTotal.setText(str(self.sumatoria()))

    def on_chkPrePago_changeEvent(self):
        state = self.chkPrePago.isChecked()
        self.txtPrePago.setEnabled(state)
        self.cboPrePago.setEnabled(state)
        if state:
            self.cboPrePago.addItem("22")
            self.cboPrePago.addItem("31")
            self.cboPrePago.addItem("32")
            self.cboPrePago.addItem("41")
        else:
            self.cboPrePago.clear()
            self.txtPrePago.clear()

    def on_extraButtons_clicked(self):
        if self.txtNombre.text():
            sender = self.sender().text()
            self.lstExtras.addItem(sender)
            self.txtTotal.setText(str(self.sumatoria()))
        else:
            pass
        # el siguiente codigo muestra el precio de cada producto
        # debe colocarse en una funcion q capture todos los cambios en la lista

    def sumatoria(self):
        total = 22
        global listaextras
        #
        listaextras = list()
        try:
            for item in range(self.lstExtras.count()):
                nombre = str(self.lstExtras.item(item).text())
                listaextras.append(nombre)
                total += int(Extras[nombre])
            if self.chkPrePago.isChecked() and self.txtPrePago.text() != '10':
                total -= int(self.cboPrePago.currentText())
        except:
            pass
        return total

    def on_commandButtons_clicked(self):

        sender = self.sender().objectName()

        if sender == "btnSalir":
            try:
                self.updatereporte()
            except:
                pass
            self.clearform()
            self.close()
        else:
            if self.txtNombre.text():
                fechahoy = str(QDate.toString(QDate.currentDate(), "yyyy-MM-dd"))
                idsocio = dicPares[str(self.txtNombre.text())]
                total = int(self.txtTotal.text())
                promocion = self.cboPrePago.currentText() if self.chkPrePago.isEnabled() and self.txtPrePago.text() == '10' else 0
                prepago = self.txtPrePago.text() if self.txtPrePago.text() else 0
                if self.chkPrePago.isChecked() and self.txtPrePago.text() == "":
                    print "falta el numero de prepago"
                else:
                    for fila in range(self.tblAsistencia.rowCount()):
                        if self.tblAsistencia.item(fila, 1) is None or self.tblAsistencia.item(fila, 1).text() == "":
                            break
                    query = """INSERT INTO registro_asistencia (
                        FechaCal,
                        UpdatedOn,
                        IdSocio,
                        Promocion,
                        Total,
                        Proteina,
                        Fibra,
                        Aloe,
                        Te,
                        Batido,
                        LiftOff,
                        PrePago,
                        Fila)
                        VALUES
                        ('%s','%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);""" \
                            % (fechacal, fechahoy, idsocio, promocion, total,
                               listaextras.count("Proteina"),
                               listaextras.count("Fibra"),
                               listaextras.count("Aloe"),
                               listaextras.count("Te"),
                               listaextras.count("Batido"),
                               listaextras.count("LiftOff"),
                               prepago, fila)
                    # print query
                    self.clearform()
                    dicPares.clear()
                    BD.interAct(query)
                    # self.filltable(str(self.cboOperador.currentText()))
                    # self.fillstatics(str(self.cboOperador.currentText()))
                    self.updatereporte()

    def on_txtNombre_text_changed(self):
        resultado = list()
        query = "SELECT \
                id, \
                Nombre, \
                Apellido \
                FROM registro_socios \
                WHERE Nombre \
                LIKE '%s%%'" % self.txtNombre.text()
        rows = BD.interAct(query)
        # dicPares.clear()
        if self.txtNombre.text() and rows:
            for row in rows:
                Resultado = "%s %s" % (row[1], row[2])
                dicPares[str(Resultado)] = row[0]
                resultado.append(Resultado)
                model.setStringList(resultado)
        if self.txtNombre.text() and not rows:
            self.txtTotal.setText(str(self.sumatoria()))

    def agregar_nombre(self):
        self.clearform()
        wid = addSocio.AddSocio(self)
        wid.exec_()

    def clearform(self):
        self.chkPrePago.setChecked(False)
        self.lstExtras.clear()
        self.txtNombre.clear()
        self.txtPrePago.clear()
        self.txtTotal.clear()
        # cleaning labels
        self.lblConsumos.clear()
        self.lblRojo.clear()
        self.lblVentas.clear()
        self.lblVerde.clear()
        self.efectivo.clear()
        self.lblRojoReal.clear()
        self.lblInsumos.clear()

    def filltable(self, operador):
        self.tblAsistencia.clearContents()
        # print operador
        if operador == "Club":
            condicion = """ FechaCal='%s'""" % fechacal
        else:
            condicion = """ FechaCal='%s' AND Operador=%s""" % (fechacal, dicoperador[operador])
        query = """
        SELECT
            registro_asistencia.Status,
            registro_socios.Nombre,
            registro_socios.Apellido,
            registro_asistencia.Proteina,
            registro_asistencia.Fibra,
            registro_asistencia.Batido,
            registro_asistencia.Te,
            registro_asistencia.Aloe,
            registro_asistencia.LiftOff,
            registro_asistencia.PrePago,
            registro_asistencia.Total,
            registro_asistencia.Fila
        FROM
            registro_socios
            LEFT JOIN registro_asistencia ON registro_asistencia.IdSocio = registro_socios.id
        WHERE
            %s;""" % condicion
        print query

        # Registros = BD.interAct(query)
        # for Registro in Registros:
        #     item = 0
        #     row = int(Registro[11])
        #     fullname = str(Registro[1] + " " + Registro[2])
        #     for col in range(self.tblAsistencia.columnCount()):
        #         if col == 1:
        #             self.tblAsistencia.setItem(row, col, QTableWidgetItem(fullname))
        #             item += 2
        #         else:
        #             if col == 9: self.tblAsistencia.setItem(row, col, QTableWidgetItem(str(Registro[item])))
        #             if str(Registro[item]) != "0" and str(Registro[item]) != "None":
        #                 self.tblAsistencia.setItem(row, col, QTableWidgetItem(str(Registro[item])))
        #             item += 1

    def fillstatics(self, operador):
        if operador == "Club":
            condicion = """ FechaCal='%s'""" % fechacal
        else:
            condicion = """ FechaCal='%s' AND Operador=%s""" % (fechacal, dicoperador[operador])
        query = """
            SELECT
                sum(total),
                sum(total)/3,
                sum(total) - sum(total)/3,
                count(),
                count()*0.3,
                (sum(total)-(sum(total)/3))-(count()*0.3),
                sum(total)/3 - sum(Promocion)
            FROM
                operador
            WHERE
                %s;""" % condicion
        # Registros = BD.interAct(query)
        # for Registro in Registros:
        #     self.lblVentas.setText(str(Registro[0]))
        #     self.lblVerde.setText(str(Registro[1]))
        #     self.lblRojo.setText(str(Registro[2]))
        #     self.lblConsumos.setText(str(Registro[3]))
        #     self.lblInsumos.setText(str(Registro[4]))
        #     self.lblRojoReal.setText(str(Registro[5]))
        #     self.efectivo.setText(str(Registro[6]))

    def updatereporte(self):
        query = """
            UPDATE reporte_mensual SET
                TConsumos=(SELECT count() FROM registro_asistencia WHERE FechaCal='%s'),
                TVentas=(SELECT sum(Total) FROM registro_asistencia WHERE FechaCal='%s'),
                Capital=(SELECT sum(Total)-sum(Total)/3 FROM registro_asistencia WHERE FechaCal='%s'),
                Promocion=(SELECT sum(Promocion) FROM registro_asistencia WHERE FechaCal='%s'),
                Ganancia=(SELECT sum(Total)/3 FROM registro_asistencia WHERE FechaCal='%s')
            WHERE
                FechaCal='%s'""" % (fechacal, fechacal, fechacal, fechacal, fechacal, fechacal)
        BD.interAct(query)

    def on_tblAsistencia_dblClicked(self):
        if self.tblAsistencia.horizontalHeaderItem(
                self.tblAsistencia.currentColumn()).text() == 'Nombre':
            fila = self.tblAsistencia.currentRow()
            for col in range(self.tblAsistencia.columnCount()):
                self.tblAsistencia.takeItem(fila, col)
            query = "DELETE FROM registro_asistencia \
                WHERE Fila='%s' \
                AND FechaCal='%s';" \
                    % (fila, fechacal)
            BD.interAct(query)
            # self.filltable(str(self.cboOperador.currentText()))
            # self.fillstatics(str(self.cboOperador.currentText()))
            self.updatereporte()