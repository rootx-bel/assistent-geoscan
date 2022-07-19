from PyQt5.QtWidgets import *
import sys, json, os
from PyQt5.QtGui import *
from PyQt5 import *
from ui.live import LiveWidget
from ui.settings import SettingsWidget
from ui.home import HomeWidget
from ui.overlay import Overlay
from ui.crop import CropWidget


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
        self.settings_widget = SettingsWidget()
        self.live_widget = LiveWidget(self)
        self.crop_widget = CropWidget()
        self.overlay = Overlay(self)
        self.overlay.hide()

        self.stacked_widget.addWidget(self.home_widget)
        self.stacked_widget.addWidget(self.live_widget)
        self.stacked_widget.addWidget(self.settings_widget)

        self.stacked_widget.setCurrentWidget(self.home_widget)

        self.overlay.set_under(self.stacked_widget)
        
        self.settings_widget.setts.messages_sound_button.clicked.connect(self.overlay.bottom_lay.volume_widget.pic_button.change_state)
        self.settings_widget.setts.messages_visual_button.clicked.connect(self.overlay.alarm.change_visible)
        self.settings_widget.changed.connect(self.accept_settings)

        self.home_widget.vmenu.buttons.menu_click.connect(self.buttons_click)
        self.overlay.top_lay.home_button.clicked.connect(self.buttons_click)
        self.overlay.top_lay.crop_button.clicked.connect(self.buttons_click)
        self.overlay.top_lay.setting_button.clicked.connect(self.buttons_click)
        self.overlay.bottom_lay.brightness_widget.slider.valueChanged.connect(self.__update_settings)
        self.overlay.bottom_lay.volume_widget.slider.valueChanged.connect(self.__update_settings)
        self.overlay.bottom_lay.volume_widget.pic_button.clicked.connect(lambda:
            self.settings_widget.setts.messages_sound_button.setChecked(
                not self.overlay.bottom_lay.volume_widget.pic_button.is_on
            )
        )

        self.live_widget.display.th.detected.connect(self.overlay.alarm.change_detect)
        self.live_widget.display.th.change_pixmap.connect(self.overlay.alarm.show)
        self.live_widget.display.th.croped.connect(self.crop_widget.add_crop)

        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.stacked_widget)

    def __update_settings(self, value):
        name = self.sender().objectName()
        self.settings_widget.change_result(name, value)

    def accept_settings(self, value):
        self.live_widget.set_settings(value)

    def buttons_click(self, value):
        if value == "load":
            pass
        elif value == "live" or value == "back":
            self.overlay.show()
            self.stacked_widget.setCurrentWidget(self.live_widget)
            self.overlay.top_lay.change_home_button('home')
            self.live_widget.set_video_thread(True)
        elif value == "settings":
            self.overlay.show()
            self.overlay.set_visible_settings(False)
            if self.stacked_widget.currentWidget() is self.live_widget:
                self.overlay.top_lay.change_home_button('back')
            self.stacked_widget.setCurrentWidget(self.settings_widget)
        elif value == "exit":
            self.parent().close()
        elif value == "home":
            if self.stacked_widget.currentWidget() is self.live_widget:
                self.live_widget.set_video_thread(False)
            self.stacked_widget.setCurrentWidget(self.home_widget)
            self.overlay.hide()
        elif value == "crop":
            if self.crop_widget.isHidden():
                self.crop_widget.show()
            else:
                self.crop_widget.hide()

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
        self.setWindowTitle("Assistent")

        self.main_widget = MainWidget()
        self.open("saves/settings.json")
        self.setCentralWidget(self.main_widget)

    def open(self, filename):
        result = {}
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                result = json.load(f)
                result['sound'] = not result['sound']
                result['visual'] = not result['visual']
        else:
            result["color"] = (255,0,0)
            result["sound"] = False
            result["visual"] = False
            result["volume"] = 50
            result["brightness"] = 50
        self.main_widget.settings_widget.result = result
        self.main_widget.settings_widget.setts.messages_sound_button.load(result["sound"])
        self.main_widget.settings_widget.setts.messages_visual_button.load(result["visual"])
        self.main_widget.overlay.alarm.load(result["visual"])
        self.main_widget.overlay.bottom_lay.volume_widget.load(result["volume"])
        self.main_widget.overlay.bottom_lay.brightness_widget.load(result["brightness"])
        self.main_widget.settings_widget.setts.color_picker.change_color(result["color"])


    def save(self, filename):
        result = self.main_widget.settings_widget.result
        result['sound'] = not result['sound']
        result['visual'] = not result['visual']
        with open(filename, 'w') as f:
            json.dump(result, f)

    def closeEvent(self, event):
        self.save("saves/settings.json")
        return super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    with open("ui/styles/style.css", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)

    win = MainWindow()
    win.resize(1440, 900)
    win.setMinimumSize(1440, 900)
    win.show()
    sys.exit(app.exec_())
