#!/usr/bin/env python

import sys
from PyQt4 import QtGui, QtCore

#lista = list()
#listb = list()
#listc = list()

lista = ['aa', 'ab', 'ac']
listb = ['ba', 'bb', 'bc']
listc = ['ca', 'cb', 'cc']
mystruct = {'A':lista, 'B':listb, 'C':listc}

class RotatedHeaderView( QtGui.QHeaderView ):
    def __init__(self, orientation, parent=None ):
        super(RotatedHeaderView, self).__init__(orientation, parent)
        self.setMinimumSectionSize(20)

    def paintSection(self, painter, rect, logicalIndex ):
        painter.save()
        # translate the painter such that rotate will rotate around the correct point
        painter.translate(rect.x()+rect.width(), rect.y())
        painter.rotate(90)
        # and have parent code paint at this location
        newrect = QtCore.QRect(0,0,rect.height(),rect.width())
        super(RotatedHeaderView, self).paintSection(painter, newrect, logicalIndex)
        painter.restore()

    def minimumSizeHint(self):
        size = super(RotatedHeaderView, self).minimumSizeHint()
        size.transpose()
        return size

    def sectionSizeFromContents(self, logicalIndex):
        size = super(RotatedHeaderView, self).sectionSizeFromContents(logicalIndex)
        size.transpose()
        return size

class MyTable(QtGui.QTableWidget):
    def __init__(self, thestruct, *args):
        QtGui.QTableWidget.__init__(self, *args)
        self.data = thestruct
        self.setmydata()

    def setmydata(self):
        vista = RotatedHeaderView(QtGui.QTableWidget)
        n = 0
        for key in self.data:
            m = 0
            for item in self.data[key]:
                newitem = QtGui.QTableWidgetItem(item)
                if key == 'A':
                    newitem.setBackground(QtGui.QColor(100,100,150))
                elif key == 'B':
                    newitem.setBackground(QtGui.QColor(100,150,100))
                else:
                    newitem.setBackground(QtGui.QColor(150,100,100))
                self.setItem(m, n, newitem)
                m += 1
            n += 1

def main(args):
    app = QtGui.QApplication(args)
    table = MyTable(mystruct, 5, 3)
    table.setHorizontalHeader(RotatedHeaderView)
    table.show()
    sys.exit(app.exec_())

if __name__=="__main__":
    main(sys.argv)
