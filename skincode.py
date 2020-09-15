#!/usr/bin/env python

import skin
import urllib
import os
from PyQt4.QtGui import *
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
# from email.mime.text import MIMEText

class Registro(QDialog, skin.Ui_Form):
    def __init__(self, parent=None):
        super(Registro, self).__init__(parent)
        self.setupUi(self)
        self.dibujartablas()
        self.connectActions()

    def connectActions(self):
        self.btnGuardar.clicked.connect(self.on_control_buttons_clicked)
        self.btnSalir.clicked.connect(self.on_control_buttons_clicked)
        self.txtReferidor.textChanged.connect(self.on_txtReferidor_change)

    def on_txtReferidor_change(self):
        state = True if self.txtReferidor.text() else False
        self.tblReferidos.setEnabled(state)

    def dibujartablas(self):
        headers = ['Nombre', 'Apellido', 'Celular', 'Relacion']
        # ancho = [70, 70, 70]
        self.tblReferidos.setRowCount(15)
        self.tblReferidos.setColumnCount(len(headers))
        n = 0
        for colname in headers:
            item = QTableWidgetItem()
            self.tblReferidos.setHorizontalHeaderItem(n, item)
            self.tblReferidos.setColumnWidth(n, 70)
            head = self.tblReferidos.horizontalHeaderItem(n)
            head.setText(colname)
            n += 1

    def crear_archivo(self):
        referidor = str(self.txtReferidor.text()).title()
        if referidor:
            for row in range(self.tblReferidos.rowCount()):
                if self.tblReferidos.item(row, 0) is not None:
                    nombre = str(self.tblReferidos.item(row, 0).text()).capitalize()
                    apellido = str(self.tblReferidos.item(row, 1).text()).capitalize()
                    nombrecompleto = '%s %s' % (nombre, apellido)
                    celular = self.tblReferidos.item(row, 2).text()
                    relacion = str(self.tblReferidos.item(row, 3).text()).capitalize()
                    query = """BEGIN:VCARD\nVERSION:2.1\nN:%s;%s;;;\nFN:%s\nTEL;CELL:%s\nX-ANDROID-CUSTOM:vnd.android.cursor.item/relation;%s;0;%s;;;;;;;;;;;;\nEND:VCARD\n""" % (apellido, nombre, nombrecompleto, celular, referidor, relacion)
                    print query
                    filename = '%s.vcf' % referidor
                    file = open(filename, 'a+')
                    file.write(query)
                    file.close()
            if self.chksendmail.isChecked():
                con = self.check_connection()
                if con:
                    print "hay coneccion"
                    self.send_email(filename)
                else:
                    print "Revise su coneccion a internet"
        else:
            print "Falta el Nombre del referidor"

    def on_control_buttons_clicked(self):
        sender = self.sender().objectName()
        if sender == 'btnGuardar':
            self.crear_archivo()
            # self.tblReferidos.clearContents()
        else:
            self.tblReferidos.clearContents()
            self.close()

    def check_connection(self):
        os.system('wget -O index.html -c https://www.dropbox.com/s/fquktkoz39g3tme/index.html?dl=0')
        con = True if os.path.isfile('index.html') and os.path.getsize('index.html') > 0 else False
        os.system('rm index.html')
        return con

    def send_email(self, filename):

        fromaddr = "marcelo.llosa.m@gmail.com"
        toaddr = "marcelo.llosa.m@gmail.com"

        msg = MIMEMultipart()

        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "%s LISTA DE CONTACTOS" % filename

        body = "Correo automatico..."

        msg.attach(MIMEText(body, 'plain'))

        attachment = open(filename, "rb")

        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

        msg.attach(part)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, "molochete")
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()
        os.system('rm %s' % filename)
