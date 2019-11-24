# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '1.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog,QLabel
from PyQt5.QtGui import QIcon, QPixmap,QImage
from PyQt5.uic import loadUi
import cv2
import pickle
cap = cv2.VideoCapture(0)

cap.set(3, 480) #set width of the frame
cap.set(4, 640) #set height of the frame
MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
age_list = ['(0, 2)', '(4, 6)', '(8, 12)', '(15, 20)', '(25, 32)', '(38, 43)', '(48, 53)', '(60, 100)']
gender_list = ['Male', 'Female']
# Load the cascade
face_cascade = cv2.CascadeClassifier('lib/haarcascade_frontalface_alt.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("face-trainner.yml")
labels = {"person_name": 1}
with open("face-labels.pickle", 'rb') as f:
	og_labels = pickle.load(f)
	labels = {v:k for k,v in og_labels.items()}
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lbl1 = QtWidgets.QLabel(self.centralwidget)
        self.lbl1.setGeometry(QtCore.QRect(40, 40, 401, 481))
        self.lbl1.setObjectName("lbl1")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.loadimage()
    def loadimage(self):
        #Set image to label
        age_net, gender_net = load_caffe_models()
        self.lbl1.setPixmap(QPixmap.fromImage(detectface_reltime('1.jpg')))
        #self.lbl1.setScaledContents(True)
def load_caffe_models():
    age_net = cv2.dnn.readNetFromCaffe('lib/deploy_age.prototxt', 'lib/age_net.caffemodel')
    gender_net = cv2.dnn.readNetFromCaffe('lib/deploy_gender.prototxt', 'lib/gender_net.caffemodel')
    return(age_net, gender_net)
def detectface(path):
        # Load the cascade
        face_cascade = cv2.CascadeClassifier('lib/haarcascade_frontalface_alt.xml')
        # Read the input image
        img = cv2.imread(path)
        #img = cv2.resize(img,(360,480))
        # Convert into grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        # Draw rectangle around the faces
        #print(faces)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        # Convert cv image to pixmap image
        cv2.imshow('img',img)
        height, width, channel = img.shape
        bytesPerLine = 3 * width
        return QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
def detectface_reltime(path):
        # Read the input image
        img = cv2.imread(path)
        #img = cv2.resize(img,(360,480))
        # Convert into grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        # Draw rectangle around the faces
        #print(faces)
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h,x:x+w]
            id_,conf =recognizer.predict(roi_gray)
            print(conf)
            print(id_)
            if conf >80 and conf <95:
                font = cv2.FONT_HERSHEY_SIMPLEX
                name = labels[id_]
                color = (0, 0, 0)
                stroke = 2
                cv2.putText(img, name, (x,y), font, 1, color, stroke, cv2.LINE_AA)
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        # Convert cv image to pixmap image
        cv2.imshow('img',img)
        height, width, channel = img.shape
        bytesPerLine = 3 * width
        return QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()        
def detectface_meta(path,age_net,gender_net):
        font = cv2.FONT_HERSHEY_SIMPLEX
        # Load the cascade
        face_cascade = cv2.CascadeClassifier('lib/haarcascade_frontalface_alt.xml')
        # Read the input image
        img = cv2.imread(path)
        #img = cv2.resize(img,(360,480))
        # Convert into grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        # Draw rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            #Get Face 
            face_img = img[y:y+h, h:h+w].copy()
            blob = cv2.dnn.blobFromImage(face_img, 1, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
            #Predict Gender
            gender_net.setInput(blob)
            gender_preds = gender_net.forward()
            gender = gender_list[gender_preds[0].argmax()]
            print("Gender : " + gender)
            #Predict Age
            age_net.setInput(blob)
            age_preds = age_net.forward()
            age = age_list[age_preds[0].argmax()]
            print("Age Range: " + age)
            overlay_text = "%s %s" % (gender, age)
            cv2.putText(img, overlay_text, (x, y), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
        # Convert cv image to pixmap image
        height, width, channel = img.shape
        bytesPerLine = 3 * width
        return QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
def detectface_videos(age_net,gender_net):
    font = cv2.FONT_HERSHEY_SIMPLEX
    while True:
        ret, img = cap.read()
        # Load the cascade
        face_cascade = cv2.CascadeClassifier('lib/haarcascade_frontalface_alt.xml')
        # Read the input image
        #img = cv2.imread(path)
        #img = cv2.resize(img,(360,480))
        # Convert into grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        # Draw rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            #Get Face 
            face_img = img[y:y+h, h:h+w].copy()
            blob = cv2.dnn.blobFromImage(face_img, 1, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
            #Predict Gender
            gender_net.setInput(blob)
            gender_preds = gender_net.forward()
            gender = gender_list[gender_preds[0].argmax()]
            #print("Gender : " + gender)
            #Predict Age
            age_net.setInput(blob)
            age_preds = age_net.forward()
            age = age_list[age_preds[0].argmax()]
            #print("Age Range: " + age)
            overlay_text = "%s %s" % (gender, age)
            cv2.putText(img, overlay_text, (x, y), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
        # Convert cv image to pixmap image
        #height, width, channel = img.shape
        #bytesPerLine = 3 * width
        cv2.imshow('frame', img)  
        #0xFF is a hexadecimal constant which is 11111111 in binary.
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break
    cap.release()
    cv2.destroyAllWindow()
def detectface_videos_realtime():
    font = cv2.FONT_HERSHEY_SIMPLEX
    while True:
        ret, img = cap.read()
        
        # Load the cascade
        face_cascade = cv2.CascadeClassifier('lib/haarcascade_frontalface_alt.xml')
        # Read the input image
        #img = cv2.imread(path)
        #img = cv2.resize(img,(360,480))
        # Convert into grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        # Draw rectangle around the faces
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h,x:x+w]
            id_,conf =recognizer.predict(roi_gray)
            if conf>=4 and conf <= 85:
                font = cv2.FONT_HERSHEY_SIMPLEX
                name = labels[id_]
                color = (0, 0, 0)
                stroke = 2
                cv2.putText(img, name, (x,y), font, 1, color, stroke, cv2.LINE_AA)
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

        cv2.imshow('frame', img)  
        #0xFF is a hexadecimal constant which is 11111111 in binary.
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break
    cap.release()
    cv2.destroyAllWindow()
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    age_net, gender_net = load_caffe_models()
    #detectface_videos_realtime()
    #detectface_videos(age_net,gender_net) 
    sys.exit(app.exec_())
