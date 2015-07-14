import os
import taglib
from PyQt5.QtCore import pyqtSignal, QUrl, Qt, pyqtSlot, QPoint
from PyQt5.QtWidgets import QTreeWidget, QAbstractItemView, QMenu, QAction
from PyQt5.QtWidgets import QTreeWidgetItem
from metadata_ui import MetadataUI


class PlaylistUI(QTreeWidget):
    trackChange = pyqtSignal(QTreeWidgetItem, int)
    unknownTrack = pyqtSignal(str)
    meta = ["TITLE", "LENGTH", "ALBUMARTIST", "ALBUM", "STYLE"]

    def __init__(self):
        print("Test this blah blah. GitHub is stupid.")
        super().__init__()
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.metadataUI = MetadataUI()
        self.songMenu = QMenu("Actions")
        self.addMenu = QMenu("Actions")
        self._connect_widgets()
        self._init_playlist()

    def _init_playlist(self):
        self._init_menus()
        for root, dirs, files in os.walk("/home/anobis/library"):
            for file in files:
                data = taglib.File(os.path.join(root,file))
                info = ['' for i in range(5)]

                try:
                    for i in range(5):
                        if i == 1:
                            length = int(data.tags.get(self.meta[i])[0]) / 1000
                            mins = int(length / 60)
                            secs = int(length - 60 * mins)
                            info[i] = str(mins) + ":%02d" % secs
                        else:
                            info[i] = data.tags.get(self.meta[i])[0]
                except:
                    if info[0] is '':
                        info[0] = "Unknown Track"

                item = QTreeWidgetItem()
                for i in range(5):
                    item.setText(i, info[i])

                item.setData(0, 1, QUrl.fromLocalFile(os.path.join(root, file)))
                self.addTopLevelItem(item)
        headers = ["Name", "Time", "Artist", "Album", "Genre"]
        self.setColumnCount(5)
        self.setHeaderLabels(headers)
        self.setColumnWidth(0, 400)
        self.setColumnWidth(1, 50)
        self.setColumnWidth(2, 200)
        self.setColumnWidth(3, 200)
        self.setColumnWidth(4, 150)

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

