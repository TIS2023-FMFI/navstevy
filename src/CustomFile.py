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
    with open(self.path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    lineToChange = None

    for index, line in enumerate(lines):
        foundId = int(line.strip().split(';')[0])
        if foundId == id:
            lineToChange = index
            break

    if lineToChange is None:
        print(f"There is no visitor with {id} ID currently on site.")
    else:
        lines[lineToChange] = visitor.getDataToWrite()

        with open(self.path, "w", encoding="utf-8") as file:
            file.writelines(lines)

        print(f"Visitor {id} changed successfully!")



    def removeVisitor(self, id):
        with open(self.path, "r", encoding="utf-8") as file:
            lines = file.readlines()
        lineToChange = None
        for index, line in enumerate(lines):
            foundId = int(line.strip().split()[0])
            if foundId == id:
                lineToChange = index
                break

        if lineToChange is None:
            print(f"There is no visitor with {id} ID currently on site.")
        else:
            lines.pop(lineToChange)

            with open(self.path, "w", encoding="utf-8") as file:
                file.writelines(lines)

            print(f"Visitor {id} removed successfully!")