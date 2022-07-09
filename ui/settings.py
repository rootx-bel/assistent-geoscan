from PyQt5.QtWidgets import QWidget, QCheckBox, QLabel, QDesktopWidget, QPushButton, QComboBox, QSlider
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class Settings(QWidget):
    def __init__(self):
        self.result = {}

        super().__init__()
        
        self.setWindowTitle("Яркость маски") # заголовок окна
        self.resize(200, 200) # размер окна
        self.lbl = QLabel('Яркость маски', self)
        self.lbl.move(555,45)

        self.setWindowTitle("Цвет маски") # заголовок окна
        self.resize(200, 200) # размер окна
        self.lbl = QLabel('Цвет маски', self)
        self.lbl.move(555,100)
        
         
        # cb = QCheckBox('Телеметрия', self)
        self.cb2 = QCheckBox('Звуковое оповещение', self)
        # cb.stateChanged.connect(self.changeTitle)
        self.cb4 = QCheckBox('Визуальное оповещение', self, )
        self.cb4.resize(500,25)
        self.cb2.resize(500,25)
        # cb.resize(500,25)

        # cb.move(100,150)
        self.cb2.move(100,100)
        self.cb4.move(100,50)


        self.setWindowTitle('Form with Single Checkbox')
        self.setFixedSize(800,500)



        win = self.frameGeometry()

        pos = QDesktopWidget().availableGeometry().center()

        win.moveCenter(pos)

        self.move(win.topLeft())
        pixmap = QPixmap('images/error--v1.png').scaled(30,30)
        label = QLabel(self)
        label.setPixmap(pixmap)
        label.move(250,45)
        label.resize(pixmap.width(), pixmap.height())

        pixmap = QPixmap('images/summer.png').scaled(35,35)
        label2 = QLabel(self)
        label2.setPixmap(pixmap)
        label2.move(520,45)
        label2.resize(pixmap.width(), pixmap.height())

        pixmap = QPixmap('images/high-volume--v1 (1).png').scaled(30,30)
        label3 = QLabel(self)
        label3.setPixmap(pixmap)
        label3.move(253,100)
        label3.resize(pixmap.width(), pixmap.height())

        pixmap = QPixmap('images/wet.png').scaled(30,30)
        label = QLabel(self)
        label.setPixmap(pixmap)
        label.move(522,100)
        label.resize(pixmap.width(), pixmap.height())

        self.button_ok = QPushButton("Применить", self)
        self.button_ok.clicked.connect(self.ok_click)
        self.button_ok.move(680,460) 

        self.button_cancel = QPushButton("Отмена", self)
        self.button_cancel.clicked.connect(self.cancel_click)
        self.button_cancel.move(575,460)

        self.combobox = QComboBox(self)
        self.combobox.addItem('Красный')
        self.combobox.addItem('Желтый')
        self.combobox.addItem('Синий')
        self.combobox.addItem('Белый')
        self.combobox.addItem('Оранжевый')
        self.combobox.addItem('Зеленый')
        self.combobox.move(650,100)

        self.my_slider = QSlider(Qt.Horizontal, self)
        self.my_slider.setGeometry(15, 20, 100, 15)
        self.my_slider.move(650,55)

        self.setGeometry(50,50,320,200)
        self.setWindowTitle("Checkbox Example")
        self.show()

   
    def ok_click(self):
        self.result['vision'] = self.cb4.isChecked()
        self.result['sound'] = self.cb2.isChecked()
        self.result['color'] = self.combobox.currentText()
        self.result['light'] = self.my_slider.value()
        print(self.result)

    def cancel_click(self):
        pass