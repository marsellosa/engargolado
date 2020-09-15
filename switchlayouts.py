#!/usr/bin/env python

from PyQt4 import QtCore, QtGui

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.central_widget = QtGui.QStackedWidget()
        self.setCentralWidget(self.central_widget)
        Page1 = page1(self)
        Page1.nextpage.clicked.connect(self.P_2)
        self.central_widget.addWidget(Page1)
    def P_2(self):
        page2 = LoginWidget(self)
        self.central_widget.addWidget(page2)
        self.central_widget.setCurrentWidget(page2)
    def P_3(self):
        print("Why won't the page open!!!???")
        page3 = Page3(self)
        self.central_widget.addWidget(Page3)
        self.central_widget.setCurrentWidget(Page3)

class LoginWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(LoginWidget, self).__init__(parent)
        self.Username = QtGui.QLineEdit(self)  
        self.Password = QtGui.QLineEdit(self)
        self.buttonLogin = QtGui.QPushButton('Login', self)
        self.buttonLogin.clicked.connect(self.handleLogin)
        loginLayout = QtGui.QFormLayout()
        loginLayout.addRow("Username", self.Username) 
        loginLayout.addRow("Password", self.Password)
        layout = QtGui.QVBoxLayout(self)
        layout.addLayout(loginLayout)
        layout.addWidget(self.Username)
        layout.addWidget(self.Password)
        layout.addWidget(self.buttonLogin)
    def handleLogin(self):
        if (self.Username.text() == 'example' and
            self.Password.text() == 'example'):
            MainWindow().P_3()
        else:
            QtGui.QMessageBox.warning(
                self, 'Error', 'Incorrect Username/Password combination!')

class page1(QtGui.QWidget):
    def __init__(self, parent=None):
        super(page1, self).__init__(parent)
        layout = QtGui.QHBoxLayout()
        self.nextpage = QtGui.QPushButton('Page2')
        layout.addWidget(self.nextpage)
        self.setLayout(layout)

class Page3(QtGui.QWidget):
    def __init__(self, parent=None):
        super(Page3, self).__init__(parent)
        layout = QtGui.QHBoxLayout()
        self.Hello = QtGui.QLabel('Hello')
        layout.addWidget(self.Hello)
        self.setLayout(layout)

if __name__ == '__main__':
    User = ''
    app = QtGui.QApplication([])
    window = MainWindow()
    window.showFullScreen()
    app.exec_()
