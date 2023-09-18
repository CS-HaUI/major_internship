import cv2
from config.config_system import *


class Camera:
    def __init__(self, source=0):
        self.source = source
        self._frame = None
        self._cam = None
        self._frame_width = None
        self._frame_height = None
        self._is_running = False
        self.res = True

    def init_camera(self):
        self._cam = cv2.VideoCapture(self.source)

    def read_frame(self):
        self.res, self._frame = self._cam.read()
        return self.res, self._frame


    def release_camera(self):
        self._cam.release()
        cv2.destroyAllWindows()
        self.__init__(source=0)