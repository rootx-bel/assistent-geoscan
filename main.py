from PyQt5.QtWidgets import *
import sys
from PyQt5.QtGui import *
from PyQt5 import *
from ui.video import RealWidget
from ui.settings import Settings
from ui.home import HomeWidget

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
        self.settings_widget = Settings(self.set_menu)
        self.real_w = RealWidget()
        
        self.stacked_widget.addWidget(self.home_widget)
        self.stacked_widget.addWidget(self.real_w)
        self.stacked_widget.addWidget(self.settings_widget)
        
        self.stacked_widget.setCurrentWidget(self.home_widget)
        
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.stacked_widget)

    def exit_click(self):
        sender = self.sender()
        print(sender.text)
        # self.QCoreApplication.instance().quit
        
    def set_live(self):
        self.stacked_widget.setCurrentWidget(self.real_w)
        self.real_w.display.th.start()
        
    def set_menu(self):
        self.stacked_widget.setCurrentWidget(self.home_widget)

class MainWindow(QMainWindow): 
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()

    def setupUi(self):
        self.setContentsMargins(0, 0, 0, 0)
        self.setWindowTitle("MainInterface")

        self.mainWidget = MainWidget()
        self.setCentralWidget(self.mainWidget)

            
if __name__ == "__main__":
    app = QApplication(sys.argv)

    with open("ui/style.css", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)

    win = MainWindow()
    win.resize(1920, 1080)
    win.show()
    sys.exit(app.exec_())