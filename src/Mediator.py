import Visitor as vis
import CustomFile as cf
import difflib
import string
import unidecode
from Communication import Communication
from threading import Thread
from PIL import Image

class Mediator:
    OUTPUT_PATH = 'src/files/signatures' # TODO nastavnie správnej cesty pre ich potreby
    def __init__(self):
        self.visitors = []      # TODO pridávanie neodhlásených z predošlého dňa
        self.file = cf.CustomFile('src/files/testFile.csv')  # TODO nastavnie správnej cesty pre ich potreby
        self.allVisitors = []
        self.leftWaitingForReview = []
        self.saveAllVisits()
        try:
            self.communication = Communication()
        except:
            self.communication = None
             # TODO dať informáciu o nepripojenom zariadení
        
    def addVisitor(self, name, surname, cardId, carTag, company, count, reason):
        visitor = vis.Visitor(None, name, surname, cardId, carTag, company, count, reason)
        state = self.startPresentation(visitor)
        if state == "signature":
            self.file.writeVisitor(visitor.getDataToWrite())  # zapíše visitora do súboru
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

    def departureVisitor(self, id):
        for vis in self.visitors[:]:
            if vis.id == id:
                self.visitors.remove(vis)
                self.leftWaitingForReview.append(vis)
                vis.registerDeparture(vis)      

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

    def startPresentation(self, temporaryVisitor):
        # Cakaj odpovede z prezentacia a reaguj na to, ked je koniec tak toto cele skonci
        # v state, data budu ulezene vsetky info
        state, data = self.communication.send_start_presentation(temporaryVisitor)
        while state == Communication.message_code["progress"]:
            state_data_result = []
            thread = Thread(target=self.communication.recieve, args=(state_data_result,))
            thread.start()
            while not state_data_result:
                self.update()
            state, data = tuple(state_data_result)
            print(state, data)
            thread.join()
        
        if state == Communication.message_code["wrong_data"]:
            return "wrong_data"
        elif state == Communication.message_code["signature"]:
            ## data je PIL obrazok podpisu
            data.save(self.OUTPUT_PATH + str(temporaryVisitor.getID()) + '.jpg')        #zapíše obrázok do súboru s ID visitora ako názov
            return "signature"
        elif state == Communication.message_code["error"]:
            print("Connection error...")
            return "error"
# Example
# m = Mediator()
# m.addVisitor('Lara', 'Taka', 1, 'BL000BS', 'Nic', 2, 2)
# findId = m.getVisitors()[5].getId()
# m.editVisitor(findId, "Sarah")
# m.addVisitor('Laura', 'Zemiakova', 1, 'KE999BS', 'Nieco', 1, 1)
# m.addVisitor('Peter', 'Zemiak', 1, 'DS111SD', 'StaleNic', 200, 3)
# zoz = m.filter(None, None, "ó")
# for i in zoz:
#     print(i.getDataToWrite())