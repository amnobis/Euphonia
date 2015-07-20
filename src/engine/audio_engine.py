from PyQt5.QtCore import pyqtSlot, QUrl, pyqtSignal
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QTreeWidgetItem


class AudioEngine(QMediaPlayer):
    reqMedia = pyqtSignal()

    def __init__(self):
        super().__init__()

    def play_music(self):
        if self.state() == QMediaPlayer.PlayingState:
            self.pause()
        elif self.state() == QMediaPlayer.PausedState:
            self.play()
        else:
            self.reqMedia.emit()

    def adjust_volume(self, loudness):
        self.setVolume(loudness)

    @pyqtSlot(int)
    def set_time(self, time):
        if abs(self.position() - time) > 99:
            self.setPosition(time)

    @pyqtSlot(QTreeWidgetItem, int)
    def play_track(self, item, column):
        filepath = item.data(0,1)
        self.setMedia(QMediaContent(filepath))
        self.pause()
        self.play_music()