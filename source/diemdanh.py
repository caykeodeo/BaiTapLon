# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtCore, QtGui, QtWidgets
from cv2 import cv2
from os import path
#from csv import DictWriter
import csv
import datetime
import pandas
import pyodbc

class Ui_frmDiemDanh(object):

    face_cascade = cv2.CascadeClassifier('../cascades/haarcascade_frontalface_alt.xml')

    recognizer = cv2.face.LBPHFaceRecognizer_create()

    conn = pyodbc.connect('Driver={SQL Server};'
                        'Server=DESKTOP-C2S1KLM;'
                        'Database=qlusername;'
                        'Trusted_Connection=yes;')

    cursor = conn.cursor()

    # Biến để lưu hình điểm danh
    image = []

    # Đánh dấu đã điểm danh hay chưa
    flag = False
    
    # Biến để lưu danh sách sinh viên
    studentsList = []

    def setupUi(self, frmDiemDanh):  

        # Code giao diện
        frmDiemDanh.setObjectName("frmDiemDanh")
        frmDiemDanh.resize(1002, 786)
        self.centralwidget = QtWidgets.QWidget(frmDiemDanh)
        self.centralwidget.setObjectName("centralwidget")
        self.tableLop = QtWidgets.QTableWidget(self.centralwidget)
        self.tableLop.setGeometry(QtCore.QRect(730, 30, 251, 251))
        self.tableLop.setObjectName("tableLop")
        self.tableLop.setColumnCount(1)
        self.tableLop.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableLop.setHorizontalHeaderItem(0, item)
        self.tableLop.itemClicked.connect(self.loadListSinhVien)
        header = self.tableLop.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)       
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.tableLop.verticalHeader().setVisible(False)
        self.tableLop.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.lblDSVang = QtWidgets.QLabel(self.centralwidget)
        self.lblDSVang.setGeometry(QtCore.QRect(20, 520, 101, 16))
        self.lblDSVang.setObjectName("lblDSVang")
        self.lblDSCoMat = QtWidgets.QLabel(self.centralwidget)
        self.lblDSCoMat.setGeometry(QtCore.QRect(370, 520, 111, 16))
        self.lblDSCoMat.setObjectName("lblDSCoMat")
        self.groupBoxChucNang = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBoxChucNang.setGeometry(QtCore.QRect(730, 290, 251, 111))
        self.groupBoxChucNang.setObjectName("groupBoxChucNang")
        self.btnDiemDanh = QtWidgets.QPushButton(self.groupBoxChucNang)
        self.btnDiemDanh.setGeometry(QtCore.QRect(20, 30, 93, 28))
        self.btnDiemDanh.setObjectName("btnDiemDanh")
        self.btnLayAnh = QtWidgets.QPushButton(self.groupBoxChucNang)
        self.btnLayAnh.setGeometry(QtCore.QRect(140, 30, 93, 28))
        self.btnLayAnh.setObjectName("btnLayAnh")
        self.btnXuatExcel = QtWidgets.QPushButton(self.groupBoxChucNang)
        self.btnXuatExcel.setGeometry(QtCore.QRect(20, 70, 211, 28))
        self.btnXuatExcel.setObjectName("btnXuatExcel")
        self.lblChonLop = QtWidgets.QLabel(self.centralwidget)
        self.lblChonLop.setGeometry(QtCore.QRect(730, 10, 55, 16))
        self.lblChonLop.setObjectName("lblChonLop")
        self.lblHinhChup = QtWidgets.QLabel(self.centralwidget)
        self.lblHinhChup.setGeometry(QtCore.QRect(20, 10, 91, 16))
        self.lblHinhChup.setObjectName("lblHinhChup")
        self.lblDisplay = QtWidgets.QLabel(self.centralwidget)
        self.lblDisplay.setGeometry(QtCore.QRect(20, 30, 691, 481))
        self.lblDisplay.setText("")
        self.lblDisplay.setObjectName("lblDisplay")
        self.lblDSLop = QtWidgets.QLabel(self.centralwidget)
        self.lblDSLop.setGeometry(QtCore.QRect(730, 410, 91, 16))
        self.lblDSLop.setObjectName("lblDSLop")
        self.listViewDSLop = QtWidgets.QListView(self.centralwidget)
        self.listViewDSLop.setGeometry(QtCore.QRect(730, 430, 251, 331))
        self.listViewDSLop.setObjectName("listViewDSLop")
        self.listViewCoMat = QtWidgets.QListView(self.centralwidget)
        self.listViewCoMat.setGeometry(QtCore.QRect(370, 540, 341, 221))
        self.listViewCoMat.setObjectName("listViewCoMat")
        self.listViewVang = QtWidgets.QListView(self.centralwidget)
        self.listViewVang.setGeometry(QtCore.QRect(20, 540, 341, 221))
        self.listViewVang.setObjectName("listViewVang")
        frmDiemDanh.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(frmDiemDanh)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1002, 26))
        self.menubar.setObjectName("menubar")
        frmDiemDanh.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(frmDiemDanh)
        self.statusbar.setObjectName("statusbar")
        frmDiemDanh.setStatusBar(self.statusbar)

        self.retranslateUi(frmDiemDanh)
        QtCore.QMetaObject.connectSlotsByName(frmDiemDanh)

        # Load data table lớp
        self.loadClasses()

        # Gán sự kiện cho button
        self.btnLayAnh.clicked.connect(self.browsePicture)
        self.btnDiemDanh.clicked.connect(self.diemDanh)
        self.btnXuatExcel.clicked.connect(self.exportExcel)


    # ---------------------------------------------------------------------------------------------------------------------
    # Hiển thị ảnh lên giao diện
    def displayPicture(self, image):
        # Chuyển ma trận hình sang đối tượng QImage của pyqt5
        height, width, channel = self.image.shape
        bytesPerLine = 3 * width
        qImg = QtGui.QImage(self.image.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888).rgbSwapped()

        # Hiển thị hình lên giao diện người dùng
        displayedPic = QtGui.QPixmap.fromImage(qImg)
        displayedPic = displayedPic.scaled(691,481, aspectRatioMode=QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
        self.lblDisplay.setPixmap(displayedPic)


    # ---------------------------------------------------------------------------------------------------------------------
    # Lấy ảnh và load DS sinh viên
    def browsePicture(self):
        # Mở cửa sổ browse file
        fileName = QtWidgets.QFileDialog.getOpenFileName(None,"Chọn ảnh lớp", "","All Files (*);;JPEG (*.jpeg;*.jpg;*.jpe;*.jfif);;PNG (*.png);;GIF (*.gif);;TIFF (*.tif;*.tff)")
        
        # Dòng if này kiểm tra xem người dùng có chọn hình nào hay không
        # Không chọn thì length = 0
        # Có chọn 1 hình thì length != 0
        if len(fileName[0]) > 0:
            # Đọc hình
            self.image = cv2.imread(fileName[0])
            # Hiển thị
            self.displayPicture(self.image)
        # Reset lại flag
        self.flag = False
     

    # ---------------------------------------------------------------------------------------------------------------------            
    # Load danh sách các lớp
    def loadClasses(self):
        self.cursor.execute('SELECT * FROM [dbo].[classes]')
        classesList = self.cursor.fetchall()
        numRow = len(classesList)
        #numCol = 2
        self.tableLop.setRowCount(numRow)
        for row in range(numRow):
            classesList[row][0] = str(classesList[row][0])
            self.tableLop.setItem(row, 0, QtWidgets.QTableWidgetItem(classesList[row][0]))
    # ---------------------------------------------------------------------------------------------------------------------            
    # Sự kiện load danh sách sinh viên
    def loadListSinhVien(self):
        self.studentsList.clear()
        model = QtGui.QStandardItemModel()
        self.listViewDSLop.setModel(model)
        model.removeRows(0,model.rowCount())
        # Load danh sách sinh viên trong 1 lớp được chọn
        row = self.tableLop.currentRow()
        if row > -1:
            malop = self.tableLop.item(row, 0).text()

            self.cursor.execute("SELECT *, flag = 'k' FROM [dbo].[student] WHERE [dbo].[student].malop = ?",(malop))
            columns = [column[0] for column in self.cursor.description]
            for row in self.cursor.fetchall():
                self.studentsList.append(dict(zip(columns, row)))

            if(len(self.studentsList) >= 0):
                model = QtGui.QStandardItemModel()
                self.listViewDSLop.setModel(model)
                for student in self.studentsList:
                    item = QtGui.QStandardItem(student['mssv'] + ' - ' + student['ten'])
                    model.appendRow(item)       
    # ---------------------------------------------------------------------------------------------------------------------
    # Điểm danh cho lớp đã chọn
    def diemDanh(self):
        row = self.tableLop.currentRow()
        
        if self.listViewDSLop.model() is None:
            error_dialog = QtWidgets.QMessageBox()
            error_dialog.setIcon(QtWidgets.QMessageBox.Critical)
            error_dialog.setWindowTitle("Lỗi")
            error_dialog.setInformativeText('Chưa chọn lớp')
            error_dialog.exec_()
            return
        if row > -1 and len(self.image) > 0:
            malop = self.tableLop.item(row, 0).text()
            yml_path = '../classes_yml/' + malop + '.yml'
            print(yml_path)
            # Kiểm tra xem file yml có tồn tại hay không
            if path.exists(yml_path):
                self.recognizer.read(yml_path)

                #dsCoMat = []

                gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

                faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4.5)

                for (x,y,w,h) in faces:
                    cv2.rectangle(self.image, (x,y), (x+w,y+h), (255,0,0),2)
                    roi_gray = gray[y:y+h, x:x+w]
                    id_, conf = self.recognizer.predict(roi_gray)
                    #if conf > 80 and conf < 95:
                    #dsCoMat.append(str(id_))
                    print("id:", id_)
                    # nếu có mặt thì bỏ flag k đi (k = vắng)
                    next((item for item in self.studentsList if item['mssv'] == str(id_)), None)['flag'] = ''

                    font = cv2.FONT_HERSHEY_COMPLEX
                    color = (230, 0, 38)
                    stroke = 2 # độ dày
                    cv2.putText(self.image, str(id_), (x, y), font, 1, color,stroke, cv2.LINE_AA)
                cv2.imwrite('../output_image/output.jpg',self.image)
                self.displayPicture(self.image)

                # Hiển thị list vắng mặt và list có mặt
                if(len(self.studentsList) >= 0):
                    modelVang = QtGui.QStandardItemModel()
                    modeCoMat = QtGui.QStandardItemModel()
                    self.listViewVang.setModel(modelVang)
                    self.listViewCoMat.setModel(modeCoMat)
    
                    for student in self.studentsList:
                        item = QtGui.QStandardItem(student['mssv'] + ' - ' + student['ten'])
                        if student['flag'] == 'k':
                            modelVang.appendRow(item)
                        else:
                            modeCoMat.appendRow(item)
                # Đánh dấu đã điểm danh xong
                self.flag = True

            # Nếu không tìm thấy file yml theo tên lớp thì sẽ báo lỗi
            else:
                error_dialog = QtWidgets.QMessageBox()
                error_dialog.setIcon(QtWidgets.QMessageBox.Critical)
                error_dialog.setWindowTitle("Lỗi")
                error_dialog.setInformativeText('Không tìm thấy trained data của lớp này')
                error_dialog.exec_()
                
        # Chưa load hình mà đã bấm điểm danh thì sẽ báo lỗi
        else:
            error_dialog = QtWidgets.QMessageBox()
            error_dialog.setIcon(QtWidgets.QMessageBox.Critical)
            error_dialog.setWindowTitle("Lỗi")
            error_dialog.setInformativeText('Chưa chọn ảnh lớp')
            error_dialog.exec_()
    
    
    # ---------------------------------------------------------------------------------------------------------------------
    # Xuất excel sau khi điểm danh
    def exportExcel(self):
        if self.flag == True:
            row = self.tableLop.currentRow()
            
            if row > -1:
                malop = self.tableLop.item(row, 0).text()
                with open('../excel/'+malop+'.csv', 'w', newline='', encoding='utf-8') as csv_file:
                    writer = csv.writer(csv_file, delimiter=';')
                    writer = csv.DictWriter(csv_file, ('mssv', 'ten', 'malop', 'flag'))
                    writer.writeheader()
                    writer.writerows(self.studentsList)
                csv_file.close()

                dialog = QtWidgets.QMessageBox()
                dialog.setInformativeText('Xuất excel thành công')
                dialog.exec_()

        else:
            error_dialog = QtWidgets.QMessageBox()
            error_dialog.setIcon(QtWidgets.QMessageBox.Critical)
            error_dialog.setWindowTitle("Lỗi")
            error_dialog.setInformativeText('Chưa điểm danh, không có dữ liệu để xuất')
            error_dialog.exec_()


    # ---------------------------------------------------------------------------------------------------------------------
    def retranslateUi(self, frmDiemDanh):
        _translate = QtCore.QCoreApplication.translate
        frmDiemDanh.setWindowTitle(_translate("frmDiemDanh", "Giao diện điểm danh"))
        item = self.tableLop.horizontalHeaderItem(0)
        item.setText(_translate("frmDiemDanh", "Tên lớp"))
        self.lblDSVang.setText(_translate("frmDiemDanh", "Danh sách vắng"))
        self.lblDSCoMat.setText(_translate("frmDiemDanh", "Danh sách có mặt"))
        self.groupBoxChucNang.setTitle(_translate("frmDiemDanh", "Chức năng"))
        self.btnDiemDanh.setText(_translate("frmDiemDanh", "Điểm danh"))
        self.btnLayAnh.setText(_translate("frmDiemDanh", "Lấy ảnh"))
        self.btnXuatExcel.setText(_translate("frmDiemDanh", "Xuất Excel"))
        self.lblChonLop.setText(_translate("frmDiemDanh", "Chọn lớp"))
        self.lblHinhChup.setText(_translate("frmDiemDanh", "Hình chụp lớp"))
        self.lblDSLop.setText(_translate("frmDiemDanh", "Danh sách lớp"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    frmDiemDanh = QtWidgets.QMainWindow()
    ui = Ui_frmDiemDanh()
    ui.setupUi(frmDiemDanh)
    frmDiemDanh.show()
    sys.exit(app.exec_())