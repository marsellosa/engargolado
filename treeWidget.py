import sys
import DB_Class
from PyQt4 import QtCore, QtGui


class Window(QtGui.QWidget):

    def __init__(self):
        global bd
        global diccionario
        diccionario = dict()
        idOwner = 1
        ParentName = ""

        bd = DB_Class.dataBase()
        bd.createCon()
        #
        QtGui.QWidget.__init__(self)
        self.treeWidget = QtGui.QTreeWidget()
        self.treeWidget.setHeaderHidden(True)
        self.addItems(self.treeWidget.invisibleRootItem(), idOwner, ParentName)
        # self.treeWidget.itemChanged.connect(self.handleChanged)
        self.treeWidget.clicked.connect(self.handleClicked)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.treeWidget)
        self.setLayout(layout)


    def closeEvent(self, QCloseEvent):
        bd.closeCon()

    def addItems(self, parent, id, ParentName):
        column = 0

#        if ParentName:
#            query = """
#                SELECT
#                    id,
#                    Nombre,
#                    Apellido
#                FROM
#                    registro_socios
#                WHERE
#                    Referidor=%s
#                ;
#                """ % id
#        else:
#            query = """
#            SELECT
#                id,
#                Nombre,
#                Apellido
#            FROM
#                registro_socios
#            WHERE
#                id=%s
#            ;
#            """ % id
#        results = bd.interAct(query)

#        column = 0
#        for result in results:
#            nombre = "%s %s" % (result[1], result[2])
#            data = "data %s" % nombre
#            diccionario[str(nombre)] = result[0]
#            if ParentName:
#                parent = self.addParent(parent, column, nombre, data)
#                print "%s %s" % (parent, nombre)
#            self.addParent(parent, column, nombre, data)
        # print diccionario

        clients_item = self.addParent(parent, column, 'Clients', 'data Clients')
        vendors_item = self.addParent(parent, column, 'Vendors', 'data Vendors')
        time_period_item = self.addParent(parent, column, 'Time Period', 'data Time Period')

#        self.addChild(socio_item, column, 'Nada Aun', 'data Nada Aun')

        self.addChild(clients_item, column, 'Type A', 'data Type A')
        self.addChild(clients_item, column, 'Type B', 'data Type B')

        self.addChild(vendors_item, column, 'Mary', 'data Mary')
        self.addChild(vendors_item, column, 'Arnold', 'data Arnold')

        self.addChild(time_period_item, column, 'Init', 'data Init')
        self.addChild(time_period_item, column, 'End', 'data End')

    def addParent(self, parent, column, title, data):
        item = QtGui.QTreeWidgetItem(parent, [title])
        item.setData(column, QtCore.Qt.UserRole, data)
        item.setChildIndicatorPolicy(QtGui.QTreeWidgetItem.ShowIndicator)
        # item.setExpanded(False)
        return item

    def addChild(self, parent, column, title, data):
        item = QtGui.QTreeWidgetItem(parent, [title])
        item.setData(column, QtCore.Qt.UserRole, data)
        item.setCheckState(column, QtCore.Qt.Unchecked)
        return item
    
    def handleChanged(self, item, column):
        if item.checkState(column) == QtCore.Qt.Checked:
            print "checked", item, item.text(column)
        if item.checkState(column) == QtCore.Qt.Unchecked:
            print "unchecked", item, item.text(column)

    def handleClicked(self, item):
        column = 0
        getSelected = self.treeWidget.selectedItems()
        basename = getSelected[column]
        getChildNode = str(basename.text(column))
        self.addItems(self.treeWidget.invisibleRootItem(), diccionario[getChildNode], getChildNode)
        print diccionario[getChildNode]
        # print item.text()


if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
