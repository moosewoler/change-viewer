# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/moose/p_project/20190116_嫦娥图像浏览器/work/changeviewer/custom_frame.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from ImageViewer import MyGraphicsView


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(991, 767)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.hlayout3 = QtWidgets.QHBoxLayout()
        self.hlayout3.setObjectName("hlayout3")
        self.lblPath = QtWidgets.QLabel(self.centralwidget)
        self.lblPath.setObjectName("lblPath")
        self.hlayout3.addWidget(self.lblPath)
        self.edtPath = QtWidgets.QLineEdit(self.centralwidget)
        self.edtPath.setObjectName("edtPath")
        self.hlayout3.addWidget(self.edtPath)
        self.verticalLayout_2.addLayout(self.hlayout3)
        self.hlayout2 = QtWidgets.QHBoxLayout()
        self.hlayout2.setObjectName("hlayout2")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.hlayout2.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.hlayout2.addWidget(self.pushButton_3)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hlayout2.addItem(spacerItem)
        self.btnOK = QtWidgets.QPushButton(self.centralwidget)
        self.btnOK.setObjectName("btnOK")
        self.hlayout2.addWidget(self.btnOK)
        self.verticalLayout_2.addLayout(self.hlayout2)

        self.graphicsScene = QtWidgets.QGraphicsScene()
        self.graphicsView = MyGraphicsView(self.graphicsScene)
        self.graphicsView.setObjectName("graphicsView")
        self.verticalLayout_2.addWidget(self.graphicsView)

        self.hlayout1 = QtWidgets.QHBoxLayout()
        self.hlayout1.setObjectName("hlayout1")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hlayout1.addItem(spacerItem1)
        self.btnPrev = QtWidgets.QPushButton(self.centralwidget)
        self.btnPrev.setObjectName("btnPrev")
        self.hlayout1.addWidget(self.btnPrev)
        self.btnReset = QtWidgets.QPushButton(self.centralwidget)
        self.btnReset.setObjectName("btnReset")
        self.hlayout1.addWidget(self.btnReset)
        self.btnNext = QtWidgets.QPushButton(self.centralwidget)
        self.btnNext.setObjectName("btnNext")
        self.hlayout1.addWidget(self.btnNext)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hlayout1.addItem(spacerItem2)
        self.verticalLayout_2.addLayout(self.hlayout1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 991, 29))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ChangE Viewer"))
        self.lblPath.setText(_translate("MainWindow", "Text"))
        self.edtPath.setText(_translate("MainWindow", "test.jpg"))
        self.pushButton_2.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_3.setText(_translate("MainWindow", "PushButton"))
        self.btnOK.setText(_translate("MainWindow", "PushButton"))
        self.btnPrev.setText(_translate("MainWindow", "<<"))
        self.btnReset.setText(_translate("MainWindow", "[1]"))
        self.btnNext.setText(_translate("MainWindow", ">>"))
