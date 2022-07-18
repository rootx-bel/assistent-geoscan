from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel,  QSlider
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QMouseEvent

class TopBarButton(QLabel):
    clicked = pyqtSignal(str)

    def __init__(self, pixmap, parent=None):
        super().__init__(parent)
        self.setPixmap(pixmap)

    def mousePressEvent(self, event):
        self.clicked.emit(self.objectName())
        return super().mousePressEvent(event)


class BottomBarButton(QLabel):
    clicked = pyqtSignal(bool)

    def __init__(self, pixmap_on, pixmap_off, parent=None):
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
    def __init__(self, name, pix1, pix2, parent=None):
        super().__init__(parent)
        self.left_lay = QHBoxLayout(self)
        self.setContentsMargins(0, 0, 0, 0)

        self.number = QLabel(self)
        self.number.setStyleSheet("""
            color: white; 
            font-size: 18pt;
            background: rgba(45, 45, 45, 200);
            border-radius: 8px;
        """)

        self.pic_button = BottomBarButton(pix1, pix2)
        self.sv = 50
        self.slider = QSlider(Qt.Horizontal, self)

        self.slider.setTickInterval(1)
        self.slider.setRange(0,100)
        self.slider.setFocusPolicy(Qt.StrongFocus)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.setSingleStep(1)
        self.slider.valueChanged.connect(self.getValue)
        self.slider.setValue(self.sv)
        self.slider.setObjectName(name)

        self.pic_button.clicked.connect(self.click_handle)
        self.slider.setStyleSheet("background-color :rgba(211, 211, 211, 0)")

        self.left_lay.addWidget(self.pic_button)
        self.left_lay.addWidget(self.slider)
        self.left_lay.addWidget(self.number, alignment=Qt.AlignRight)

    def getValue(self,x):
        y = str(x)+"%"
        self.number.setText(y)
        

    def click_handle(self, state):
        self.slider.setEnabled(state)
        if not state:
            self.sv = self.slider.value()
            self.slider.setValue(0)
        else:
            self.slider.setValue(self.sv)


class HorizontalBottomLay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color :rgba(0, 0, 0, 0)")
        self.bot_layout = QHBoxLayout(self)
        self.setContentsMargins(0, 0, 0, 0)
        self.volume_widget = BottomSlider("volume", QPixmap(
            "ui/images/overlay/volume.png"), QPixmap("ui/images/overlay/mute.png"))
        self.brightness_widget = BottomSlider("brightness", QPixmap(
            "ui/images/overlay/brightness.png"), QPixmap("ui/images/overlay/brightness_off.png"))
        self.bot_layout.addStretch(1)
        self.bot_layout.addWidget(
            self.volume_widget, alignment=Qt.AlignVCenter, stretch=1)
        self.bot_layout.addStretch(1)
        self.bot_layout.addWidget(
            self.brightness_widget, alignment=Qt.AlignVCenter, stretch=1)
        self.bot_layout.addStretch(1)
        self.setLayout(self.bot_layout)


class HorizontalTopLay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color :rgba(0, 0, 0, 0)")
        self.top_layout = QHBoxLayout(self)
        self.setContentsMargins(0, 0, 0, 0)
        self.home_button = TopBarButton(QPixmap("ui/images/overlay/home.png"))
        self.home_button.setObjectName("home")
        self.setting_button = TopBarButton(
            QPixmap("ui/images/overlay/gear.png"))
        self.setting_button.setObjectName("settings")
        self.top_layout.addWidget(
            self.home_button, alignment=Qt.AlignTop | Qt.AlignLeft)
        self.top_layout.addWidget(
            self.setting_button, alignment=Qt. AlignTop | Qt.AlignRight)
        self.setLayout(self.top_layout)

    def change_home_button(self, name):
        self.home_button.setObjectName(name)
        if name == 'home':
            self.home_button.setPixmap(QPixmap("ui/images/overlay/home.png"))
        elif name == 'back':
            self.home_button.setPixmap(QPixmap("ui/images/overlay/back.png"))


class Overlay():
    def __init__(self, parent=None):
        self.__parent = parent
        self.top_lay = HorizontalTopLay(parent)
        self.bottom_lay = HorizontalBottomLay(parent)

    def set_under(self, widget):
        widget.stackUnder(self.bottom_lay)
        widget.stackUnder(self.top_lay)

    def hide(self):
        self.top_lay.hide()
        self.bottom_lay.hide()

    def show(self):
        self.set_visible_settings(True)
        self.top_lay.show()
        self.bottom_lay.show()

    def set_visible_settings(self, visible=True):
        if visible:
            self.top_lay.setting_button.show()
        else:
            self.top_lay.setting_button.hide()

    def resizeEvent(self, event):
        self.top_lay.setGeometry(
            0, 0, self.__parent.frameGeometry().width(), 100)
        self.bottom_lay.setGeometry(0, self.__parent.height(
        ) - 100, self.__parent.frameGeometry().width(), 100)


 