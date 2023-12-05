import customtkinter as ctk
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

        button = ctk.CTkButton(self, text="Naspat", command=lambda: controller.show_frame(MainMenu))
        button.pack()

        submit = ctk.CTkButton(self, text="Spustit prezentaciu", command=lambda: self.saveInfo())
        submit.pack()


        self.name = ctk.CTkEntry(self, placeholder_text="meno")
        self.name.pack()

        self.surname= ctk.CTkEntry(self, placeholder_text="priezvisko")
        self.surname.pack()
        self.id = ctk.CTkEntry(self, placeholder_text="id")
        self.id.pack()
        self.car_num = ctk.CTkEntry(self, placeholder_text="spz")
        self.car_num.pack()
        self.company = ctk.CTkEntry(self, placeholder_text="firma")
        self.company.pack()
        self.group_size = ctk.CTkEntry(self, placeholder_text="pocet ludi v skupine")
        self.group_size.pack()

        '''pridat tlacidlo na pridanie moznosti'''

        options = [
            "navsteva",
            "inspekcia",
            "donaska"
        ]

        self.visit_reason = ctk.CTkOptionMenu(master=self, values=options)
        self.visit_reason.pack()

    def saveInfo(self):
        if self.checkInfo():
            ...


    def checkInfo(self):
        ...


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

app = MainScreen()
app.mainloop()