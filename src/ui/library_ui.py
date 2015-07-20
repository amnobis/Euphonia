import taglib

from PyQt5.QtCore import pyqtSignal, QUrl, Qt, pyqtSlot, QPoint
from PyQt5.QtWidgets import QTreeWidget, QAbstractItemView, QMenu, QAction, QTreeWidgetItem
from PyQt5.QtGui import QFont

from src.ui.metadata_ui import MetadataUI

class LibraryUI(QTreeWidget):
    trackChange = pyqtSignal(QTreeWidgetItem, int)
    unknownTrack = pyqtSignal(str)
    meta = ["TRACKNUMBER", "TITLE", "ALBUMARTIST", "ALBUM", "LENGTH", "BITRATE", "STYLE"]

    def __init__(self):
        super().__init__()
        self.setIndentation(0)
        self.setSortingEnabled(True)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.metadataUI = MetadataUI()
        self.songMenu = QMenu("Actions")
        self.addMenu = QMenu("Actions")
        self._connect_widgets()
        self._init_menus()

    def init_playlist(self, lib):
        for song_meta in lib.values():
            info = ['' for i in range(7)]
            try:
                for i in range(7):
                    if i == 4:
                        length = int(song_meta.get(self.meta[i])[0]) / 1000
                        mins = int(length / 60)
                        secs = int(length - 60 * mins)
                        info[i] = str(mins) + ":%02d" % secs
                    elif i == 5:
                        info[i] = song_meta.get(self.meta[i])[0] + " kbit/s"
                    else:
                        info[i] = song_meta.get(self.meta[i])[0]
            except:
                pass

            item = QTreeWidgetItem()
            for i in range(7):
                item.setText(i, info[i])

            item.setData(0, 1, QUrl.fromLocalFile(song_meta.get("DIR")))
            self.addTopLevelItem(item)

        headers = ["#", "Title", "Artist", "Album", "Dur.", "Bitrate", "Genre"]
        self.setColumnCount(6)
        self.header().setDefaultAlignment(Qt.AlignCenter)
        self.setHeaderLabels(headers)
        self.setColumnWidth(0, 50)
        self.setColumnWidth(1, 200)
        self.setColumnWidth(2, 150)
        self.setColumnWidth(3, 150)
        self.setColumnWidth(4, 50)
        self.setColumnWidth(5, 100)
        self.setColumnWidth(6, 50)

    def next_track(self):
        item = self.itemBelow(self.currentItem())
        if item is None:
            item = self.topLevelItem(0)
        self.setCurrentItem(item)
        self.trackChange.emit(item, 0)

    def prev_track(self):
        item = self.itemAbove(self.currentItem())
        if item is None:
            item = self.topLevelItem(self.topLeveLitemCount() - 1)
        self.setCurrentItem(item)
        self.trackChange.emit(item, 0)

    def _connect_widgets(self):
        self.customContextMenuRequested.connect(self.show_menu)
        self.metadataUI.save_metadata.connect(self.save_metadata)
        self.metadataUI.closeButton.clicked.connect(self.close_metadata)

    @pyqtSlot(QPoint)
    def show_menu(self, point):
        if self.currentItem() is None:
            self.addMenu.exec(self.mapToGlobal(point))
        else:
            self.songMenu.exec(self.mapToGlobal(point))

    def _init_menus(self):
        self._init_song_menu()
        self._init_add_menu()

    def _init_add_menu(self):
        self.menuAdd = QAction("Add Songs...", self.addMenu)
        self.addMenu.addAction(self.menuAdd)

    def _init_song_menu(self):
        self.menuPlay = QAction("Play Song", self.songMenu)
        self.menuEdit = QAction("Edit Metadata", self.songMenu)
        self.songMenu.addActions([self.menuPlay, self.menuEdit])
        self.menuPlay.triggered.connect(self.current_track)
        self.menuEdit.triggered.connect(self.show_metadata)

    def current_track(self):
        self.trackChange.emit(self.currentItem(), 0)

    def show_metadata(self):
        self.setEnabled(False)
        self.metadataUI.load_data(self.currentItem())
        self.metadataUI.show()

    def close_metadata(self):
        self.setEnabled(True)

    def save_metadata(self, data):
        edit = taglib.File(self.currentItem().data(0,1).path())

        for i in range(5):
            if i == 1:
                edit.tags[self.meta[i]] = self._parse_time_string(data[self.meta[i]])
            else:
                edit.tags[self.meta[i]] = data[self.meta[i]]

            self.currentItem().setText(i, data[self.meta[i]])

        edit.save()
        self.setEnabled(True)

    def _parse_time_string(self, val):
        ms = val.split(":")

        return str((int(ms[0]) * 60 + int(ms[1])) * 1000)

