from PyQt5.QtCore import pyqtSignal, Qt, QUrl, pyqtSlot
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QToolButton, QStyle, QTreeWidgetItem, QSlider


class audioUI(QWidget):
    nextTrack = pyqtSignal()
    prevTrack = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.player = QMediaPlayer()
        self.layout = QHBoxLayout()
        self.playButton = QToolButton(self)
        self.prevButton = QToolButton(self)
        self.nextButton = QToolButton(self)
        self.timeSlider = timeSlider(Qt.Horizontal)
        print("hello")
	self.initControls()
        self.connectControls()

    def initControls(self):
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

    def connectControls(self):
        self.prevButton.clicked.connect(self.rewMusic)
        self.nextButton.clicked.connect(self.nextMusic)

    def updateSlider(self, time):
        self.timeSlider.setValue(time)

    def sliderDuration(self, duration):
        self.timeSlider.setRange(0, duration)

    def rewMusic(self):
        if self.timeSlider.value() < self.timeSlider.maximum() / 1000:
            self.prevTrack.emit()
        else:
            self.timeSlider.setValue(0)

    def nextMusic(self):
        self.nextTrack.emit()

    @pyqtSlot(QMediaPlayer.State)
    def setPlayButton(self, state):
        if state == QMediaPlayer.PlayingState:
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

class timeSlider(QSlider):
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
