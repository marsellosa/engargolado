#!/usr/bin/env python

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QLineEdit

class LineCompletion(QLineEdit):
    completion_items = [u"hello", u"world"]

    def __init__(self, parent = None):
        QLineEdit.__init__(self, parent)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Tab:
            for item in self.completion_items:
                if item.startswith(self.text()):
                    self.setText(item)
                    break
            event.accept()
        else:
            QLineEdit.keyPressEvent(self, event)