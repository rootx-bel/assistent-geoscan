from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, pyqtSignal
from ui.colorpicker.picker import ColorPicker


class FourStateButton(QLabel):
    hovered = pyqtSignal(bool)
    clicked = pyqtSignal(bool)

    is_checked = False
    is_entered = False

    image = None
    image_hover = None
    image_checked = None
    image_checked_hover = None

    def __init__(self, parent  = None):
        super().__init__(parent)

    def setImage(self, image):
        self.image = image
        self.setPixmap(self.image)

    def setChecked(self, state):
        if state:
            if self.is_entered:
                self.pixmap = self.image_checked_hover
            else:
                self.pixmap = self.image_checked
        else:
            if self.is_entered:
                self.pixmap = self.image_hover
            else:
                self.pixmap = self.image
        self.setPixmap(self.pixmap)
        self.is_checked = state

    def enterEvent(self, event):
        self.is_entered = True
        self.hovered.emit(self.is_checked)
        self.setChecked(self.is_checked)
        return super().enterEvent(event)

    def leaveEvent(self, event):
        self.is_entered = False
        self.setChecked(self.is_checked)
        return super().leaveEvent(event)

    def mousePressEvent(self, event):
        self.setChecked(not self.is_checked)
        self.clicked.emit(self.is_checked)
        return super().mousePressEvent(event)

    def load(self, value):
        if value:
            self.clicked.emit(value)


class SettingsPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.label = QLabel(self)
        self.label.setObjectName("settings_panel")

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(60, 60, 60, 60)
        self.setLayout(self.layout)

        self.vbox = QVBoxLayout(self)
        self.messages_topic_image = QLabel(self)
        self.messages_topic_image.setPixmap(QPixmap("ui/images/settings/messages/topic.png"))
        self.vbox.addWidget(self.messages_topic_image, alignment=Qt.AlignLeft | Qt.AlignTop)

        self.msgs_hbox = QHBoxLayout(self)

        self.messages_topic_dots = QLabel(self)
        self.messages_topic_dots.setPixmap(QPixmap("ui/images/settings/messages/dots.png"))
        self.msgs_hbox.addStretch(1)
        self.msgs_hbox.addWidget(self.messages_topic_dots, alignment=Qt.AlignHCenter)

        self.msgs_hbox_vbox = QVBoxLayout()
        self.messages_visual_button = FourStateButton(self)
        self.messages_visual_button.setObjectName("visual")
        self.messages_visual_button.setImage(QPixmap("ui/images/settings/messages/visual/off.png"))
        self.messages_visual_button.image_hover = QPixmap("ui/images/settings/messages/visual/off-hover.png")
        self.messages_visual_button.image_checked = QPixmap("ui/images/settings/messages/visual/on.png")
        self.messages_visual_button.image_checked_hover = QPixmap("ui/images/settings/messages/visual/on-hover.png")
        self.msgs_hbox_vbox.addWidget(self.messages_visual_button, alignment=Qt.AlignTop)

        self.messages_sound_button = FourStateButton(self)
        self.messages_sound_button.setObjectName("sound")
        self.messages_sound_button.setImage(QPixmap("ui/images/settings/messages/sound/off.png"))
        self.messages_sound_button.image_hover = QPixmap("ui/images/settings/messages/sound/off-hover.png")
        self.messages_sound_button.image_checked = QPixmap("ui/images/settings/messages/sound/on.png")
        self.messages_sound_button.image_checked_hover = QPixmap("ui/images/settings/messages/sound/on-hover.png")
        self.msgs_hbox_vbox.addWidget(self.messages_sound_button, alignment=Qt.AlignTop)

        self.msgs_hbox_vbox.setContentsMargins(0, 70, 0, 0)

        self.msgs_hbox.addLayout(self.msgs_hbox_vbox)
        self.msgs_hbox.addStretch(1)
        self.vbox.addLayout(self.msgs_hbox)
        self.vbox.addStretch(5)

        self.layout.addLayout(self.vbox)

        self.layout.addStretch(1)
        self.line = QLabel()
        self.line.setPixmap(QPixmap("ui/images/line.png"))
        self.layout.addWidget(self.line)
        self.layout.addStretch(1)

        self.mask_vbox = QVBoxLayout(self)
        self.mask_topic_image = QLabel(self)
        self.mask_topic_image.setPixmap(QPixmap("ui/images/settings/mask/topic.png"))
        self.mask_vbox.addWidget(self.mask_topic_image, alignment=Qt.AlignRight | Qt.AlignTop)

        self.mask_vbox_hbox = QHBoxLayout(self)
        self.color_picker = ColorPicker(width=250, startupcolor=[0, 255, 255])
        self.color_picker.setObjectName("color")
        
        self.mask_vbox_hbox.addWidget(self.color_picker, alignment=Qt.AlignRight | Qt.AlignTop)
        self.mask_vbox.addLayout(self.mask_vbox_hbox)
        
        self.mask_vbox_hbox_vbox = QVBoxLayout(self)
        self.mask_vbox_hbox_vbox.addStretch(1)
        self.mask_dots = QLabel(self)
        self.mask_dots.setPixmap(QPixmap("ui/images/settings/mask/dots.png"))
        self.mask_vbox_hbox_vbox.addWidget(self.mask_dots, alignment=Qt.AlignRight | Qt.AlignTop)
        self.mask_vbox_hbox.addLayout(self.mask_vbox_hbox_vbox)
        self.mask_vbox_hbox_vbox.addStretch(8)
       
        self.layout.addLayout(self.mask_vbox)

    def resizeEvent(self, event):
        self.label.resize(self.size())
        return super().resizeEvent(event)


class SettingsWidget(QWidget):
    changed = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.result = {}

        self.background = QLabel(self)
        self.background.setObjectName("settings_widget")

        self.main_vbox = QVBoxLayout(self)

        self.settings_panel_hbox = QHBoxLayout(self)

        self.settings_panel_hbox.addStretch(1)

        self.line_left = QLabel()
        self.line_left.setPixmap(QPixmap("ui/images/line.png"))
        self.settings_panel_hbox.addWidget(self.line_left, 1, alignment=Qt.AlignCenter)

        self.setts = SettingsPanel(self)
        self.settings_panel_hbox.addWidget(self.setts, 12)

        self.setts.messages_visual_button.clicked.connect(self.change_state)
        self.setts.messages_sound_button.clicked.connect(self.change_state)

        self.line_right = QLabel()
        self.line_right.setPixmap(QPixmap("ui/images/line.png"))
        self.settings_panel_hbox.addWidget(self.line_right, 1, alignment=Qt.AlignCenter)

        self.settings_panel_hbox.addStretch(1)

        self.setts.color_picker.change_value.connect(self.change_state)

        self.main_vbox.addStretch(1)
        self.main_vbox.addLayout(self.settings_panel_hbox, stretch=2)
        self.main_vbox.addStretch(1)

        self.setLayout(self.main_vbox)
    
    def change_result(self, name, value):
        self.result[name] = value
        self.changed.emit(self.result)

    def change_state(self, value):
        name = self.sender().objectName()
        self.change_result(name, value)

    def resizeEvent(self, event):
        self.background.resize(self.size())
        return super().resizeEvent(event)