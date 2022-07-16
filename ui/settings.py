from ctypes import alignment
from PyQt5.QtWidgets import QWidget, QCheckBox, QLabel, QDesktopWidget, QVBoxLayout, QPushButton, QComboBox, QSlider, QApplication, QMainWindow, QHBoxLayout
from PyQt5.QtGui import QPixmap, QResizeEvent
from PyQt5.QtCore import Qt
import sys


class Settings(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.result = {}

        self.label = QLabel(self)
        self.label.setObjectName("setts")

        self.layout = QHBoxLayout(self)
        self.setLayout(self.layout)

        # self.layout.addWidget()

    def resizeEvent(self, a0: QResizeEvent) -> None:
        self.label.resize(self.size())
        return super().resizeEvent(a0)


class SettingsWidget(QWidget):
    def __init__(self, exit_func=None):
        super().__init__()
        self.result = {}

        self.label = QLabel(self)
        self.label.setObjectName("settings-widget")

        self.layout = QVBoxLayout(self)
        self.hbox = QHBoxLayout(self)

        self.line = QLabel()
        self.line.setPixmap(QPixmap("ui/images/line.png"))
        self.hbox.addWidget(self.line, 1, alignment=Qt.AlignCenter)

        self.setts = Settings(self)
        self.hbox.addWidget(self.setts, 3)

        self.line2 = QLabel()
        self.line2.setPixmap(QPixmap("ui/images/line.png"))
        self.hbox.addWidget(self.line2, 1, alignment=Qt.AlignCenter)

        self.layout.addStretch(1)
        self.layout.addLayout(self.hbox)
        self.layout.addStretch(1)

        # self.hbox.setStretch(1, 3)
        self.setLayout(self.layout)

    def resizeEvent(self, a0: QResizeEvent) -> None:
        self.label.resize(self.size())
        return super().resizeEvent(a0)

    def get_result(self):
        return self.result


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = QMainWindow()

    with open("ui/styles/style.css", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)

    start = SettingsWidget()

    win.setCentralWidget(start)
    win.resize(1920, 1080)
    win.setMinimumSize(1920, 1080)
    win.show()

    sys.exit(app.exec_())
