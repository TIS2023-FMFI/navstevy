import Visitor as vis
import CustomFile as cf
import difflib
import string
import unidecode
from Communication import Communication
from threading import Thread
from PIL import Image

OUTPUT_PATH = 'files/signatures/' # TODO nastavnie správnej cesty pre ich potreby
FILE_PATH = 'files/testFile.csv'

class Mediator:
    def __init__(self):
        self.visitors = []      # TODO pridávanie neodhlásených z predošlého dňa
        self.file = cf.CustomFile(FILE_PATH)
        self.allVisitors = []
        self.saveAllVisits()
        self.communication = Communication()

        
    def addVisitor(self, controlFrame, name, surname, cardId, carTag, company, count, reason):
        visitor = vis.Visitor(None, name, surname, cardId, carTag, company, count, reason)
        state, data = self.startPresentation(visitor, controlFrame)

        if state == Communication.message_code["signature"]:
            ## data je PIL image
            data.save(OUTPUT_PATH + visitor.getSignatureFileName())  
            self.file.writeVisitor(visitor.getDataToWrite())  # zapíše visitora do súboru
            self.allVisitors.append(visitor)
            self.visitors.append(visitor)
        return state, data
        
    def editVisitor(self, id, name=None, surname=None, cardId=None, carTag=None, company=None, count=None, reason=None):
        for vis in self.visitors:
            if vis.getId() == id:
                vis.edit(name, surname, cardId, carTag, company, count, reason)
                self.file.edit(id, vis)
                break

        for vis in self.allVisitors:
            if vis.getId() == id:
                vis.edit(name, surname, cardId, carTag, company, count, reason)
                break


    def departureVisitor(self, id, controlFrame):
        for vis in self.visitors[:]:
            if vis.getId() == id:
                self.visitors.remove(vis)
                vis.registerDeparture()
                state, data = self.startReview(vis, controlFrame)
                if state == Communication.message_code["rating"]:
                    vis.addReview(data)
                self.file.edit(vis.getId(), vis)
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

    def startPresentation(self, visitor: vis.Visitor, controlFrame):
        # Cakaj odpovede z prezentacia a reaguj na to, ked je koniec tak toto cele skonci
        # v state, data budu ulezene vsetky info
        state, data = self.communication.send_start_presentation(visitor)
        self.restart_signal = False
        while state == Communication.message_code["progress"]:
            
            if data is not None:
                controlFrame.showProgress(data)
            
            state_data_result = []
            thread = Thread(target=self.communication.recieve, args=(state_data_result,))
            thread.start()
            while not state_data_result:
                controlFrame.update()
            state, data = tuple(state_data_result)
            thread.join()
            
        return state, data
    
    def startReview(self, visitor, controlFrame):
        state, data = self.communication.send_start_review(visitor)
        self.restart_signal = False
        while state == Communication.message_code["progress"]:
            state_data_result = []
            thread = Thread(target=self.communication.recieve, args=(state_data_result,))
            thread.start()
            while not state_data_result:
                controlFrame.update()
            state, data = tuple(state_data_result)
            thread.join()

        return state, data

    def endPresentation(self):
        self.communication.send_end_presentation()

if __name__ == "__main__": 
    m = Mediator()
    m.addVisitor('Lara', 'Taka', 1, 'BL000BS', 'Nic', 2, 2)
    findId = m.getVisitors()[5].getId()
    m.editVisitor(findId, "Sarah")
    zoz = m.filter(None, None, "ó")
    for i in zoz:
        print(i.getDataToWrite())