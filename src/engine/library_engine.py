import json, os, taglib
from PyQt5.QtCore import pyqtSignal, QObject

class LibraryEngine(QObject):
    importLibrary = pyqtSignal(dict)
    meta = ["TITLE", "LENGTH", "ALBUMARTIST", "ALBUM", "STYLE"]

    def __init__(self):
        super().__init__()
        self.lib_file = "src/library.json"
        self.library = {}
        self.playlist_data = []
        
    def load_library(self):
        lib = open(self.lib_file, "r")
        self.library = json.load(lib)
        self.importLibrary.emit(self.library)

    def add_directory(self, dirs):
        for dir in dirs:
            for root, subs, files in os.walk(dir):
                for file in files:
                    if not file.lower().endswith(('.mp3', '.flac')):
                        continue
                    tag_file = taglib.File(os.path.join(root, file))
                    if not self._contains_song(tag_file):
                        tag_file.tags["DIR"] = root + "/" + file
                        tag_file.tags["BITRATE"] = [str(tag_file.bitrate)]
                        self.library[len(self.library) + 1] = tag_file.tags
                    tag_file.save()
        json.dump(self.library, open(self.lib_file, 'w'), indent=2)
        self.importLibrary.emit(self.library)

    def _contains_song(self, tag_file):
        meta = tag_file.tags
        for data in self.library.values():
            if data.get("TITLE") == meta.get("TILE") and \
               data.get("LENGTH") == meta.get("LENGTH"):
                if meta.get("TITLE") is None:
                    self._unknown_track(tag_file)
                return True
        return False

    def _unknown_track(self, tag_file):
        tag_file.tags["TITLE"] = "Unknown Tracks"
        tag_file.save()