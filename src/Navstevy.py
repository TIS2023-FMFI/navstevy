class Navstevy:
    def __init__(self, id, name, surname, cardId, company, arrival = None, departure = None, signature = None, review = None):
        self.__id = id
        self.name = name
        self.surname = surname
        self.cardId = cardId
        self.company = company
        self.arrival = arrival
        self.departure = departure
        self.signature = signature
        self.review = review

    def getId(self):
        return self.__id

    def setId(self,id):
        self.__id = id