
from PyQt5 import QtCore, QtGui, QtWidgets
from nessus import *
from jsonreader import *
from PyQt5.QtWidgets import *
import types
from scanCreator import Ui_ScanCreationDialog
import sys

global app


class Ui_NessusScanManagerTool(object):
    def setupUi(self, NessusScanManagerTool):
        NessusScanManagerTool.setObjectName("NessusScanManagerTool")
        NessusScanManagerTool.resize(384, 575)
        self.nessus = Connector(GetNessusConsole())
        self.centralwidget = QtWidgets.QWidget(NessusScanManagerTool)
        self.centralwidget.setObjectName("centralwidget")
        self.scansTable = QtWidgets.QTableWidget(self.centralwidget)
        self.scansTable.setGeometry(QtCore.QRect(40, 80, 311, 351))
        self.scansTable.setObjectName("scansTable")
        self.scansTable.setColumnCount(3)
        self.scansTable.setRowCount(0)
        self.scansTable.setHorizontalHeaderLabels("ID;Name;Status".split(";"))
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 50, 47, 13))
        self.label.setObjectName("label")
        self.refreshButton = QtWidgets.QPushButton(self.centralwidget)
        self.refreshButton.setGeometry(QtCore.QRect(270, 50, 75, 23))
        self.refreshButton.setObjectName("refreshButton")
        self.refreshButton.clicked.connect(self.builtTable)
        self.newButton = QtWidgets.QPushButton(self.centralwidget)
        self.newButton.setGeometry(QtCore.QRect(50, 450, 75, 23))
        self.newButton.setObjectName("newButton")
        self.newButton.clicked.connect(self.callScanCreator)
        self.deleteButton = QtWidgets.QPushButton(self.centralwidget)
        self.deleteButton.setGeometry(QtCore.QRect(270, 450, 75, 23))
        self.deleteButton.setObjectName("deleteButton")
        self.deleteButton.clicked.connect(self.deleteSelectedScans)
        self.launchButton = QtWidgets.QPushButton(self.centralwidget)
        self.launchButton.setGeometry(QtCore.QRect(160, 450, 75, 23))
        self.launchButton.setObjectName("launchButton")
        self.launchButton.clicked.connect(self.launchSelectedScans)
        self.pauseButton = QtWidgets.QPushButton(self.centralwidget)
        self.pauseButton.setGeometry(QtCore.QRect(50, 490, 75, 23))
        self.pauseButton.setObjectName("pauseButton")
        self.pauseButton.clicked.connect(self.pauseSelectedScans)
        self.resumeButton = QtWidgets.QPushButton(self.centralwidget)
        self.resumeButton.setGeometry(QtCore.QRect(160, 490, 75, 23))
        self.resumeButton.setObjectName("resumeButton")
        self.resumeButton.clicked.connect(self.resumeSelectedScans)
        self.stopButton = QtWidgets.QPushButton(self.centralwidget)
        self.stopButton.setGeometry(QtCore.QRect(270, 490, 75, 23))
        self.stopButton.setObjectName("stopButton")
        self.stopButton.clicked.connect(self.stopSelectedScans)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(40, 20, 47, 13))
        self.label_2.setObjectName("label_2")
        self.connectionStatus = QtWidgets.QLineEdit(self.centralwidget)
        self.connectionStatus.setGeometry(QtCore.QRect(90, 20, 113, 20))
        self.connectionStatus.setObjectName("connectionStatus")
        self.connectionStatus.setText('Disconnected')
        self.connectionStatus.setReadOnly(True)
        NessusScanManagerTool.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(NessusScanManagerTool)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 384, 21))
        self.menubar.setObjectName("menubar")
        self.menuStart = QtWidgets.QMenu(self.menubar)
        self.menuStart.setObjectName("menuStart")
        NessusScanManagerTool.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(NessusScanManagerTool)
        self.statusbar.setObjectName("statusbar")
        NessusScanManagerTool.setStatusBar(self.statusbar)
        self.actionConnect_to_Nessus = QtWidgets.QAction(NessusScanManagerTool)
        self.actionConnect_to_Nessus.setObjectName("actionConnect_to_Nessus")
        self.actionDisconnect = QtWidgets.QAction(NessusScanManagerTool)
        self.actionDisconnect.setObjectName("actionDisconnect")
        self.menuStart.addAction(self.actionConnect_to_Nessus)
        self.menuStart.addAction(self.actionDisconnect)
        self.menubar.addAction(self.menuStart.menuAction())


        #my COde
        self.actionConnect_to_Nessus.triggered.connect(self.connectToNessus)
        self.actionDisconnect.triggered.connect(self.disconnectFromNessus)


        self.retranslateUi(NessusScanManagerTool)
        QtCore.QMetaObject.connectSlotsByName(NessusScanManagerTool)

    def retranslateUi(self, NessusScanManagerTool):
        _translate = QtCore.QCoreApplication.translate
        NessusScanManagerTool.setWindowTitle(_translate("NessusScanManagerTool", "MainWindow"))
        self.label.setText(_translate("NessusScanManagerTool", "Scans:"))
        self.refreshButton.setText(_translate("NessusScanManagerTool", "Refresh"))
        self.newButton.setText(_translate("NessusScanManagerTool", "New"))
        self.deleteButton.setText(_translate("NessusScanManagerTool", "Delete"))
        self.launchButton.setText(_translate("NessusScanManagerTool", "Launch"))
        self.pauseButton.setText(_translate("NessusScanManagerTool", "Pause"))
        self.resumeButton.setText(_translate("NessusScanManagerTool", "Resume"))
        self.stopButton.setText(_translate("NessusScanManagerTool", "Stop"))
        self.label_2.setText(_translate("NessusScanManagerTool", "Status:"))
        self.menuStart.setTitle(_translate("NessusScanManagerTool", "Start"))
        self.actionConnect_to_Nessus.setText(_translate("NessusScanManagerTool", "Connect to Nessus"))
        self.actionDisconnect.setText(_translate("NessusScanManagerTool", "Disconnect"))


