from PyQt5.QtWidgets import *
import sys
import os
from PyQt5.QtGui import *
from PyQt5 import *
from cv2 import resize
from ui.video import RealWidget
from ui.settings import Settings
from ui.start import StartWidget
from PyQt5.QtCore import Qt



class MainWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUI()

    def setupUI(self):
        self.layout = QVBoxLayout(self)
        self.setContentsMargins(0, 0, 0, 0)

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setContentsMargins(0, 0, 0, 0)
        self.start_buttons = StartWidget()
        self.setts = Settings(self.set_menu)
        self.real_w = RealWidget()
        
        self.stacked_widget.addWidget(self.start_buttons)
        self.stacked_widget.addWidget(self.real_w)
        self.stacked_widget.addWidget(self.setts)
        
        
        self.stacked_widget.setCurrentWidget(self.start_buttons)
        
        self.layout.addWidget(self.stacked_widget)
        self.start_buttons.liveButton.clicked.connect(self.set_live)
        self.start_buttons.loadButton.clicked.connect(self.set_menu)
        self.start_buttons.settingsButton.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.setts))

        self.geo_label = QLabel()
        self.geo_label.setPixmap(QPixmap("ui/images/logo.png"))
        self.layout.addWidget(self.geo_label, alignment = Qt.AlignCenter | Qt.AlignRight )

        self.layout.addStretch()

        self.logosLabel = QLabel()
        self.logosLabel.setPixmap(QPixmap("ui/images/logos.png"))
        self.layout.addWidget(self.logosLabel, alignment= Qt.AlignRight | Qt.AlignBottom)


        
        
    def set_live(self):
        self.stacked_widget.setCurrentWidget(self.real_w)
        self.real_w.display.th.start()
        
    def set_menu(self):
        self.stacked_widget.setCurrentWidget(self.start_buttons)


        

# class MainWidget(QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setupUI()

#     def setupUI(self):
#         self.layout = QVBoxLayout(self)

#         self.stacked_widget = QStackedWidget()
#         self.start_buttons = StartWidget()
#         self.setts = Settings(self.set_menu)
#         self.real_w = RealWidget()
        
#         self.stacked_widget.addWidget(self.start_buttons)
#         self.stacked_widget.addWidget(self.real_w)
#         self.stacked_widget.addWidget(self.setts)
        
        
#         self.stacked_widget.setCurrentWidget(self.start_buttons)
        
#         self.layout.addWidget(self.stacked_widget)
#         self.start_buttons.liveButton.clicked.connect(self.set_live)
#         self.start_buttons.loadButton.clicked.connect(self.set_menu)
#         self.start_buttons.settingsButton.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.setts))

#         self.logosLabel = QLabel(self)
#         self.logosLabel.setPixmap(QPixmap("ui/images/logo.png"))
#         self.layout.addWidget(self.logosLabel)
        
#     def set_live(self):
#         self.stacked_widget.setCurrentWidget(self.real_w)
#         self.real_w.display.th.start()
        
#     def set_menu(self):
#         self.stacked_widget.setCurrentWidget(self.start_buttons)



class MainWindow(QMainWindow): 
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("MainInterface") 
       
        self.setStyleSheet(
            """
            MainWindow{
                border-image: url("ui/images/log.png") 0 0 0 0 stretch stretch
            }
            """
        )

        self.mainWidget = MainWidget()
        self.setCentralWidget(self.mainWidget)

            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())