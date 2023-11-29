import Visitor
import Preview
import CustomFile

class Mediator:
    def __init__(self):
        self.vissitors = []
        self.fileReader = CustomFile("/Users/lubos/Desktop/navstevy/files/test_file.csv")  # Add the file extension
    
    def addVisitor(self, visitor):
        self.vissitors.append(visitor)
        self.fileReader.writeData(str(visitor))  # Write the visitor data to the file
    
    def getVisitors(self):
        return self.vissitors

# Example
m = Mediator()
m.addVisitor(10)
m.fileReader.readData()
m.fileReader.closeFile() 