from PyQt5.QtCore import pyqtSignal, Qt, pyqtSlot
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QToolButton, QStyle, QSlider


class AudioUI(QWidget):
    next_track = pyqtSignal()
    prev_track = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.player = QMediaPlayer()
        self.layout = QHBoxLayout()
        self.playButton = QToolButton(self)
        self.prevButton = QToolButton(self)
        self.nextButton = QToolButton(self)
        self.timeSlider = TimeSlider(Qt.Horizontal)
        self.init_controls()
        self.connect_controls()

    def init_controls(self):
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.resize(40, 40)

        self.nextButton.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipForward))
        self.nextButton.resize(40,40)

        self.prevButton.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipBackward))
        self.prevButton.resize(40,40)

        self.layout.addWidget(self.prevButton)
        self.layout.addWidget(self.playButton)
        self.layout.addWidget(self.nextButton)
        self.layout.addWidget(self.timeSlider)

        self.setLayout(self.layout)

    def connect_controls(self):
        self.prevButton.clicked.connect(self.rewind_music)
        self.nextButton.clicked.connect(self.next_music)

    def update_slider(self, time):
        self.timeSlider.setValue(time)

    def slider_duration(self, duration):
        self.timeSlider.setRange(0, duration)

    def rewind_music(self):
        if self.timeSlider.value() < self.timeSlider.maximum() / 1000:
            self.prev_track.emit()
        else:
            self.timeSlider.setValue(0)

    def next_music(self):
        self.next_track.emit()

    @pyqtSlot(QMediaPlayer.State)
    def set_play_button(self, state):
        if state == QMediaPlayer.PlayingState:
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

class TimeSlider(QSlider):
    def __init__(self, orientation):
        super().__init__()
        self.setOrientation(orientation)
        self.paintSlider()

    def mousePressEvent(self, mouse):
        if mouse.button() == Qt.LeftButton:
            value = self.minimum() + \
                    ((self.maximum() - self.minimum())
                     * mouse.x() / self.width())
            self.setValue(value)

    def paintSlider(self):
        self.setStyleSheet("QSlider::add-page:horizontal { \
                                background: white \
                            }" + \
                           "QSlider::sub-page:horizontal { \
                                background: lightblue \
                            }")