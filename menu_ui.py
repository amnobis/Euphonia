from PyQt5.QtWidgets import QMenuBar

class MenuUI(QMenuBar):
    def __init__(self):
        super().__init__()
        self.initMenus()

    def initMenus(self):
        #self.fileMenu = self.addMenu("&File")
        self.addMenu("&File")
        self.addMenu("&Edit")
        self.addMenu("&Help")
