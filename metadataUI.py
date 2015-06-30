from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog, QPushButton, \
    QGridLayout, QLineEdit, QLabel, QTreeWidgetItem


class metadataUI(QDialog):
    saveMeta = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.closeButton = QPushButton("Cancel")
        self.saveButton = QPushButton("Save")
        self.titleEdit = QLineEdit()
        self.titleLabel = QLabel("Title")
        self.timeEdit = QLineEdit()
        self.timeLabel = QLabel("Time")
        self.artistEdit = QLineEdit()
        self.artistLabel = QLabel("Artist")
        self.albumEdit = QLineEdit()
        self.albumLabel = QLabel("Album")
        self.genreEdit = QLineEdit()
        self.genreLabel = QLabel("Genre")
        self.layout = QGridLayout()
        self.setWindowTitle("Edit Metadata")
        self.initUI()

    def initUI(self):
        self.layout.addWidget(self.titleLabel, 0, 0)
        self.layout.addWidget(self.titleEdit, 0, 1, 1, 3)
        self.layout.addWidget(self.timeLabel, 1, 0)
        self.layout.addWidget(self.timeEdit, 1, 1, 1, 3)
        self.layout.addWidget(self.artistLabel, 2, 0)
        self.layout.addWidget(self.artistEdit, 2, 1, 1, 3)
        self.layout.addWidget(self.albumLabel, 3, 0)
        self.layout.addWidget(self.albumEdit, 3, 1, 1, 3)
        self.layout.addWidget(self.genreLabel, 4, 0)
        self.layout.addWidget(self.genreEdit, 4, 1, 1, 3)

        self.layout.addWidget(self.saveButton, 5, 2, 1, 1)
        self.layout.addWidget(self.closeButton, 5, 3, 1, 1)
        self.setLayout(self.layout)
        self.closeButton.clicked.connect(self.close)
        self.saveButton.clicked.connect(self.saveData)

    def loadData(self, item):
        self.titleEdit.setText(item.text(0))
        self.timeEdit.setText(item.text(1))
        self.artistEdit.setText(item.text(2))
        self.albumEdit.setText(item.text(3))
        self.genreEdit.setText(item.text(4))

    def saveData(self):
        data = {}
        data["TITLE"] = self.titleEdit.text()
        data["LENGTH"] = self.timeEdit.text()
        data["ALBUMARTIST"] = self.artistEdit.text()
        data["ALBUM"] = self.albumEdit.text()
        data["STYLE"] = self.genreEdit.text()
        self.saveMeta.emit(data)
        self.close()
