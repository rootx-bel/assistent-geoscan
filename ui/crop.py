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
        orig_pixmap = QPixmap.fromImage(self.__convert2qt(orig))
        mask_pixmap = QPixmap.fromImage(self.__convert2qt(mask))
        if not orig_pixmap.isNull() and not mask_pixmap.isNull():
            self.orig_crop.setPixmap(orig_pixmap)
            self.mask_crop.setPixmap(mask_pixmap)

    def resizeEvent(self, event):
        if self.orig_crop.pixmap() is not None:
            self.orig_crop.setPixmap(
                self.orig_crop.pixmap().scaled(
                    self.orig_crop.width(),
                    2147483647
                )
            )
        if self.mask_crop.pixmap() is not None:
            self.mask_crop.setPixmap(
                self.mask_crop.pixmap().scaled(
                    self.mask_crop.width(),
                    2147483647
                )
            )
        return super().resizeEvent(event)

class CropWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Crop frame')
        self.setContentsMargins(0, 0, 0, 0)
        self.scroll = QScrollArea(self)
        self.scroll.setStyleSheet("""border-image: url("ui/images/home/background.png") 0 0 0 0;""")
        self.area_widget = QWidget(self)
        self.area_layout = QVBoxLayout(self)

        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.area_widget)

        self.area_widget.setLayout(self.area_layout)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.scroll)
        self.setLayout(self.layout)

    def add_crop(self, orig, mask):
        crop_item = CropItemWidget(orig, mask)
        self.area_layout.addWidget(crop_item)

    def resizeEvent(self, event):
        self.scroll.setGeometry(0, 0, self.frameGeometry().width(), self.frameGeometry().height())
        return super().resizeEvent(event)