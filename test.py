from PyQt5 import QtCore, QtGui, QtWidgets

import cv2
from PIL import Image, ImageTk
import face_recognition

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(640, 480)
        Dialog.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.OpenHandCursor))
        self.showCamera = QtWidgets.QGraphicsView(Dialog)
        self.showCamera.setGeometry(QtCore.QRect(20, 20, 390, 440))
        self.showCamera.setObjectName("showCamera")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(430, 370, 190, 90))
        self.pushButton.setObjectName("pushButton")
        self.name_input = QtWidgets.QTextEdit(Dialog)
        self.name_input.setGeometry(QtCore.QRect(430, 180, 130, 30))
        self.name_input.setObjectName("name_input")
        self.name_label = QtWidgets.QLabel(Dialog)
        self.name_label.setGeometry(QtCore.QRect(430, 150, 70, 30))
        self.name_label.setObjectName("name_label")
        self.signup_label = QtWidgets.QLabel(Dialog)
        self.signup_label.setGeometry(QtCore.QRect(470, 120, 120, 40))
        self.signup_label.setObjectName("signup_label")
        self.name_check = QtWidgets.QPushButton(Dialog)
        self.name_check.setGeometry(QtCore.QRect(570, 180, 50, 30))
        self.name_check.setObjectName("name_check")
        self.showTime = QtWidgets.QLCDNumber(Dialog)
        self.showTime.setGeometry(QtCore.QRect(420, 30, 200, 40))
        self.showTime.setObjectName("showTime")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(430, 220, 190, 30))
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "Login"))
        self.name_label.setText(_translate("Dialog", "Name"))
        self.signup_label.setText(_translate("Dialog", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt;\">Sign Up</span></p></body></html>"))
        self.name_check.setText(_translate("Dialog", "Check"))
        self.pushButton_2.setText(_translate("Dialog", "Take Photo"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec())
