import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtGui import *
from audioEngine import audioEngine
from playlistUI import playlistUI
from audioUI import audioUI
from echoNest import echoNest

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.playlistUI = playlistUI()
        self.audioUI = audioUI()
        self.engine = audioEngine()
        self.echoNest = echoNest()
        self.mainWidget = QWidget()
        self.layout = QGridLayout(self.mainWidget)
        self.connectWidgets()
        self.playlistUI.initPlaylist()
        self.initUI()

    def initUI(self):
        self.layout.addWidget(self.playlistUI, 0, 1)
        self.layout.addWidget(self.audioUI, 1, 1)
        self.setCentralWidget(self.mainWidget)
        self.setGeometry(600, 300, 1000, self.height())
        self.setWindowTitle('Euphonia')
        self.show()

    def connectWidgets(self):
        self.playlistUI.itemDoubleClicked.connect(self.engine.playTrack)
        self.playlistUI.trackChange.connect(self.engine.playTrack)
        self.playlistUI.unknownTrack.connect(self.echoNest.getTrack)

        self.audioUI.nextTrack.connect(self.playlistUI.nextTrack)
        self.audioUI.prevTrack.connect(self.playlistUI.prevTrack)
        self.audioUI.playButton.clicked.connect(self.engine.playMusic)
        self.audioUI.prevButton.clicked.connect(lambda: self.engine.setTime(0))
        self.audioUI.timeSlider.valueChanged.connect(self.engine.setTime)

        self.engine.reqMedia.connect(self.playlistUI.currTrack)
        self.engine.stateChanged.connect(self.audioUI.setPlayButton)
        self.engine.positionChanged.connect(self.audioUI.updateSlider)
        self.engine.durationChanged.connect(self.audioUI.sliderDuration)

    def testSignal(self):
        print("Signal has occured")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())