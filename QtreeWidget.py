#!/usr/bin/env python

import sys
from PyQt4 import QtCore, QtGui


class Window(QtGui.QWidget):

    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.treeWidget = QtGui.QTreeWidget()
        self.treeWidget.setHeaderHidden(True)
        self.addItems(self.treeWidget.invisibleRootItem())
        self.treeWidget.itemChanged.connect (self.handleChanged)
        self.treeWidget.itemClicked.connect(self.handleClicked)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.treeWidget)
        self.setLayout(layout)

    def addItems(self, parent):
        column = 0
        #clients_item = self.addParent(parent, column, 'Clients', 'data Clients')
        spa_item = self.addParent(parent, column, 'SPA', 'data SPA')
        vendors_item = self.addParent(parent, column, 'Vendors', 'data Vendors')
        time_period_item = self.addParent(parent, column, 'Time Period', 'data Time Period')

##        self.addChild(clients_item, column, 'Type A', 'data Type A')
##        self.addChild(clients_item, column, 'Type B', 'data Type B')
        referidor = self.addParent(spa_item, column, 'Karina Gallardo', 'data Karina Gallardo')
        self.addParent(referidor, column, 'Cinthia Bolanhos', 'data Cinthia Bolanhos')

        self.addChild(vendors_item, column, 'Mary', 'data Mary')
        self.addChild(vendors_item, column, 'Arnold', 'data Arnold')

        self.addChild(time_period_item, column, 'Init', 'data Init')
        self.addChild(time_period_item, column, 'End', 'data End')

    def addParent(self, parent, column, title, data):
        item = QtGui.QTreeWidgetItem(parent, [title])
        item.setData(column, QtCore.Qt.UserRole, data)
        item.setChildIndicatorPolicy(QtGui.QTreeWidgetItem.ShowIndicator)
        item.setExpanded (True)
        return item

    def addChild(self, parent, column, title, data):
        item = QtGui.QTreeWidgetItem(parent, [title])
        item.setData(column, QtCore.Qt.UserRole, data)
        item.setCheckState (column, QtCore.Qt.Unchecked)
        return item

    def handleChanged(self, item, column):
        if item.checkState(column) == QtCore.Qt.Checked:
            print "checked", QtCore.Qt.Checked, item.text(column)
        if item.checkState(column) == QtCore.Qt.Unchecked:
            print "unchecked", item.checkState(column), item.text(column)
    def handleClicked(self, item, column):
        print item.text(column)
if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
