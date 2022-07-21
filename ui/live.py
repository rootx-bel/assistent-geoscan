import cv2
from back.video import VideoThread
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import pyqtSignal, QSize, Qt, pyqtSlot
from exif import Image
from GPSPhoto import gpsphoto
import numpy as np

class PlayStreaming(QWidget):
    resize_signal = pyqtSignal(QSize)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

    def setCVImage(self, cvimg):
        rgbImage = cv2.cvtColor(cvimg, cv2.COLOR_BGR2RGB)
        qimg = QImage(
            rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)

    def initUI(self):
        self.label = QLabel(self)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.label, alignment=Qt.AlignCenter)
        self.th = VideoThread(0, parent=self)
        self.th.change_pixmap.connect(self.setImage)
        self.resize_signal.connect(self.th.scaled)
        self.setLayout(self.layout)


class LiveWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.display = PlayStreaming()
        self.layout.addWidget(
            self.display, alignment=Qt.AlignCenter, stretch=1)
        self.setLayout(self.layout)

    def resizeEvent(self, event):
        self.display.resize_signal.emit(self.size())
        super().resizeEvent(event)

    def set_video_thread(self, status = True):
        if status:
            self.display.th.start()
        else:
            self.display.th.quit()

    def set_settings(self, param):
        self.display.th.frame_processor.set_settings(param)