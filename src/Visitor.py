from datetime import datetime

class Visitor:
    def __init__(self, id, name, surname, cardId, carTag, company, count, reason, arrival=None, departure=None, signature=None, review=None):
        self.id = id
        self.name = name
        self.surname = surname
        self.cardId = cardId
        self.carTag = carTag
        self.company = company
        self.count = count
        self.reasonOfVisit = reason
        self.arrival = arrival if arrival is not None else datetime.now().strftime("%d-%m-%Y %H:%M")    #formátovanie času deň-mesiac-rok hodina:minúta
        self.departure = departure
        self.signature = signature
        self.review = review                    #zmení sa po prijatí spravy od komunikácie

    def getId(self):
        return self.id
    
    def getDataToWrite(self):
        data_string = f"{self.id};{self.name};{self.surname};{self.cardId};{self.carTag};{self.company};{self.count};{self.reasonOfVisit};{self.arrival}"
        
        # pridaj departure, signature, and review ak bude dostupné
        if self.departure:
            data_string += f";{self.departure}"
        else:
            data_string += ";"
        if self.signature:
            data_string += f";{self.signature}"
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
    
    def removeVisitor(self, id):
        with open(self.path, "a+") as file:
            file.seek(0)
            lines = file.readlines()
            if 1 <= id <= len(lines):
                lines[id] = ""      #id je zatiaľ rovnaké ako pozícia riadku v texte
                self.numOfLines -= 1
                with open(self.path, 'w') as file:
                    file.seek(0)
                    file.writelines(lines)
                file.close()
                print(f"Line {id} deleted successfully.")
            else:
                print("Invalid line number.")
        file.close()