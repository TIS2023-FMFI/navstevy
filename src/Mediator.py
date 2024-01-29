import Visitor as vis
import CustomFile as cf
import difflib
import string


class Mediator:
    def __init__(self):
        self.visitors = []      # TODO pridávanie neodhlásených z predošlého dňa
        self.file = cf.CustomFile('../navstevy/src/files/testFile.csv')  # TODO nastavnie správnej cesty pre ich potreby
        self.allVisitors = []
        self.saveAllVisits()
        
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
<<<<<<< HEAD
    
    def removeVisitor(self, id):
        for vis in self.visitors:
            if vis.id == id:
                self.visitors.remove(vis)
        self.file.removeVisitor(id)

    def leftVisitor(self, id):
=======

    def departureVisitor(self, id):
>>>>>>> 7c92dbae7c46e3c7a5c4af6f31b2ccee1891f2c8
        for vis in self.visitors[:]:
            if vis.id == id:
                self.visitors.remove(vis)
                #vis.registerDeparture()        # zaznamenať odchod visitora tu alebo v GUI?  

    def generateId(self):  # TODO vygenerovanie unikátneho id pre každý zápis. Zatiaľ takto:
        return self.file.numOfLines

    def getVisitors(self):
        return self.visitors

    def isSimillar(self, partialString, correctString):
        partialStringCleaned = partialString.lower().translate(str.maketrans("", "", string.punctuation))
        correctStringCleaned = correctString.lower().translate(str.maketrans("", "", string.punctuation))
        close_matches = difflib.get_close_matches(partialStringCleaned, [correctStringCleaned], n=1, cutoff=0.8)
        if close_matches:
            return close_matches[0]
        else:
            return None


    def filter(self, dateFrom = None, dateTo = None, name = None, surname = None, company = None): 
        filteredList = self.allVisitors.copy()

        if dateFrom:
            filteredList = [visitor for visitor in filteredList if visitor.arrival >= dateFrom]
        if dateTo:
            filteredList = [visitor for visitor in filteredList if visitor.arrival <= dateTo]
        if name:
            filteredList = [visitor for visitor in filteredList if self.isSimillar(name, visitor.name) != None]
        if surname:
            filteredList = [visitor for visitor in filteredList if self.isSimillar(surname, visitor.surname) != None]
        if company:
            filteredList = [visitor for visitor in filteredList if self.isSimillar(company, visitor.company) != None]

        return filteredList


    def saveAllVisits(self):
        temp = self.file.readData()
        self.allVisitors.clear()
        for visit in temp:
            info = visit.strip().split(';')
            visitor = vis.Visitor(info[0], info[1], info[2], info[3], info[4], info[5], info[6], info[7], info[8], info[9], info[10], info[11])
            self.allVisitors.append(visitor)

# Example
m = Mediator()
# m.addVisitor('Nina', 'Mrkvickova', 1, 'BL000BS', 'Nic', 2, 2)
# m.addVisitor('Laura', 'Zemiakova', 1, 'KE999BS', 'Nieco', 1, 1)
# m.addVisitor('Peter', 'Zemiak', 1, 'DS111SD', 'StaleNic', 200, 3)
zoz = m.filter(None, None, None, "Zemiak")
for i in zoz:
    print(i.getDataToWrite())