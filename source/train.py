# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\2019-2020\Ki1\CongNgheMoi\BaiTapLon\gui\test.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QWidget
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.uic import loadUi
import cv2
import os
from os.path import dirname, abspath
import numpy as np
from PIL import Image
import pickle
import os.path as path
import sys
import pyodbc
from PyQt5 import QtCore, QtGui, QtWidgets
import shutil
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-C2S1KLM;'
                      'Database=qlusername;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()

current_id = 0
label_ids = {}
y_labels = []
x_train = []

# Duong dan toi lib cascade
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_dir2_cas = dirname(str(BASE_DIR))
image_dir_cas = os.path.join(image_dir2_cas, "cascades\haarcascade_frontalface_alt.xml")
face_cascade = cv2.CascadeClassifier(image_dir_cas)


recognizer = cv2.face.LBPHFaceRecognizer_create()


model_getImg = QtGui.QStandardItemModel()
model_getTrain = QtGui.QStandardItemModel()


class Train(object):
    
    def __init__(self,model_getImg,model_getTrain):
        self.model_getImg = model_getImg
        self.model_getTrain = model_getTrain
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(599, 550)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(30, 340, 541, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(
            self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.pushButton_2 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)

        self.btn_train = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.btn_train.setObjectName("btn_train")
        self.horizontalLayout.addWidget(self.btn_train)

        self.btn_refresh = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.btn_refresh.setObjectName("btn_train")
        self.horizontalLayout.addWidget(self.btn_refresh)

        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(340, 10, 160, 191))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.txt_ten = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.txt_ten.setText("")
        self.txt_ten.setObjectName("txt_ten")
        self.verticalLayout.addWidget(self.txt_ten)
        self.txt_mssv = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.txt_mssv.setObjectName("txt_mssv")
        self.verticalLayout.addWidget(self.txt_mssv)
        self.txt_lop = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.txt_lop.setObjectName("txt_lop")
        self.verticalLayout.addWidget(self.txt_lop)
        self.btn_layAnh = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btn_layAnh.setObjectName("btn_layAnh")
        self.verticalLayout.addWidget(self.btn_layAnh)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(510, 20, 61, 121))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(
            self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.tbl_getIma = QtWidgets.QTableView(self.centralwidget)
        self.tbl_getIma.setGeometry(QtCore.QRect(30, 210, 541, 121))
        self.tbl_getIma.setObjectName("tbl_getIma")
        self.tbl_getIma.verticalHeader().setVisible(False)
        self.tbl_getIma.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tbl_getIma.setEditTriggers(QtWidgets.QTableView.NoEditTriggers)
        self.tbl_getIma.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tbl_train = QtWidgets.QTableView(self.centralwidget)
        self.tbl_train.setGeometry(QtCore.QRect(30, 380, 541, 121))
        self.tbl_train.setObjectName("tbl_train")
        self.tbl_train.verticalHeader().setVisible(False)
        self.tbl_train.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tbl_train.setEditTriggers(QtWidgets.QTableView.NoEditTriggers)
        self.tbl_train.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(30, 10, 301, 191))
        # self.frame.setStyleSheet("")
        self.frame.setFrameShape(QtWidgets.QFrame.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 599, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # chinh bang

        model_getImg.setHorizontalHeaderLabels(['Tên', 'MSSV', 'Lớp'])
        model_getImg.setColumnCount(3)
        self.tbl_getIma.setModel(model_getImg)

        model_getTrain.setHorizontalHeaderLabels(['Tên', 'MSSV', 'Lớp'])
        model_getTrain.setColumnCount(3)
        self.tbl_train.setModel(model_getTrain)

        # gan su kien
        self.btn_layAnh.clicked.connect(self.getImg_student)

        self.btn_train.clicked.connect(self.faces_train)
        self.btn_refresh.clicked.connect(self.load_table)
        self.pushButton_2.clicked.connect(self.deleteStuden)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Giao diện lấy ảnh"))
        self.pushButton_2.setText(_translate("MainWindow", "Xóa"))
        self.btn_train.setText(_translate("MainWindow", "Train"))
        self.btn_layAnh.setText(_translate("MainWindow", "Lấy ảnh"))
        self.btn_refresh.setText(_translate("MainWindow", "Refresh 2 bảng"))
        self.label_2.setText(_translate("MainWindow", "Họ và tên"))
        self.label.setText(_translate("MainWindow", "MSSV"))
        self.label_3.setText(_translate("MainWindow", "Lớp"))

    def deleteStuden(self):
        for index in sorted(self.tbl_getIma.selectionModel().selectedRows()):
            row=index.row()
        data1=model_getImg.data(model_getImg.index(row, 0))
        data2=model_getImg.data(model_getImg.index(row, 1))
        data3=model_getImg.data(model_getImg.index(row, 2))
        shutil.rmtree('../ima_student/'+data1+'_'+data2+'_'+data3)
        self.load_table()

    def getImg_student(self):
        cap = cv2.VideoCapture(0)
        if(self.txt_ten.text() == ''):
            QtWidgets.QMessageBox.about(QWidget(), "Wanning", "Tên không được rỗng")
            return
        if(self.txt_mssv.text() == ''):
            QtWidgets.QMessageBox.about(QWidget(), "Wanning", "Mssv không được rỗng")
            return
        if(self.txt_lop.text == ''):
            QtWidgets.QMessageBox.about(QWidget(), "Wanning", "Lớp không được rỗng")
            return
        image_dir = os.path.join(image_dir2_cas, "ima_student")

        title = self.txt_ten.text()+"_"+self.txt_mssv.text()+"_"+self.txt_lop.text()

        if not os.path.exists(image_dir+'/'+title):
            os.mkdir(image_dir + "/" + title)
            print("Directory ", image_dir+'\\' + title,  " Created ")
        else:
            QtWidgets.QMessageBox.about(
                self, "Wanning", "da ton tai sinh vien trong he thong")
            self.txt_ten.setText('')
            self.txt_mssv.setText('')
            self.txt_lop.setText('')
            return

        dem = 0
        while True:
            ret, img = cap.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            for (x, y, w, h) in faces:
                dem = dem + 1
                print(dem)
                label = str(title)
                label_ids[label] = 0
                id_ = label_ids[label]
                roi = gray[y:y+h, x:x+w]
                cv2.imwrite(image_dir + "/" + title + "/" + "." +
                            str(dem) + ".jpg", gray[y:y+h, x:x+w])
                x_train.append(roi)
                cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.imshow('frames', img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cap.release()
                break
            if dem == 100:
                self.load_table()
                cap.release()
                cv2.destroyAllWindows()
                break

    def check_trained(self, trainer_mssv, mssv):
        for i in range(len(mssv)):
            if trainer_mssv in mssv:
                return True
            else:
                return False
    def check_mssv_list(self, mssv):
        if mssv == []:
            return True
        else:
            return False
    def faces_train(self):
        print("Start Train!")
        image_dir2 = dirname(str(BASE_DIR))
        image_dir = os.path.join(image_dir2, "ima_student")
        labels_id1 = {}
        label_add_database = []
        y_labels = []
        x_train = []
        malop = []
        for root, dirs, files in os.walk(image_dir):
            for file in files:
                if file.endswith("png") or file.endswith("jpg"):
                    path = os.path.join(root, file)
                    label = os.path.basename(root)
                    lbl_split1 = label.split("_")
                    if not label in labels_id1:
                        labels_id1[label] = lbl_split1[2]
                        label_add_database.append(label)
                    if not labels_id1[label] in malop:   
                        malop.append(labels_id1[label])
        for i in range(len(malop)):
            labels_id = {}
            y_labels = []
            x_train = []
            for root, dirs, files in os.walk(image_dir):
                for file in files:
                    if file.endswith("png") or file.endswith("jpg"):
                        path = os.path.join(root, file)
                        label = os.path.basename(root)
                        lbl_split = label.split("_")
                        if(malop[i] == lbl_split[2]):
                            if not label in labels_id:
                                labels_id[label] = int(lbl_split[1])
                            id_ = labels_id[label]
                            pil_image = Image.open(path)
                            image_array = np.array(pil_image, "uint8")  
                            faces = face_cascade.detectMultiScale(image_array, 1.1, 4)
                            for (x, y, w, h) in faces:
                                roi = image_array[y:y+h, x:x+w]
                                x_train.append(roi)
                                y_labels.append(id_)
                        else:
                            continue                          
            with open(image_dir2 + "/pickles/" +malop[i]+".pickle", "wb") as f:
                pickle.dump(labels_id, f)
            recognizer.train(x_train, np.array(y_labels))
            recognizer.save(image_dir2 + "/classes_yml/"+malop[i]+".yml")
        student = []
        mssv = []
        list_class = cursor.execute('SELECT * FROM classes')
        result = cursor.fetchall()
        list_student = cursor.execute('SELECT * FROM student')
        print(malop)
        print(len(result)==0)
        for i in list_student:
            mssv.append(i[0])

        for i in range(len(label_add_database)):
            student.append(label_add_database[i].split("_"))
        
        if(len(result)==0):
            for j in range(len(malop)):
                cursor.execute('INSERT INTO qlusername.dbo.classes(malop) values(?)',
                            (malop[j]))
                
                cursor.commit()
        else:
            for i in malop:
                flag = 0
                for j in range(len(result)):
                    if(i==result[j][0]):
                        flag +=1
                if(flag==0):
                    cursor.execute('INSERT INTO qlusername.dbo.classes(malop) values(?)',
                                (malop[j]))
                    cursor.commit()                    

        for i in range(len(student)):
            if self.check_mssv_list(mssv) == True:
                cursor.execute('INSERT INTO qlusername.dbo.student(ten,mssv,malop) values(?,?,?)',
                               (student[i][0], student[i][1], student[i][2]))
                cursor.commit()
            elif self.check_trained(student[i][1], mssv) == False:
                cursor.execute('INSERT INTO qlusername.dbo.student(ten,mssv,malop) values(?,?,?)',
                               (student[i][0], student[i][1], student[i][2]))
                cursor.commit()
            else:
                print("Sinh vien", student[i][1], "da co trong he thong")
        self.load_table()
        print("Done!")

    

    def load_table(self):
        model_getImg.clear()
        model_getTrain.clear()
        image_dir2 = dirname(str(BASE_DIR))
        image_dir = os.path.join(image_dir2, "ima_student")

        students = []
        students_Trained = [] 
        mssv = []
        list_student = cursor.execute('SELECT * FROM student')
        for i in list_student:
            mssv.append(i[0])
            students_Trained.append(i)
        
        
        for root, dirs, files in os.walk(image_dir):
            for file in files:
                if file.endswith("png") or file.endswith("jpg"):
                    label = os.path.basename(root)
                    info = label.split('_')
                    if not info in students:
                        students.append(info)
        #print(students)
        item_ten_list = []
        item_mssv_list = []
        item_lop_list = []

        item_ten_trained = []
        item_mssv_trained = []
        item_lop_trained = []

        for i in range(len(students)):
            if self.check_mssv_list(mssv) == True:
                item_ten_list.append(students[i][0])
                item_mssv_list.append(students[i][1])
                item_lop_list.append(students[i][2])
            else: 
                if self.check_trained(students[i][1], mssv) == False:
                    item_ten_list.append(students[i][0])
                    item_mssv_list.append(students[i][1])
                    item_lop_list.append(students[i][2])
        for i in range(len(students_Trained)):
            item_mssv_trained.append(students_Trained[i][0]) 
            item_ten_trained.append(students_Trained[i][1])
            item_lop_trained.append(students_Trained[i][2])
        
        for i in range(len(item_mssv_list)):
            item_ten = QtGui.QStandardItem(str(item_ten_list[i]))
            model_getImg.setItem(i, 0, item_ten)

            item_mssv = QtGui.QStandardItem(str(item_mssv_list[i]))
            model_getImg.setItem(i, 1, item_mssv)

            item_lop = QtGui.QStandardItem(str(item_lop_list[i]))
            model_getImg.setItem(i, 2, item_lop)
        
        for i in range(len(item_mssv_trained)):
            item_ten = QtGui.QStandardItem(str(item_ten_trained[i]))
            model_getTrain.setItem(i, 0, item_ten)

            item_mssv = QtGui.QStandardItem(str(item_mssv_trained[i]))
            model_getTrain.setItem(i, 1, item_mssv)

            item_lop = QtGui.QStandardItem(str(item_lop_trained[i]))
            model_getTrain.setItem(i, 2, item_lop)
        
        model_getImg.setHorizontalHeaderLabels(['Tên', 'MSSV', 'Lớp'])
        model_getTrain.setHorizontalHeaderLabels(['Tên', 'MSSV', 'Lớp'])


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Train()
    ui.setupUi(MainWindow)
    ui.load_table()
    MainWindow.show()
    sys.exit(app.exec_())
