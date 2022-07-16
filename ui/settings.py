from PyQt5.QtWidgets import QWidget, QCheckBox, QLabel, QDesktopWidget, QPushButton, QComboBox, QSlider, QApplication, QMainWindow
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sys


class Settings(QWidget):
    def __init__(self, exit_func):
        self.result = {}
        self.__exit_func = exit_func

        super().__init__()

        self.setWindowTitle("Прозрачность маски")  # заголовок окна
        self.resize(200, 200)  # размер окна
        self.lbl = QLabel('Прозрачность маски', self)
        self.lbl.move(555, 55)

        self.setWindowTitle("Цвет маски")  # заголовок окна
        self.resize(200, 200)  # размер окна
        self.lbl = QLabel('Цвет маски', self)
        self.lbl.move(555, 107)

        # cb = QCheckBox('Телеметрия', self)
        self.cb2 = QCheckBox('Звуковое оповещение', self)
        # cb.stateChanged.connect(self.changeTitle)
        self.cb4 = QCheckBox('Визуальное оповещение', self, )
        self.cb4.resize(500, 25)
        self.cb2.resize(500, 25)
        # cb.resize(500,25)

        # cb.move(100,150)
        self.cb2.move(100, 100)
        self.cb4.move(100, 50)

        self.setWindowTitle('Form with Single Checkbox')
        self.setFixedSize(800, 500)

        win = self.frameGeometry()

        pos = QDesktopWidget().availableGeometry().center()

        win.moveCenter(pos)

        self.move(win.topLeft())
        pixmap = QPixmap('ui/images/error--v1.png').scaled(30, 30)
        label = QLabel(self)
        label.setPixmap(pixmap)
        label.move(250, 45)
        label.resize(pixmap.width(), pixmap.height())

        pixmap = QPixmap('ui/images/summer.png').scaled(35, 35)
        label2 = QLabel(self)
        label2.setPixmap(pixmap)
        label2.move(520, 45)
        label2.resize(pixmap.width(), pixmap.height())

        pixmap = QPixmap('ui/images/high-volume--v1 (1).png').scaled(30, 30)
        label3 = QLabel(self)
        label3.setPixmap(pixmap)
        label3.move(253, 100)
        label3.resize(pixmap.width(), pixmap.height())

        pixmap = QPixmap('ui/images/wet.png').scaled(30, 30)
        label = QLabel(self)
        label.setPixmap(pixmap)
        label.move(522, 100)
        label.resize(pixmap.width(), pixmap.height())

        self.button_ok = QPushButton("Применить", self)
        self.button_ok.clicked.connect(self.ok_click)
        self.button_ok.move(680, 460)

        self.button_cancel = QPushButton("Отмена", self)
        self.button_cancel.clicked.connect(self.__exit_func)
        self.button_cancel.move(575, 460)

        self.combobox = QComboBox(self)
        self.combobox.addItem('Красный')
        self.combobox.addItem('Желтый')
        self.combobox.addItem('Синий')
        self.combobox.addItem('Белый')
        self.combobox.addItem('Оранжевый')
        self.combobox.addItem('Зеленый')
        self.combobox.move(650, 100)

        self.my_slider = QSlider(Qt.Horizontal, self)
        self.my_slider.setValue(50)
        self.my_slider.setMaximum(100)
        self.my_slider.setMinimum(0)
        self.my_slider.setGeometry(15, 20, 100, 15)
        self.my_slider.move(650, 55)

        self.setGeometry(50, 50, 320, 200)
        self.setWindowTitle("Checkbox Example")
        self.show()

    def ok_click(self):
        self.result['vision'] = self.cb4.isChecked()
        self.result['sound'] = self.cb2.isChecked()
        self.result['color'] = self.combobox.currentText()
        self.result['light'] = self.my_slider.value()
        # print(self.result)
        self.__exit_func()

    def get_result(self):
        return self.result


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = QMainWindow()

    start = Settings()

    win.setCentralWidget(start)
    win.show()

    sys.exit(app.exec_())
