from datetime import datetime

class Visitor:
    def __init__(self, id, name, surname, cardId, carTag, company, count, reason, arrival=None, departure=None, signature=None, review=None):
        date = datetime.now()
        if id is None:
            self.id = self.generateId(date)
        else: 
            self.id = id
        self.name = name
        self.surname = surname
        self.cardId = cardId
        self.carTag = carTag
        self.company = company
        self.count = count
        self.reasonOfVisit = reason
        self.arrival = arrival if arrival is not None else date.strftime("%d-%m-%Y %H:%M")    #formátovanie času deň-mesiac-rok hodina:minúta
        self.departure = departure
        self.review = review                    #zmení sa po prijatí spravy od komunikácie

    def generateId(self, date):
        id = str(date.year)[2:] + str(date.month) + str(date.day) + str(date.minute) + str(date.second)
        return int(id)

    def getId(self):
        return self.id
    
    def getDataToWrite(self):
        data_string = f"{self.id};{self.name};{self.surname};{self.cardId};{self.carTag};{self.company};{self.count};{self.reasonOfVisit};{self.arrival}"
        # pridaj departure, signature, and review ak bude dostupné
        if self.departure:
            data_string += f";{self.departure}"
        else:
            data_string += ";"
        if self.review:
            data_string += f";{self.review}"
        else:
            data_string += ";\n"
        return data_string

    def registerDeparture(self):
        self.departure = datetime.now().strftime("%d-%m-%Y %H:%M")

    def edit(self, name = None, surname = None, cardId = None, carTag = None, company = None, count = None, reason = None):
        if name is not None:
            self.name = name
        if surname is not None:
            self.surname = surname
        if cardId is not None:
            self.cardId = cardId
        if carTag is not None:
            self.carTag = carTag
        if company is not None:
            self.company = company
        if count is not None:
            self.count = count
        if reason is not None:
            self.reasonOfVisit = reason

    def addReview(self, review):
        self.review = review

    def getDepartureInfo(self): 
        return self.departure, self.review
    
    def setDepartureInfo(self, departure = None, review = None):
        if departure:
            self.departure = departure
        if review:
            self.review = review