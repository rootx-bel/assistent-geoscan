from PyQt5.QtWidgets import *
import sys
from PyQt5.QtGui import *
from PyQt5 import *


class MainWindow(QMainWindow): 
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()
    def setupUi(self):
        self.setWindowTitle("MainInterface") 

        stacked_widget =  QStackedWidget()

        layout =  QVBoxLayout()
        layout.addWidget(stacked_widget)
        self.setLayout(layout)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    
    win.show()
    sys.exit(app.exec_())