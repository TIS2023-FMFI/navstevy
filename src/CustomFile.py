class CustomFile:
    def __init__(self, path):
        self.path = path
        try:
            self.file = open(path, "a+")  # Use "a+" to open the file for both reading and appending
        except OSError:
            print("Súbor sa nepodarilo vytvoriť!")  # Later, you might want to raise an error instead of just printing
    
    def writeData(self, data):
        self.file.write(data + ';')  # Add a ; character after each data entry
    
    def readData(self):
        self.file.seek(0)  # Move the file pointer to the beginning
        data = self.file.read()
        print(data)

    def closeFile(self):
        self.file.close()

