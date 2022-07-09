# Main file
from ui.video import RealWidget

from PyQt5 import QtWidgets

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = RealWidget()
    w.resize(1000, 800)
    w.showMaximized()
    sys.exit(app.exec_())