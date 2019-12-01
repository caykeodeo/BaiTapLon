# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'menu.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from userGui import Ui_QuanLy
from diemdanh import Ui_frmDiemDanh
from train import Train
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog,QLabel,QWidget
from PyQt5.QtGui import QIcon, QPixmap,QImage
from PyQt5.uic import loadUi
import cv2
import pickle
import os

class Menu(object):
    def openTrain(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Train(QtGui.QStandardItemModel(),QtGui.QStandardItemModel())
        self.ui.setupUi(self.window)
        self.ui.load_table()
        self.window.show()
    def openDiemDanh(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_frmDiemDanh()
        self.ui.setupUi(self.window)
        self.window.show()
    def openQuanLy(self):
        self.window = QtWidgets.QWidget()
        self.ui = Ui_QuanLy()
        self.ui.setupUi(self.window)
        self.window.show()    
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(300, 387)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(30, 60, 231, 51))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(30, 130, 231, 51))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(30, 200, 231, 51))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(Form)
        self.pushButton_4.setGeometry(QtCore.QRect(30, 270, 231, 51))
        self.pushButton_4.setObjectName("pushButton_4")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(60, 10, 181, 31))
        self.label.setObjectName("label")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        #action button
        self.pushButton.clicked.connect(self.openTrain)
        self.pushButton_2.clicked.connect(self.openDiemDanh)
        self.pushButton_3.clicked.connect(self.openQuanLy)
        self.pushButton_4.clicked.connect(self.logout)
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Menu"))
        self.pushButton.setText(_translate("Form", "Đăng ký danh sách sinh viên"))
        self.pushButton_2.setText(_translate("Form", "Điểm danh sinh viên"))
        self.pushButton_3.setText(_translate("Form", "Quản lý user"))
        self.pushButton_4.setText(_translate("Form", "Đăng xuất"))
        self.label.setText(_translate("Form", "Menu chức năng chính"))
    def logout(self):
        os.chdir(os.path.dirname(sys.argv[0]))
        
        os.startfile('login.py')
        sys.exit()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Menu()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
