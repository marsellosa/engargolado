from PyQt5.QtWidgets import QDateEdit, QApplication, QCalendarWidget
from PyQt5.QtGui import *
from PyQt5.QtCore import *

# try:
#     _fromUtf8 = QString.fromUtf8
# except AttributeError:
#     _fromUtf8 = lambda s: s
try:
    _encoding = QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)

class PyDateEdit(QDateEdit):
    #
    # Initialize base class
    # Force use of the calendar popup
    # Set default values for calendar properties
    #
    def __init__(self, parent=None):
        super(PyDateEdit, self).__init__(parent)

        # Main values for initials settings
        font = QFont()
        font.setFamily("Ubuntu Condensed")
        font.setPointSize(12)
        self.setFont(font)
        self.setCalendarPopup(True)
        self.setDate(QDate.currentDate())
        self.setDisplayFormat('d/MMM/yyyy')
        self.setObjectName("dateEdit")
        self.__cw = None
        self.__currentDate = QDate.currentDate()
        self.__firstDayOfWeek = Qt.Monday
        self.__gridVisible = True
        self.__horizontalHeaderFormat = QCalendarWidget.ShortDayNames
        self.__verticalHeaderFormat = QCalendarWidget.ISOWeekNumbers
        self.__navigationBarVisible = True

    #
    # Call event handler of base class
    # Get the calendar widget, if not already done
    # Set the calendar properties
    #
    def mousePressEvent(self, event):
        super(PyDateEdit, self).mousePressEvent(event)

        if not self.__cw:
            self.__cw = self.findChild(QCalendarWidget)
            if self.__cw:
                self.__cw.setFirstDayOfWeek(self.__firstDayOfWeek)
                self.__cw.setGridVisible(self.__gridVisible)
                self.__cw.setHorizontalHeaderFormat(self.__horizontalHeaderFormat)
                self.__cw.setVerticalHeaderFormat(self.__verticalHeaderFormat)
                self.__cw.setNavigationBarVisible(self.__navigationBarVisible)
                # self.__cw.setSelectedDate(self.__currentDate)

    #
    # Make sure, the calendarPopup property is invisible in Designer
    #
    def getCalendarPopup(self):
        return True

    calendarPopup = pyqtProperty(bool, fget=getCalendarPopup)

    def getCurrentDate(self):
        return self.__currentDate

    currentDate = pyqtProperty(bool, fget=getCurrentDate)

    #
    # Property firstDayOfWeek: Qt::DayOfWeek
    # Get: getFirstDayOfWeek()
    # Set: setFirstDayOfWeek()
    # Reset: resetFirstDayOfWeek()
    #
    def getFirstDayOfWeek(self):
        return self.__firstDayOfWeek

    def setFirstDayOfWeek(self, dayOfWeek):
        if dayOfWeek != self.__firstDayOfWeek:
            self.__firstDayOfWeek = dayOfWeek
            if self.__cw:
                self.__cw.setFirstDayOfWeek(dayOfWeek)

    def resetFirstDayOfWeek(self):
        if self.__firstDayOfWeek != Qt.Monday:
            self.__firstDayOfWeek = Qt.Monday
            if self.__cw:
                self.__cw.setFirstDayOfWeek(Qt.Monday)

    firstDayOfWeek = pyqtProperty(Qt.DayOfWeek,
                                  fget=getFirstDayOfWeek,
                                  fset=setFirstDayOfWeek,
                                  freset=resetFirstDayOfWeek)

    #
    # Property gridVisible: bool
    # Get: isGridVisible()
    # Set: setGridVisible()
    # Reset: resetGridVisible()
    #
    def isGridVisible(self):
        return self.__gridVisible

    def setGridVisible(self, show):
        if show != self.__gridVisible:
            self.__gridVisible = show
            if self.__cw:
                self.__cw.setGridVisible(show)

    def resetGridVisible(self):
        if self.__gridVisible != False:
            self.__gridVisible = False
            if self.__cw:
                self.__cw.setGridVisible(False)

    gridVisible = pyqtProperty(bool,
                               fget=isGridVisible,
                               fset=setGridVisible,
                               freset=resetGridVisible)

    #
    # Property horizontalHeaderFormat: QCalendarWidget::HorizontalHeaderFormat
    # Get: getHorizontalHeaderFormat()
    # Set: setHorizontalHeaderFormat()
    # Reset: resetHorizontalHeaderFormat()
    #
    def getHorizontalHeaderFormat(self):
        return self.__horizontalHeaderFormat

    def setHorizontalHeaderFormat(self, format):
        if format != self.__horizontalHeaderFormat:
            self.__horizontalHeaderFormat = format
            if self.__cw:
                self.__cw.setHorizontalHeaderFormat(format)

    def resetHorizontalHeaderFormat(self):
        if self.__horizontalHeaderFormat != QCalendarWidget.ShortDayNames:
            self.__horizontalHeaderFormat = QCalendarWidget.ShortDayNames
            if self.__cw:
                self.__cw.setHorizontalHeaderFormat(QCalendarWidget.ShortDayNames)

    horizontalHeaderFormat = pyqtProperty(QCalendarWidget.HorizontalHeaderFormat,
                                          fget=getHorizontalHeaderFormat,
                                          fset=setHorizontalHeaderFormat,
                                          freset=resetHorizontalHeaderFormat)

    #
    # Property verticalHeaderFormat: QCalendarWidget::VerticalHeaderFormat
    # Get: getVerticalHeaderFormat()
    # Set: setVerticalHeaderFormat()
    # Reset: resetVerticalHeaderFormat()
    #
    def getVerticalHeaderFormat(self):
        return self.__verticalHeaderFormat

    def setVerticalHeaderFormat(self, format):
        if format != self.__verticalHeaderFormat:
            self.__verticalHeaderFormat = format
            if self.__cw:
                self.__cw.setVerticalHeaderFormat(format)

    def resetVerticalHeaderFormat(self):
        if self.__verticalHeaderFormat != QCalendarWidget.ISOWeekNumbers:
            self.__verticalHeaderFormat = QCalendarWidget.ISOWeekNumbers
            if self.__cw:
                self.__cw.setVerticalHeaderFormat(QCalendarWidget.ISOWeekNumbers)

    verticalHeaderFormat = pyqtProperty(QCalendarWidget.VerticalHeaderFormat,
                                        fget=getVerticalHeaderFormat,
                                        fset=setVerticalHeaderFormat,
                                        freset=resetVerticalHeaderFormat)

    #
    # Property navigationBarVisible: bool
    # Get: isNavigationBarVisible()
    # Set: setNavigationBarVisible()
    # Reset: resetNavigationBarVisible()
    #
    def isNavigationBarVisible(self):
        return self.__navigationBarVisible

    def setNavigationBarVisible(self, visible):
        if visible != self.__navigationBarVisible:
            self.__navigationBarVisible = visible
            if self.__cw:
                self.__cw.setNavigationBarVisible(visble)

    def resetNavigationBarVisible(self):
        if self.__navigationBarVisible != True:
            self.__navigationBarVisible = True
            if self.__cw:
                self.__cw.setNavigationBarVisible(True)

    navigationBarVisible = pyqtProperty(bool,
                                        fget=isNavigationBarVisible,
                                        fset=setNavigationBarVisible,
                                        freset=resetNavigationBarVisible)