# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'comanda_07mar18.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Engargolado(object):
    def setupUi(self, Engargolado):
        Engargolado.setObjectName("Engargolado")
        Engargolado.resize(864, 672)
        font = QtGui.QFont()
        font.setFamily("Ubuntu Condensed")
        Engargolado.setFont(font)
        self.tabMain = QtWidgets.QTabWidget(Engargolado)
        self.tabMain.setGeometry(QtCore.QRect(10, 40, 841, 631))
        self.tabMain.setObjectName("tabMain")
        self.tabEngargolado = QtWidgets.QWidget()
        self.tabEngargolado.setObjectName("tabEngargolado")
        self.tblAsistenciaGeneral = QtWidgets.QTableWidget(self.tabEngargolado)
        self.tblAsistenciaGeneral.setGeometry(QtCore.QRect(130, 10, 551, 501))
        self.tblAsistenciaGeneral.setObjectName("tblAsistenciaGeneral")
        self.tblAsistenciaGeneral.setColumnCount(0)
        self.tblAsistenciaGeneral.setRowCount(0)
        self.cboOperador = QtWidgets.QComboBox(self.tabEngargolado)
        self.cboOperador.setGeometry(QtCore.QRect(690, 80, 141, 27))
        self.cboOperador.setObjectName("cboOperador")
        self.layoutWidget = QtWidgets.QWidget(self.tabEngargolado)
        self.layoutWidget.setGeometry(QtCore.QRect(694, 10, 141, 61))
        self.layoutWidget.setObjectName("layoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.layoutWidget)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Ubuntu Condensed")
        font.setPointSize(11)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.lblNomSem = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lblNomSem.setFont(font)
        self.lblNomSem.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lblNomSem.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblNomSem.setObjectName("lblNomSem")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lblNomSem)
        self.txtBloque = QtWidgets.QTextEdit(self.tabEngargolado)
        self.txtBloque.setGeometry(QtCore.QRect(690, 380, 141, 171))
        self.txtBloque.setObjectName("txtBloque")
        self.line_3 = QtWidgets.QFrame(self.tabEngargolado)
        self.line_3.setGeometry(QtCore.QRect(10, 550, 821, 20))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.lblDetalle = QtWidgets.QLabel(self.tabEngargolado)
        self.lblDetalle.setGeometry(QtCore.QRect(10, 560, 821, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lblDetalle.setFont(font)
        self.lblDetalle.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lblDetalle.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblDetalle.setWordWrap(False)
        self.lblDetalle.setObjectName("lblDetalle")
        self.splitter_6 = QtWidgets.QSplitter(self.tabEngargolado)
        self.splitter_6.setGeometry(QtCore.QRect(690, 110, 141, 251))
        self.splitter_6.setOrientation(QtCore.Qt.Vertical)
        self.splitter_6.setObjectName("splitter_6")
        self.layoutWidget1 = QtWidgets.QWidget(self.splitter_6)
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.formLayout_2 = QtWidgets.QFormLayout(self.layoutWidget1)
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_5 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_5.setObjectName("label_5")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.lblConsumos = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lblConsumos.setFont(font)
        self.lblConsumos.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblConsumos.setObjectName("lblConsumos")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lblConsumos)
        self.layoutWidget2 = QtWidgets.QWidget(self.splitter_6)
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.formLayout_3 = QtWidgets.QFormLayout(self.layoutWidget2)
        self.formLayout_3.setContentsMargins(0, 0, 0, 0)
        self.formLayout_3.setObjectName("formLayout_3")
        self.label_6 = QtWidgets.QLabel(self.layoutWidget2)
        self.label_6.setObjectName("label_6")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.lblVendido = QtWidgets.QLabel(self.layoutWidget2)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lblVendido.setFont(font)
        self.lblVendido.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblVendido.setObjectName("lblVendido")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lblVendido)
        self.layoutWidget3 = QtWidgets.QWidget(self.splitter_6)
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.formLayout_4 = QtWidgets.QFormLayout(self.layoutWidget3)
        self.formLayout_4.setContentsMargins(0, 0, 0, 0)
        self.formLayout_4.setObjectName("formLayout_4")
        self.label_9 = QtWidgets.QLabel(self.layoutWidget3)
        self.label_9.setObjectName("label_9")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_9)
        self.lblSobreRojo = QtWidgets.QLabel(self.layoutWidget3)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lblSobreRojo.setFont(font)
        self.lblSobreRojo.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblSobreRojo.setObjectName("lblSobreRojo")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lblSobreRojo)
        self.layoutWidget4 = QtWidgets.QWidget(self.splitter_6)
        self.layoutWidget4.setObjectName("layoutWidget4")
        self.formLayout_9 = QtWidgets.QFormLayout(self.layoutWidget4)
        self.formLayout_9.setContentsMargins(0, 0, 0, 0)
        self.formLayout_9.setObjectName("formLayout_9")
        self.label_7 = QtWidgets.QLabel(self.layoutWidget4)
        self.label_7.setObjectName("label_7")
        self.formLayout_9.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.lblInsumos = QtWidgets.QLabel(self.layoutWidget4)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lblInsumos.setFont(font)
        self.lblInsumos.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblInsumos.setObjectName("lblInsumos")
        self.formLayout_9.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lblInsumos)
        self.layoutWidget5 = QtWidgets.QWidget(self.splitter_6)
        self.layoutWidget5.setObjectName("layoutWidget5")
        self.formLayout_5 = QtWidgets.QFormLayout(self.layoutWidget5)
        self.formLayout_5.setContentsMargins(0, 0, 0, 0)
        self.formLayout_5.setObjectName("formLayout_5")
        self.label_13 = QtWidgets.QLabel(self.layoutWidget5)
        self.label_13.setObjectName("label_13")
        self.formLayout_5.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_13)
        self.lblDescuento = QtWidgets.QLabel(self.layoutWidget5)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lblDescuento.setFont(font)
        self.lblDescuento.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblDescuento.setObjectName("lblDescuento")
        self.formLayout_5.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lblDescuento)
        self.layoutWidget6 = QtWidgets.QWidget(self.splitter_6)
        self.layoutWidget6.setObjectName("layoutWidget6")
        self.formLayout_6 = QtWidgets.QFormLayout(self.layoutWidget6)
        self.formLayout_6.setContentsMargins(0, 0, 0, 0)
        self.formLayout_6.setObjectName("formLayout_6")
        self.lblMayoreo = QtWidgets.QLabel(self.layoutWidget6)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lblMayoreo.setFont(font)
        self.lblMayoreo.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblMayoreo.setObjectName("lblMayoreo")
        self.formLayout_6.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lblMayoreo)
        self.label_8 = QtWidgets.QLabel(self.layoutWidget6)
        self.label_8.setObjectName("label_8")
        self.formLayout_6.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_8)
        self.layoutWidget7 = QtWidgets.QWidget(self.splitter_6)
        self.layoutWidget7.setObjectName("layoutWidget7")
        self.formLayout_7 = QtWidgets.QFormLayout(self.layoutWidget7)
        self.formLayout_7.setContentsMargins(0, 0, 0, 0)
        self.formLayout_7.setObjectName("formLayout_7")
        self.label = QtWidgets.QLabel(self.layoutWidget7)
        self.label.setObjectName("label")
        self.formLayout_7.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.lblSobreVerde = QtWidgets.QLabel(self.layoutWidget7)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lblSobreVerde.setFont(font)
        self.lblSobreVerde.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblSobreVerde.setObjectName("lblSobreVerde")
        self.formLayout_7.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lblSobreVerde)
        self.layoutWidget8 = QtWidgets.QWidget(self.splitter_6)
        self.layoutWidget8.setObjectName("layoutWidget8")
        self.formLayout_8 = QtWidgets.QFormLayout(self.layoutWidget8)
        self.formLayout_8.setContentsMargins(0, 0, 0, 0)
        self.formLayout_8.setObjectName("formLayout_8")
        self.label_10 = QtWidgets.QLabel(self.layoutWidget8)
        self.label_10.setObjectName("label_10")
        self.formLayout_8.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_10)
        self.lblEfectivo = QtWidgets.QLabel(self.layoutWidget8)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lblEfectivo.setFont(font)
        self.lblEfectivo.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblEfectivo.setObjectName("lblEfectivo")
        self.formLayout_8.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lblEfectivo)
        self.layoutWidget9 = QtWidgets.QWidget(self.tabEngargolado)
        self.layoutWidget9.setGeometry(QtCore.QRect(130, 520, 191, 27))
        self.layoutWidget9.setObjectName("layoutWidget9")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget9)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.chkPrePago = QtWidgets.QCheckBox(self.layoutWidget9)
        font = QtGui.QFont()
        font.setFamily("Ubuntu Condensed")
        self.chkPrePago.setFont(font)
        self.chkPrePago.setChecked(False)
        self.chkPrePago.setObjectName("chkPrePago")
        self.horizontalLayout.addWidget(self.chkPrePago)
        self.txtPrePago = QtWidgets.QLineEdit(self.layoutWidget9)
        self.txtPrePago.setEnabled(False)
        self.txtPrePago.setMaximumSize(QtCore.QSize(30, 30))
        self.txtPrePago.setBaseSize(QtCore.QSize(10, 10))
        self.txtPrePago.setInputMask("")
        self.txtPrePago.setObjectName("txtPrePago")
        self.horizontalLayout.addWidget(self.txtPrePago)
        self.cboPrePago = QtWidgets.QComboBox(self.layoutWidget9)
        self.cboPrePago.setEnabled(False)
        self.cboPrePago.setObjectName("cboPrePago")
        self.horizontalLayout.addWidget(self.cboPrePago)
        self.layoutWidget10 = QtWidgets.QWidget(self.tabEngargolado)
        self.layoutWidget10.setGeometry(QtCore.QRect(510, 520, 161, 27))
        self.layoutWidget10.setObjectName("layoutWidget10")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget10)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_4 = QtWidgets.QLabel(self.layoutWidget10)
        font = QtGui.QFont()
        font.setFamily("Ubuntu Condensed")
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.txtTotal = QtWidgets.QLineEdit(self.layoutWidget10)
        font = QtGui.QFont()
        font.setFamily("Ubuntu Condensed")
        self.txtTotal.setFont(font)
        self.txtTotal.setObjectName("txtTotal")
        self.horizontalLayout_2.addWidget(self.txtTotal)
        self.btnLimpiar = QtWidgets.QPushButton(self.layoutWidget10)
        self.btnLimpiar.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/Comanda/gnome_edit_clear.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnLimpiar.setIcon(icon)
        self.btnLimpiar.setObjectName("btnLimpiar")
        self.horizontalLayout_2.addWidget(self.btnLimpiar)
        self.btnGuardar = QtWidgets.QPushButton(self.layoutWidget10)
        font = QtGui.QFont()
        font.setFamily("Ubuntu Condensed")
        self.btnGuardar.setFont(font)
        self.btnGuardar.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("images/Comanda/media_floppy_green.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnGuardar.setIcon(icon1)
        self.btnGuardar.setObjectName("btnGuardar")
        self.horizontalLayout_2.addWidget(self.btnGuardar)
        self.layoutWidget11 = QtWidgets.QWidget(self.tabEngargolado)
        self.layoutWidget11.setGeometry(QtCore.QRect(10, 10, 111, 121))
        self.layoutWidget11.setObjectName("layoutWidget11")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget11)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.btnBasica = QtWidgets.QPushButton(self.layoutWidget11)
        self.btnBasica.setObjectName("btnBasica")
        self.verticalLayout.addWidget(self.btnBasica)
        self.lstExtras = QtWidgets.QListWidget(self.layoutWidget11)
        self.lstExtras.setObjectName("lstExtras")
        self.verticalLayout.addWidget(self.lstExtras)
        self.layoutWidget.raise_()
        self.layoutWidget.raise_()
        self.layoutWidget.raise_()
        self.splitter_6.raise_()
        self.tblAsistenciaGeneral.raise_()
        self.cboOperador.raise_()
        self.layoutWidget.raise_()
        self.txtBloque.raise_()
        self.line_3.raise_()
        self.lblDetalle.raise_()
        self.tabMain.addTab(self.tabEngargolado, "")
        self.tabAsistenciaPersonal = QtWidgets.QWidget()
        self.tabAsistenciaPersonal.setObjectName("tabAsistenciaPersonal")
        self.tblAsistenciaPersonal = QtWidgets.QTableWidget(self.tabAsistenciaPersonal)
        self.tblAsistenciaPersonal.setGeometry(QtCore.QRect(10, 10, 691, 521))
        self.tblAsistenciaPersonal.setObjectName("tblAsistenciaPersonal")
        self.tblAsistenciaPersonal.setColumnCount(0)
        self.tblAsistenciaPersonal.setRowCount(0)
        self.splitter = QtWidgets.QSplitter(self.tabAsistenciaPersonal)
        self.splitter.setGeometry(QtCore.QRect(710, 10, 111, 111))
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.label_11 = QtWidgets.QLabel(self.splitter)
        self.label_11.setObjectName("label_11")
        self.calAsisteDesde = QtWidgets.QDateEdit(self.splitter)
        self.calAsisteDesde.setObjectName("calAsisteDesde")
        self.label_12 = QtWidgets.QLabel(self.splitter)
        self.label_12.setObjectName("label_12")
        self.calAsisteHasta = QtWidgets.QDateEdit(self.splitter)
        self.calAsisteHasta.setObjectName("calAsisteHasta")
        self.tabMain.addTab(self.tabAsistenciaPersonal, "")
        self.tabReferidos = QtWidgets.QWidget()
        self.tabReferidos.setObjectName("tabReferidos")
        self.tblReferidos = QtWidgets.QTableWidget(self.tabReferidos)
        self.tblReferidos.setGeometry(QtCore.QRect(10, 10, 691, 521))
        self.tblReferidos.setObjectName("tblReferidos")
        self.tblReferidos.setColumnCount(0)
        self.tblReferidos.setRowCount(0)
        self.tabMain.addTab(self.tabReferidos, "")
        self.tabCotizador = QtWidgets.QWidget()
        self.tabCotizador.setObjectName("tabCotizador")
        self.lstProductos = QtWidgets.QListWidget(self.tabCotizador)
        self.lstProductos.setGeometry(QtCore.QRect(20, 50, 101, 401))
        self.lstProductos.setObjectName("lstProductos")
        self.lblTotal_Productos = QtWidgets.QLabel(self.tabCotizador)
        self.lblTotal_Productos.setGeometry(QtCore.QRect(20, 10, 101, 41))
        self.lblTotal_Productos.setObjectName("lblTotal_Productos")
        self.spinBox = QtWidgets.QSpinBox(self.tabCotizador)
        self.spinBox.setGeometry(QtCore.QRect(770, 20, 51, 33))
        self.spinBox.setObjectName("spinBox")
        self.btnBatido1 = QtWidgets.QPushButton(self.tabCotizador)
        self.btnBatido1.setGeometry(QtCore.QRect(140, 50, 89, 25))
        self.btnBatido1.setObjectName("btnBatido1")
        self.tabMain.addTab(self.tabCotizador, "")
        self.btnSalir = QtWidgets.QPushButton(Engargolado)
        self.btnSalir.setGeometry(QtCore.QRect(760, 10, 91, 27))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("images/Comanda/style5.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnSalir.setIcon(icon2)
        self.btnSalir.setObjectName("btnSalir")
        self.layoutWidget12 = QtWidgets.QWidget(Engargolado)
        self.layoutWidget12.setGeometry(QtCore.QRect(10, 0, 311, 36))
        self.layoutWidget12.setObjectName("layoutWidget12")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.layoutWidget12)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.lblNombre = QtWidgets.QLabel(self.layoutWidget12)
        font = QtGui.QFont()
        font.setFamily("Ubuntu Condensed")
        self.lblNombre.setFont(font)
        self.lblNombre.setObjectName("lblNombre")
        self.gridLayout_2.addWidget(self.lblNombre, 0, 0, 1, 1)
        self.btnNombre = QtWidgets.QPushButton(self.layoutWidget12)
        self.btnNombre.setMaximumSize(QtCore.QSize(30, 16777215))
        self.btnNombre.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("images/Comanda/Add User Group Woman Man-48.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnNombre.setIcon(icon3)
        self.btnNombre.setObjectName("btnNombre")
        self.gridLayout_2.addWidget(self.btnNombre, 0, 1, 1, 1)
        self.txtNombre = QtWidgets.QLineEdit(self.layoutWidget12)
        self.txtNombre.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Ubuntu Condensed")
        self.txtNombre.setFont(font)
        self.txtNombre.setObjectName("txtNombre")
        self.gridLayout_2.addWidget(self.txtNombre, 0, 2, 1, 1)
        self.lblHistorico = QtWidgets.QLabel(Engargolado)
        self.lblHistorico.setGeometry(QtCore.QRect(334, 10, 411, 21))
        self.lblHistorico.setObjectName("lblHistorico")
        self.btnSalir.raise_()
        self.layoutWidget.raise_()
        self.tabMain.raise_()
        self.lblHistorico.raise_()

        self.retranslateUi(Engargolado)
        self.tabMain.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Engargolado)

        productos = ['Proteina', 'Fibra', 'Waffle', 'Colageno', 'Drive',
                     'Rebuild', 'Aloe', 'Te', 'Batido', 'Jalea', 'Barra', 'Sopa']
        top = 140
        for producto in productos:
            self.btnProductos = QtWidgets.QPushButton(self.tabEngargolado)
            self.btnProductos.setGeometry(10, top, 109, 25)
            self.btnProductos.setText(producto)
            self.btnProductos.clicked.connect(self.on_extraButtons_clicked)
            top += 30

    def retranslateUi(self, Engargolado):
        _translate = QtCore.QCoreApplication.translate
        Engargolado.setWindowTitle(_translate("Engargolado", "Engargolado"))
        self.label_3.setText(_translate("Engargolado", "Fecha:"))
        self.lblNomSem.setText(_translate("Engargolado", "lblNomSem"))
        self.lblDetalle.setText(_translate("Engargolado", "TextLabel"))
        self.label_5.setText(_translate("Engargolado", "Consumos:"))
        self.lblConsumos.setText(_translate("Engargolado", "CON"))
        self.label_6.setText(_translate("Engargolado", "Vendido:"))
        self.lblVendido.setText(_translate("Engargolado", "TVE"))
        self.label_9.setText(_translate("Engargolado", "Rojo :"))
        self.lblSobreRojo.setText(_translate("Engargolado", "<html><head/><body><p><span style=\" color:#aa0000;\">SRO</span></p></body></html>"))
        self.label_7.setText(_translate("Engargolado", "Insumos :"))
        self.lblInsumos.setText(_translate("Engargolado", "INS"))
        self.label_13.setText(_translate("Engargolado", "Descuento:"))
        self.lblDescuento.setText(_translate("Engargolado", "<html><head/><body><p><span style=\" color:#ff0000;\">DTO</span></p></body></html>"))
        self.lblMayoreo.setText(_translate("Engargolado", "<html><head/><body><p>MAY</p></body></html>"))
        self.label_8.setText(_translate("Engargolado", "Mayoreo:"))
        self.label.setText(_translate("Engargolado", "Verde :"))
        self.lblSobreVerde.setText(_translate("Engargolado", "<html><head/><body><p><span style=\" color:#55aa00;\">SVE</span></p></body></html>"))
        self.label_10.setText(_translate("Engargolado", "Efectivo:"))
        self.lblEfectivo.setText(_translate("Engargolado", "<html><head/><body><p><span style=\" color:#00aa00;\">EFE</span></p></body></html>"))
        self.chkPrePago.setText(_translate("Engargolado", "PrePago:"))
        self.label_4.setText(_translate("Engargolado", "a Pagar:"))
        self.btnLimpiar.setToolTip(_translate("Engargolado", "Limpiar"))
        self.btnGuardar.setToolTip(_translate("Engargolado", "Guardar"))
        self.btnBasica.setText(_translate("Engargolado", "Basica"))
        self.tabMain.setTabText(self.tabMain.indexOf(self.tabEngargolado), _translate("Engargolado", "Engargolado"))
        self.label_11.setText(_translate("Engargolado", "Desde:"))
        self.label_12.setText(_translate("Engargolado", "Hasta:"))
        self.tabMain.setTabText(self.tabMain.indexOf(self.tabAsistenciaPersonal), _translate("Engargolado", "Asistencia Personal"))
        self.tabMain.setTabText(self.tabMain.indexOf(self.tabReferidos), _translate("Engargolado", "Referidos"))
        self.lblTotal_Productos.setText(_translate("Engargolado", "Cantidad: "))
        self.btnBatido1.setText(_translate("Engargolado", "Batido"))
        self.tabMain.setTabText(self.tabMain.indexOf(self.tabCotizador), _translate("Engargolado", "Cotizador"))
        self.btnSalir.setText(_translate("Engargolado", "Salir"))
        self.lblNombre.setText(_translate("Engargolado", "Nombre:"))
        self.lblHistorico.setText(_translate("Engargolado", "Ultima Visita:"))