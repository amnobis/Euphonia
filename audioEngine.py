from PyQt5.QtCore import pyqtSlot, QUrl, pyqtSignal
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QTreeWidgetItem


class audioEngine(QMediaPlayer):
    reqMedia = pyqtSignal()

    def __init__(self):
        super().__init__()

    def playMusic(self):
        if self.state() == QMediaPlayer.PlayingState:
            self.pause()
        elif self.state() == QMediaPlayer.PausedState:
            self.play()
        else:
            self.reqMedia.emit()

    @pyqtSlot(int)
    def setTime(self, time):
        if abs(self.position() - time) > 99:
            self.setPosition(time)

    @pyqtSlot(QTreeWidgetItem, int)
    def playTrack(self, item, column):
        filepath = item.data(0,1)
        self.setMedia(QMediaContent(filepath))
        self.pause()
        self.playMusic()