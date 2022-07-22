from PyQt5.QtMultimedia import QSoundEffect
from PyQt5.QtCore import QUrl

class SoundAlarm():
    def __init__(self, path):
        self.is_sound = True
        self.sound = QSoundEffect()
        self.sound.setSource(QUrl.fromLocalFile(path))
        self.sound.setVolume(50 * 0.01)
    
    def alarm(self, detect):
        if self.is_sound and detect and not self.sound.isPlaying():
            self.sound.play()

    def set_volume(self, value):
        self.sound.setVolume(value * 0.01)
    
    def change_sound(self):
        self.is_sound = not self.is_sound

    def load(self, sounding):
        self.is_sound = not sounding