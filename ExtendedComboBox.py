#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QCompleter, QComboBox, QSortFilterProxyModel

class ExtendedComboBox(QComboBox):
    def __init__(self, parent=None):
        super(ExtendedComboBox, self).__init__(parent)

        self.setFocusPolicy(Qt.StrongFocus)
        self.setEditable(True)
        self.setCurrentIndex(-1)
        # self.activated.connect(self.on_completer_activated)

        # add a filter model to filter matching items
        self.pFilterModel = QSortFilterProxyModel(self)
        self.pFilterModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.pFilterModel.setSourceModel(self.model())

        # add a completer, which uses the filter model
        self.completer = QCompleter(self.pFilterModel, self)
        # always show all (filtered) completions
        self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.setCompleter(self.completer)

        # connect signals
        # self.lineEdit().textEdited[unicode].connect(self.pFilterModel.setFilterFixedString)
        # self.completer.activated.connect(self.on_completer_activated)
        

    # # on selection of an item from the completer, select the corresponding item from combobox
    # def on_completer_activated(self, received):
    #
    #     if type( received ) != int:
    #         # index = self.findText(received)
    #         # self.setCurrentIndex(index)
    #         # print "Es el texto: %s & index: %s" % (self.itemText(index), index)
    #         print "Es el texto como viene: %s" % received
    #         return received
    #     else:
    #         print "Es el texto extraido del numero enviado: %s " % self.itemText(received)
    #         return self.itemText(received)


    # on model change, update the models of the filter and completer as well 
    def setModel(self, model):
        super(ExtendedComboBox, self).setModel(model)
        self.pFilterModel.setSourceModel(model)
        self.completer.setModel(self.pFilterModel)


    # on model column change, update the model column of the filter and completer as well
    def setModelColumn(self, column):
        self.completer.setCompletionColumn(column)
        self.pFilterModel.setFilterKeyColumn(column)
        super(ExtendedComboBox, self).setModelColumn(column)



# if __name__ == "__main__":
#     import sys
#     from PyQt4.QtGui import QStringListModel, QApplication
#
#     app = QApplication(sys.argv)
#
#     string_list = ['hola muchachos', 'adios amigos', 'hello world', 'good bye']
#
#     combo = ExtendedComboBox()
#
#     # either fill the standard model of the combobox
#     combo.addItems(string_list)
#
#     # or use another model
#     #combo.setModel(QStringListModel(string_list))
#
#     combo.resize(300, 40)
#     combo.show()
#
#     sys.exit(app.exec_())
