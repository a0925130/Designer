# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1269, 878)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.viewData = QtWidgets.QLabel(self.centralwidget)
        self.viewData.setGeometry(QtCore.QRect(10, 10, 761, 441))
        self.viewData.setText("")
        self.viewData.setObjectName("viewData")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 731, 1011, 111))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.warning_display = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("標楷體")
        font.setPointSize(22)
        self.warning_display.setFont(font)
        self.warning_display.setText("")
        self.warning_display.setObjectName("warning_display")
        self.verticalLayout.addWidget(self.warning_display)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(800, 300, 441, 71))
        font = QtGui.QFont()
        font.setPointSize(22)
        self.label.setFont(font)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setStyleSheet("background-color: blue;\n"
                                 "color:white;")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(10, 460, 771, 41))
        font = QtGui.QFont()
        font.setPointSize(22)
        self.label_6.setFont(font)
        self.label_6.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_6.setStyleSheet("background-color: blue;\n"
                                   "color:white;")
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 510, 771, 181))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.lamp_status = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.lamp_status.setStyleSheet("background-color: red;\n"
                                       "border-radius: 85px;\n"
                                       "")
        self.lamp_status.setText("")
        self.lamp_status.setObjectName("lamp_status")
        self.horizontalLayout_4.addWidget(self.lamp_status)
        self.robot_status = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.robot_status.setStyleSheet("background-color: red;\n"
                                        "border-radius: 85px;\n"
                                        "")
        self.robot_status.setText("")
        self.robot_status.setObjectName("robot_status")
        self.horizontalLayout_4.addWidget(self.robot_status)
        self.track_status = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.track_status.setStyleSheet("background-color: red;\n"
                                        "border-radius: 85px;\n"
                                        "")
        self.track_status.setText("")
        self.track_status.setObjectName("track_status")
        self.horizontalLayout_4.addWidget(self.track_status)
        self.camera_status = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.camera_status.setStyleSheet("background-color: red;\n"
                                         "border-radius: 85px;\n"
                                         "")
        self.camera_status.setText("")
        self.camera_status.setObjectName("camera_status")
        self.horizontalLayout_4.addWidget(self.camera_status)
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(780, 20, 481, 271))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Open_all = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Open_all.sizePolicy().hasHeightForWidth())
        self.Open_all.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("標楷體")
        font.setPointSize(22)
        self.Open_all.setFont(font)
        self.Open_all.setAutoFillBackground(False)
        self.Open_all.setStyleSheet("background-color: green;\n"
                                    "border-radius: 50px;\n"
                                    "color:white;")
        self.Open_all.setObjectName("Open_all")
        self.horizontalLayout.addWidget(self.Open_all)
        self.emergency = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.emergency.sizePolicy().hasHeightForWidth())
        self.emergency.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("標楷體")
        font.setPointSize(22)
        self.emergency.setFont(font)
        self.emergency.setStyleSheet("background-color: red;\n"
                                     "border-radius: 50px;\n"
                                     "color:white;")
        self.emergency.setObjectName("emergency")
        self.horizontalLayout.addWidget(self.emergency)
        self.layoutWidget1 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget1.setGeometry(QtCore.QRect(800, 380, 441, 331))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.track = QtWidgets.QPushButton(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.track.sizePolicy().hasHeightForWidth())
        self.track.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.track.setFont(font)
        self.track.setStyleSheet("background-color:white;\n"
                                 "border-radius: 50px;")
        self.track.setObjectName("track")
        self.verticalLayout_2.addWidget(self.track)
        self.robot_button = QtWidgets.QPushButton(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.robot_button.sizePolicy().hasHeightForWidth())
        self.robot_button.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.robot_button.setFont(font)
        self.robot_button.setStyleSheet("background-color:white;\n"
                                        "border-radius: 50px;")
        self.robot_button.setObjectName("robot_button")
        self.verticalLayout_2.addWidget(self.robot_button)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.Camera_switch = QtWidgets.QPushButton(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Camera_switch.sizePolicy().hasHeightForWidth())
        self.Camera_switch.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.Camera_switch.setFont(font)
        self.Camera_switch.setStyleSheet("background-color:white;\n"
                                         "border-radius: 50px;")
        self.Camera_switch.setObjectName("Camera_switch")
        self.verticalLayout_3.addWidget(self.Camera_switch)
        self.lamp_switch = QtWidgets.QPushButton(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lamp_switch.sizePolicy().hasHeightForWidth())
        self.lamp_switch.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.lamp_switch.setFont(font)
        self.lamp_switch.setStyleSheet("background-color:white;\n"
                                       "border-radius: 50px;")
        self.lamp_switch.setObjectName("lamp_switch")
        self.verticalLayout_3.addWidget(self.lamp_switch)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        self.layoutWidget2 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget2.setGeometry(QtCore.QRect(10, 691, 771, 41))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.layoutWidget2)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget2)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_2.setFont(font)
        self.label_2.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setTextInteractionFlags(
            QtCore.Qt.LinksAccessibleByMouse | QtCore.Qt.TextSelectableByKeyboard | QtCore.Qt.TextSelectableByMouse)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.label_4 = QtWidgets.QLabel(self.layoutWidget2)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        self.label_5 = QtWidgets.QLabel(self.layoutWidget2)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_3.addWidget(self.label_5)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget2)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.stop_all = QtWidgets.QPushButton(self.centralwidget)
        self.stop_all.setGeometry(QtCore.QRect(1050, 720, 171, 131))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stop_all.sizePolicy().hasHeightForWidth())
        self.stop_all.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.stop_all.setFont(font)
        self.stop_all.setStyleSheet("background-color: red;\n"
                                    "border-radius: 50px;\n"
                                    "color:white;")
        self.stop_all.setObjectName("stop_all")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "功能鍵"))
        self.label_6.setText(_translate("MainWindow", "狀態監測"))
        self.Open_all.setText(_translate("MainWindow", "一鍵啟動"))
        self.emergency.setText(_translate("MainWindow", "急停按鈕"))
        self.track.setText(_translate("MainWindow", "履帶控制"))
        self.robot_button.setText(_translate("MainWindow", "手臂控制"))
        self.Camera_switch.setText(_translate("MainWindow", "相機控制"))
        self.lamp_switch.setText(_translate("MainWindow", "燈光控制"))
        self.label_2.setText(_translate("MainWindow", "燈光狀況"))
        self.label_4.setText(_translate("MainWindow", "手臂狀態"))
        self.label_5.setText(_translate("MainWindow", "履帶狀態"))
        self.label_3.setText(_translate("MainWindow", "影像狀況"))
        self.stop_all.setText(_translate("MainWindow", "關閉"))