import sys
from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QApplication
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt

from src.engine.audio_engine import AudioEngine
from src.engine.library_engine import LibraryEngine
from src.ui.audio_ui import AudioUI
from src.ui.library_ui import LibraryUI
from src.ui.menu_ui import MenuUI
from src.ui.playlist_ui import PlaylistUI

class MainWindow(QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self._set_style()
        self.libraryUI = LibraryUI()
        self.playlistUI = PlaylistUI()
        #self.libraryUI = QTreeWidget()
        self.audioUI = AudioUI()
        self.menuUI = MenuUI(self)
        self.engine = AudioEngine()
        self.library = LibraryEngine()
        self.mainWidget = QWidget()
        self.layout = QGridLayout(self.mainWidget)
        self._connect_widgets()
        self._init_ui()
        self.library.load_library()

    def _init_ui(self):
        self.layout.addWidget(self.playlistUI, 0, 0, 1, 3)
        self.layout.addWidget(self.libraryUI, 0, 3, 1, 1)
        self.layout.addWidget(self.audioUI, 1, 0, 1, 4)
        self.setCentralWidget(self.mainWidget)
        self.setMenuBar(self.menuUI)
        self.setGeometry(300, 300, 1100, self.height())
        self.setWindowTitle('Euphonia')
        self.show()

    def _connect_widgets(self):
        self.libraryUI.itemDoubleClicked.connect(self.engine.play_track)
        self.libraryUI.trackChange.connect(self.engine.play_track)

        self.audioUI.next_track.connect(self.libraryUI.next_track)
        self.audioUI.prev_track.connect(self.libraryUI.prev_track)
        self.audioUI.playButton.clicked.connect(self.engine.play_music)
        self.audioUI.prevButton.clicked.connect(lambda: self.engine.set_time(0))
        self.audioUI.timeSlider.valueChanged.connect(self.engine.set_time)
        
        self.menuUI.addDirectory.connect(self.library.add_directory)

        self.library.importLibrary.connect(self.libraryUI.init_playlist)

        self.engine.reqMedia.connect(self.libraryUI.current_track)
        self.engine.stateChanged.connect(self.audioUI.set_play_button)
        self.engine.positionChanged.connect(self.audioUI.update_slider)
        self.engine.durationChanged.connect(self.audioUI.slider_duration)

    def _set_style(self):

        dark_palette = QPalette()

        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)
        #self.parent.setStyle("Fusion")
        #self.parent.setPalette(dark_palette)
        self.parent.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow(app)
    sys.exit(app.exec_())
