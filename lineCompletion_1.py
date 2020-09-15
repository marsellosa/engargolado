#!/usr/bin/env python

import sys
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QApplication, QCompleter, QLineEdit, QStringListModel, QSortFilterProxyModel

def get_data(model):
    model.setStringList(["Paola Llosa", "Pedro Cardozo", "wara", "here"])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    edit = QLineEdit()

    model = QStringListModel()

    completer = QCompleter()
    completer.setModel(model)
    completer.setCaseSensitivity(Qt.CaseInsensitive)

    edit.setCompleter(completer)

    get_data(model)

    edit.show()
    sys.exit(app.exec_())
