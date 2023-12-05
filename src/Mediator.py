import Visitor as vs
import Preview as pr
import CustomFile as cf

class Mediator:
    def __init__(self):
        self.visitors = []
        self.fileReader = cf.CustomFile('../navstevy/src/files/test_file.txt')  # Add the file extension
    
    def addVisitor(self, visitor):
        self.visitors.append(visitor)
        self.fileReader.writeData(str(visitor))  # Write the visitor data to the file
    
    def getVisitors(self):
        return self.visitors

# Example
m = Mediator()
m.addVisitor(10)
m.fileReader.readData()
m.fileReader.closeFile() 