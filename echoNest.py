from PyQt5.QtCore import pyqtSlot, QObject
from PyQt5.QtWidgets import QWidget
from pyechonest import config, track

class echoNest(QWidget):
    def __init__(self):
        super().__init__()
        config.ECHO_NEST_API_KEY="HWUCDLFUYFKZK2OWC"

    @pyqtSlot(str)
    def getTrack(self, filepath):
        return None