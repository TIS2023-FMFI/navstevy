class CustomFile:   
    def __init__(self, path):   
        self.path = path
        try:
            file = open(path, "r", encoding="utf-8")  # Use "a+" to open the file for both reading and appending
        except OSError as e:
            print(f"Error opening file {path}: {e}")
        file.close()

    def writeVisitor(self, data):
        with open(self.path, "a+",encoding="utf-8") as file:
            file.write(data)
        file.close()
    
    def readData(self):
        dataInStrings = []
        with open(self.path, "r",encoding="utf-8") as file:
            file.seek(0)  # dôležité dať pointer na začiatok ak cheme čiťať celý súbor
            dataInStrings = file.readlines()
        file.close()
        return dataInStrings

    def edit(self, id, visitor):
        with open(self.path, "r",encoding="utf-8") as file:
            file.seek(0)
            lines = file.readlines()
            lineCount = 0
            lineToChange = -1
            for line in lines:
                foundId = int(line.strip().split(';')[0])
                if foundId == id:
                    lineToChange = lineCount
                    break
                lineCount += 1
            if lineToChange == -1: 
                print(f"There is no visitor with {id} ID curently on site.")
            else:
                with open(self.path, "w",encoding="utf-8") as file2:
                    lines[lineToChange] = visitor.getDataToWrite()
                    file.seek(0)
                    file2.writelines(lines)
                    file2.close()
                    f"Visitor {id} changed successfully!"
        file.close()

    def removeVisitor(self, id):
        with open(self.path, "r",encoding="utf-8") as file:
            file.seek(0)
            lines = file.readlines()
            lineCount = 0
            lineToChange = -1
            for line in lines:
                foundId = int(line.strip().split()[0])
                if foundId == id:
                    lineToChange = lineCount
                    break
                lineCount += 1
            if lineToChange == -1: 
                print(f"There is no visitor with {id} ID curently on site.")
            else:
                with open(self.path, "w",encoding="utf-8") as file2:
                    lines[lineToChange] = ""
                    file.seek(0)
                    file2.writelines(lines)
                    file2.close()
                    print(f"Visitor {id} removed successfully!")
        file.close()