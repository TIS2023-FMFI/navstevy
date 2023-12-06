import customtkinter as ctk
import Mediator as med
LARGE_FONT = ("times new roman", 12)


class MainScreen(ctk.CTk):
    def __init__(self):
        ctk.CTk.__init__(self)
        self.geometry("1200x600")
        self.width = 1200
        self.height = 600

        self.minsize(500, 500)


        self.container = ctk.CTkFrame(self)
        self.container.pack(side="top", fill="both", expand = True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (MainMenu, Entry, Ongoing, Visit_History):

            frame = F(self.container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainMenu)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.configure(width=1000, height=1000)
        frame.tkraise()
        self.current_frame = cont

    def resize(self):
        self.width = self.winfo_width()
        self.height = self.winfo_screenheight()
        self.show_frame(self.current_frame)



class MainMenu(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)

        label = ctk.CTkLabel(self, text="Uvod", font=LARGE_FONT)
        label.place(relx=0.5, rely=0.1)

        button = ctk.CTkButton(self, text="Prichod", command=lambda: controller.show_frame(Entry))
        button.place(relx=0.5, rely=0.3)

        button2 = ctk.CTkButton(self, text="Prebiehajuce", command=lambda: controller.show_frame(Ongoing))
        button2.place(relx=0.5, rely=0.4)

        button3 = ctk.CTkButton(self, text="Historia", command=lambda: controller.show_frame(Visit_History))
        button3.place(relx=0.5, rely=0.5, )

class Entry(ctk.CTkFrame):
    def __init__(self, parent, controller):
        self.controller = controller
        self.parent = parent
        ctk.CTkFrame.__init__(self, parent)


        label = ctk.CTkLabel(self, text="Zapis Navstevy", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button = ctk.CTkButton(self, text="Naspat", command=lambda: self.goBack())
        button.pack()

        submit = ctk.CTkButton(self, text="Spustit prezentaciu", command=lambda: self.saveInfo())
        submit.pack()


        self.name = ctk.CTkEntry(self, placeholder_text="meno")
        self.name.pack()

        self.surname= ctk.CTkEntry(self, placeholder_text="priezvisko")
        self.surname.pack()
        self.card_id = ctk.CTkEntry(self, placeholder_text="id")
        self.card_id.pack()
        self.car_num = ctk.CTkEntry(self, placeholder_text="spz")
        self.car_num.pack()
        self.company = ctk.CTkEntry(self, placeholder_text="firma")
        self.company.pack()
        self.group_size = ctk.CTkEntry(self, placeholder_text="pocet ludi v skupine")
        self.group_size.pack()

        '''pridat tlacidlo na pridanie moznosti'''

        self.options = [
            "navsteva manazera",
            "audit",
            "instalacia",
            "oprava zariadeni"



        ]

        self.visit_reason = ctk.CTkOptionMenu(master=self, values=self.options)
        self.visit_reason.pack()
    def goBack(self):
        self.clearEntry()
        self.controller.show_frame(MainMenu)

    def clearEntry(self):
        self.name.delete(0, 'end')
        self.name.configure(fg_color='#343638')
        self.surname.delete(0, 'end')
        self.surname.configure(fg_color='#343638')
        self.card_id.delete(0, 'end')
        self.card_id.configure(fg_color='#343638')
        self.car_num.delete(0, 'end')
        self.car_num.configure(fg_color='#343638')
        self.company.delete(0, 'end')
        self.company.configure(fg_color='#343638')
        self.group_size.delete(0, 'end')
        self.group_size.configure(fg_color='#343638')
        self.visit_reason.set(self.options[0])

    def saveInfo(self):
        if self.checkInfo():
            m.addVisitor(self.name,self.surname, self.card_id, self.car_num,self.company, self.group_size, self.visit_reason)

    def badEngtry(self,entry):
        entry.configure(fg_color='red')

    def isInt(self,entry):
        try:
            int(self.group_size.get())
            return True
        except ValueError:
            return False

    def checkInfo(self):
        flag = True

        if(self.name.get() == ''):
            flag = False
            self.badEngtry(self.name)

        if (self.surname.get() == ''):
            flag = False
            self.badEngtry(self.surname)

        if (self.card_id.get() == ''):
            flag = False
            self.badEngtry(self.card_id)

        if not (self.isInt(self.card_id)):
            flag = False
            self.badEngtry(self.card_id)

        if (self.car_num.get() == ''):
            flag = False
            self.badEngtry(self.car_num)

        if (self.company.get() == ''):
            flag = False
            self.badEngtry(self.company)

        if (self.group_size.get() == ''):
            flag = False
            self.badEngtry(self.group_size)

        if not(self.isInt(self.group_size)):
            flag = False
            self.badEngtry(self.group_size)

        return flag

class Ongoing(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        label = ctk.CTkLabel(self, text="Prebiehajuce Navstevy", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button = ctk.CTkButton(self, text="Naspat", command=lambda: controller.show_frame(MainMenu))
        button.pack()


class Visit_History(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        label = ctk.CTkLabel(self, text="Historia Navstev", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button = ctk.CTkButton(self, text="Back", command=lambda: controller.show_frame(MainMenu))
        button.pack()

m = med.Mediator()
app = MainScreen()
app.mainloop()