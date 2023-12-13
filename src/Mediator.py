import Visitor as vis
import Preview as pre
import CustomFile as cf

class Mediator:
    def __init__(self):
        self.visitors = []      # TODO pridávanie neodhlásených z predošlého dňa
        self.file = cf.CustomFile('../navstevy/src/files/testFile.csv')  # TODO nastavnie správnej cesty pre ich potreby
    
    def addVisitor(self, name, surname, cardId, carTag, company, count, reason):
        visitor = vis.Visitor(self.generateId(), name, surname, cardId, carTag, company, count, reason)
        self.file.writeVisitor(visitor.getDataToWrite())  # zapíše visitora do súboru
        self.visitors.append(visitor)

    def editVisitor(self, id, name = None, surname = None, cardId = None, carTag = None, company = None, count = None, reason = None):
        changedVisiotor = None
        for vis in self.visitors: 
            if vis.getId() == id:
                vis.edit(name, surname, cardId, carTag, company, count, reason)
                changedVisiotor = vis
                break
        if changedVisiotor is None:
            print("We do not have this visitor right now!")
        else:
            self.file.edit(id, changedVisiotor)
    
    def generateId(self):  # TODO vygenerovanie unikátneho id pre každý zápis. Zatiaľ takto:
        return self.file.numOfLines

    def getVisitors(self):
        return self.visitors
    
    def filter(self): 
        ...

# Example
# m = Mediator()
# m.addVisitor("Fero", "Malý", 1, "BL123BL", "MatFyz", 4, "nudím sa")
# m.addVisitor("Jana", "Iná", 1, "KE123BL", "FMFI", 1, "skúšam dva")
# m.editVisitor(1, "Nina", None, None, "BL987BL")
# m.file.readData()
# m.file.closeFile() 