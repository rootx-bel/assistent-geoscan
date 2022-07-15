from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QEvent, pyqtSignal, QObject

class ButtonCommunicate(QObject):
    menu_click = pyqtSignal(str)

class Buttons(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.buttons_signal = ButtonCommunicate()

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 80, 0, 0)

        self.load = QLabel()
        self.load.setObjectName("load")
        self.load.setPixmap(QPixmap("ui/images/load.png"))

        self.live = QLabel()
        self.live.setObjectName("live")
        self.live.setPixmap(QPixmap("ui/images/live.png"))

        self.settings = QLabel()
        self.settings.setObjectName("settings")
        self.settings.setPixmap(QPixmap("ui/images/settings.png"))

        self.exit = QLabel()
        self.exit.setObjectName("exit")
        self.exit.setPixmap(QPixmap("ui/images/exit.png"))

        self.layout.addWidget(self.load, alignment=Qt.AlignBottom)
        self.layout.addWidget(self.live, alignment=Qt.AlignBottom)
        self.layout.addWidget(self.settings, alignment=Qt.AlignBottom)
        self.layout.addWidget(self.exit, alignment=Qt.AlignBottom)
        self.load.installEventFilter(self)
        self.live.installEventFilter(self)
        self.settings.installEventFilter(self)
        self.exit.installEventFilter(self)
        self.setLayout(self.layout)

    def eventFilter(self, object, event):
        # print(object.objectName())
        if event.type() == QEvent.Enter:
            object.setPixmap(
                QPixmap(f"ui/images/{object.objectName()}-hover.png"))
            self.stop = True
            return True
        elif event.type() == QEvent.Leave:
            object.setPixmap(
                QPixmap(f"ui/images/{object.objectName()}.png"))
            self.stop = False
        elif event.type() == QEvent.MouseButtonPress:
            self.buttons_signal.menu_click.emit(object.objectName())
        return False


class ButtonsMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.dots = QLabel()
        self.dots.setObjectName("dots")
        self.dots.setPixmap(QPixmap("ui/images/alldots.png"))
        self.layout.addWidget(self.dots, alignment=Qt.AlignVCenter)

        self.buttons = Buttons(self)
        self.layout.addWidget(self.buttons, alignment=Qt.AlignVCenter)

        self.setLayout(self.layout)


class HomeWidget(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName('home-widget')

        self.layout = QHBoxLayout()
        self.layout.addStretch(1)
        self.vmenu = ButtonsMenu(self)
        self.layout.addWidget(self.vmenu)
        self.logo = QLabel(self)
        self.logo.setPixmap(QPixmap("ui/images/logo.png"))

        self.layout.addStretch(10)
        self.layout.addWidget(self.logo, alignment=Qt.AlignVCenter)

        self.partners = QLabel(self)
        self.partners.setPixmap(QPixmap("ui/images/partners.png"))
        self.layout.addWidget(self.partners,
                              alignment=Qt.AlignBottom | Qt.AlignRight, stretch=1)

        self.setLayout(self.layout)