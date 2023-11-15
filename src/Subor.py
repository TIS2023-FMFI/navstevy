class Subor:
    def __init__(self, path):
        self.__path = path
        try:
            self.__subor = open(path, "w")
        except OSError:
            print("Súbor sa nepodarilo vytvoriť!")          #later raise error
        self.__subor.close()
    
    def writeData(self, data):
        ...
    def readData(self):
        ...