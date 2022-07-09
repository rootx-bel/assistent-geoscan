from PyQt5.QtWidgets import *
import sys
from PyQt5.QtGui import *
from PyQt5 import *
from ui.video import RealWidget


class MainWindow(QMainWindow): 
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()
    def setupUi(self):
        self.setWindowTitle("MainInterface") 
        

        stacked_widget =  QStackedWidget()
        real_w = RealWidget()
        stacked_widget.addWidget(real_w)
        stacked_widget.setCurrentWidget(real_w)

        self.setCentralWidget(stacked_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    
    win.show()
    sys.exit(app.exec_())