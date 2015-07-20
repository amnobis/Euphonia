import os
import taglib

from PyQt5.QtCore import pyqtSignal, QUrl, Qt, pyqtSlot, QPoint
from PyQt5.QtWidgets import QTreeWidget, QAbstractItemView, QMenu, QAction, QHeaderView
from PyQt5.QtWidgets import QTreeWidgetItem

from src.ui.metadata_ui import MetadataUI

class PlaylistUI(QTreeWidget):
    def __init__(self):
        super().__init__()
        self.test = QTreeWidgetItem()
        self.test.setText(0, "Hello")
        self.header().close()
        self.addTopLevelItem(self.test)