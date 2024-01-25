import Visitor as vis
import CustomFile as cf

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

    def departureVisitor(self, id):
        for vis in self.visitors[:]:
            if vis.id == id:
                self.visitors.remove(vis)
                #vis.registerDeparture()        # zaznamenať odchod visitora tu alebo v GUI?  

    def generateId(self):  # TODO vygenerovanie unikátneho id pre každý zápis. Zatiaľ takto:
        return self.file.numOfLines

    def getVisitors(self):
        return self.visitors

    def filter(self, sortBy, sortDesc=False, dateFrom = None, dateTo = None, name = None, surname = None, company = None, review=None): 
        filteredList = self.allVisitors.copy()

        if dateFrom:
            filteredList = [visitor for visitor in filteredList if visitor.arrival >= dateFrom]
        if dateTo:
            filteredList = [visitor for visitor in filteredList if visitor.arrival <= dateTo]
        if name:
            filteredList = [visitor for visitor in filteredList if visitor.name == name]
        if surname:
            filteredList = [visitor for visitor in filteredList if visitor.surname == surname]
        if company:
            filteredList = [visitor for visitor in filteredList if visitor.company == company]
        # if reason:
        #     filteredList = [visitor for visitor in filteredList if visitor.reason == reason]
        if review:
            filteredList = [visitor for visitor in filteredList if visitor.review == review]

        return filteredList

    def sort(self, sortBy, sortDesc=False):
        sortedList = self.allVisitors.copy()
        if sortBy == 'name':   
            filteredList = sorted(sortedList, key=lambda visitor: visitor.name)
        elif sortBy == 'surname':
            filteredList = sorted(sortedList, key=lambda visitor: visitor.surname)
        elif sortBy == 'dateFrom':
            filteredList = sorted(sortedList, key=lambda visitor: visitor.dateFrom)
        elif sortBy == 'dateTo':  
            filteredList = sorted(sortedList, key=lambda visitor: visitor.dateTo)
        elif sortBy == 'company': 
            filteredList = sorted(sortedList, key=lambda visitor: visitor.surname)
        elif sortBy == 'reason': 
            filteredList = sorted(sortedList, key=lambda visitor: visitor.reason)
        elif sortBy == 'cardId': 
            filteredList = sorted(sortedList, key=lambda visitor: visitor.cardId)
        elif sortBy == 'carId': 
            filteredList = sorted(sortedList, key=lambda visitor: visitor.cardId)

        if sortDesc:
            filteredList.reverse()

    def saveAllVisits(self):
        temp = self.file.readData()
        self.allVisitors.clear()
        for visit in temp:
            info = visit.strip().split(';')
            visitor = vis.Visitor(info[0], info[1], info[2], info[3], info[4], info[5], info[6], info[7], info[8], info[9], info[10], info[11])
            self.allVisitors.append(visitor)
            

        

# Example
m = Mediator()
m.addVisitor('Nina', 'Mrkvickova', 1, 'BL000BS', 'Nic', 2)
m.addVisitor('Laura', 'Zemiakova', 1, 'KE999BS', 'Nieco', 1)
m.addVisitor('Peter', 'Zemiak', 1, 'DS111SD', 'StaleNic', 200)