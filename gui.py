#from PyQt5.QtWidgets import *
#def main():
#    app = QApplication([])
#    window = QWidget()
#    layout = QVBoxLayout()
#    button = QPushButton('Top')
#    def notification():
#        alert = QMessageBox()
#        alert.setText('You clicked the button!')
#        alert.exec()
#
#    button.clicked.connect(notification)
#    layout.addWidget(button)
#    layout.addWidget(QPushButton('Bottom'))
#    window.setLayout(layout)
#    window.show()
#    app.exec()
#main()
#
import sys
from datetime import datetime
import calendar
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDate

class calendarPopup(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Calendar Demo')
        self.setGeometry(300, 300, 350, 250)
        self.initUI()
    def initUI(self):
        self.calendar = QCalendarWidget(self)
        self.button = QPushButton(self)
        self.button.setText("Approve")
        self.button.move(20,210)
        self.button.clicked.connect(self.notification)
        self.calendar.move(20, 20)
        self.calendar.setGridVisible(True)
        Year = datetime.now().year
        Month = datetime.now().month
        Day = datetime.now().day
        self.calendar.setMinimumDate(QDate(Year, Month, Day))
        if (Day + 15) > calendar.monthrange(Year, Month)[1]:
            newDay = (Day + 15) - calendar.monthrange(Year, Month)[1]
            self.calendar.setMaximumDate(QDate(Year, Month+1, newDay))
        else:
            self.calendar.setMaximumDate(QDate(Year, Month, Day + 15))
        self.calendar.setSelectedDate(QDate(Year, Month, 1))
        self.calendar.clicked.connect(self.printDateInfo)

    def printDateInfo(self, qDate):
        self.qDate = qDate
        print('{0}/{1}/{2}'.format(qDate.month(), qDate.day(), qDate.year()))
        print(f'Day Number of the year: {qDate.dayOfYear()}')
        print(f'Day Number of the week: {qDate.dayOfWeek()}')

    def notification(self):
            alert = QMessageBox()
            alert.setText('{0}/{1}/{2}'.format(self.qDate.month(), self.qDate.day(), self.qDate.year()))
            alert.exec()
'''
def main():
    app = QApplication(sys.argv)
    demo = CalendarDemo()
    demo.show()
    #label = QLabel('Hello World!')
    #label.show()
    
    sys.exit(app.exec_())
'''
def main():
    app = QApplication(sys.argv)
    window = QWidget()
    layout = QVBoxLayout()
    cal = calendarPopup()
    button = QPushButton('Top')
    button2 = QPushButton('Bottom')
    line = QLineEdit("Here")
    layout.addWidget(line)
    def notification():
        alert = QMessageBox()
        alert.setText('You clicked the button!')
        alert.exec()
    def calendar():
        cal.show()
    button.clicked.connect(notification)
    button2.clicked.connect(calendar)
    layout.addWidget(button)
    layout.addWidget(button2)
    window.setLayout(layout)
    window.show()
    app.exec(app.exec_())
main()