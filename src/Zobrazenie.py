import tkinter as tk

class Zobrazenie:
    def __init__(self, width, height):
        self.__root = tk.Tk(width, height)
        self.__visitting = False

    def show(self, name):
        ...
    
    def popUp(self, name):
        ...

    def getOngoingVisit(self):
        return self.__visitting
    
    def setOngoingVisit(self, bollean):
        if bollean:
            self.__visitting = True
        else: 
            self.__visitting = False
    
    def getRoot(self):
        return self.__root

