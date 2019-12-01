# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'userGui.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from register import Register
from changePass import ChangePass
import pyodbc
from cv2 import cv2
import shutil
class Ui_QuanLy(object):
    face_cascade = cv2.CascadeClassifier('../cascades/haarcascade_frontalface_alt.xml')

    recognizer = cv2.face.LBPHFaceRecognizer_create()

    conn = pyodbc.connect('Driver={SQL Server};'
                        'Server=DESKTOP-C2S1KLM;'
                        'Database=qlusername;'
                        'Trusted_Connection=yes;')

    cursor = conn.cursor()
    def openWindow1(self):
        self.openWindow = QtWidgets.QDialog()
        self.ui = Register()
        self.ui.setupUi(self.openWindow)
        self.openWindow.show()
    def openWindow2(self,username,password):
        self.openWindow = QtWidgets.QDialog()
        self.ui = ChangePass(username,password)
        self.ui.setupUi(self.openWindow)
        self.openWindow.show()
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(506, 319)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(30, 20, 421, 41))
        self.label.setObjectName("label")
        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setGeometry(QtCore.QRect(20, 70, 461, 151))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)       
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(0, 240, 101, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(120, 240, 111, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(260, 240, 111, 31))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(Form)
        self.pushButton_4.setGeometry(QtCore.QRect(390, 240, 111, 31))
        self.pushButton_4.setObjectName("pushButton_4")
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.loadBang()
        #----------------------------------------------------------------------
        self.pushButton.clicked.connect(self.openWindow1)
        self.pushButton_4.clicked.connect(self.loadBang)
        self.pushButton_3.clicked.connect(self.deleteUser)
        self.pushButton_2.clicked.connect(self.changePassword)
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Quản lý user"))
        self.label.setText(_translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt;\">Quản lý user</span></p></body></html>"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "User Name"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Password"))
        self.pushButton.setText(_translate("Form", "Thêm user"))
        self.pushButton_2.setText(_translate("Form", "Đổi password"))
        self.pushButton_3.setText(_translate("Form", "Xóa user"))
        self.pushButton_4.setText(_translate("Form", "Refresh"))
    #----------------------------------------------------------------------------------------------------
    #Load bảng
    def loadBang(self):
        self.cursor.execute('SELECT * FROM [dbo].[account]')
        userList = self.cursor.fetchall()
        numrow = len(userList)
        numcol = 2
        self.tableWidget.setRowCount(numrow)
        for row in range(numrow):
            for col in range(numcol):
                self.tableWidget.setItem(row,col,QtWidgets.QTableWidgetItem(str(userList[row][col])))
    #----------------------------------------------------------------------------------------------------
    #Xóa user
    def deleteUser(self):
        row = self.tableWidget.currentRow()
        self.cursor.execute("DELETE FROM account WHERE username = '"+self.tableWidget.item(row,0).text()+"'")
        self.cursor.commit()
        shutil.rmtree('../ima_user/'+self.tableWidget.item(row,0).text())
        self.loadBang()
    #----------------------------------------------------------------------------------------------------
    #Sửa password
    def changePassword(self):
        row = self.tableWidget.currentRow()
        self.openWindow2(self.tableWidget.item(row,0).text(),self.tableWidget.item(row,1).text())
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_QuanLy()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
