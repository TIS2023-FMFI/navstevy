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
    
    def removeVisitor(self, id):
        for vis in self.visitors:
            if vis.id == id:
                self.visitors.remove(vis)
        # self.file.removeVisitor(id)        #ak chceme aby fungovalo treba zmeniť systém ID

    def leftVisitor(self, id):
        for vis in self.visitors[:]:
            if vis.id == id:
                self.visitors.remove(vis)
                #vis.registerDeparture()        # zaznamenať odchod vo visitorovi tu alebo v GUI

    def generateId(self):  # TODO vygenerovanie unikátneho id pre každý zápis. Zatiaľ takto:
        return self.file.numOfLines

    def getVisitors(self):
        return self.visitors
    
    def filterOngoing(self, sortBy, sortDesc=False, dateFrom=None, name=None, surname=None, company=None):
        filteredList = self.visitors

        if dateFrom:
            filteredList = [visitor for visitor in filteredList if visitor.date >= dateFrom]
        if name:
            filteredList = [visitor for visitor in filteredList if visitor.name == name]
        if surname:
            filteredList = [visitor for visitor in filteredList if visitor.surname == surname]
        if company:
            filteredList = [visitor for visitor in filteredList if visitor.company == company]

        if sortBy == 'name':   
            filteredList = sorted(filteredList, key=lambda visitor: visitor.name)
        elif sortBy == 'surname':
            filteredList = sorted(filteredList, key=lambda visitor: visitor.surname)
        elif sortBy == 'dateFrom':
            filteredList = sorted(filteredList, key=lambda visitor: visitor.dateFrom)
        elif sortBy == 'dateTo':  
            filteredList = sorted(filteredList, key=lambda visitor: visitor.dateTo)
        elif sortBy == 'company': 
            filteredList = sorted(filteredList, key=lambda visitor: visitor.surname)

        if sortDesc:
            filteredList.reverse()

        return filteredList

    def filterAll(self, sortBy, sortDesc=False, dateFrom = None, dateTo = None, name = None, surname = None, company = None, reason = None, review=None): 
        filteredList = self.allVisitors

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
        if reason:
            filteredList = [visitor for visitor in filteredList if visitor.reason == reason]
        if review:
            filteredList = [visitor for visitor in filteredList if visitor.review == review]

        if sortBy == 'name':   
            filteredList = sorted(filteredList, key=lambda visitor: visitor.name)
        elif sortBy == 'surname':
            filteredList = sorted(filteredList, key=lambda visitor: visitor.surname)
        elif sortBy == 'dateFrom':
            filteredList = sorted(filteredList, key=lambda visitor: visitor.dateFrom)
        elif sortBy == 'dateTo':  
            filteredList = sorted(filteredList, key=lambda visitor: visitor.dateTo)
        elif sortBy == 'company': 
            filteredList = sorted(filteredList, key=lambda visitor: visitor.surname)
        elif sortBy == 'reason': 
            filteredList = sorted(filteredList, key=lambda visitor: visitor.reason)
        elif sortBy == 'review': 
            filteredList = sorted(filteredList, key=lambda visitor: visitor.review)

        if sortDesc:
            filteredList.reverse()

        return filteredList

    def saveAllVisits(self):                   
            temp = self.file.readData()
            self.allVisitors.clear()
            for visit in temp:
                info = visit.strip().split(';')
                cleanedInfo = [value if value != '' else None for value in info]
                visitor = vis.Visitor(*cleanedInfo)
                if None in cleanedInfo:
                    self.visitors.append(visitor)
                self.allVisitors.append(visitor)
            

        

# Example
m = Mediator()
m.addVisitor('Nina', 'Mrkvickova', 1, 'BL000BS', 'Nic', 2, 'AAAAAA')
m.addVisitor('Laura', 'Zemiakova', 1, 'KE999BS', 'Nieco', 1, '111111')
m.addVisitor('Peter', 'Zemiak', 1, 'DS111SD', 'StaleNic', 200,'2222222')
m.removeVisitor(1)