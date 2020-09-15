# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from datetime import date
import AgregarSocio, DB_Class
import db_func
# import postgres_db as sql #coneccion a base de datos postgresql en linea

class AddSocio(QDialog, AgregarSocio.Ui_Contacto):
    def __init__(self, parent=None):
        super(AddSocio, self).__init__(parent)
        self.setupUi(self)
        self.connectActions()
        self.valIniciales()

    def valIniciales(self):
        global Buscar
        global BD
        global id
        global FechaHoy
        global dicPares
        global dicReferidor
        global dicOperador
        global model
        global func
        id = ""
        dicReferidor = dict()
        dicOperador = dict()
        dicPares = dict()
        model = QStringListModel()
        completer = QCompleter()
        completer.setModel(model)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        #
        self.txtReferidor.setCompleter(completer)
        # self.txtOperador.setCompleter(completer)
        # self.txtApellido.setCompleter(completer)
        #
        FechaHoy = str(QDate.toString(QDate.currentDate(), "yyyy-MM-dd"))
        # importamos el modulo de la base de datos
        BD = DB_Class.dataBase()
        # creamos la conexion a la base de datos
        BD.createCon()
        #
        func = db_func.reporte()
        #
        
        #
        Buscar = True
        self.cboOperador.clear()
        self.cboOperador.addItem('-SELECCIONAR-')
        for row in func.operadores_club():
            fullName = "%s %s" % (row[1], row[2])
            dicOperador[str(fullName)] = row[0]
            self.cboOperador.addItem(fullName)
            ###


        self.cboContacto1.addItem("Movil")

        self.cboRelacion.addItem("Amig@")
        self.cboRelacion.addItem("Herman@")
        self.cboRelacion.addItem("Personalizar")

        self.btnGuardar.setEnabled(False)
        self.txtReferidor.clear()
        self.txtNombre.clear()
        self.txtApellido.clear()
        self.txtContacto1.clear()
        self.txtContacto2.clear()
        self.lblFecha.clear()

    def connectActions(self):
        self.txtNombre.textChanged.connect(self.on_txt_nombre_apellido_changed)
        self.txtApellido.textChanged.connect(self.on_txt_nombre_apellido_changed)
        self.txtContacto1.textChanged.connect(self.on_txt_dato_changed)
        self.txtContacto2.textChanged.connect(self.on_txt_dato_changed)
        self.cboRelacion.currentIndexChanged.connect(self.on_cboRelacion_changed)

        self.lst_Socios.clicked.connect(self.lst_Socios_Clicked)
        self.btnLimpiar.clicked.connect(self.clear_form)
        self.btnGuardar.clicked.connect(self.btnGuardar_Clicked)
        self.btnSalir.clicked.connect(self.on_btnsalir_clicked)

        self.txtReferidor.textChanged.connect(self.on_txtreferidor_changed)
        self.cboOperador.currentIndexChanged.connect(self.on_cboOperador_changed)
        # self.txtOperador.textChanged.connect(self.on_txtreferidor_changed)

    def on_cboRelacion_changed(self):
        if self.cboRelacion.currentText() == 'Personalizar':
            text, ok = QInputDialog.getText(self, 'Etiqueta Perzonalizada', '')
            self.cboRelacion.clear()
            if ok:
                self.cboRelacion.addItem(str(text).title())
                self.cboRelacion.addItem("Personalizar")
            else:
                self.cboRelacion.addItem("Amig@")
                self.cboRelacion.addItem("Herman@")
                self.cboRelacion.addItem("Personalizar")

    def on_cboOperador_changed(self):
        self.verificar_form()

    def on_txtreferidor_changed(self):
        resultado = list()
        # sender = self.sender().objectName()
        texto = self.sender().text()

        if texto:
            query = """SELECT 
                            id,     
                            Nombre, 
                            Apellido 
                        FROM 
                            registro_socios
                        WHERE 
                            Nombre
                        LIKE 
                            '%s%%'""" % texto
            rows = BD.interAct(query)
            for row in rows:
                Resultado = "%s %s" % (row[1], row[2])
                dicPares[str(Resultado)] = row[0]
                resultado.append(Resultado)
                model.setStringList(resultado)
        self.verificar_form()
            # print dicPares

    def on_txt_dato_changed(self):
        criterio = self.sender().text()
        self.lst_Socios.clear()
        if criterio:
            query = """
                SELECT
                    registro_socios.id as Id,
                    registro_socios.Nombre as Nombre,
                    registro_socios.Apellido as Apellido,
                    registro_contacto.Dato as Dato,
                    registro_contacto.Tipo as Tipo
                FROM
                    registro_contacto
                LEFT JOIN registro_socios on registro_contacto.IdSocio = registro_socios.id
                where Dato like '%s%%';""" % criterio
            rows = BD.interAct(query)
            for row in rows:
                resultado = "%s %s" % (row[1], row[2])
                dicPares[str(resultado)] = row[0]
                self.lst_Socios.addItem(resultado)

    def on_txt_nombre_apellido_changed(self):

        sender = self.sender().objectName()
        criterio = str(self.sender().text())

        if Buscar:
            condicion = sender[3:]
            # if sender == "txtNombre": condicion = "Nombre"
            # if sender == "txtApellido": condicion = "Apellido"
            # if sender == "txtContacto1": condicion = "Cel1"
            self.lst_Socios.clear()
            self.verificar_form()
            if criterio:
                # pg_query = "SELECT id, nombre_completo, referidor_id FROM socios_socio WHERE nombre_completo LIKE '%s%%'" % (criterio.upper())
                # print('pg_query: ', pg_query)

                query = """SELECT
                                id,
                                Nombre,
                                Apellido,
                                referidor
                            FROM 
                                registro_socios    
                            WHERE 
                                %s 
                            LIKE
                                '%s%%'""" % (condicion, criterio)
                rows = BD.interAct(query)
                for row in rows:
                    resultado = "%s %s" % (row[1], row[2])
                    dicPares[str(resultado)] = row[0]
                    self.lst_Socios.addItem(resultado)
                    print('id: ', row[0], 'nombre_completo', resultado, 'referidor_id', row[3])


                # pg_rows = sql.connect(pg_query)
                # print('pg_rows: ', pg_rows)
                # for row in pg_rows:
                #     resultado = row[1]
                #     dicPares[str(resultado)] = row[0]
                #     self.lst_Socios.addItem(resultado)
                #     print('id: ', row[0], 'nombre_completo', resultado, 'referidor_id', row[2])

    def lst_Socios_Clicked(self):
        global id
        global Buscar

        id = dicPares[str(self.lst_Socios.currentItem().text())]
        query = """SELECT
                        registro_socios.InsertedOn as Fecha,
                        registro_socios.Referidor as Referidor,
                        registro_socios.Operador as Operador,
                        registro_socios.Nombre as Nombre,
                        registro_socios.Apellido as Apellido,
                        registro_contacto.Dato as Dato,
                        registro_contacto.Tipo as Tipo
                    FROM
                        registro_socios
                        LEFT JOIN registro_contacto ON registro_contacto.IdSocio = registro_socios.id
                    WHERE
                        registro_socios.id=%s;""" % id
        # query = "SELECT Referidor, Nombre, Apellido, Cumple, Operador FROM registro_socios WHERE id ='%s'" % id
        # lista = BD.interAct(query)
        # print lista
        Buscar = False
        for item in BD.interAct(query):
            msg = "Registrado el: %s" % item[0] if item[0] != '' else "No tiene fecha de Registro"
            self.lblFecha.setText(msg)
            referidor = item[1]
            operador = item[2]
            self.txtNombre.setText(item[3])
            self.txtApellido.setText(item[4])
            # self.txtContacto2.setText(item[3])
        # query = "SELECT Dato, Tipo FROM registro_contacto WHERE IdSocio ='%s'" % id
        # lista = BD.interAct(query)
        # for item in lista:
            if item[5] is not None: self.txtContacto1.setText(item[5])
            if item[6] is not None:
                self.cboContacto1.clear()
                self.cboContacto1.addItem(item[6])

        query = "SELECT Nombre, Apellido FROM registro_socios WHERE id ='%s'" % referidor
        lista = BD.interAct(query)
        for item in lista:
            nombrecompleto = "%s %s" % (item[0], item[1])
            dicPares[nombrecompleto] = referidor
            self.txtReferidor.setText(nombrecompleto)
        query = "SELECT Nombre, Apellido FROM registro_socios WHERE id ='%s'" % operador
        lista = BD.interAct(query)
        for item in lista:
            nombrecompleto = "%s %s" % (item[0], item[1])
            dicPares[nombrecompleto] = operador
            #self.txtOperador.setText(nombrecompleto)
            self.cboOperador.clear()
            self.cboOperador.addItem(nombrecompleto)
        Buscar = True
        self.lst_Socios.clear()
        self.btnGuardar.setEnabled(False)
        # print "Lista: %s" % lista

    def btnGuardar_Clicked(self):
        nombre = self.txtNombre.text().upper()
        apellido = self.txtApellido.text().upper()
        idreferidor = dicPares[str(self.txtReferidor.text())]
        idoperador = dicOperador[str(self.cboOperador.currentText())]
        cumple = str(self.txtContacto2.text())
        nombre_completo = nombre + ' ' + apellido
        # variables de la base postgre
        genero = 'MASCULINO'
        key_code = ''
        edited_on = date.today()
        activo = True
        # print('nombre_completo', nombre_completo) 
        if id:
            query = """UPDATE registro_socios SET
                Nombre='%s',
                Apellido='%s',
                Referidor='%s',
                Operador='%s',
                Cumple='%s' WHERE id=%s""" % (nombre, apellido, idreferidor, idoperador, cumple, id)

        else:
            FechaHoy = date(2019,12,6)
            pg_query = "INSERT INTO public.socios_socio (nombre_completo, inserted_on, referidor_id, anfitrion_id, genero, key_code, edited_on, activo) VALUES ('%s','%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (nombre_completo, FechaHoy, idreferidor, idoperador, genero, key_code, edited_on, activo)

            query = """INSERT INTO registro_socios (
                Nombre,
                Apellido,
                Cumple,
                Referidor,
                Operador,
                InsertedOn)
                VALUES ('%s','%s','%s','%s','%s','%s');""" % (nombre, apellido, cumple, idreferidor, idoperador, FechaHoy)

            # (str(nombre.upper()), str(apellido.upper()), str(celular.upper()), str(mail.upper()), FechaHoy)
        BD.interAct(str(query))
        # for x in range(1024,1044):
            # print(x, '.- pg_query: ', pg_query)
        #sql.connect(pg_query)
        if self.txtContacto1.text():
            IdSocio = "SELECT id FROM registro_socios WHERE Nombre='%s' AND Apellido='%s'" % (nombre, apellido)
            query = """INSERT INTO registro_contacto (
                            IdSocio,
                            Dato,
                            Tipo)
                            VALUES ((%s), '%s', '%s');""" % (IdSocio, self.txtContacto1.text(), self.cboContacto1.currentText())
            # print query
            BD.interAct(str(query))

        # print query
        self.btnLimpiar.click()
        dicReferidor.clear()

    def clear_form(self):
        self.valIniciales()

    def verificar_form(self):
        state = False if self.txtNombre.text() == '' \
            or self.txtApellido.text() == '' \
            or self.txtReferidor.text() == '' \
            or self.cboOperador.currentText() == "-SELECCIONAR-" else True
        self.btnGuardar.setEnabled(state)

    def on_btnsalir_clicked(self):
        # BD.closeCon()
        self.close()
