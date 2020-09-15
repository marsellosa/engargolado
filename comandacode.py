# -*- coding: utf-8 -*-
import locale
import datetime
# sudo apt-get install python3-pyqt5
# o pipenv install PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import db_func
import comanda
import DB_Class
import addSocio
from datetime import date
from rotated import RotatedHeaderView
from pyDate import PyDateEdit
try:
    _encoding = QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)


class Registro(QDialog, comanda.Ui_Engargolado):
    def __init__(self, parent=None):
        super(Registro, self).__init__(parent)
        self.setupUi(self)
        self.valIniciales()
        self.dibujartablas()
        self.connectActions()
        self.on_calFecha_changed()

    def dibujartablas(self):
        nombre_col = ['Status', 'Nombre', 'PrePago', 'Efectivo', 'Vendido',
                      'S.Rojo', 'Insumos', 'Descuento', 'Mayoreo', 'S.Verde']
        ancho = [25, 140, 25, 40, 35, 35, 35, 35, 35, 35]
        self.tblAsistenciaGeneral.setHorizontalHeader(
            RotatedHeaderView(self.tblAsistenciaGeneral))
        self.tblAsistenciaGeneral.setRowCount(150)
        self.tblAsistenciaGeneral.setColumnCount(len(nombre_col))
        for nombre in nombre_col:
            col_index = nombre_col.index(nombre)
            self.tblAsistenciaGeneral.setHorizontalHeaderItem(
                col_index, QTableWidgetItem(nombre))
            self.tblAsistenciaGeneral.setColumnWidth(
                col_index, ancho[col_index])

        self.tblAsistenciaPersonal.setHorizontalHeader(
            RotatedHeaderView(self.tblAsistenciaPersonal))
        self.tblReferidos.setHorizontalHeader(
            RotatedHeaderView(self.tblReferidos))

    def valIniciales(self):
        global BD
        global func
        global model
        global dic_id_socio
        global dic_referidor
        global dic_asistencia
        global dic_mayoreo
        global esClienteDe
        global Extras
        global esOperador
        global insumos

        Extras = {
            'Proteina': 12.5,
            'Fibra':    12.5,
            'Batido':   15,
            'Basica':   27,
            'Aloe':     8.5,
            'Te':       8.5,
            'Barra':    21,
            'Drive':    6.5,
            'Rebuild':  16.5,
            'Waffle':   20,
            'Jalea':    7.5,
            'Barra':	21,
            'Colageno': 13,
            'Sopa':     18
        }
        dic_mayoreo = {'WARA QUIROGA': 0.1}
        # factores mulplicadores
        insumos = 1
        # diccionarios
        esOperador = dict()
        dic_id_socio = dict()
        dic_referidor = dict()
        esClienteDe = dict()
        dic_asistencia = dict()
        # importamos el modulo de la base de datos
        BD = DB_Class.dataBase()
        # creamos la conexion a la base de datos
        BD.createCon()
        func = db_func.reporte()
        model = QStringListModel()
        # dibujar el calendario del formulario
        self.calFecha = PyDateEdit(self.layoutWidget)
        self.calFecha.setCursor(QCursor(Qt.ArrowCursor))
        self.calFecha.setDate(QDate.currentDate())
        self.formLayout.setWidget(1, QFormLayout.SpanningRole, self.calFecha)
        # establecer un rango inicial de 6 meses para consulta de visitas al club
        primer_dia = datetime.date.today() - datetime.timedelta(days=180)
        PrimerDia = QDate(primer_dia.year, primer_dia.month, primer_dia.day)
        self.calAsisteDesde.setDate(PrimerDia)
        self.calAsisteHasta.setDate(QDate.currentDate())

        #
        font = QFont()
        font.setFamily("Ubuntu Condensed")
        #
        completer = QCompleter()
        completer.setMaxVisibleItems(5)
        completer.setModel(model)
        completer.setCaseSensitivity(Qt.CaseInsensitive)

        #
        self.txtNombre.setCompleter(completer)
        self.chkPrePago.setEnabled(False)

        # codigo que carga el combo operador
        self.cboOperador.addItem('CLUB')
        for row in func.operadores_club():
            fullName = "%s %s" % (row[1], row[2])
            esOperador[str(fullName)] = row[0]
            self.cboOperador.addItem(fullName)
            ###

        self.clearform()
        self.clearlabels()

    def connectActions(self):
        self.btnNombre.clicked.connect(self.agregar_nombre)
        self.btnSalir.clicked.connect(self.on_commandButtons_clicked)
        self.btnGuardar.clicked.connect(self.on_commandButtons_clicked)
        self.btnLimpiar.clicked.connect(self.clearform)
        self.btnBasica.clicked.connect(self.on_extraButtons_clicked)
        # cambio de lenguentas en el tabulador principal
        self.tabMain.currentChanged.connect(self.on_tabmain_changed)

        self.cboPrePago.currentIndexChanged.connect(self.on_cboPrePago_changed)
        self.cboOperador.currentIndexChanged.connect(
            self.on_cboOperador_changed)

        self.txtPrePago.textChanged.connect(self.on_cboPrePago_changed)
        self.txtNombre.textChanged.connect(self.on_txtNombre_text_changed)

        self.calFecha.dateChanged.connect(self.on_calFecha_changed)
        self.calAsisteDesde.dateChanged.connect(self.on_calAsiste_changed)
        self.calAsisteHasta.dateChanged.connect(self.on_calAsiste_changed)

        self.tblAsistenciaGeneral.doubleClicked.connect(
            self.on_tblAsistenciaGeneral_dblClicked)

        self.chkPrePago.stateChanged.connect(self.on_chkPrePago_changeEvent)

        self.lstExtras.doubleClicked.connect(self.on_lstExtra_doubleClicked)
        self.lstProductos.doubleClicked.connect(self.on_lstExtra_doubleClicked)

    def llenar_tbl_reporte(self):
        # ESTA FUNCION NO ESTA EN USO
        # pass
        # funcion que llena la tabla de reporte mes a mes

        xDia, xMes, xAnho, fechaDesde = 1, QDate.month(
            self.calFecha.date()), QDate.year(self.calFecha.date()), ""
        dicSemana = dict()

        query = "SELECT * FROM reporte_mensual WHERE fecha_calendario = '%s'" % fecha_calendario
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
                        diaDeSemana = QDate.longDayName(QDate.dayOfWeek(
                            QDate.fromString(formatFecha, "yyyyMMdd")))
                        if diaDeSemana == "lunes":
                            NoSem = QDate.weekNumber(
                                QDate.fromString(formatFecha, "yyyyMMdd"))
                            dicSemana[fechaHasta] = NoSem[0]
                            if fechaDesde:
                                query = """
                                INSERT INTO
                                    reporte_semanal (fechaDesde, fechaHasta, noSem)
                                VALUES
                                    ('%s', '%s', '%s')""" % (fechaDesde, fechaHasta, dicSemana[fechaDesde])
                                BD.interAct(query)
                                if xMes != xMez:
                                    break
                            fechaDesde = fechaHasta
                        if xMes == xMez:
                            query = """
                            INSERT INTO
                                reporte_mensual (fecha_calendario, Semana)
                            VALUES
                                ('%s', '%s')""" % (fechaHasta, diaDeSemana)
                            BD.interAct(query)
                xMez += 1

    def on_tabmain_changed(self):
        icono = QIcon()
        # or self.tabMain.tabText(self.tabMain.currentIndex()) == "Cotizador":
        if self.tabMain.tabText(self.tabMain.currentIndex()) == "Engargolado":
            icono.addPixmap(
                QPixmap("images/Comanda/media_floppy_green.png"), QIcon.Normal, QIcon.Off)
            state = True
        else:
            icono.addPixmap(
                QPixmap("images/Comanda/search_icon.png"), QIcon.Normal, QIcon.Off)
            self.on_commandButtons_clicked()
            state = False

    def on_calAsiste_changed(self):
        if self.calAsisteDesde.date() > self.calAsisteHasta.date():
            self.calAsisteHasta.setDate(self.calAsisteDesde.date())
            # print "desde no puede ser mayor que hasta"
        self.on_commandButtons_clicked()

    def on_calFecha_changed(self):
        global fecha_calendario
        global nombreDia
        fecha_calendario = str(QDate.toString(
            self.calFecha.date(), "yyyy-MM-dd"))
        formatFecha = fecha_calendario.replace('-', '')
        nombreDia = QDate.longDayName(QDate.dayOfWeek(
            QDate.fromString(formatFecha, "yyyyMMdd")))
        self.filltable(str(self.cboOperador.currentText()))
        self.fillstatics(str(self.cboOperador.currentText()))

    def on_cboOperador_changed(self):
        state = True if self.cboOperador.currentText() == 'CLUB' else False
        self.txtNombre.setEnabled(state)
        self.btnGuardar.setEnabled(state)
        self.clearform()
        self.filltable(str(self.cboOperador.currentText()))
        self.fillstatics(str(self.cboOperador.currentText()))

    def on_cboPrePago_changed(self):
        if self.cboPrePago.currentText() == 'Personalizar':
            text, ok = QInputDialog.getText(self, 'Pre Pago Perzonalizado', '')
            self.cboPrePago.clear()
            if ok:
                self.cboPrePago.addItem(str(text).title())
            self.on_chkPrePago_changeEvent()
        self.txtTotal.setText(str(self.sumatoria()))

    def on_lstExtra_change(self, event): pass
    # print "el evento: %s" % event

    def on_lstExtra_doubleClicked(self, index):
        if self.tabMain.tabText(self.tabMain.currentIndex()) == "Engargolado":
            self.lstExtras.takeItem(self.lstExtras.currentRow())
            self.txtTotal.setText(str(self.sumatoria()))
        if self.tabMain.tabText(self.tabMain.currentIndex()) == "Cotizador":
            self.lstProductos.takeItem(self.lstProductos.currentRow())
            # print "Nombre: %s" % (self.cotizador())

    def on_chkPrePago_changeEvent(self):
        if self.txtNombre.text():
            state = self.chkPrePago.isChecked()
            self.txtPrePago.setEnabled(state)
            self.cboPrePago.setEnabled(state)
            if state:
                precios = ['27', '39.5', '52', 'Personalizar']
                for precio in precios:
                    self.cboPrePago.addItem(precio)

                if self.txtNombre:
                    id_socio = dic_id_socio[str(self.txtNombre.text())]
                    nro_prepago = BD.interAct(
                        f"""
                        SELECT
                            pre_pago+1
                        FROM
                            registro_asistencia
                        WHERE
                            id_socio={id_socio}
                        AND
                            pre_pago<>0
                        ORDER BY
                            fecha_calendario DESC, pre_pago DESC
                            LIMIT 1;
                    """
                    )
                    if not nro_prepago:
                        self.txtPrePago.setText("1")
                    else:
                        b = [item for (item,) in nro_prepago]
                        self.txtPrePago.setText(
                            "1") if b[0] > 10 or b[0] == 0 else self.txtPrePago.setText(str(b[0]))
            else:
                self.cboPrePago.clear()
                self.txtPrePago.clear()

    def on_extraButtons_clicked(self):

        sender = self.sender().text()
        objName = self.sender().objectName()
        # print(sender)
        if self.tabMain.tabText(self.tabMain.currentIndex()) == "Engargolado":
            if self.txtNombre.text():
                # self.lstExtras.addItem(objName[3:])
                self.lstExtras.addItem(sender)
                self.txtTotal.setText(str(self.sumatoria()))
        # if self.tabMain.tabText(self.tabMain.currentIndex()) == "Cotizador":
        #     self.lstProductos.addItem(objName[3:])
            # self.btnBatido.setText()
            # print "%s: %s" % (sender, self.cotizador(sender))
            # print "sender: %s" %

        # el siguiente codigo muestra el precio de cada producto
        # debe colocarse en una funcion q capture todos los cambios en la lista

    def cotizador(self, producto):
        global listaproductos

        listaproductos = list()

        try:
            for item in range(self.lstProductos.count()):
                nombre = str(self.lstProductos.item(item).text())
                listaproductos.append(nombre)

        except:
            pass
        self.lblTotal_Productos.setText(
            """ Productos: %s""" % str(self.lstProductos.count()))
        return listaproductos.count(producto)

    def sumatoria(self):
        global descuento
        global sobre_verde
        global sobre_rojo
        global valorPPago
        global consumido
        global aPagar
        global mayoreo

        factor_descuento = 0.1 if dic_id_socio[fullname] != 21 else 0.15
        factor_mayoreo, factor_sobre_rojo = 0.1, 0.6
        # factor_mayoreo = 0 if dic_mayoreo[fullname] == 1 else
        valorPPago, consumido, descuento, aPagar = 0, 0, 0, 0
        global listaextras
        #
        listaextras = list()
        try:
            for item in range(self.lstExtras.count()):
                nombre = str(self.lstExtras.item(item).text())
                listaextras.append(nombre)
                consumido += float(Extras[nombre])
                aPagar = consumido
                sobre_rojo = consumido * factor_sobre_rojo
                mayoreo = consumido * \
                    factor_mayoreo if esClienteDe[fullname] != 1 else 0

            if self.chkPrePago.isChecked():
                valorPPago = float(self.cboPrePago.currentText())
                aPagar = consumido - valorPPago
                descuento = valorPPago * factor_descuento
            # Solo muestra ganancia si el socio no eres tu
            sobre_verde = float(consumido - sobre_rojo - insumos - descuento -
                                mayoreo) if dic_id_socio[fullname] != esClienteDe[fullname] else 0
            self.txtBloque.setText("""Consumido:\t= %.1f\nSobre Rojo:\t- %.1f\ninsumos:\t- %.1f\nDcnto(%s):\t- %.1f\nMayoreo:\t- %.1f\n \t--------\nSobre Verde:\t%.1f\n""" %
                                   (consumido, sobre_rojo, insumos, valorPPago, descuento, mayoreo, sobre_verde))
            # self.txtBloque.setText("Consumido:{:>17}\nSobre Rojo:{:>-17}\nInsumos:{:>20}\nDescuento:{:>20}\nMayoreo:{:>20}".format(consumido, sobre_rojo, insumos, valorPPago, descuento, mayoreo, sobre_verde))

        except:
            self.txtBloque.clear()
            # pass
        return aPagar

    def on_commandButtons_clicked(self):
        global fullname
        # locale.setlocale(locale.LC_TIME, self.env.context['lang'] + '.utf8')
        fila = 0
        # factor_SR = 0.6 #0.6 es el equivalente a 2/3 de la nutricion, tomando el numero entero

        sender = self.sender().objectName()

        if sender == "btnSalir":
            try:
                self.updatereporte(id_operador)
            except:
                pass
            self.clearform()
            self.close()
        else:
            if self.txtNombre.text():
                id_socio = dic_id_socio[fullname]
                if self.tabMain.tabText(self.tabMain.currentIndex()) == "Engargolado":
                    # operador = es el id de operador
                    operador = esClienteDe[fullname]
                    # fechahoy = la fecha de hoy
                    fechahoy = date.today().strftime('%Y-%m-%d')
                    # fechahoy = str(QDate.toString(QDate.currentDate(), "yyyy-MM-dd"))
                    # print(fechahoy)
                    # conteo de productos para inventario
                    # --------------------INICIO-------------------------------
                    dic_precios = {

                    }

                    lista_ingredientes = [
                        {
                            'Producto': 'Basica',
                            'Batido': 2,
                            'Aloe': 1,
                            'Te': 1
                        },
                        {
                            'Producto': 'Waffle',
                            'Batido': 1,
                            'Proteina': 1,
                            'Huevo': 1,
                            'Avena': 3,
                            'Polvo': 1
                        },
                        {
                            'Producto': 'Galletas',
                            'Batido': 2,
                            'PDM': 1,
                            'Avena': 3,
                            'Huevo': 1,
                            'Aceite': 15,
                            'Polvo': 0.125
                        }
                    ]

                    for fila in range(self.tblAsistenciaGeneral.rowCount()):
                        if self.tblAsistenciaGeneral.item(fila, 1) is None or self.tblAsistenciaGeneral.item(fila, 1).text() == "":
                            break

                    dic_productos = {}
                    for extra in listaextras:
                        if extra in dic_productos:
                            dic_productos[extra] += 1
                        else:
                            dic_productos[extra] = 1

                    for extra in dic_productos:
                        query = """ INSERT INTO registro_consumos (
                            id_socio,
                            fila_nro,
                            producto,
                            cantidad,
                            inserted_on,
                            edited_on
                        ) VALUES (
                            {:d}, {:d}, '{}', {:.2f}, '{}', '{}'
                        );""".format(id_socio, fila, extra, dic_productos[extra], fecha_calendario, fechahoy)

                        BD.interAct(query)

                    fecha_actual = datetime.datetime.now()
                    nDia = fecha_actual.strftime('%A').capitalize()

                    # -------------------------- FIN -------------------------------
                    batido = listaextras.count("Batido")
                    aloe = listaextras.count("Aloe")
                    te = listaextras.count("Te")

                    if listaextras.count("Basica"):
                        cantBasicas = listaextras.count("Basica")
                        batido += 2 * cantBasicas
                        aloe += cantBasicas
                        te += cantBasicas

                    efectivo = 0 if not self.txtTotal.text() else float(self.txtTotal.text())
                    pre_pago = 0 if not self.txtPrePago.text() else int(self.txtPrePago.text())

                    query = """INSERT INTO registro_asistencia (
                        status,
                        fecha_calendario,
                        updated_on,
                        id_socio,
                        efectivo,
                        proteina,
                        fibra,
                        aloe,
                        te,
                        batido,
                        rebuild,
                        drive,
                        lift_off,
                        pre_pago,
                        fila,
                        consumido,
                        sobre_rojo,
                        insumos,
                        descuento,
                        mayoreo,
                        sobre_verde)
                        VALUES
                        ('%s','%s','%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);""" \
                            % (status, fecha_calendario, fechahoy, id_socio, efectivo,
                               listaextras.count("Proteina"),
                               listaextras.count("Fibra"),
                               aloe,
                               te,
                               batido,
                               listaextras.count("Rebuild"),
                               listaextras.count("Drive"),
                               listaextras.count("Waffle"),
                               pre_pago,
                               fila,
                               consumido,
                               sobre_rojo,
                               insumos,
                               descuento,
                               mayoreo,
                               sobre_verde)
                    # print query
                    # print "399: esClienteDe: %s" % esClienteDe
                    BD.interAct(query)
                    self.clearform()
                    self.filltable(str(self.cboOperador.currentText()))
                    self.updatereporte(operador)
                    self.fillstatics(str(self.cboOperador.currentText()))

                if self.tabMain.tabText(self.tabMain.currentIndex()) == "Asistencia Personal":
                    self.tblAsistenciaPersonal.clearContents()
                    fecha_desde = str(QDate.toString(
                        self.calAsisteDesde.date(), "yyyy-MM-dd"))
                    fecha_hasta = str(QDate.toString(
                        self.calAsisteHasta.date(), "yyyy-MM-dd"))
                    nombre_col = ['Dia', 'Fecha', 'PrePago', 'Efectivo', 'Vendido',
                                  'S.Rojo', 'Insumos', 'Descuento', 'Mayoreo', 'S.Verde']
                    ancho_col = {
                        'Dia': 80,
                        'Fecha': 80,
                        'Proteina': 25,
                        'Fibra': 25,
                        'Batido': 25,
                        'Te': 25,
                        'Aloe': 25,
                        'LiftOff': 25,
                        'Rebuild': 25,
                        'Drive': 25,
                        'PrePago': 25,
                        'Efectivo': 40,
                        'Vendido': 35,
                        'S.Rojo': 35,
                        'Insumos': 35,
                        'Descuento': 35,
                        'Mayoreo': 35,
                        'S.Verde': 35
                    }

                    query = f"""SELECT
                                    fecha_calendario,
                                    pre_pago,
                                    efectivo,
                                    consumido,
                                    sobre_rojo,
                                    insumos,
                                    descuento,
                                    mayoreo,
                                    sobre_verde
                                FROM
                                    registro_asistencia
                                WHERE
                                    id_socio={id_socio} and fecha_calendario between '{fecha_desde}' and '{fecha_hasta}'
                                ORDER BY
                                    fecha_calendario DESC
                                """  # % (id_socio, fecha_desde, fecha_hasta)
                    lista_asistencia = BD.interAct(query)
                    # self.tblAsistenciaPersonal.setHorizontalHeader(RotatedHeaderView(self.tblAsistenciaPersonal))
                    self.tblAsistenciaPersonal.setColumnCount(len(nombre_col))
                    self.tblAsistenciaPersonal.setRowCount(
                        len(lista_asistencia))
                    for nombre in nombre_col:  # con este for dibujamos la tabla
                        col_index = nombre_col.index(nombre)
                        self.tblAsistenciaPersonal.setHorizontalHeaderItem(
                            col_index, QTableWidgetItem(nombre))
                        self.tblAsistenciaPersonal.setColumnWidth(
                            col_index, ancho_col[nombre])

                        for fila in lista_asistencia:
                            fila_index = lista_asistencia.index(fila)
                            diaDeSemana = datetime.datetime.strptime(
                                fila[0], '%Y-%m-%d').strftime('%A').capitalize()
                            # print('fila', fila)
                            item = diaDeSemana if col_index == 0 else fila[col_index - 1]
                            # print('col_index', col_index, 'fila_index', fila_index, 'item:', item)
                            # if str(item[col]) != "0" and str(item[col]) != "None":
                            self.tblAsistenciaPersonal.setItem(
                                fila_index, col_index, QTableWidgetItem(str(item)))
                        # fila += 1
                    # for item in func.consumo_personal(id_socio):

                    query = f"""SELECT
                                    sum(efectivo),
                                    sum(sobre_rojo),
                                    sum(mayoreo),
                                    sum(aloe),
                                    sum(te),
                                    sum(batido),
                                    sum(fibra)
                                FROM
                                    registro_asistencia
                                WHERE
                                    id_socio={id_socio} and fecha_calendario BETWEEN '{fecha_desde}' AND '{fecha_hasta}'
                                    """  # % (id_socio, fecha_desde, fecha_hasta)

                    for item in BD.interAct(query):
                        print("linea 721: efectivo = %.1f" % item[0])
                        print("sobre_rojo = %.1f" % item[1])
                        print("mayoreo = %.1f" % item[2])
                        print("Aloe: %s, Te: %s, Batido: %s, Fibra:%s" %
                              (item[3], item[4], item[5], item[6]))

                if self.tabMain.tabText(self.tabMain.currentIndex()) == "Referidos":
                    self.tblReferidos.clear()
                    ancho_col, nombre_col = [70, 140], ['Fecha', 'Nombre']

                    referidos = f"""SELECT
                                    InsertedOn,
                                    nombre,
                                    apellido
                                FROM
                                    registro_socios
                                WHERE
                                    referidor={id_socio}
                                ORDER BY
                                    InsertedOn
                                DESC
                                    """  # % (id_socio)
                    lista_referidos = BD.interAct(referidos)
                    self.tblReferidos.setRowCount(len(lista_referidos))
                    self.tblReferidos.setColumnCount(len(nombre_col))
                    for nombre in nombre_col:  # con este for dibujamos la tabla
                        col_index = nombre_col.index(nombre)
                        self.tblReferidos.setColumnWidth(
                            col_index, ancho_col[col_index])
                        self.tblReferidos.setHorizontalHeaderItem(
                            col_index, QTableWidgetItem(nombre))

                        for referido in lista_referidos:  # con este for cargamos los datos de la lista a la tabla
                            fila_index = lista_referidos.index(referido)
                            nombre_completo = "%s %s" % (
                                referido[1], referido[2])
                            item = nombre_completo if col_index == 1 else referido[col_index]
                            self.tblReferidos.setItem(
                                fila_index, col_index, QTableWidgetItem(item))
