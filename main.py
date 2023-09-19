import sys
# pip install pyqt5
import cv2, time
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from main_gui import Ui_MainWindow
from config.config_system import *
from system.components import CaptureVideo

fps = 0


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._translate = QtCore.QCoreApplication.translate
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self)
        self.configUI()

        self.uic.startButton.clicked.connect(self.start_capture_video)
        self.uic.endButton.clicked.connect(self.stop_capture_video)

        self.thread = {}

    def configUI(self):
        self.uic.tabWidget.setGeometry(QtCore.QRect(START_X, START_Y, TABWIDGET_W, TABWIDGET_H))
        # self.uic.detectBox.setGeometry(QtCore.QRect(
        #     DETECT_BOX[0],
        #     DETECT_BOX[1],
        #     DETECT_BOX[2],
        #     DETECT_BOX[3]
        # ))

    def closeEvent(self, event):
        self.stop_capture_video()

    def stop_capture_video(self):
        self.thread[1].stop()

    def start_capture_video(self):
        self.thread[1] = CaptureVideo(index=1)
        self.thread[1].start()
        self.thread[1].signal.connect(self.show_wedcam)

    def show_wedcam(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.uic.showFps.setText(f"FPS: {self.thread[1].fps}")
        self.uic.label_2.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(591, 311, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())
