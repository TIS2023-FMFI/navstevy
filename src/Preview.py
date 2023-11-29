import tkinter as tk

class Preview:
    def __init__(self, width, height):
        tk.Tk.__init__(self)
        
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


