import tkinter as tk

class Zobrazenie:
    def __init__(self, width, height):
        tk.Tk.__init__(self)
        tk.Tk.configure(self, width=width, height=height)    
        self.container = tk.Frame(self)
        self.visitting = False

    def show(self, name):
        ...
    
    def popUp(self, name):
        ...

    def getOngoingVisit(self):
        return self.visitting
    
    def setOngoingVisit(self, bollean):
        if bollean:
            self.visitting = True
        else: 
            self.visitting = False


