class Subor:
    def __init__(self, path):
        self.path = path
        try:
            self.subor = open(path, "w")
        except OSError:
            print("Súbor sa nepodarilo vytvoriť!")          #later raise error
        self.subor.close()
    
    def writeData(self, data):
        ...
    def readData(self):
        ...