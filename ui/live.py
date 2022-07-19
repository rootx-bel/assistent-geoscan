import cv2
from back.video import FrameProcessor
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QThread, pyqtSignal, QSize, Qt, pyqtSlot
import math
import piexif
import os
from exif import Image
from GPSPhoto import gpsphoto
import numpy as np

try:
    import wx
    app = wx.App(False)
    width, height = wx.GetDisplaySize()
except:
    width, height = 1920, 1080

class Thread(QThread):
    change_pixmap = pyqtSignal(QImage)
    scaled_size = QSize(width, height)
    fp = FrameProcessor()
    detected = pyqtSignal(bool)
    croped = pyqtSignal(np.ndarray, np.ndarray)

    def __init__(self, src_path, save_path, device, parent=None):
        self.__run = True
        super().__init__(parent)
        self.device = device
        self.save_path = save_path
        self.path = src_path
        self.name = 0
        self.frame_count = 0

    def save_metadata(self, img, data):
        name = self.path.split('.')[0].split('/')[-1]
        if not os.path.exists(self.save_path + '/' + name):
            os.mkdir(self.save_path + '/' + name)
        path = str(self.save_path) +'/' + name + '/' + str(self.name) + '.jpg'
        cv2.imwrite(path, img)
        photo = gpsphoto.GPSPhoto(path)
        info = gpsphoto.GPSInfo((data[1], data[0]), alt=int(data[2]))
        photo.modGPSData(info, path)
        self.name += 1

    def run(self):
        cap = cv2.VideoCapture(self.device)
        video = False
        metadata_exists = False
        if type(self.device) == str:
            try:
                property_id = int(cv2.CAP_PROP_FRAME_COUNT) 
                self.frame_count = int(cv2.VideoCapture.get(cap, property_id))
                self.fp.process_subtitles(self.device)
                metadata_exists = True
            except:
                pass
            video = True
        while self.__run:
            ret, frame = cap.read()
            if ret:
                img, is_detected, data, crop_orig, crop  = self.fp.get_segmentation(frame, video)
                self.detected.emit(is_detected)
                if is_detected:
                    if metadata_exists:
                        self.save_metadata(img, data)
                    self.croped.emit(crop_orig, crop)
                    
                convertToQtFormat = QImage(
                    img.data, img.shape[1], img.shape[0], QImage.Format_BGR888)
                p = convertToQtFormat.scaled(
                    self.scaled_size)
                self.change_pixmap.emit(p)

    def scaled(self, scaled_size):
        self.scaled_size = scaled_size

    def quit(self):
        self.__run = False
        super().quit()

    def start(self):
        self.__run = True
        super().start()

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
        self.th = Thread('c.mp4','saves','c.mp4',parent=self)
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
        self.display.th.fp.set_settings(param)