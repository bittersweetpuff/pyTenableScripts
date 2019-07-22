import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Main(QWidget):
    window = None

    def __init__(self, parent=None):
        super().__init__(parent)
        self.title = '___'
        self.left = 0
        self.top = 0
        self.width = 300
        self.height = 200
        self.Table()

    def Table(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        BtnShow = QPushButton("&Show row values", self)
        BtnShow.setFixedSize(40,30)
        BtnShow.clicked.connect(self.on_click)

        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(2)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setItem(0,0, QTableWidgetItem("One"))
        self.tableWidget.setItem(0,1, QTableWidgetItem("1234"))
        self.tableWidget.setItem(0,2, QTableWidgetItem("Online"))
        self.tableWidget.setItem(1,0, QTableWidgetItem("Two"))
        self.tableWidget.setItem(1,1, QTableWidgetItem("4321"))
        self.tableWidget.setItem(1,2, QTableWidgetItem("Offline"))
        self.tableWidget.move(0,0)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)

        self.resize(640, 480)
        self.move(300, 300)
        self.setWindowTitle('Table')
        self.show()

    def on_click(self):
        indexes = []
        for selectionRange in self.tableWidget.selectedRanges():
            indexes.extend(range(selectionRange.topRow(), selectionRange.bottomRow()+1))

        for i in indexes:
            print("name: ", self.tableWidget.item(i, 0).text())
            print("id: ", self.tableWidget.item(i, 1).text())
            print("status: ", self.tableWidget.item(i, 2).text())

if __name__ == '__main__':

    app = QApplication(sys.argv)
    okno = Main()
    sys.exit(app.exec_())
