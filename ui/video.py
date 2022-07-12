from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
from back.video import FrameProcessor
from ui.settings import Settings

try:
    import wx
    app=wx.App(False)
    width, height = wx.GetDisplaySize()
except:
    width, height = 1920, 1080

class Thread(QtCore.QThread):
    change_pixmap = QtCore.pyqtSignal(QtGui.QImage)
    scaled_size = QtCore.QSize(width, height)
    
    
    def run(self):
        fp = FrameProcessor()
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if ret:
                img = fp.get_segmentation(frame)
                #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                convertToQtFormat = QtGui.QImage(rgb_image.data, rgb_image.shape[1], rgb_image.shape[0], QtGui.QImage.Format_BGR888)
                p = convertToQtFormat.scaled(self.scaled_size, QtCore.Qt.KeepAspectRatio)
                self.change_pixmap.emit(p)

    def scaled(self, scaled_size):
        self.scaled_size = scaled_size


class PlayStreaming(QtWidgets.QLabel):
    resize = QtCore.pyqtSignal(QtCore.QSize)
    def __init__(self):
        super(PlayStreaming, self).__init__()
        self.initUI()

    @QtCore.pyqtSlot(QtGui.QImage)
    def setImage(self, image):
        self.label.setPixmap(QtGui.QPixmap.fromImage(image))

    def setCVImage(self, cvimg):
        rgbImage = cv2.cvtColor(cvimg, cv2.COLOR_BGR2RGB)
        qimg = QtGui.QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QtGui.QImage.Format_RGB888)
        

    def initUI(self):
        self.setWindowTitle("Image")
        # create a label
        self.label = QtWidgets.QLabel(self)
        self.th = Thread(self)
        self.th.change_pixmap.connect(self.setImage)
        self.resize.connect(self.th.scaled)
        lay = QtWidgets.QVBoxLayout(self)
        lay.addWidget(self.label, alignment=QtCore.Qt.AlignCenter)

    def resizeEvent(self, event):
        self.resize.emit(self.size())


class RealWidget(QtWidgets.QWidget):
    def __init__(self):
        super(RealWidget, self).__init__()
        self.setWindowTitle('Visual Assistant')
        self.settings = Settings(lambda: self.stacked_widget.setCurrentWidget(real_w))

        # Initialize tab screen
        self.tabs = QtWidgets.QTabWidget()
        self.tab1 = QtWidgets.QWidget()
        self.tab2 = QtWidgets.QWidget()

        # Add tabs
        self.tabs.addTab(self.tab1, "Live Stream")
        self.tabs.addTab(self.tab2, "Settings")

        # Create first tab
        self.createGridLayout()
        self.tab1.layout = QtWidgets.QVBoxLayout()
        self.display = PlayStreaming()
        self.tab1.layout.addWidget(self.display, stretch=1)
        # self.tab1.layout.addWidget(self.horizontalGroupBox)
        self.tab1.setLayout(self.tab1.layout)
        self.tab2.layout = QtWidgets.QVBoxLayout()
        self.tab2.layout.addWidget(self.settings, stretch=1)
        self.tab2.setLayout(self.tab2.layout)

        # Add tabs to widget
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.tabs)

    def createGridLayout(self):
        layout = QtWidgets.QGridLayout()
        
    def show(self):
        self.display.th.start()
        super().show(self)

    def hide(self):
        self.display.th.quit()
        