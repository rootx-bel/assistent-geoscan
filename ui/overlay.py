import sys
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, 
QHBoxLayout, QAbstractButton, QLabel,  QSlider)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QPixmap, QMouseEvent
# from ui.settings import Settings

class TopBarButton(QLabel):
    clicked = pyqtSignal(str)

    def __init__(self, pixmap, parent = None):
        super().__init__(parent)
        self.setPixmap(pixmap)

    def mousePressEvent(self, event):
        self.clicked.emit(self.objectName())
        return super().mousePressEvent(event)

class BottomBarButton(QLabel):
    clicked = pyqtSignal(bool)

    def __init__(self, pixmap_on, pixmap_off, parent = None):
        super().__init__(parent)
        self.pixmap_on = pixmap_on
        self.pixmap_off = pixmap_off
        self.pixmap = self.pixmap_on
        self.setPixmap(self.pixmap)
        self.is_on = True

    def mousePressEvent(self, ev: QMouseEvent) -> None:
        self.pixmap = self.pixmap_off if self.is_on else self.pixmap_on
        self.is_on = not self.is_on
        self.setPixmap(self.pixmap)
        self.clicked.emit(self.is_on)
        return super().mousePressEvent(ev)

class BottomSlider(QWidget):
    # valueChanged = pyqtSignal(str, int)

    def __init__(self, name, pix1, pix2, parent = None):
        super().__init__(parent)
        self.left_lay = QHBoxLayout(self)
        self.setContentsMargins(0, 0, 0, 0)

        self.pic_button = BottomBarButton(pix1, pix2)
        self.sv = 30
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(self.sv)
        self.slider.setObjectName(name)
        # self.slider.valueChanged.connect(lambda: self.valueChanged.emit(self.objectName(), self.slider.value()))

        self.pic_button.clicked.connect(self.click_handle)
        self.slider.setStyleSheet("background-color :rgba(211, 211, 211, 0)")

        self.left_lay.addWidget(self.pic_button)
        self.left_lay.addWidget(self.slider)

    def click_handle(self, state):
        self.slider.setEnabled(state)
        if not state:
            self.sv = self.slider.value()
            self.slider.setValue(0)
        else:
            self.slider.setValue(self.sv)

class HorizontalBottomLay(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.bot_layout = QHBoxLayout(self)
        self.setContentsMargins(0, 0, 0, 0)
        self.volume_widget = BottomSlider("volume", QPixmap("ui/images/icons/volume.png"), QPixmap("ui/images/icons/mute.png"))
        self.brightness_widget = BottomSlider("brightness", QPixmap("ui/images/icons/brightness.png"), QPixmap("ui/images/icons/brightness_off.png"))
        self.bot_layout.addStretch(1)
        self.bot_layout.addWidget(self.volume_widget, alignment = Qt.AlignVCenter, stretch=1)
        self.bot_layout.addStretch(1)
        self.bot_layout.addWidget(self.brightness_widget, alignment = Qt.AlignVCenter, stretch=1)
        self.bot_layout.addStretch(1)
        self.setLayout(self.bot_layout)

class HorizontalTopLay(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.top_layout = QHBoxLayout(self)
        self.setContentsMargins(0, 0, 0, 0)
        self.home_button = TopBarButton(QPixmap("ui/images/icons/home.png"))
        self.home_button.setObjectName("home")
        self.setting_button = TopBarButton(QPixmap("ui/images/icons/gear.png"))
        self.setting_button.setObjectName("settings")
        self.top_layout.addWidget(self.home_button, alignment = Qt.AlignVCenter | Qt.AlignLeft)
        self.top_layout.addWidget(self.setting_button, alignment = Qt. AlignVCenter | Qt.AlignRight)
        self.setLayout(self.top_layout)

class Overlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('New_Main')
        self.setStyleSheet("background-color: rgba(0, 0, 0, 0)")
        self.layout = QVBoxLayout()
        self.top_lay = HorizontalTopLay()
        self.layout.addWidget(self.top_lay, alignment = Qt.AlignTop)
        self.bottom_lay = HorizontalBottomLay()
        self.layout.addWidget(self.bottom_lay, alignment=Qt.AlignBottom)
        self.setLayout(self.layout)

    def resizeEvent(self, event):
        self.setGeometry(self.parent().frameGeometry())
        self.top_lay.setGeometry(0, 0, self.parent().frameGeometry().width(), self.top_lay.frameGeometry().height())
        self.bottom_lay.setGeometry(0, self.bottom_lay.y(), self.parent().frameGeometry().width(), self.bottom_lay.frameGeometry().height())