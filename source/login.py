# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog,QLabel,QWidget
from PyQt5.QtGui import QIcon, QPixmap,QImage
from PyQt5.uic import loadUi
import cv2
import pickle
from register import Register
from menu import Menu
import pyodbc
import os
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-C2S1KLM;'
                      'Database=qlusername;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()
cursor.execute('SELECT * FROM qlusername.dbo.account')
# Load the cascade
face_cascade = cv2.CascadeClassifier('../cascades/haarcascade_frontalface_alt.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()

#labels = {"person_name": 1}
#with open("face-labels.pickle", 'rb') as f:
	#og_labels = pickle.load(f)
	#labels = {v:k for k,v in og_labels.items()}
# Open webcam
class Ui_Frame1(QWidget):
    def openWindow1(self):
        self.openWindow = QtWidgets.QDialog()
        self.ui = Register()
        self.ui.setupUi(self.openWindow)
        self.openWindow.show()
    def openMenu(self):
        self.window = QtWidgets.QWidget()
        self.ui = Menu()
        self.ui.setupUi(self.window)
        Frame1.hide()
        self.window.show()
    def setupUi(self, Frame1):
        Frame1.setObjectName("Frame1")
        Frame1.resize(395, 179)
        self.lineEdit = QtWidgets.QLineEdit(Frame1)
        self.lineEdit.setGeometry(QtCore.QRect(110, 40, 181, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(Frame1)
        self.lineEdit_2.setGeometry(QtCore.QRect(110, 80, 181, 31))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lblUserName = QtWidgets.QLabel(Frame1)
        self.lblUserName.setGeometry(QtCore.QRect(20, 40, 71, 21))
        self.lblUserName.setObjectName("lblUserName")
        self.lblPassWord = QtWidgets.QLabel(Frame1)
        self.lblPassWord.setGeometry(QtCore.QRect(20, 80, 81, 21))
        self.lblPassWord.setObjectName("lblPassWord")
        self.btnFaceLogin = QtWidgets.QPushButton(Frame1)
        self.btnFaceLogin.setGeometry(QtCore.QRect(10, 130, 111, 41))
        self.btnFaceLogin.setObjectName("btnFaceLogin")
        self.btnLogin = QtWidgets.QPushButton(Frame1)
        self.btnLogin.setGeometry(QtCore.QRect(300, 40, 81, 71))
        self.btnLogin.setObjectName("btnLogin")
        self.btnCancel = QtWidgets.QPushButton(Frame1)
        self.btnCancel.setGeometry(QtCore.QRect(270, 130, 111, 41))
        self.btnCancel.setObjectName("btnCancel")
        self.btnRegister = QtWidgets.QPushButton(Frame1)
        self.btnRegister.setGeometry(QtCore.QRect(140, 130, 111, 41))
        self.btnRegister.setObjectName("btnRegister")

        self.retranslateUi(Frame1)
        #action button
        self.btnCancel.clicked.connect(QtWidgets.qApp.quit)
        self.btnLogin.clicked.connect(self.loginbtn)

        self.btnFaceLogin.clicked.connect(self.detectface_videos)
        self.btnRegister.clicked.connect(self.openWindow1)

        QtCore.QMetaObject.connectSlotsByName(Frame1)
    def retranslateUi(self, Frame1):
        _translate = QtCore.QCoreApplication.translate
        Frame1.setWindowTitle(_translate("Frame1", "Giao diện đăng nhập"))
        self.lblUserName.setText(_translate("Frame1", "User Name"))
        self.lblPassWord.setText(_translate("Frame1", "Password"))
        self.btnFaceLogin.setText(_translate("Frame1", "Face Login"))
        self.btnLogin.setText(_translate("Frame1", "Login"))
        self.btnCancel.setText(_translate("Frame1", "Cancel"))
        self.btnRegister.setText(_translate("Frame1", "Register"))
    def loginbtn(self):
        cursor.execute('SELECT * FROM qlusername.dbo.account where username = ?',(self.lineEdit.text()))
        result = cursor.fetchall()
        if cursor.rowcount == 0 :
            QtWidgets.QMessageBox.about(self, "Wanning", "Không tồn tại username")
            self.lineEdit.setText('')
            self.lineEdit_2.setText('')
            return
        
        if result[0][1] == self.lineEdit_2.text():
            QtWidgets.QMessageBox.about(QWidget(), "Wanning", "Đăng nhập thành công")
            #QtWidgets.QMessageBox.about(self, "Wanning", "Thành công")
            self.openMenu()
        else:
            QtWidgets.QMessageBox.about(self, "Wanning", "Thất Bại")

    def detectface_videos(self):
        if self.lineEdit.text() == '':
            QtWidgets.QMessageBox.about(self, "Wanning", "Vui lòng nhập username để thực hiện")
            return
        cap = cv2.VideoCapture(0)
        cap.set(3, 480) #set width of the frame
        cap.set(4, 640) #set height of the frame
        cursor.execute('SELECT * FROM qlusername.dbo.account where username = ?',(self.lineEdit.text()))
        result = cursor.fetchall()
        if cursor.rowcount == 0 :
            QtWidgets.QMessageBox.about(self, "Wanning", "Không tồn tại username")
            self.lineEdit.setText('')
            self.lineEdit_2.setText('')
            return        
        labels = {0: result[0][0]}
        recognizer.read("../user_yml/"+result[0][0]+".yml")
        font = cv2.FONT_HERSHEY_SIMPLEX
    
        while True:
            ret, img = cap.read()
            # Load the cascade
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            #Detect faces
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            # Draw rectangle around the faces
            a = ''
            for (x, y, w, h) in faces:
                roi_gray = gray[y:y+h,x:x+w]
                id_,conf =recognizer.predict(roi_gray)
                if conf < 50:
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    name = labels[id_]
                    a = name
                    color = (0, 0, 0)
                    stroke = 2
                    cv2.putText(img, name, (x,y), font, 1, color, stroke, cv2.LINE_AA)
                cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.imshow('frames', img)
            if a == result[0][0]:
                QtWidgets.QMessageBox.about(QWidget(), "Wanning", "Đăng nhập thành công")
                self.openMenu()
                cv2.destroyAllWindows
                cap.release()
                
                break
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyWindow('frames')
                cap.release()
                break
        cv2.destroyAllWindows()        


if __name__ == "__main__":
    print(os.getcwd())
    app = QtWidgets.QApplication(sys.argv)
    Frame1 = QtWidgets.QFrame()
    ui = Ui_Frame1()
    ui.setupUi(Frame1)
    Frame1.show()
    sys.exit(app.exec_())
