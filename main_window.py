from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QApplication
import sys

from audio_engine import AudioEngine
from audio_ui import AudioUI
from playlist_ui import PlaylistUI


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.PlaylistUI = PlaylistUI()
        self.AudioUI = AudioUI()
        self.engine = AudioEngine()
        self.mainWidget = QWidget()
        self.layout = QGridLayout(self.mainWidget)
        self._connect_widgets()
        self.PlaylistUI.init_playlist()
        self.init_ui()

    def init_ui(self):
        self.layout.addWidget(self.PlaylistUI, 0, 1)
        self.layout.addWidget(self.AudioUI, 1, 1)
        self.setCentralWidget(self.mainWidget)
        self.setGeometry(300, 300, 1100, self.height())
        self.setWindowTitle('Euphonia')
        self.show()

    def _connect_widgets(self):
        self.PlaylistUI.itemDoubleClicked.connect(self.engine.play_track)
        self.PlaylistUI.trackChange.connect(self.engine.play_track)

        self.AudioUI.next_track.connect(self.PlaylistUI.next_track)
        self.AudioUI.prev_track.connect(self.PlaylistUI.prev_track)
        self.AudioUI.playButton.clicked.connect(self.engine.play_music)
        self.AudioUI.prevButton.clicked.connect(lambda: self.engine.set_time(0))
        self.AudioUI.timeSlider.valueChanged.connect(self.engine.set_time)

        self.engine.reqMedia.connect(self.PlaylistUI.current_track)
        self.engine.stateChanged.connect(self.AudioUI.set_play_button)
        self.engine.positionChanged.connect(self.AudioUI.update_slider)
        self.engine.durationChanged.connect(self.AudioUI.slider_duration)

    def test_signal(self):
        print("Signal has occured")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
    