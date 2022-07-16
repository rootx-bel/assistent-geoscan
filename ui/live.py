import cv2
from back.video import FrameProcessor
from ui.settings import Settings
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QThread, pyqtSignal, QSize, Qt, pyqtSlot, QEvent

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

    def run(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if ret:
                img, is_detected = self.fp.get_segmentation(frame)
                convertToQtFormat = QImage(
                    img.data, img.shape[1], img.shape[0], QImage.Format_BGR888)
                p = convertToQtFormat.scaled(
                    self.scaled_size)
                self.change_pixmap.emit(p)

    def scaled(self, scaled_size):
        self.scaled_size = scaled_size


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
        self.th = Thread(self)
        self.th.change_pixmap.connect(self.setImage)
        self.resize_signal.connect(self.th.scaled)
        self.setLayout(self.layout)


class LiveWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.display = PlayStreaming()
        # self.settings = Settings(
        #     lambda: self.display.th.fp.set_settings(self.settings.get_result()))

        self.layout.addWidget(
            self.display, alignment=Qt.AlignCenter, stretch=1)
        self.setLayout(self.layout)

    def resizeEvent(self, event):
        self.display.resize_signal.emit(self.size())
        super().resizeEvent(event)
