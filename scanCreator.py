
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from nessus import *
from jsonreader import *

class Ui_ScanCreationDialog(object):
    def setupUi(self, ScanCreationDialog, nessus):
        self.nessus = nessus
        ScanCreationDialog.setObjectName("ScanCreationDialog")
        ScanCreationDialog.resize(522, 440)
        self.label = QtWidgets.QLabel(ScanCreationDialog)
        self.label.setGeometry(QtCore.QRect(230, 10, 71, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(ScanCreationDialog)
        self.label_2.setGeometry(QtCore.QRect(30, 50, 61, 20))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(ScanCreationDialog)
        self.label_3.setGeometry(QtCore.QRect(306, 90, 41, 20))
        self.label_3.setObjectName("label_3")
        self.nameField = QtWidgets.QLineEdit(ScanCreationDialog)
        self.nameField.setGeometry(QtCore.QRect(360, 90, 113, 20))
        self.nameField.setObjectName("nameField")
        self.label_4 = QtWidgets.QLabel(ScanCreationDialog)
        self.label_4.setGeometry(QtCore.QRect(36, 90, 41, 20))
        self.label_4.setObjectName("label_4")
        self.policy_idField = QtWidgets.QLineEdit(ScanCreationDialog)
        self.policy_idField.setGeometry(QtCore.QRect(90, 90, 113, 20))
        self.policy_idField.setObjectName("policy_idField")
        self.label_5 = QtWidgets.QLabel(ScanCreationDialog)
        self.label_5.setGeometry(QtCore.QRect(296, 130, 51, 20))
        self.label_5.setObjectName("label_5")
        self.folder_idField = QtWidgets.QLineEdit(ScanCreationDialog)
        self.folder_idField.setGeometry(QtCore.QRect(360, 130, 113, 20))
        self.folder_idField.setObjectName("folder_idField")
        self.label_6 = QtWidgets.QLabel(ScanCreationDialog)
        self.label_6.setGeometry(QtCore.QRect(16, 130, 61, 20))
        self.label_6.setObjectName("label_6")
        self.scanner_idField = QtWidgets.QLineEdit(ScanCreationDialog)
        self.scanner_idField.setGeometry(QtCore.QRect(90, 130, 113, 20))
        self.scanner_idField.setObjectName("scanner_idField")
        self.label_7 = QtWidgets.QLabel(ScanCreationDialog)
        self.label_7.setGeometry(QtCore.QRect(306, 170, 41, 20))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(ScanCreationDialog)
        self.label_8.setGeometry(QtCore.QRect(26, 170, 51, 20))
        self.label_8.setObjectName("label_8")
        self.starttimeField = QtWidgets.QLineEdit(ScanCreationDialog)
        self.starttimeField.setGeometry(QtCore.QRect(90, 170, 113, 20))
        self.starttimeField.setObjectName("starttimeField")
        self.label_9 = QtWidgets.QLabel(ScanCreationDialog)
        self.label_9.setGeometry(QtCore.QRect(316, 210, 31, 20))
        self.label_9.setObjectName("label_9")
        self.rrulesField = QtWidgets.QLineEdit(ScanCreationDialog)
        self.rrulesField.setGeometry(QtCore.QRect(360, 210, 113, 20))
        self.rrulesField.setObjectName("rrulesField")
        self.label_10 = QtWidgets.QLabel(ScanCreationDialog)
        self.label_10.setGeometry(QtCore.QRect(56, 290, 21, 20))
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(ScanCreationDialog)
        self.label_11.setGeometry(QtCore.QRect(266, 250, 81, 20))
        self.label_11.setObjectName("label_11")
        self.aclsField = QtWidgets.QLineEdit(ScanCreationDialog)
        self.aclsField.setGeometry(QtCore.QRect(90, 290, 113, 20))
        self.aclsField.setObjectName("aclsField")
        self.label_12 = QtWidgets.QLabel(ScanCreationDialog)
        self.label_12.setGeometry(QtCore.QRect(26, 330, 51, 20))
        self.label_12.setObjectName("label_12")
        self.targetsField = QtWidgets.QLineEdit(ScanCreationDialog)
        self.targetsField.setGeometry(QtCore.QRect(90, 330, 113, 21))
        self.targetsField.setObjectName("targetsField")
        self.label_13 = QtWidgets.QLabel(ScanCreationDialog)
        self.label_13.setGeometry(QtCore.QRect(26, 250, 61, 20))
        self.label_13.setObjectName("label_13")
        self.label_14 = QtWidgets.QLabel(ScanCreationDialog)
        self.label_14.setGeometry(QtCore.QRect(316, 330, 31, 20))
        self.label_14.setObjectName("label_14")
        self.label_15 = QtWidgets.QLabel(ScanCreationDialog)
        self.label_15.setGeometry(QtCore.QRect(316, 290, 31, 20))
        self.label_15.setObjectName("label_15")
        self.file_targetsField = QtWidgets.QLineEdit(ScanCreationDialog)
        self.file_targetsField.setGeometry(QtCore.QRect(90, 250, 113, 20))
        self.file_targetsField.setObjectName("file_targetsField")
        self.label_16 = QtWidgets.QLabel(ScanCreationDialog)
        self.label_16.setGeometry(QtCore.QRect(26, 210, 51, 20))
        self.label_16.setObjectName("label_16")
        self.timezoneField = QtWidgets.QLineEdit(ScanCreationDialog)
        self.timezoneField.setGeometry(QtCore.QRect(90, 210, 113, 20))
        self.timezoneField.setObjectName("timezoneField")
        self.emailsField = QtWidgets.QLineEdit(ScanCreationDialog)
        self.emailsField.setGeometry(QtCore.QRect(360, 290, 113, 20))
        self.emailsField.setObjectName("emailsField")
        self.agent_group_idField = QtWidgets.QLineEdit(ScanCreationDialog)
        self.agent_group_idField.setGeometry(QtCore.QRect(360, 250, 113, 20))
        self.agent_group_idField.setObjectName("agent_group_idField")
        self.templateComboBox = QtWidgets.QComboBox(ScanCreationDialog)
        self.templateComboBox.setGeometry(QtCore.QRect(90, 50, 381, 22))
        self.templateComboBox.setObjectName("templateComboBox")
        self.launchComboBox = QtWidgets.QComboBox(ScanCreationDialog)
        self.launchComboBox.setGeometry(QtCore.QRect(360, 170, 111, 22))
        self.launchComboBox.setObjectName("launchComboBox")
        self.detailsField = QtWidgets.QLineEdit(ScanCreationDialog)
        self.detailsField.setGeometry(QtCore.QRect(360, 330, 113, 21))
        self.detailsField.setObjectName("detailsField")
        self.createButton = QtWidgets.QPushButton(ScanCreationDialog)
        self.createButton.setGeometry(QtCore.QRect(340, 380, 75, 23))
        self.createButton.setObjectName("createButton")

        self.cancelButton = QtWidgets.QPushButton(ScanCreationDialog)
        self.cancelButton.setGeometry(QtCore.QRect(430, 380, 75, 23))
        self.cancelButton.setObjectName("cancelButton")



        #MY DEF STARTS HERE:
        self.createButton.clicked.connect(self.getValues)
        self.cancelButton.clicked.connect(self.nessus.logout)
        self.launchComboBox.addItems(['', 'ON_DEMAND', 'DAILY', 'WEEKLY', 'MONTHLY', 'YEARLY'])
        self.templateComboBox.addItems(nessus.dataKeeper.FilterTemplateResultsTitles())
        self.succesMSG = QMessageBox()
        self.errorMSG = QMessageBox()

        self.retranslateUi(ScanCreationDialog)
        QtCore.QMetaObject.connectSlotsByName(ScanCreationDialog)

    def retranslateUi(self, ScanCreationDialog):
        _translate = QtCore.QCoreApplication.translate
        ScanCreationDialog.setWindowTitle(_translate("ScanCreationDialog", "Dialog"))
        self.label.setText(_translate("ScanCreationDialog", "Scan Designer"))
        self.label_2.setText(_translate("ScanCreationDialog", "Template*"))
        self.label_3.setText(_translate("ScanCreationDialog", "Name*"))
        self.label_4.setText(_translate("ScanCreationDialog", "Policy ID"))
        self.label_5.setText(_translate("ScanCreationDialog", "Folder ID"))
        self.label_6.setText(_translate("ScanCreationDialog", "Scanner ID"))
        self.label_7.setText(_translate("ScanCreationDialog", "Launch"))
        self.label_8.setText(_translate("ScanCreationDialog", "Start Time"))
        self.label_9.setText(_translate("ScanCreationDialog", "Rules"))
        self.label_10.setText(_translate("ScanCreationDialog", "Acls"))
        self.label_11.setText(_translate("ScanCreationDialog", "Agent Group ID"))
        self.label_12.setText(_translate("ScanCreationDialog", "Targets*"))
        self.label_13.setText(_translate("ScanCreationDialog", "File Targets"))
        self.label_14.setText(_translate("ScanCreationDialog", "Details"))
        self.label_15.setText(_translate("ScanCreationDialog", "Emails"))
        self.label_16.setText(_translate("ScanCreationDialog", "Timezone"))
        self.createButton.setText(_translate("ScanCreationDialog", "Create"))
        self.cancelButton.setText(_translate("ScanCreationDialog", "Cancel"))


    def getValues(self):
        #obligatory data
        payload = dict()
        name = self.nameField.text()
        uuid = self.nessus.dataKeeper.BuildUUIDDict()[self.templateComboBox.currentText()]
        text_targets = self.targetsField.text()

        policy_id = self.policy_idField.text()
        if policy_id != '':
            payload['policy_id'] = int(policy_id)

        folder_id = self.folder_idField.text()
        if folder_id != '':
            payload['folder_id'] = int(folder_id)

        scanner_id = self.scanner_idField.text()
        if scanner_id != '':
            payload['scanner_id'] = int(scanner_id)

        launch = self.launchComboBox.currentText()
        if launch != '':
            payload['launch'] = launch

        starttime = self.starttimeField.text()
        if starttime != '':
            payload['starttime'] = starttime

        rrules = self.rrulesField.text()
        if rrules != '':
            payload['rrules'] = rrules

        timezone = self.timezoneField.text()
        if timezone != '':
            payload['timezone'] = timezone

        file_targets = self.file_targetsField.text()
        if file_targets != '':
            payload['file_targets'] = file_targets

        description = self.detailsField.text()
        if description != '':
            payload['description'] = description

        emails = self.emailsField.text()
        if emails != '':
            payload['emails'] = emails

        acls = self.aclsField.text()
        if acls != '':
            payload['acls'] = acls.split(", ")

        agent_group_id = self.agent_group_idField.text()
        if agent_group_id != '':
            payload['agent_group_id'] = agent_group_id.split(", ")

        #print(payload)
        try:
            self.nessus.scans.create(name = name, uuid = uuid, targets = text_targets, **payload)
        except Exception:
            self.errorMSG.setText("Error")
            self.errorMSG.exec()
        else:
            self.succesMSG.setText("Succes")




if __name__ == "__main__":
    import sys

    gpwd = GetPass()
    #guser = getpass.getuser()
    guser = GetUser()
    FMT = "%(asctime)-15s %(levelname)s	%(module)s %(lineno)d %(message)s"
    logging.basicConfig(format=FMT)
    LOGGER.setLevel(logging.DEBUG)
    LOGGER.debug("starting")
    connector = Connector(GetNessusConsole())
    app = QtWidgets.QApplication(sys.argv)
    ScanCreationDialog = QtWidgets.QDialog()
    connector.login(guser, gpwd)
    connector.dataKeeper.Prepare()
    ui = Ui_ScanCreationDialog()
    ui.setupUi(ScanCreationDialog, connector)
    ScanCreationDialog.show()


    sys.exit(app.exec_())
    connector.logout()
