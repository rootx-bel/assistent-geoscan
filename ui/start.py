from PyQt5.QtWidgets import QWidget, QCheckBox, QLabel, QPushButton, QComboBox, QSlider, QApplication, QMainWindow, QDesktopWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import *
import sys


class StartWidget(QWidget):

    def __init__(self):
        super().__init__()
        liveButton = QPushButton("Live flight")
        loadButton = QPushButton("Load videos")
        settingsButton = QPushButton("Settings")
        exitButton = QPushButton("Exit")
       
        exitButton.clicked.connect(self.exitButtonClicked) 

        vbox = QVBoxLayout()
        vbox.addStretch()
        vbox.addWidget(liveButton)
        vbox.addWidget(loadButton)
        vbox.addWidget(settingsButton)
        vbox.addWidget(exitButton)
        vbox.addLayout(vbox)
        vbox.addStretch()
        self.setLayout(vbox)
        vbox.setAlignment(Qt.AlignCenter)
        self.setWindowTitle('Buttons')
        
    def exitButtonClicked(self):
        #save settings here
        self.QCoreApplication.instance().quit       

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = QMainWindow()
    
    start = StartWidget()

    win.setCentralWidget(start)
    win.show()

    sys.exit(app.exec_())