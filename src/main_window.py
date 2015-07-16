import sys
from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QApplication

from src.engine.audio_engine import AudioEngine
from src.ui.audio_ui import AudioUI
from src.ui.playlist_ui import PlaylistUI
from src.ui.menu_ui import MenuUI


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.playlistUI = PlaylistUI()
        self.audioUI = AudioUI()
        self.menuUI = MenuUI()
        self.engine = AudioEngine()
        self.mainWidget = QWidget()
        self.layout = QGridLayout(self.mainWidget)
        self._connect_widgets()
        self._init_ui()

    def _init_ui(self):
        self.layout.addWidget(self.playlistUI, 0, 1)
        self.layout.addWidget(self.audioUI, 1, 1)
        self.setCentralWidget(self.mainWidget)
        self.setMenuBar(self.menuUI)
        self.setGeometry(300, 300, 1100, self.height())
        self.setWindowTitle('Euphonia')
        self.show()

    def _connect_widgets(self):
        self.playlistUI.itemDoubleClicked.connect(self.engine.play_track)
        self.playlistUI.trackChange.connect(self.engine.play_track)

        self.audioUI.next_track.connect(self.playlistUI.next_track)
        self.audioUI.prev_track.connect(self.playlistUI.prev_track)
        self.audioUI.playButton.clicked.connect(self.engine.play_music)
        self.audioUI.prevButton.clicked.connect(lambda: self.engine.set_time(0))
        self.audioUI.timeSlider.valueChanged.connect(self.engine.set_time)

        self.engine.reqMedia.connect(self.playlistUI.current_track)
        self.engine.stateChanged.connect(self.audioUI.set_play_button)
        self.engine.positionChanged.connect(self.audioUI.update_slider)
        self.engine.durationChanged.connect(self.audioUI.slider_duration)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
    