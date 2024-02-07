import Visitor as vis
import CustomFile as cf
import difflib
import string
import unidecode
from Communication import Communication
from threading import Thread
from PIL import Image

OUTPUT_PATH = '../src/files/signatures' # TODO nastavnie správnej cesty pre ich potreby
FILE_PATH = '../src/files/testFile.csv'

class Mediator:
    def __init__(self):
        self.visitors = []      # TODO pridávanie neodhlásených z predošlého dňa
        self.file = cf.CustomFile(FILE_PATH)
        self.allVisitors = []
        self.saveAllVisits()
        try:
            self.communication = Communication()
        except:
            self.communication = None
             # TODO dať informáciu o nepripojenom zariadení
        
    def addVisitor(self, name, surname, cardId, carTag, company, count, reason):
        visitor = vis.Visitor(None, name, surname, cardId, carTag, company, count, reason)
        state = None
        #state = self.startPresentation(visitor)
        if state == "signature":
            self.file.writeVisitor(visitor.getDataToWrite())  # zapíše visitora do súboru
            self.allVisitors.append(visitor)
            self.visitors.append(visitor)
            return state
        return state
        

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
            for vis in self.allVisitors:
                if vis.getId() == id:
                    vis.edit(name, surname, cardId, carTag, company, count, reason)

    def departureVisitor(self, id):
        for vis in self.visitors[:]:
            if vis.id == id:
                self.visitors.remove(vis)
                vis.registerDeparture(vis)
                self.startReview(vis)
                self.updateAllVisitors(id)
                break

    def updateAllVisitors(self, id):
        for vis in self.allVisitors:
            if vis.getId() == id:
                vis.setDepartureInfo(*vis.getDepartureInfo())
                break

    def getVisitors(self):
        return self.visitors

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

    def startPresentation(self, visitor):
        # Cakaj odpovede z prezentacia a reaguj na to, ked je koniec tak toto cele skonci
        # v state, data budu ulezene vsetky info
        state, data = self.communication.send_start_presentation(visitor)
        while state == Communication.message_code["progress"]:
            state_data_result = []
            thread = Thread(target=self.communication.recieve, args=(state_data_result,))
            thread.start()
            while not state_data_result:
                self.update()
            state, data = tuple(state_data_result)
            print(state, data)
            thread.join()
        
        if state == Communication.message_code["signature"]:
            ## data je PIL obrazok podpisu
            data.save(self.OUTPUT_PATH + str(visitor.getID()) + '.jpg')        #zapíše obrázok do súboru s ID visitora ako názov
        elif state == Communication.message_code["error"]:
            print(state)
        return state
    
    def startReview(self, visitor):
        state, data = self.communication.send_start_review(visitor)
        while state == Communication.message_code["progress"]:
            state_data_result = []
            thread = Thread(target=self.communication.recieve, args=(state_data_result,))
            thread.start()
            while not state_data_result:
                self.update()
            state, data = tuple(state_data_result)
            print(state, data)
            thread.join()

        if state == Communication.message_code["review"]:
            visitor.addReview(data)
            self.updateAllVisitors()
        elif state == Communication.message_code["error"]:
            print(state)
        return state

# Example
#m = Mediator()
#m.addVisitor('Lara', 'Taka', 1, 'BL000BS', 'Nic', 2, 2)
#findId = m.getVisitors()[5].getId()
#m.editVisitor(findId, "Sarah")
# zoz = m.filter(None, None, "ó")
# for i in zoz:
#     print(i.getDataToWrite())