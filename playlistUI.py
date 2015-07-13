import os
import taglib
from PyQt5.QtCore import pyqtSignal, QUrl, Qt, pyqtSlot, QPoint
from PyQt5.QtWidgets import QTreeWidget, QAbstractItemView, QMenu, QAction
from PyQt5.QtWidgets import QTreeWidgetItem
from metadataUI import metadataUI


class playlistUI(QTreeWidget):
    trackChange = pyqtSignal(QTreeWidgetItem, int)
    unknownTrack = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.metadataUI = metadataUI()
        self.songMenu = QMenu("Actions")
        self.addMenu = QMenu("Actions")
        self.connectWidgets()

    def initPlaylist(self):
        self.initMenus()
        for root, dirs, files in os.walk("/home/anobis/library"):
            for file in files:
                data = taglib.File(os.path.join(root,file))
                title = ''
                time = ''
                comp = ''
                album = ''
                genre = ''
                if data.tags.get("TITLE") is None:
                    print(data.tags)
                    self.unknownTrack.emit(str(os.path.join(root, file)))

                if data.tags.get("LENGTH") != None:
                    length = int(data.tags.get("LENGTH")[0]) / 1000
                    mins = int(length / 60)
                    secs = int(length - 60 * mins)
                    time = str(mins) + ":%02d" % secs

                if data.tags.get("TITLE") != None:
                    title = data.tags.get("TITLE")[0]
                else:
                    title = "Unknown Track"

                if data.tags.get("ALBUMARTIST") != None:
                    comp = data.tags.get("ALBUMARTIST")[0]

                if data.tags.get("ALBUM") != None:
                    album = data.tags.get("ALBUM")[0]

                if data.tags.get("STYLE") != None:
                    genre = data.tags.get("STYLE")[0]

                item = QTreeWidgetItem()
                item.setText(0, title)
                item.setText(1, time)
                item.setText(2, comp)
                item.setText(3, album)
                item.setText(4, genre)
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

    def nextTrack(self):
        item = self.itemBelow(self.currentItem())
        if item is None:
            item = self.topLevelItem(0)
        self.setCurrentItem(item)
        self.trackChange.emit(item, 0)

    def prevTrack(self):
        item = self.itemAbove(self.currentItem())
        if item is None:
            item = self.topLevelItem(self.topLeveLitemCount() - 1)
        self.setCurrentItem(item)
        self.trackChange.emit(item, 0)

    def connectWidgets(self):
        self.customContextMenuRequested.connect(self.showMenu)
        self.metadataUI.saveMeta.connect(self.saveMeta)

    @pyqtSlot(QPoint)
    def showMenu(self, point):
        if self.currentItem() is None:
            self.addMenu.exec(self.mapToGlobal(point))
        else:
            self.songMenu.exec(self.mapToGlobal(point))

    def initMenus(self):
        self.initSongMenu()
        self.initAddMenu()
    
    def initAddMenu(self):
        self.menuAdd = QAction("Add Songs...", self.addMenu)
        self.addMenu.addAction(self.menuAdd)
    
    def initSongMenu(self):
        self.menuPlay = QAction("Play Song", self.songMenu)
        self.menuEdit = QAction("Edit Metadata", self.songMenu)
        self.songMenu.addActions([self.menuPlay, self.menuEdit])
        self.menuPlay.triggered.connect(self.currTrack)
        self.menuEdit.triggered.connect(self.showMeta)

    def currTrack(self):
        self.trackChange.emit(self.currentItem(), 0)

    def showMeta(self):
        self.setEnabled(False)
        self.metadataUI.loadData(self.currentItem())
        self.metadataUI.show()

    def saveMeta(self, data):
        edit = taglib.File(self.currentItem().data(0,1).path())
        edit.tags["TITLE"] = data["TITLE"]
        self.currentItem().setText(0, data["TITLE"])
        self.setEnabled(True)
