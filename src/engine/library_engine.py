import json, os

class LibraryEngine:
    def __init__(self):
        print(os.getcwd())
        self.lib_file = open("../../library.json", "r")
        self.library = {}
        print("Handling the Library")
        
    def load_library(self):
        self.library = json.load(self.lib_file)
        print(self.library)
    
    def add_directory(self):
        print("sup dawg")
        