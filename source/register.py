# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'register.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

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
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-C2S1KLM;'
                      'Database=qlusername;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()
face_cascade = cv2.CascadeClassifier('opencv/sources/data/haarcascades/haarcascade_frontalface_alt.xml')
#face_cascade = cv2.CascadeClassifier('opencv/sources/data/lbpcascades/lbpcascade_frontalface_improved.xml')
#face_cascade = cv2.CascadeClassifier('opencv/sources/data/haarcascades_cuda/haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
current_id = 0
label_ids = {}
y_labels = []
x_train = []
cap = cv2.VideoCapture(0)

class Register(QWidget):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Register")
        Dialog.resize(311, 154)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 110, 201, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(10, 60, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.txtUserName = QtWidgets.QLineEdit(Dialog)
        self.txtUserName.setGeometry(QtCore.QRect(110, 20, 141, 21))
        self.txtUserName.setObjectName("txtUserName")
        self.txtPassWord = QtWidgets.QLineEdit(Dialog)
        self.txtPassWord.setGeometry(QtCore.QRect(110, 60, 141, 21))
        self.txtPassWord.setText("")
        self.txtPassWord.setEchoMode(QtWidgets.QLineEdit.Password)
        self.txtPassWord.setObjectName("txtPassWord")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(self.train)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "User Name"))
        self.label_2.setText(_translate("Dialog", "Password"))
    def train(self):
        if self.txtPassWord.text() == '':
            QtWidgets.QMessageBox.about(self, "Wanning", "Nhập username và password")
            return
        if not os.path.exists('ima_user/'+self.txtUserName.text()):
            os.mkdir('ima_user/'+self.txtUserName.text())
            print("Directory " , 'ima_user/'+self.txtUserName.text() ,  " Created ")
            cursor.execute('INSERT INTO qlusername.dbo.account(username,pass) values(?,?)',(self.txtUserName.text(),self.txtPassWord.text()))
            cursor.commit()
        else:    
            QtWidgets.QMessageBox.about(self, "Wanning", "Đã tồn tại user trong hệ thống")
            self.txtUserName.setText('')
            return
        dem =0
        while True:
            ret, img = cap.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            for (x, y, w, h) in faces:
                dem = dem + 1
                print(dem)
                label = self.txtUserName.text()
                label_ids[label] = 0
                id_ = label_ids[label]
                roi = gray[y:y+h, x:x+w]
                cv2.imwrite("ima_user/"+label+"/"+"."+str(dem)+".jpg",gray[y:y+h,x:x+w])
                x_train.append(roi)
                y_labels.append(id_)
                cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.imshow('frames', img)
            if cv2.waitKey(1) & 0xFF == ord('q'): 
                break
            if dem == 100:
                cv2.destroyAllWindows()
                break    
        with open("face-labels.pickle", 'wb') as f:
            pickle.dump(label_ids, f)
        recognizer.train(x_train, np.array(y_labels))
        recognizer.write("user_yml/"+self.txtUserName.text()+".yml")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Register()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