##################### PESTAÑA DE COTIZADOR ############################################
                if self.tabMain.tabText(self.tabMain.currentIndex()) == "Cotizador":
                    productos = ['Aloe', 'Te', 'Batido']

            else:
                self.tblAsistenciaPersonal.clearContents()
                self.tblReferidos.clearContents()

    def on_btnProductos_clicked(self):
        sender = self.sender().text()
        self.lstProductos.addItem(sender)
        print(sender)

    def on_txtNombre_text_changed(self, texto):
        global status
        global fullname
        resultado = list()
        # print texto

        if texto:
            query = f"""
                SELECT DISTINCT
                    nombre,
                    apellido,
                    id_socio,
                    operador,
                    Referidor,
                    registro_socios.id
                FROM
                    registro_socios
                LEFT JOIN
                    (SELECT id_socio, count(*) AS numero FROM registro_asistencia GROUP BY id_socio) AS idt
                ON registro_socios.id = idt.id_socio
                WHERE
                    registro_socios.nombre
                LIKE
                    '%{texto}%'
                ORDER BY idt.numero DESC
                """  # % texto

            rows = BD.interAct(query)
            # print('rows', rows)
            if rows:
                for row in rows:
                    fullname = "%s %s" % (row[0], row[1])
                    dic_asistencia[str(fullname)] = row[2]
                    esClienteDe[str(fullname)] = row[3]
                    dic_referidor[str(fullname)] = row[4]
                    dic_id_socio[str(fullname)] = row[5]
                    resultado.append(fullname)
                    model.setStringList(resultado)

            else:
                fullname = str(texto)
                try:
                    if dic_asistencia[fullname] is None:
                        status = 'N' if esClienteDe[fullname] == dic_referidor[fullname] else 'R'
                    else:
                        status = ''

                    self.lstExtras.clear()
                    self.lstExtras.addItem("Basica")
                    self.chkPrePago.setEnabled(True)
                    self.txtTotal.setText(str(self.sumatoria()))

                except KeyError as e:
                    print('I got a KeyError - reason "%s"' % str(e))
        else:
            self.lstExtras.clear()
            self.chkPrePago.setEnabled(False)
            self.txtTotal.clear()

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
        self.txtBloque.clear()

    def clearlabels(self):
        self.lblNomSem.clear()
        self.lblConsumos.clear()
        self.lblSobreRojo.clear()
        self.lblVendido.clear()
        self.lblSobreVerde.clear()
        self.lblMayoreo.clear()
        self.lblEfectivo.clear()
        self.lblInsumos.clear()
        self.lblDescuento.clear()
        # self.lblDetalle.clear()
        #
        dic_id_socio.clear()
        esClienteDe.clear()
        dic_referidor.clear()
        dic_asistencia.clear()

    def filltable(self, operador):
        self.tblAsistenciaGeneral.clearContents()
        condicion = "" if operador == "CLUB" else " AND operador=%s" % esOperador[operador]
        query = """
        SELECT
            registro_asistencia.status,
            registro_socios.Nombre,
            registro_socios.Apellido,
            registro_asistencia.pre_pago,
            registro_asistencia.efectivo,
            registro_asistencia.consumido,
            registro_asistencia.sobre_rojo,
            registro_asistencia.insumos,
            registro_asistencia.descuento,
            registro_asistencia.mayoreo,
            registro_asistencia.sobre_verde,
            registro_asistencia.fila
        FROM
            registro_socios
            LEFT JOIN registro_asistencia ON registro_asistencia.id_socio = registro_socios.id
        WHERE
            fecha_calendario='%s'%s;""" % (fecha_calendario, condicion)
        # print query

        Registros = BD.interAct(query)
        # print(Registros)
        for Registro in Registros:
            item = 0
            row = int(Registro[11])
            fullname = str(Registro[1] + " " + Registro[2])
            for col in range(self.tblAsistenciaGeneral.columnCount()):
                # print('Registro',Registro[item])
                if col == 1:
                    self.tblAsistenciaGeneral.setItem(
                        row, col, QTableWidgetItem(fullname))
                    item += 2
                else:
                    # if col == 11:
                    #     self.tblAsistenciaGeneral.setItem(row, col, QTableWidgetItem(str(Registro[item])))
                    if str(Registro[item]) != "0" and str(Registro[item]) != "None":
                        self.tblAsistenciaGeneral.setItem(
                            row, col, QTableWidgetItem(str(Registro[item])))
                    item += 1

    def fillstatics(self, operador):
        condicion = "" if operador == "CLUB" else " AND id_operador=%s" % esOperador[
            operador]
        query = f"""
                SELECT
                    ifnull(sum(consumos_totales),0) as consumos_totales,
                    ifnull(sum(consumido),0) as vendido,
                    ifnull(sum(sobre_rojo),0) as sobre_rojo,
                    ifnull(sum(insumos),0) as insumos,
                    ifnull(sum(descuento),0) as descuento,
                    ifnull(sum(mayoreo),0) as mayoreo,
                    ifnull(sum(sobre_verde),0) as SVerde,                    
                    ifnull(sum(efectivo),0) as efectivo
                FROM
                    reporte_mensual
                WHERE
                    fecha_calendario='{fecha_calendario}'{condicion};"""  # % (fecha_calendario, condicion)
        # print query
        self.lblNomSem.setText(nombreDia)
        for item in BD.interAct(query):
            self.lblConsumos.setText(str(item[0]))
            self.lblVendido.setText(str("%.1f" % item[1]))
            self.lblSobreRojo.setText(str(
                "<html><body><p><span style=\" color:#aa0000;\">%.1f</span></p></body></html>" % item[2]))
            self.lblInsumos.setText(str("%.1f" % item[3]))
            self.lblDescuento.setText(str("%.1f" % item[4]))
            self.lblMayoreo.setText(str("%.1f" % item[5]))
            self.lblSobreVerde.setText(str(
                "<html><body><p><span style=\" color:#55aa00;\">%.1f</span></p></body></html>" % item[6]))
            self.lblEfectivo.setText(str("%.1f" % item[7]))
        formatFecha = fecha_calendario.replace('-', '')
        noSem = QDate.weekNumber(QDate.fromString(formatFecha, "yyyyMMdd"))
        Anho = QDate.year(self.calFecha.date())
        query = """
                SELECT
                    fechaDesde,
                    fechaHasta
                FROM
                    reporte_semanal
                WHERE
                    noSem='%s'
                AND
                    fechaDesde LIKE '%s%%';""" % (noSem[0], Anho)
        for fecha in BD.interAct(query):
            query = """
                    SELECT
                        ifnull(sum(consumos_totales)/7.0,0) as promedio_consumos,
                        ifnull(sum(sobre_verde),0) as SVerde,
                        ifnull(sum(efectivo),0) as efectivo,
                        ifnull(sum(referidos),0) as referidos,
                        ifnull(sum(consumo_personal),0) as consumo_personal
                    FROM
                        reporte_mensual
                    WHERE
                        fecha_calendario >= '%s' 
                    AND 
                        fecha_calendario <'%s'%s;""" % (str(fecha[0]), str(fecha[1]), condicion)
            # print query
            for item in BD.interAct(query):
                self.lblDetalle.setText("""Sem #%s | Del: %s Al: %s | Promedio: %.1f | Ganancia: %.1f | Efectivo: %.1f | Referidos: %.1f | Consumo Personal: %.1f
                """ % (noSem[0], fecha[0], fecha[1], item[0], item[1], item[2], item[3], item[4]))

    def updatereporte(self, id_operador):

        efectivo, consumido, sobre_rojo, insumos, \
            descuento, mayoreo, sobre_verde, consumos_totales = 0, 0, 0, 0, 0, 0, 0, 0

        query = """
                        SELECT
                            ifnull(sum(efectivo),0) as efectivo,
                            ifnull(sum(consumido),0) as cosumido,
                            ifnull(sum(sobre_rojo),0) as sobre_rojo,
                            ifnull(sum(insumos),0) as insumos,
                            ifnull(sum(descuento),0) as descuento,
                            ifnull(sum(mayoreo),0) as mayoreo,
                            ifnull(sum(sobre_verde),0) as sobre_verde,
                            ifnull(count(),0) as consumos_totales
                            
                        FROM
                            operador
                        WHERE
                            fecha_calendario='%s' AND operador=%s""" % (fecha_calendario, id_operador)
        for item in BD.interAct(query):
            efectivo = item[0]
            consumido = item[1]
            sobre_rojo = item[2]
            insumos = item[3]
            descuento = item[4]
            mayoreo = item[5]
            sobre_verde = item[6]
            consumos_totales = item[7]
            # TODO: revisar la variable insumos

        nuevos = f"""SELECT
                        ifnull(count(),0)
                    FROM
                        operador
                    WHERE
                        fecha_calendario='{fecha_calendario}'
                    AND
                        status='N'
                    AND
                        operador={id_operador}"""  # % (fecha_calendario, id_operador)

        referidos = f"""SELECT
                            ifnull(count(),0)
                        FROM
                            operador
                        WHERE
                            fecha_calendario='{fecha_calendario}'
                        AND
                            status='R'
                        AND
                            operador={id_operador}"""  # % (fecha_calendario, id_operador)

        consumo_personal = f"""SELECT
                                    ifnull(sum(sobre_rojo),0)
                                FROM
                                    operador
                                WHERE
                                    fecha_calendario='{fecha_calendario}'
                                AND
                                    id_socio={id_operador}"""  # % (fecha_calendario, id_operador)
        # print "Ganancia es %s si el operador es %s" % (porGanancia, id_operador)
        # TODO: eliminar sobre_rojo_real y sobre_verde_real
        # TODO: agregar mayoreo y efectivo
        query = f"""UPDATE reporte_mensual SET
        consumos_nuevos = ({nuevos}),
        referidos = ({referidos}),
        consumo_personal = ({consumo_personal}),
        consumos_totales = {consumos_totales},
        efectivo = {efectivo},
        consumido = {consumido},
        sobre_rojo = {sobre_rojo},
        descuento = {descuento},
        sobre_verde = {sobre_verde},
        insumos = {insumos},
        mayoreo = {mayoreo}
        WHERE
        fecha_calendario = '{fecha_calendario}'
        AND
        id_operador = {id_operador}"""

        BD.interAct(query)
        # print query
        query = f"""
            INSERT INTO
                reporte_mensual (
                fecha_calendario,
                Semana,
                consumos_nuevos,
                referidos,
                consumos_totales,
                consumo_personal,
                sobre_verde,
                consumido,
                sobre_rojo,
                insumos,
                descuento,
                mayoreo,
                efectivo,
                id_operador)
            SELECT
                '{fecha_calendario}',
                '{nombreDia}',
                ({nuevos}),
                ({referidos}),
                {consumos_totales},
                ({consumo_personal}),
                {sobre_verde},
                {consumido},
                {sobre_rojo},
                {insumos},
                {descuento},
                {mayoreo},
                {efectivo},
                {id_operador}
            WHERE NOT EXISTS
                (SELECT changes() AS change FROM reporte_mensual WHERE change <> 0)"""  # \
        # % (fecha_calendario,
        #    nombreDia,
        #    nuevos,
        #    referidos,
        #    consumos_totales,
        #    consumo_personal,
        #    sobre_verde,
        #    consumido,
        #    sobre_rojo,
        #    insumos,
        #    descuento,
        #    mayoreo,
        #    efectivo,
        #    id_operador)
        BD.interAct(query)

    def update_reporte_semanal(self): pass
    # TODO: codigo para llenar el reporte semanal (hoja azul)

    def on_tblAsistenciaGeneral_dblClicked(self):
        global id_operador
        fecha_hoy = str(QDate.toString(QDate.currentDate(), "yyyy-MM-dd"))
        col_number = self.tblAsistenciaGeneral.currentColumn()
        print(col_number)
        if self.tblAsistenciaGeneral.horizontalHeaderItem(
                col_number).text() == 'Nombre':
            # if fecha_calendario == fecha_hoy:
            fila = self.tblAsistenciaGeneral.currentRow()
            # print('fila que quitaste', fila)
            for col in range(self.tblAsistenciaGeneral.columnCount()):
                self.tblAsistenciaGeneral.takeItem(fila, col)
            query = """
                SELECT
                    operador
                FROM
                    registro_socios
                LEFT JOIN
                    registro_asistencia ON registro_asistencia.id_socio = registro_socios.id
                WHERE
                    fila=%s and fecha_calendario='%s';""" % (fila, fecha_calendario)
            for item in BD.interAct(query):
                id_operador = item[0]
                query = """
                    DELETE FROM
                        registro_asistencia
                    WHERE fila='%s' AND fecha_calendario='%s';""" % (fila, fecha_calendario)
                BD.interAct(query)
                query = """
                    DELETE FROM registro_consumos
                    WHERE fila_nro={}
                    AND inserted_on='{}';
                """.format(fila, fecha_calendario)
                BD.interAct(query)
                self.clearform()
                self.filltable(str(self.cboOperador.currentText()))
                self.updatereporte(id_operador)
                self.fillstatics(str(self.cboOperador.currentText()))
