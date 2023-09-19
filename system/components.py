import cv2, time
from PyQt5.QtCore import QThread, pyqtSignal
import numpy as np


class CaptureVideo(QThread):
    signal = pyqtSignal(np.ndarray)


    def __init__(self, index):
        self.index = index
        print("start threading", self.index)
        super(CaptureVideo, self).__init__()
        self.start_time = time.time()
        self.frame_count = 0
        self.fps = 0

    def run(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, cv_img = cap.read()
            if ret:
                # ---------------- FPS ------------------
                self.frame_count += 1
                elapsed_time = time.time() - self.start_time
                if elapsed_time > 1:
                    self.fps = int(self.frame_count / elapsed_time)
                    self.frame_count = 0
                    self.start_time = time.time()
                # ---------------- FPS ------------------
                self.signal.emit(cv_img)

    def stop(self):
        # print("stop threading", self.index)
        self.terminate()
