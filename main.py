from PyQt5.QtWidgets import *
import sys
from PyQt5.QtGui import *
from PyQt5 import *
from ui.video import RealWidget
from ui.settings import Settings
from ui.start import StartWidget


class MainWindow(QMainWindow): 
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()
    def setupUi(self):
        self.setWindowTitle("MainInterface") 
        

        self.stacked_widget =  QStackedWidget()
        self.start_buttons = StartWidget()
        self.setts = Settings()
        self.real_w = RealWidget()
        
        self.stacked_widget.addWidget(self.start_buttons)
        self.stacked_widget.addWidget(self.real_w)
        self.stacked_widget.addWidget(self.setts)
        
        
        self.stacked_widget.setCurrentWidget(self.start_buttons)
        # self.stacked_widget.setCurrentWidget(self.setts)

        self.setCentralWidget(self.stacked_widget)
        # if self.start_buttons.liveButton is clicked:
        #     self.stacked_widget.setCurrentWidget(self.real_w)
        self.start_buttons.liveButton.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.real_w))
        self.start_buttons.loadButton.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.start_buttons))
        self.start_buttons.settingsButton.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.setts))

            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    
    win.show()
    sys.exit(app.exec_())