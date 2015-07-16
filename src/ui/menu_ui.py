from PyQt5.QtWidgets import QMenuBar, QMenu, QFileDialog, \
                            QAction, QListView, QTreeView, \
                            QFileSystemModel, QAbstractItemView
from PyQt5.QtCore import pyqtSignal, pyqtSlot

class MenuUI(QMenuBar):
    def __init__(self):
        super().__init__()
        self.file_menu = QMenu("&File")
        self.edit_menu = QMenu()
        self.help_menu = QMenu()
        self._init_menus()

    def _init_menus(self):
        self._file_menu()

    def _file_menu(self):
        self.add_library = QAction("&Add Library...", self)
        self.file_menu.addAction(self.add_library)
        self.file_menu.addAction("&Save Library...")
        self.file_menu.addAction("E&xit")
        self._connect_widgets()
        self.addMenu(self.file_menu)

    def _connect_widgets(self):
        self.add_library.triggered.connect(self._add_library)

    def _add_library(self):
        self.dialog = QFileDialog()
        self.dialog.setFileMode(QFileDialog.DirectoryOnly)
        self.dialog.setOption(QFileDialog.DontUseNativeDialog, True)

        for view in self.dialog.findChildren((QListView, QTreeView)):
            if isinstance(view.model(), QFileSystemModel):
                view.setSelectionMode(QAbstractItemView.MultiSelection)

        if self.dialog.exec():
            dirs = self.dialog.selectedFiles()
