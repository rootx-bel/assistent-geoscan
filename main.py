from PyQt5.QtWidgets import *
import sys
from PyQt5.QtGui import *
from PyQt5 import *
from PyQt5.QtCore import QCoreApplication
from ui.live import LiveWidget
from ui.settings import SettingsWidget
from ui.home import HomeWidget
from ui.overlay import Overlay

class MainWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUI()

    def setupUI(self):
        self.layout = QVBoxLayout(self)
        self.setContentsMargins(0, 0, 0, 0)

        self.stacked_widget = QStackedWidget(self)
        self.stacked_widget.setContentsMargins(0, 0, 0, 0)
        self.home_widget = HomeWidget(self)
        self.settings_widget = SettingsWidget(self.return_home)
        self.real_widget = LiveWidget(self)
        self.overlay = Overlay(self)
        self.overlay.hide()

        self.stacked_widget.addWidget(self.home_widget)
        self.stacked_widget.addWidget(self.real_widget)
        self.stacked_widget.addWidget(self.settings_widget)

        self.stacked_widget.setCurrentWidget(self.home_widget)

        self.stacked_widget.stackUnder(self.overlay)

        self.home_widget.vmenu.buttons.buttons_signal.menu_click.connect(self.buttons_click)
        self.overlay.top_lay.home_button.clicked.connect(self.buttons_click)
        self.overlay.top_lay.setting_button.clicked.connect(self.buttons_click)
        self.overlay.bottom_lay.brightness_widget.slider.valueChanged.connect(self.update_settings)

        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.stacked_widget)

    def update_settings(self, value):
        name = self.sender().objectName()
        self.settings_widget.result[name] = value

    def return_home(self):
        self.stacked_widget.setCurrentWidget(self.home_widget)
        self.overlay.hide()

    def buttons_click(self, value):
        if value == "load":
            pass
        elif value == "live":
            self.overlay.show()
            self.stacked_widget.setCurrentWidget(self.real_widget)
            self.real_widget.display.th.start()
        elif value == "settings":
            self.overlay.hide()
            self.stacked_widget.setCurrentWidget(self.settings_widget)
        elif value == "exit":
            QCoreApplication.instance().quit()
        elif value == "home":
            self.stacked_widget.setCurrentWidget(self.home_widget)
            self.overlay.hide()

    def resizeEvent(self, event):
        self.overlay.resizeEvent(event)
        return super().resizeEvent(event)

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('main')
        self.setupUi()

    def setupUi(self):
        self.setContentsMargins(0, 0, 0, 0)
        self.setWindowTitle("MainInterface")

        self.mainWidget = MainWidget()
        self.setCentralWidget(self.mainWidget)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    with open("ui/styles/style.css", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)

    win = MainWindow()
    win.resize(1920, 1080)
    win.setMinimumSize(1920, 1080)
    win.show()
    sys.exit(app.exec_())