from PyQt5.QtWidgets import QWidget, QLabel, QScrollArea, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap

class CropItemWidget(QWidget):
    def __init__(self, orig, mask, parent=None):
        super().__init__(parent)
        self.initUI()
        self.set_images(orig, mask)

    def initUI(self):
        self.layout = QHBoxLayout(self)
        self.orig_crop = QLabel(self)
        self.mask_crop = QLabel(self)
        self.layout.addWidget(self.orig_crop)
        self.layout.addWidget(self.mask_crop)

    def __convert2qt(self, img):
        return QImage(img.data, img.shape[1], img.shape[0], QImage.Format_BGR888)

    def set_images(self, orig, mask):
        self.orig_crop.setPixmap(QPixmap.fromImage(self.__convert2qt(orig)))
        self.mask_crop.setPixmap(QPixmap.fromImage(self.__convert2qt(mask)))

    def resizeEvent(self, event):
        self.orig_crop.setPixmap(
            self.orig_crop.pixmap().scaled(
                self.orig_crop.width(),
                2147483647,
                Qt.KeepAspectRatio
            )
        )
        self.mask_crop.setPixmap(
            self.mask_crop.pixmap().scaled(
                self.mask_crop.width(),
                2147483647,
                Qt.KeepAspectRatio
            )
        )
        return super().resizeEvent(event)

class CropWidget(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
    
    def initUI(self):
        self.back = QLabel(self)
        self.back.setObjectName('crop_widget')
        self.area_widget = QWidget(self)
        self.area_layout = QVBoxLayout(self)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)
        self.setWidget(self.area_widget)

        self.area_widget.setLayout(self.area_layout)

    def add_crop(self, orig, mask):
        crop_item = CropItemWidget(orig, mask)
        self.area_layout.addWidget(crop_item)

    def resizeEvent(self, event):
        self.back.resize(self.size())
        return super().resizeEvent(event)