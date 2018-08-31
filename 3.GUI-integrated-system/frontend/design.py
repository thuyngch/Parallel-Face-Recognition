# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frontend/design.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(933, 507)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.wgVideo = QtWidgets.QWidget(self.centralwidget)
        self.wgVideo.setGeometry(QtCore.QRect(0, 10, 655, 495))
        self.wgVideo.setObjectName("wgVideo")
        self.lbWebVideo = QtWidgets.QLabel(self.centralwidget)
        self.lbWebVideo.setGeometry(QtCore.QRect(10, 0, 101, 17))
        self.lbWebVideo.setObjectName("lbWebVideo")
        self.lbExtrFace = QtWidgets.QLabel(self.centralwidget)
        self.lbExtrFace.setGeometry(QtCore.QRect(670, 0, 81, 17))
        self.lbExtrFace.setObjectName("lbExtrFace")
        self.wgFaceCrop = QtWidgets.QWidget(self.centralwidget)
        self.wgFaceCrop.setGeometry(QtCore.QRect(660, 10, 271, 181))
        self.wgFaceCrop.setObjectName("wgFaceCrop")
        self.lbInfo = QtWidgets.QLabel(self.wgFaceCrop)
        self.lbInfo.setGeometry(QtCore.QRect(10, 160, 261, 17))
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.lbInfo.setFont(font)
        self.lbInfo.setScaledContents(True)
        self.lbInfo.setObjectName("lbInfo")
        self.txtName = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.txtName.setGeometry(QtCore.QRect(670, 240, 261, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtName.sizePolicy().hasHeightForWidth())
        self.txtName.setSizePolicy(sizePolicy)
        self.txtName.setTabChangesFocus(True)
        self.txtName.setObjectName("txtName")
        self.lbName = QtWidgets.QLabel(self.centralwidget)
        self.lbName.setGeometry(QtCore.QRect(670, 220, 91, 17))
        self.lbName.setObjectName("lbName")
        self.btnCancel = QtWidgets.QPushButton(self.centralwidget)
        self.btnCancel.setGeometry(QtCore.QRect(830, 275, 101, 31))
        self.btnCancel.setObjectName("btnCancel")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Facial Recognition"))
        self.lbWebVideo.setText(_translate("MainWindow", "WebcamVideo"))
        self.lbExtrFace.setText(_translate("MainWindow", "Recognition"))
        self.lbInfo.setText(_translate("MainWindow", "No face detected"))
        self.lbName.setText(_translate("MainWindow", "Registration"))
        self.btnCancel.setText(_translate("MainWindow", "Cancel"))

