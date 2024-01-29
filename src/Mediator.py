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

    def departureVisitor(self, id, review):
        for vis in self.visitors[:]:
            if vis.id == id:
                self.visitors.remove(vis)
                vis.registerDeparture(vis, review)      

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
            dateFrom = dateFrom.strip()
            if dateFrom == "":
                dateFrom = None
            filteredList = [visitor for visitor in filteredList if visitor.arrival >= dateFrom]
        if dateTo:
            dateTo = dateTo.strip()
            if dateTo == "":
                dateTo = None
            filteredList = [visitor for visitor in filteredList if visitor.arrival <= dateTo]
        if name:
            name = name.strip()
            if name == "":
                name = None
            filteredList = [visitor for visitor in filteredList if self.isSimillar(name, visitor.name) != None]
        if surname:
            surname = surname.strip()
            if surname == "":
                surname = None
            filteredList = [visitor for visitor in filteredList if self.isSimillar(surname, visitor.surname) != None]
        if company:
            company = company.strip()
            if company == "":
                company = None
            filteredList = [visitor for visitor in filteredList if self.isSimillar(company, visitor.company) != None]
        return filteredList


    def saveAllVisits(self):
        temp = self.file.readData()
        self.allVisitors.clear()
        for visit in temp:
            info = visit.strip().split(';')
            infoCleaned = [value if value != '' else None for value in info]
            visitor = vis.Visitor(*infoCleaned)
            if (visitor.departure == None):
                self.visitors.append(visitor)
            self.allVisitors.append(visitor)

# Example
m = Mediator()
# m.addVisitor('Nina', 'Mrkvickova', 1, 'BL000BS', 'Nic', 2, 2)
# m.addVisitor('Laura', 'Zemiakova', 1, 'KE999BS', 'Nieco', 1, 1)
# m.addVisitor('Peter', 'Zemiak', 1, 'DS111SD', 'StaleNic', 200, 3)
# zoz = m.filter(None, None, "Nina")
# for i in zoz:
#     print(i.getDataToWrite())