class CustomFile:   
    def __init__(self, path):   
        self.path = path
        try:
            self.file = open(path, "a+")  # Use "a+" to open the file for both reading and appending
        except OSError as e:
            print(f"Error opening file {path}: {e}")
        self.numOfLines = self.getNumOfLines()
    
    def getNumOfLines(self): 
        self.file.seek(0)
        data = self.file.readlines()
        num = len(data)
        if num == 1 and data[0] == "": 
            return 0
        return num

    def writeData(self, data):
        self.file.write(data)
        self.numOfLines += 1    # dôležité pre generovanie ID
    
    def readData(self):
        self.file.seek(0)  # dôležité dať pointer na začiatok ak cheme čiťať celý súbor
        data = self.file.read()
        print(data)

    def closeFile(self):
        self.file.close()

    def edit(self, id, visitor):
        self.file.seek(0)
        lines = self.file.readlines()
        if 1 <= id <= len(lines):
            lines[id] = visitor.getDataToWrite()      #id je zatiaľ rovnaké ako pozícia riadku v texte
            with open(self.path, 'w') as file:
                file.seek(0)
                file.writelines(lines)
            file.close()
            print(f"Line {id} replaced successfully.")
        else:
            print("Invalid line number.")



