# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tissueloc.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets\
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QImage
import cv2, imutils


class Ui_tissueloc(object):
    def setupUi(self, tissueloc):
        tissueloc.setObjectName("tissueloc")
        tissueloc.resize(810, 708)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(tissueloc.sizePolicy().hasHeightForWidth())
        tissueloc.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(tissueloc)
        self.centralwidget.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(11, 11, 791, 671))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.img_lbl = QtWidgets.QLabel(self.layoutWidget)
        self.img_lbl.setText("")
        self.img_lbl.setObjectName("img_lbl")
        self.gridLayout.addWidget(self.img_lbl, 0, 0, 1, 2)
        self.open_btn = QtWidgets.QPushButton(self.layoutWidget)
        self.open_btn.setObjectName("open_btn")
        self.gridLayout.addWidget(self.open_btn, 1, 0, 1, 1)
        self.save_btn = QtWidgets.QPushButton(self.layoutWidget)
        self.save_btn.setObjectName("save_btn")
        self.gridLayout.addWidget(self.save_btn, 1, 1, 1, 1)
        self.color_slider = QtWidgets.QSlider(self.layoutWidget)
        self.color_slider.setOrientation(QtCore.Qt.Vertical)
        self.color_slider.setObjectName("color_slider")
        self.gridLayout.addWidget(self.color_slider, 0, 2, 1, 1)
        tissueloc.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(tissueloc)
        self.statusbar.setObjectName("statusbar")
        tissueloc.setStatusBar(self.statusbar)

        self.retranslateUi(tissueloc)
        self.color_slider.valueChanged['int'].connect(self.color_slider.setValue)
        self.open_btn.clicked.connect(self.open_btn.click)
        self.save_btn.clicked.connect(self.save_btn.click)
        QtCore.QMetaObject.connectSlotsByName(tissueloc)


		# Added code here
		self.filename = None # Will hold the image address location
		self.tmp = None # Will hold the temporary image for display
		self.color_value_now = 0 # Updated brightness value


	def loadImage(self):
		""" This function will load the user selected image
			and set it to label using the setPhoto function
		"""
		self.filename = QFileDialog.getOpenFileName(filter="Image (*.*)")[0]
		self.image = cv2.imread(self.filename)
		self.setPhoto(self.image)


	def setPhoto(self,image):
		""" This function will take image input and resize it
			only for display purpose and convert it to QImage
			to set at the label.
		"""
		self.tmp = image
		image = imutils.resize(image, width=640)
		frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		image = QImage(frame, frame.shape[1],frame.shape[0],frame.strides[0],QImage.Format_RGB888)
		self.img_lbl.setPixmap(QtGui.QPixmap.fromImage(image))


    def retranslateUi(self, tissueloc):
        _translate = QtCore.QCoreApplication.translate
        tissueloc.setWindowTitle(_translate("tissueloc", "TissueLoc"))
        self.open_btn.setText(_translate("tissueloc", "Open"))
        self.save_btn.setText(_translate("tissueloc", "Save"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    tissueloc = QtWidgets.QMainWindow()
    ui = Ui_tissueloc()
    ui.setupUi(tissueloc)
    tissueloc.show()
    sys.exit(app.exec_())
