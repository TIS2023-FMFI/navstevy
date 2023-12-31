import customtkinter as ctk
LARGE_FONT = ("Verdana", 12)
BASE_FG_COLOR = '#343638'
'''
Tak ako aj v tkinter aj customtkinter pouziva tie iste buttons labels...
jediny rozdiel ze su nazvate CTkButton, CTkLabel ... 
'''
class MainScreen(ctk.CTk):
    def __init__(self):
        ctk.CTk.__init__(self)
        self.geometry("1200x600")
        self.minsize(500, 500)

        self.container = ctk.CTkFrame(self)
        self.container.pack(side="top", fill="both", expand = True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (Uvod, Prichod,Prebiehajuce,Historia):

            frame = F(self.container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Uvod)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.configure(width=1000, height=1000)
        frame.tkraise()


'''This are gonna be the classes that will have the buttons and functions that will change the screen and create popups'''
class Uvod(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)

        label = ctk.CTkLabel(self, text="Uvod", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button = ctk.CTkButton(self, text="Prichod", command=lambda: controller.show_frame(Prichod))
        button.pack()

        button2 = ctk.CTkButton(self, text="Prebiehajuce", command=lambda: controller.show_frame(Prebiehajuce))
        button2.pack()

        button3 = ctk.CTkButton(self, text="Historia", command=lambda: controller.show_frame(Historia))
        button3.pack()

class Prichod(ctk.CTkFrame):
    def __init__(self, parent, controller):
        self.controller = controller
        self.parent = parent
        ctk.CTkFrame.__init__(self, parent)
        label = ctk.CTkLabel(self, text="Prichod", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button = ctk.CTkButton(self, text="Back", command=lambda: controller.show_frame(Uvod))
        button.pack()

        submit = ctk.CTkButton(self, text="Submit", command=lambda: self.getInfo())
        submit.pack()

        '''placeholder_text je inicialny text ktory sa prepise'''
        self.meno = ctk.CTkEntry(self, placeholder_text="meno")
        self.meno.pack()

        self.priezvisko = ctk.CTkEntry(self, placeholder_text="priezvisko")
        self.priezvisko.pack()
        self.id = ctk.CTkEntry(self, placeholder_text="id")
        self.id.pack()
        self.spz = ctk.CTkEntry(self, placeholder_text="spz")
        self.spz.pack()
        self.firma = ctk.CTkEntry(self, placeholder_text="firma")
        self.firma.pack()
        self.pocet = ctk.CTkEntry(self, placeholder_text="pocet")
        self.pocet.pack()

        options = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday"
        ]
        '''optionmenu je dropdown menu 
            do value sa vkladaju moznosti ako zoznam
        '''
        self.dovod = ctk.CTkOptionMenu(master=self, values=options)
        self.dovod.pack()

    def isNumber(self, n):
        try:
            int(n)
            return True
        except ValueError:
            return False

    def getInfo(self):
        if self.isNumber(self.pocet.get()):
            self.controller.show_frame(Uvod)
            self.meno.delete(0, 'end')
            self.priezvisko.delete(0, 'end')
            self.id.delete(0, 'end')
            self.firma.delete(0, 'end')
            self.spz.delete(0, 'end')
            self.pocet.delete(0, 'end')
            self.pocet.configure(fg_color=BASE_FG_COLOR)
            self.dovod.set("Monday")
        else:
            self.pocet.delete(0, 'end')
            print(self.pocet.cget("fg_color"))
            self.pocet.configure(fg_color="red")


class Prebiehajuce(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        label = ctk.CTkLabel(self, text="Prebiehajuce", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button = ctk.CTkButton(self, text="Back", command=lambda: controller.show_frame(Uvod))
        button.pack()

class Historia(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        label = ctk.CTkLabel(self, text="Historia", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button = ctk.CTkButton(self, text="Back", command=lambda: controller.show_frame(Uvod))
        button.pack()


app = MainScreen()
app.mainloop()

