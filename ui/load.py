from traceback import print_tb
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFileDialog, QTabWidget, QProgressBar, QStackedWidget
from PyQt5.QtCore import Qt, pyqtSignal, QUrl
from PyQt5.QtGui import QPixmap
from glob import glob
from back.video import VideoThread, VideoWriter
# from ui.live import PlayStreaming
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
# class VideoStreaming(PlayStreaming):
#     def __init__(self, filename, parent = None):
#         super().__init__(parent)
#         self.th = VideoReader(filename, self)

class Button(QLabel):
    hovered = pyqtSignal(bool)
    clicked = pyqtSignal(str)

    def __init__(self, pixmap, parent=None):
        super().__init__(parent)
        self.setPixmap(pixmap)

    def enterEvent(self, event):
        self.hovered.emit(True)
        return super().enterEvent(event)

    def leaveEvent(self, event):
        self.hovered.emit(False)
        return super().leaveEvent(event)

    def mousePressEvent(self, event):
        self.clicked.emit(self.objectName())
        return super().mousePressEvent(event)

class PathField(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.background = QLabel(self)
        self.background.setObjectName("path_field")

        self.layout = QHBoxLayout(self)
        
        self.text = QLabel(self)
        self.text.setObjectName("path_field_text")

        self.button = Button(QPixmap("ui/images/load/folder.png"), self)
        self.button.clicked.connect(self.open_directory_dialog)

        self.layout.addWidget(self.text, alignment=Qt.AlignLeft)
        self.layout.addWidget(self.button, alignment=Qt.AlignRight)

    def resizeEvent(self, event):
        self.background.resize(self.size())
        return super().resizeEvent(event)

    def open_directory_dialog(self):
        self.text.setText(str(QFileDialog.getExistingDirectory(self, "Выберите директорию")))
    

class FileForm(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout(self)

        self.title = QLabel(self)
        self.layout.addWidget(self.title, 1, Qt.AlignLeft)

        self.field = PathField(self)
        self.layout.addWidget(self.field, 2)


class LoadPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.label = QLabel(self)
        self.label.setObjectName("load_panel")

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(30, 30, 30, 30)
        
        
        load_text = QLabel(self)
        load_text.setText('Открыть папку')
        load_text.setObjectName('load_text')
        self.layout.addWidget(load_text)

        self.load_file_dialog_form = FileForm(self)
        self.layout.addWidget(self.load_file_dialog_form)

        save_text = QLabel(self)
        save_text.setText('Сохранить в папку')
        save_text.setObjectName('save_text')
        self.layout.addWidget(save_text)

        self.save_file_dialog_form = FileForm(self)
        self.layout.addWidget(self.save_file_dialog_form)

        self.start_button = Button(QPixmap("ui/images/load/start.png"),self)
        self.start_button.setObjectName("load_start")
        self.layout.addWidget(self.start_button, alignment=Qt.AlignHCenter)

    def resizeEvent(self, event):
        self.label.resize(self.size())
        return super().resizeEvent(event)

class LoadWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.background = QLabel(self)
        self.background.setObjectName("load_widget")

        self.main_vbox = QVBoxLayout(self)

        self.load_panel_hbox = QHBoxLayout(self)

        self.load_panel_hbox.addStretch(1)

        self.line_left = QLabel()
        self.line_left.setPixmap(QPixmap("ui/images/line.png"))
        self.load_panel_hbox.addWidget(self.line_left, 1, alignment=Qt.AlignCenter)

        self.panel = LoadPanel(self)
        self.load_panel_hbox.addWidget(self.panel, 12)

        self.line_right = QLabel()
        self.line_right.setPixmap(QPixmap("ui/images/line.png"))
        self.load_panel_hbox.addWidget(self.line_right, 1, alignment=Qt.AlignCenter)

        self.load_panel_hbox.addStretch(1)

        self.main_vbox.addStretch(1)
        self.main_vbox.addLayout(self.load_panel_hbox, stretch=2)
        self.main_vbox.addStretch(1)

        self.setLayout(self.main_vbox)

    def resizeEvent(self, event):
        self.background.resize(self.size())
        super().resizeEvent(event)

    def get_file_paths(self):
        return self.panel.load_file_dialog_form.field.text.text(), self.panel.save_file_dialog_form.field.text.text()

class ProgressWidget(QWidget):
    finished = pyqtSignal(bool)

    def __init__(self, src, save_path, parent=None):
        super().__init__(parent)
        self.__current_frame = 0
        self.save_path = save_path
        self.layout = QHBoxLayout(self)
        self.progress = QProgressBar(self)
        self.progress.setValue(0)
        self.layout.addWidget(self.progress, alignment=Qt.AlignVCenter )

        self.th = VideoThread(src, save_path, parent=self)
        self.th.start()
        
        self.video_writer = VideoWriter(save_path, self.th.file_processor.folder_path)
        self.th.change_pixmap.connect(self.counter)

    def counter(self, frame):
        self.video_writer.addFrame(frame)
        self.__current_frame += 1
        self.progress.setValue(int(self.__current_frame / self.th.frame_count * 100))
        if self.progress.value() == 100:
            self.video_writer.save()
            self.finished.emit(True)

class VideoWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.StreamPlayback)
        self.mediaPlayer.setVolume(0)
        self.display = QVideoWidget(self)
        self.mediaPlayer.setVideoOutput(self.display)
        
        self.layout.addWidget(self.display, alignment=Qt.AlignCenter, stretch=1)
        self.setLayout(self.layout)

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()
    
    def set_video(self, path):
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(path)))
        self.mediaPlayer.pause()

    def resizeEvent(self, event):
        self.display.setGeometry(0, 0, self.parent().width(), self.parent().height())
        super().resizeEvent(event)

class TabViewerItemWidget(QWidget):
    def __init__(self, src, save_path, parent=None):
        super().__init__(parent)
        

        self.layout = QHBoxLayout(self)
        self.setContentsMargins(50, 0, 50, 0)
        self.progress_widget = ProgressWidget(src, save_path, self)

        self.video_widget = VideoWidget(self)
        
        self.stacked_widget = QStackedWidget(self)
        self.stacked_widget.addWidget(self.progress_widget)
        self.stacked_widget.addWidget(self.video_widget)

        self.progress_widget.finished.connect(self.set_video_widget)
        
        self.layout.addWidget(self.stacked_widget)
        self.setLayout(self.layout)

    def set_video_widget(self):
        self.video_widget.set_video(self.progress_widget.video_writer.save_path)
        self.stacked_widget.setCurrentWidget(self.video_widget)

class TabViewerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.tab = QTabWidget(self)
        self.setContentsMargins(100, 0, 100, 0)
        self.layout = QVBoxLayout(self)
        self.layout.addStretch(1)
        self.layout.addWidget(self.tab, stretch=10)
        self.layout.addStretch(1)

        self.setLayout(self.layout)

    def set_video(self, src_dir, save_dir):
        for video in glob(f'{src_dir}/*.*'):
            video = video.replace('\\', '/')
            self.tab.addTab(TabViewerItemWidget(video, save_dir, self), video.split('/')[-1])   

    def stop_threads(self):
        for index in range(self.tab.count()):
            self.tab.widget(index).progress_widget.th.quit()