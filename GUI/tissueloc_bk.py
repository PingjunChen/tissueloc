# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tissueloc.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QImage
import cv2, imutils, copy
import numpy as np

from tl_utils import rgb2gray, locate_tissue_cnts


class Ui_tissueloc(object):
    def setupUi(self, tissueloc):
        tissueloc.setObjectName("tissueloc")
        tissueloc.resize(810, 708)
        tissueloc.setFixedSize(810, 708)
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
        self.color_slider.setRange(132, 228)
        self.color_slider.valueChanged['int'].connect(self.color_value)
        self.open_btn.clicked.connect(self.loadImage)
        self.save_btn.clicked.connect(self.save_btn.click)
        QtCore.QMetaObject.connectSlotsByName(tissueloc)


		# Added code here
        self.filename = None # Will hold the image address location
        self.color_value_now = 200 # Updated brightness value
        self.max_width = 780
        self.max_height = 680


    def loadImage(self):
        self.filename = QFileDialog.getOpenFileName(filter="Image (*.*)")[0]
        self.image = cv2.imread(self.filename)
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        # convert to rgb to gray
        self.gray_img = rgb2gray(self.image)
        self.color_slider.setValue(self.color_value_now)
        cnts = locate_tissue_cnts(self.gray_img, self.color_value_now)

        show_img = copy.deepcopy(self.image)
        cv2.drawContours(show_img, cnts, -1, (0, 255, 0), 9)
        self.setPhoto(show_img)


    def setPhoto(self, image):
        hw_ratio = image.shape[0] * 1.0 / image.shape[1]
        if hw_ratio <= self.max_height * 1.0 / self.max_width:
            resize_w = self.max_width
        else:
            resize_w = int(image.shape[1] * self.max_height * 1.0 / image.shape[0])
        image = imutils.resize(image, width = resize_w)
        image = QImage(image, image.shape[1], image.shape[0], image.strides[0], QImage.Format_RGB888)
        self.img_lbl.setPixmap(QtGui.QPixmap.fromImage(image))
        self.img_lbl.setAlignment(QtCore.Qt.AlignCenter)


    def color_value(self, value):
        """ Take the colore threshold from vertical slider.
        """
        self.color_value_now = value
        print("Current threshold: {}".format(self.color_value_now))
        self.update_tissueloc()


    def changeColorValue(self, img, value):
        """ Take the image and the threshold and perform the tissue localization.
        """
        cnts = locate_tissue_cnts(self.gray_img, self.color_value_now)
        show_img = copy.deepcopy(self.image)
        cv2.drawContours(show_img, cnts, -1, (0, 255, 0), 9)

        return show_img


    def update_tissueloc(self):
        img = self.changeColorValue(self.image, self.color_value_now)
        self.setPhoto(img)


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
