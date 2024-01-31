import Visitor as vis
import CustomFile as cf
import difflib
import string
import unidecode
from Communication import Communication

class Mediator:
    def __init__(self):
        self.visitors = []      # TODO pridávanie neodhlásených z predošlého dňa
        self.file = cf.CustomFile('../src/files/testFile.csv')  # TODO nastavnie správnej cesty pre ich potreby
        self.allVisitors = []
        self.saveAllVisits()
        try:
            self.communication = Communication()
        except:
            self.communication = None
        
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
                vis.registerDeparture(vis)      

    def generateId(self):  # TODO vygenerovanie unikátneho id pre každý zápis. Zatiaľ takto:
        return self.file.numOfLines

    def getVisitors(self):
        return self.visitors

    def isSimillar(self, partialString, correctString):             #not using
        partialStringCleaned = partialString.lower().translate(str.maketrans("", "", string.punctuation))
        correctStringCleaned = correctString.lower().translate(str.maketrans("", "", string.punctuation))
        close_matches = difflib.get_close_matches(partialStringCleaned, [correctStringCleaned], n=1, cutoff=0.8)
        if close_matches:
            return close_matches[0]
        else:
            return None

    def contains(self, partialString, correctString):
        partialStringCleaned = unidecode.unidecode(partialString.lower().translate(str.maketrans("", "", string.punctuation)))
        correctStringCleaned = unidecode.unidecode(correctString.lower().translate(str.maketrans("", "", string.punctuation)))
        if partialStringCleaned in correctStringCleaned:
            return True
        return False


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
            filteredList = [visitor for visitor in filteredList if self.contains(name, visitor.name) == True]
        if surname:
            surname = surname.strip()
            if surname == "":
                surname = None
            filteredList = [visitor for visitor in filteredList if self.contains(surname, visitor.surname) == True]
        if company:
            company = company.strip()
            if company == "":
                company = None
            filteredList = [visitor for visitor in filteredList if self.contains(company, visitor.company) == True]
        return filteredList


    def saveAllVisits(self):
        temp = self.file.readData()
        self.allVisitors.clear()
        for visit in temp:
            info = visit.strip().split(';')
            infoCleaned = [value if value != '' else None for value in info]
            infoCleaned[0] = int(infoCleaned[0])
            visitor = vis.Visitor(*infoCleaned)
            if (visitor.departure == None):
                self.visitors.append(visitor)
            self.allVisitors.append(visitor)

# Example
# m = Mediator()
# m.addVisitor('Nina', 'Mrkvickova', 1, 'BL000BS', 'Nic', 2, 2)
# m.addVisitor('Laura', 'Zemiakova', 1, 'KE999BS', 'Nieco', 1, 1)
# m.addVisitor('Peter', 'Zemiak', 1, 'DS111SD', 'StaleNic', 200, 3)
# zoz = m.filter(None, None, "ó")
# for i in zoz:
#     print(i.getDataToWrite())