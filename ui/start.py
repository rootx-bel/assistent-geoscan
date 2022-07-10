from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys


class StartWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.liveButton = QPushButton("Live flight")
        self.loadButton = QPushButton("Load videos")
        self.settingsButton = QPushButton("Settings")
        self.exitButton = QPushButton("Exit")
       
        self.exitButton.clicked.connect(self.exitButtonClicked)
        vbox = QVBoxLayout()
        vbox.addStretch()
        vbox.addWidget(self.liveButton)
        vbox.addWidget(self.loadButton)
        vbox.addWidget(self.settingsButton)
        vbox.addWidget(self.exitButton)
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
    
    start_buttons = StartWidget()

    win.setCentralWidget(start_buttons)
    win.show()

    sys.exit(app.exec_())