################################################################################
########################### My COde Starts Here ################################
################################################################################


    def connectToNessus(self):
        gpwd = GetPass()
        guser = GetUser()
        self.nessus.login(guser, gpwd)
        self.nessus.dataKeeper.Prepare()
        self.connectionStatus.setText('Connected')


    def disconnectFromNessus(self):
        self.nessus.logout()
        self.scansTable.setRowCount(0)
        self.connectionStatus.setText('Disconnected')


    def getScanIDFromTable(self):
        indexes = []
        for selectionRange in self.scansTable.selectedRanges():
            indexes.extend(range(selectionRange.topRow(), selectionRange.bottomRow()+1))
            return indexes


    def deleteSelectedScans(self):
        indexes = self.getScanIDFromTable()
        for i in indexes:
            self.nessus.scans.delete(int(self.scansTable.item(i, 0).text()))
        self.builtTable()


    def launchSelectedScans(self):
        indexes = self.getScanIDFromTable()
        for i in indexes:
            self.nessus.scans.launch(int(self.scansTable.item(i, 0).text()))
        self.builtTable()


    def pauseSelectedScans(self):
        indexes = self.getScanIDFromTable()
        for i in indexes:
            self.nessus.scans.pause(int(self.scansTable.item(i, 0).text()))
        self.builtTable()


    def resumeSelectedScans(self):
        indexes = self.getScanIDFromTable()
        for i in indexes:
            self.nessus.scans.resume(int(self.scansTable.item(i, 0).text()))
        self.builtTable()


    def stopSelectedScans(self):
        indexes = self.getScanIDFromTable()
        for i in indexes:
            self.nessus.scans.stop(int(self.scansTable.item(i, 0).text()))
        self.builtTable()


    def callScanCreator(self):
        self.ScanCreationDialog = QtWidgets.QDialog()
        self.creatorui = Ui_ScanCreationDialog()
        self.creatorui.setupUi(self.ScanCreationDialog, self.nessus)
        self.ScanCreationDialog.show()


    def builtTable(self):
        results = self.nessus.dataKeeper.FilterScanResults({'id', 'name', 'status'})
        rows = len(results)
        self.scansTable.setRowCount(rows)
        self.scansTable.setColumnCount(3)
        currentRow = 0
        for scan in results:
            self.scansTable.setItem(currentRow, 0, QTableWidgetItem(str(scan['id'])))
            self.scansTable.setItem(currentRow, 1, QTableWidgetItem(scan['name']))
            self.scansTable.setItem(currentRow, 2, QTableWidgetItem(scan['status']))
            currentRow = currentRow + 1




if __name__ == "__main__":
    import sys
    FMT = "%(asctime)-15s %(levelname)s	%(module)s %(lineno)d %(message)s"
    logging.basicConfig(format=FMT)
    LOGGER.setLevel(logging.DEBUG)
    LOGGER.debug("starting")
    app = QtWidgets.QApplication(sys.argv)
    NessusScanManagerTool = QtWidgets.QMainWindow()
    ui = Ui_NessusScanManagerTool()
    ui.setupUi(NessusScanManagerTool)
    NessusScanManagerTool.show()
    sys.exit(app.exec_())
