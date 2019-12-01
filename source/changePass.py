# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ChangePass.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!
from os.path import dirname, abspath
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog,QLabel,QWidget
from PyQt5.QtGui import QIcon, QPixmap,QImage
from PyQt5.uic import loadUi
import cv2
import os
import numpy as np
from PIL import Image
import pickle
import os.path as path
import sys
import pyodbc
from PyQt5 import QtCore, QtGui, QtWidgets
class ChangePass(object):
    face_cascade = cv2.CascadeClassifier('cascades/haarcascade_frontalface_alt.xml')

    recognizer = cv2.face.LBPHFaceRecognizer_create()

    conn = pyodbc.connect('Driver={SQL Server};'
                        'Server=DESKTOP-C2S1KLM;'
                        'Database=qlusername;'
                        'Trusted_Connection=yes;')

    cursor = conn.cursor()
    def __init__(self,username,password):
        self.username = username
        self.password = password
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(280, 155)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(40, 100, 201, 31))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(4, 20, 81, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(30, 60, 55, 16))
        self.label_2.setObjectName("label_2")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(100, 20, 151, 21))
        self.lineEdit.setText("")
        self.lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(100, 60, 151, 21))
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_2.setObjectName("lineEdit_2")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(self.changePass)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Đổi password"))
        self.label.setText(_translate("Dialog", "Password mới"))
        self.label_2.setText(_translate("Dialog", "Nhập lại"))
    #-------------------------------------------------------------------------------------
    #Đổi pass
    def changePass(self):
        
        if(self.lineEdit.text()==''):
            QtWidgets.QMessageBox.about(QWidget(), "Wanning", "Nhập password mới")
            return
        elif  (self.lineEdit_2.text() == ''):
            QtWidgets.QMessageBox.about(QWidget(), "Wanning", "Nhập lại password mới")
            return
        elif (self.lineEdit.text() != self.lineEdit_2.text()):
            QtWidgets.QMessageBox.about(QWidget(), "Wanning", "Nhập lại password không khớp")
            self.lineEdit.setText('')
            self.lineEdit_2.setText('')
            return
        elif (self.lineEdit.text().lower() == self.password.lower()):
            QtWidgets.QMessageBox.about(QWidget(), "Wanning", "Password mới phải khác password cũ")
            self.lineEdit.setText('')
            self.lineEdit_2.setText('')
            return
        self.cursor.execute("UPDATE account set pass = '"+self.lineEdit_2.text()+"' WHERE username = '"+self.username+"'")
        self.cursor.commit()
        QtWidgets.QMessageBox.about(QWidget(), "Wanning", "Chương trình sẽ khởi động lại")
        os.chdir(os.path.dirname(sys.argv[0]))
        
        os.startfile('login.py')
        sys.exit()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = ChangePass()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
