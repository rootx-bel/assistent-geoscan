from PyQt5 import QtCore, QtGui, QtDesigner
from myui import *

def dump_ui(widget, path):
    builder = QtDesigner.QFormBuilder()
    stream = QtCore.QFile(path)
    stream.open(QtCore.QIODevice.WriteOnly)
    builder.save(stream, widget)
    stream.close()

app = QtGui.QApplication([''])

dialog = QtGui.QDialog()
Ui_Dialog().setupUi(dialog)

dialog.show()

dump_ui(dialog, 'myui.ui')