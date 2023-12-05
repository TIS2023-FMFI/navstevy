import Visitor as vis
import Preview as pre
import CustomFile as cf

class Mediator:
    def __init__(self):
<<<<<<< HEAD
        self.vissitors = []
        self.fileReader = cf.CustomFile('../navstevy/src/files/test_file.csv')  # Add the file extension
=======
        self.visitors = []
        self.fileReader = cf.CustomFile('../navstevy/src/files/test_file.txt')  # Add the file extension
>>>>>>> 65a7005ba01fadc96b1e019fc689650d43a0f91c
    
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