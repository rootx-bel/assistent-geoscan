from PyQt5.QtWidgets import QHBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import Qt

class Overlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.button1 = QPushButton(self)
        self.button1.resize(100, 500)
        self.button1.setText("MENU")
        self.button1.clicked.connect(lambda: print("menu click"))

        self.button2 = QPushButton(self)
        self.button2.resize(500, 100)
        self.button2.setText("SETTINGS")
        self.button2.clicked.connect(lambda: print("setting click"))

        self.layout.addWidget(self.button1, alignment=Qt.AlignLeft | Qt.AlignTop)
        self.layout.addWidget(self.button2, alignment=Qt.AlignRight | Qt.AlignTop)