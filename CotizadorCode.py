
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
import CotizadorUi
from rotated import RotatedHeaderView
from pyDate import PyDateEdit


class MainForm(QDialog, CotizadorUi.Ui_Form):
    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)
        self.setupUi(self)

    def main(self):
        self.show()


app = QApplication(sys.argv)
ui = MainForm()
ui.main()
app.exec_()