class CustomFile:   
    def __init__(self, path):   
        self.path = path
        try:
            file = open(path, "a+")  # Use "a+" to open the file for both reading and appending
        except OSError as e:
            print(f"Error opening file {path}: {e}")
        self.numOfLines = self.getNumOfLines()
        file.close()

    def getNumOfLines(self): 
        with open(self.path, "r") as file:
            file.seek(0)
            data = file.readlines()
            num = len(data)
            if num == 1 and data[0] == "": 
                return 0
        file.close()
        return num

    def writeVisitor(self, data):
        with open(self.path, "a+") as file:
            file.write(data)
            self.numOfLines += 1    # dôležité pre generovanie správneho ID
        file.close()
    
    def readData(self):
        dataInStrings = []
        with open(self.path, "r") as file:
            file.seek(0)  # dôležité dať pointer na začiatok ak cheme čiťať celý súbor
            dataInStrings = file.readlines()
        file.close()
        return dataInStrings

    def edit(self, id, visitor):
        with open(self.path, "a+") as file:
            file.seek(0)
            lines = file.readlines()
            if 1 <= id <= len(lines):
                lines[id] = visitor.getDataToWrite()      #id je zatiaľ rovnaké ako pozícia riadku v texte
                with open(self.path, 'w') as file:
                    file.seek(0)
                    file.writelines(lines)
                file.close()
                print(f"Line {id} replaced successfully.")
            else:
                print("Invalid line number.")
        file.close()

    def removeVisitor(self, id):
        with open(self.path, "a+") as file:
            file.seek(0)
            lines = file.readlines()
            if 1 <= id <= len(lines):
                lines[id] = ""      #id je zatiaľ rovnaké ako pozícia riadku v texte
                self.numOfLines -= 1
                with open(self.path, 'w') as file:
                    file.seek(0)
                    file.writelines(lines)
                file.close()
                print(f"Line {id} deleted successfully.")
            else:
                print("Invalid line number.")
        file.close()
