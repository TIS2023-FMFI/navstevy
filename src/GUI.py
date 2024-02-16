import customtkinter as ctk
import Mediator as med
import CTkTable as t
from Communication import Communication
from PIL import Image

BASE_FG_COLOR = '#343638'
LARGE_FONT = ("times new roman", 18)
VERY_LARGE_FONT = ("times new roman", 32)
ICONS_PATH = 'files/icons/'
ASC = "\u25B3"
DESC = "\u25BD"

class MainScreen(ctk.CTk):
    def __init__(self, mediator):
        ctk.CTk.__init__(self)
        self.iconbitmap(ICONS_PATH + "icon.ico")
        self.title("Evidencia návštev")
        self.protocol("WM_DELETE_WINDOW", self.close_app)

        self.geometry("1200x620")
        self.mediator = mediator
        

        self.minsize(620, 620)

        self.container = ctk.CTkFrame(self)
        self.container.pack(side="top", fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.options = self.mediator.loadOptions()

        self.frames = {}

        for F in (MainMenu, Entry, Ongoing, Visit_History, Edit, Control):
            frame = F(self.container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainMenu)
        if self.mediator.file.fileLoaded == False:
            popup = ctk.CTkToplevel(self)
            popup.protocol("WM_DELETE_WINDOW", self.close_app)
            popup.title("Nastal problém!")
            popup.geometry("500x300")
            popup.grab_set()
            label = ctk.CTkLabel(popup, text="Nepodarilo sa načítať súbor s návštevami.\nPri obnove súboru postupejte prosím podľa manuálu.", font=LARGE_FONT, text_color="red")
            label.place(relx=0.13, rely=0.40)

    def close_app(self):
        self.destroy()
        self.mediator.communication.close()
        exit()

    def show_frame(self, cont):
        if cont == Edit:
            self.frames[Edit].enterVisitor()
        frame = self.frames[cont]
        frame.configure(width=1000, height=1000)
        frame.tkraise()
        self.current_frame = cont

    def update_tables(self):
        self.frames[Ongoing].update_table()
        self.frames[Visit_History].update_table()


class MainMenu(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        frame = ctk.CTkFrame(self,width=400,height=600)

        title = ctk.CTkLabel(frame, text="Úvod", font=VERY_LARGE_FONT)
        title.place(relx=0.4,rely=0.1)

        entry = ctk.CTkButton(frame, text="Príchod",font=LARGE_FONT,width=225,height=70, command=lambda: controller.show_frame(Entry))
        entry.place(relx=0.23, rely=0.3)

        ongoing = ctk.CTkButton(frame, text="Prebiehajúce návštevy",font=LARGE_FONT,width=225,height=70, command=lambda: controller.show_frame(Ongoing))
        ongoing.place(relx=0.23, rely=0.5)

        history = ctk.CTkButton(frame, text="História návštev",font=LARGE_FONT,width=225,height=70, command=lambda: controller.show_frame(Visit_History))
        history.place(relx=0.23, rely=0.7)

        self.error_application_image = ctk.CTkImage(Image.open(ICONS_PATH + "tablet_error.png"), None, (50, 50))
        self.error_cable_image = ctk.CTkImage(Image.open(ICONS_PATH + "connection_error.png"),  None, (50, 50))
        self.no_error_image = ctk.CTkImage(Image.new("RGBA", (50, 50), (0, 0, 0, 0)), None, (50, 50))

        self.error_cable = ctk.CTkLabel(self, text="", font=LARGE_FONT, image=self.error_cable_image)
        self.error_cable.place(relx=0, rely=0.8)

        self.error_application = ctk.CTkLabel(self, text="", font=LARGE_FONT, image=self.error_application_image)
        self.error_application.place(relx=0, rely=0.9)

        frame.grid(padx=10,pady=10)
        self.grid_rowconfigure(0,weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.show_connection_status()

    def show_connection_status(self):
        if not self.controller.mediator.communication.is_device_connected:
            self.error_cable.configure(True, image=self.error_cable_image)
        else:
            self.error_cable.configure(True, image=self.no_error_image)

        if not self.controller.mediator.communication.is_application_running:
            self.error_application.configure(True, image=self.error_application_image)
        else:
            self.error_application.configure(True, image=self.no_error_image)
        self.after(1000, self.show_connection_status)

class Entry(ctk.CTkFrame):
    def __init__(self, parent, controller):
        self.controller = controller
        ctk.CTkFrame.__init__(self, parent)

        frame = ctk.CTkFrame(self,width=600,height=600)

        title = ctk.CTkLabel(frame, text="Zápis návštevy", font=VERY_LARGE_FONT)
        title.place(relx=0.37,y=10)

        name_label = ctk.CTkLabel(frame, text="Meno:")
        name_label.place(x=210.5,y=75)
        self.name = ctk.CTkEntry(frame, placeholder_text="meno", width=150)
        self.name.place(x=260,y=75)

        lsurname = ctk.CTkLabel(frame, text="Priezvisko:")
        lsurname.place(x=185,y=110)
        self.surname = ctk.CTkEntry(frame, placeholder_text="priezvisko", width=150)
        self.surname.place(x=260,y=110)

        lcard_id = ctk.CTkLabel(frame, text="Id karty:")
        lcard_id.place(x=201.3,y=145)
        self.card_id = ctk.CTkEntry(frame, placeholder_text="id karty", width=150)
        self.card_id.place(x=260,y=145)

        lcar_num = ctk.CTkLabel(frame, text="Spz:")
        lcar_num.place(x=222,y=180)
        self.car_num = ctk.CTkEntry(frame, placeholder_text="spz", width=150)
        self.car_num.place(x=260,y=180)

        lcompany = ctk.CTkLabel(frame, text="Firma:")
        lcompany.place(x=210.5,y=215)
        self.company = ctk.CTkEntry(frame, placeholder_text="firma", width=150)
        self.company.place(x=260,y=215)

        lgroup_size = ctk.CTkLabel(frame, text="Počet ľudí:")
        lgroup_size.place(x=186.4,y=250)
        self.group_size = ctk.CTkEntry(frame, placeholder_text="počet ľudí v skupine", width=150)
        self.group_size.place(x=260,y=250)

        lvisit_reason = ctk.CTkLabel(frame, text="Dôvod návštevy:")
        lvisit_reason.place(x=154, y=285)
        self.visit_reason = ctk.CTkOptionMenu(frame, values=self.controller.options, width=150)
        self.visit_reason.place(x=260,y=285)

        addOption = ctk.CTkButton(frame, text="Upraviť dôvody", command=lambda: self.changeOptions(), width=150)
        addOption.place(x=425,y=285)

        submit = ctk.CTkButton(frame, text="Spustiť prezentáciu",height=40, command=lambda: self.save_info(), width=150)
        submit.place(x=130,y=500)

        back = ctk.CTkButton(frame, text="Naspäť",height=40, command=lambda: self.go_back(), width=150, fg_color="red", hover_color="darkred")
        back.place(x=320,y=500)

        self.error_application_image = ctk.CTkImage(Image.open(ICONS_PATH + "tablet_error.png"), None, (50, 50))
        self.error_cable_image = ctk.CTkImage(Image.open(ICONS_PATH + "connection_error.png"),  None, (50, 50))
        self.no_error_image = ctk.CTkImage(Image.new("RGBA", (50, 50), (0, 0, 0, 0)), None, (50, 50))

        self.error_cable = ctk.CTkLabel(self, text="", font=LARGE_FONT, image=self.error_cable_image)
        self.error_cable.place(relx=0, rely=0.8)

        self.error_application = ctk.CTkLabel(self, text="", font=LARGE_FONT, image=self.error_application_image)
        self.error_application.place(relx=0, rely=0.9)

        frame.grid(padx=10, pady=10)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.show_connection_status()

       
 
    def show_connection_status(self):
        if not self.controller.mediator.communication.is_device_connected:
            self.error_cable.configure(True, image=self.error_cable_image)
        else:
            self.error_cable.configure(True, image=self.no_error_image)

        if not self.controller.mediator.communication.is_application_running:
            self.error_application.configure(True, image=self.error_application_image)
        else:
            self.error_application.configure(True, image=self.no_error_image)
        self.after(1000, self.show_connection_status)

    def go_back(self):
        self.clear_entry()
        self.controller.show_frame(MainMenu)

    def clear_entry(self):
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
        self.visit_reason.set(self.controller.options[0])


    def save_info(self):
        if self.check_info():
            name = self.name.get()
            surname = self.surname.get()
            card_id = int(self.card_id.get())
            car_num = self.car_num.get()
            company = self.company.get()
            group_size = int(self.group_size.get())
            visit_reason = self.visit_reason.get()
            self.controller.show_frame(Control)
            self.controller.frames[Control].waitForPresentation(name, surname, card_id, car_num, company, group_size, visit_reason)

    def bad_entry(self, entry):
        entry.configure(fg_color='red')

    def good_entry(self, entry):
        entry.configure(fg_color='#343638')

    def is_int(self, entry):
        try:
            int(entry.get())
            return True
        except ValueError:
            return False

    def check_info(self):
        flag = True

        if (self.name.get() == ''):
            flag = False
            self.bad_entry(self.name)
        else:
            self.good_entry(self.name)

        if (self.surname.get() == ''):
            flag = False
            self.bad_entry(self.surname)
        else:
            self.good_entry(self.surname)

        if (self.card_id.get() == ''):
            flag = False
            self.bad_entry(self.card_id)
        if self.is_int(self.card_id):
            self.good_entry(self.card_id)
        else:
            flag = False
            self.bad_entry(self.card_id)

        if (self.car_num.get() == ''):
            flag = False
            self.bad_entry(self.car_num)
        else:
            self.good_entry(self.car_num)

        if (self.company.get() == ''):
            flag = False
            self.bad_entry(self.company)
        else:
            self.good_entry(self.company)

        if (self.group_size.get() == ''):
            flag = False
            self.bad_entry(self.group_size)
        elif not (self.is_int(self.group_size)):
            flag = False
            self.bad_entry(self.group_size)
        else:
            self.good_entry(self.group_size)

        return flag
    
    def changeOptions(self):
        def go_back():
            self.controller.frames[Entry].visit_reason.configure(values=self.controller.options)
            self.controller.frames[Entry].visit_reason.set(self.controller.options[0])
            visitReasonPop.configure(values=self.controller.options)
            visitReasonPop.set(self.controller.options[0])
            popup.destroy()
        def delete_option():
            self.controller.options.remove(visitReasonPop.get())
            visitReasonPop.set(self.controller.options[0])
            visitReasonPop.configure(values=self.controller.options)
            self.controller.mediator.saveOptions(self.controller.options)
        def add_option():
            if entry.get() not in self.controller.options:
                self.controller.options.append(entry.get())
                visitReasonPop.configure(values=self.controller.options)
                self.controller.frames[Entry].visit_reason.configure(values=self.controller.options)
                self.controller.mediator.saveOptions(self.controller.options)
                entry.delete(0, "end")
                

        popup = ctk.CTkToplevel(self.controller)
        popup.title("Úprava dôvodov návštevy")
        popup.geometry('400x200')
        popup.attributes('-topmost', 'true')
        popup.grab_set()
        label = ctk.CTkLabel(popup, text="Pridajte alebo odstránte dôvody návštevy", font=LARGE_FONT)
        label.pack()
        
        entry = ctk.CTkEntry(popup,placeholder_text="Dôvod", width=150)
        entry.place(x=40, y=100)
        add = ctk.CTkButton(popup, text="Pridaj",command=lambda : add_option(), width=150)
        add.place(x=210, y=100)

        visitReasonPop = ctk.CTkOptionMenu(popup, values=self.controller.options, width=150)
        visitReasonPop.place(x=40,y=50)
        

        for x in self.controller.options:
            print(x)
        
        remove = ctk.CTkButton(popup, text="Odstráň", command=lambda: delete_option(), width=150)
        remove.place(x=210,y=50)

        back = ctk.CTkButton(popup, text="Naspäť",command=lambda: go_back(), fg_color="red", hover_color="darkred", width=150)
        back.place(y = 150,x = 210)

        popup.mainloop()

class Ongoing(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.chosenVisitor = [None,None]

        frame = ctk.CTkFrame(self, width=600, height=600)

        title = ctk.CTkLabel(frame, text="Prebiehajúce Návštevy", font=VERY_LARGE_FONT)
        title.place(relx=0.3, y=10)

        name = ctk.CTkLabel(frame, text="Meno")
        name.place(x=78, y=85)
        surname = ctk.CTkLabel(frame, text="Priezvisko" )
        surname.place(x=205, y=85)
        company = ctk.CTkLabel(frame, text="Firma")
        company.place(x=360, y=85)
        review = ctk.CTkLabel(frame, text="Číslo karty")
        review.place(x=485, y=85)

        submit = ctk.CTkButton(frame, text="Odchod", command=lambda: self.submit(), width=150, height=40)
        submit.place(x=40,y=500)
        edit = ctk.CTkButton(frame, text="Úprava", command=lambda: self.edit_chosen_visitor(), width=150, height=40)
        edit.place(x=225,y=500)
        button = ctk.CTkButton(frame, text="Naspäť", command=lambda: self.go_back(), width=150, height=40, fg_color="red", hover_color="darkred")
        button.place(x=410,y=500)

        scrollable_frame = ctk.CTkScrollableFrame(frame, width=600,fg_color="gray17")
        scrollable_frame.place(relx=0,rely=0.2)
        
        self.table = t.CTkTable(scrollable_frame, row=len(self.controller.mediator.visitors),
                                column=4, values=self.list_ongoing(), 
                                command=self.on_row_clicked)
        
        self.table.pack()
        self.restore_table()

        self.error_application_image = ctk.CTkImage(Image.open(ICONS_PATH + "tablet_error.png"), None, (50, 50))
        self.error_cable_image = ctk.CTkImage(Image.open(ICONS_PATH + "connection_error.png"),  None, (50, 50))
        self.no_error_image = ctk.CTkImage(Image.new("RGBA", (50, 50), (0, 0, 0, 0)), None, (50, 50))

        self.error_cable = ctk.CTkLabel(self, text="", font=LARGE_FONT, image=self.error_cable_image)
        self.error_cable.place(relx=0, rely=0.8)

        self.error_application = ctk.CTkLabel(self, text="", font=LARGE_FONT, image=self.error_application_image)
        self.error_application.place(relx=0, rely=0.9)

        frame.grid(padx=10, pady=10)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.show_connection_status()

       

    def show_connection_status(self):
        if not self.controller.mediator.communication.is_device_connected:
            self.error_cable.configure(True, image=self.error_cable_image)
        else:
            self.error_cable.configure(True, image=self.no_error_image)

        if not self.controller.mediator.communication.is_application_running:
            self.error_application.configure(True, image=self.error_application_image)
        else:
            self.error_application.configure(True, image=self.no_error_image)
        self.after(1000, self.show_connection_status)



    def set_default(self, row):
        if row % 2 == 0:
            self.table.edit_row(row, fg_color='gray21')
        else:
            self.table.edit_row(row, fg_color='gray17')

    def restore_table(self):
        for row in range(self.table.rows):
            self.set_default(row)

    def on_row_clicked(self, data):
        if self.chosenVisitor[0]:
            self.set_default(self.chosenVisitor[1])
        self.chosenVisitor = [self.controller.mediator.visitors[data['row']],data['row']]
        self.table.edit_row(self.chosenVisitor[1], fg_color='green')

    def go_back(self):
        if self.chosenVisitor:
            self.chosenVisitor = [None,None]
        self.restore_table()
        self.controller.show_frame(MainMenu)

    def edit_chosen_visitor(self):
        if self.chosenVisitor[0]:
            self.controller.frames[Edit].chosenVisitor = self.chosenVisitor
            self.controller.show_frame(Edit)
        else:
            self.notify()

    def submit(self):
        if self.chosenVisitor[0]:
            visitorx = self.chosenVisitor[0]
            self.controller.mediator.departureVisitor(visitorx.getId(), self)
            self.controller.update_tables()
            self.go_back()
            popup = ctk.CTkToplevel(self.controller)
            popup.geometry('300x200')
            popup.attributes('-topmost', 'true')
            label = ctk.CTkLabel(popup, text="Odoslany review", font=LARGE_FONT)
            label.pack()
            popup.mainloop()
        else:
            self.notify()

    def is_good(self, string):
        if string:
             return string
        else:
            return ''

    def list_ongoing(self):
        visitors = self.controller.mediator.visitors
        filtered = []
        for v in visitors:
            name = self.is_good(v.name)
            surname = self.is_good(v.surname)
            company = self.is_good(v.company)
            cardId = self.is_good(v.cardId)
            filtered.append([name, surname,company, cardId])
        return filtered

    def notify(self):
        popup = ctk.CTkToplevel(self.controller)
        popup.geometry('300x200')
        popup.title("Upozornenie")
        popup.grab_set()
        label = ctk.CTkLabel(popup, text="Vyberte návštevu ktorú chcete upraviť.", font=LARGE_FONT)
        label.place(x=12, y=75)
        popup.mainloop()

    def update_table(self):
        visitors = self.list_ongoing()
        self.table.rows = len(visitors)
        self.table.update_values(visitors)

class Visit_History(ctk.CTkFrame):
    def __init__(self, parent, controller):
        self.controller = controller
        ctk.CTkFrame.__init__(self, parent)

        self.filtered_visitors = None
        self.sorted = [None,None]

        frame = ctk.CTkFrame(self, width=800,height=600)

        title = ctk.CTkLabel(frame, text="História Návštev", font=VERY_LARGE_FONT)
        title.place(y=20, relx=0.35)

        scrollable_frame = ctk.CTkScrollableFrame(frame, width=800, fg_color="gray17")
        scrollable_frame.place(relx=0, rely=0.4)
        self.table = t.CTkTable(scrollable_frame, row=len(self.controller.mediator.allVisitors), column=5,
                                values=self.list_visitors(), command=self.show_visitor)
        self.table.pack()
        self.table.colors = ["gray30", "gray4"]
        self.restore_table()

        name_label = ctk.CTkLabel(frame, text="Meno:")
        name_label.place(x=82,y=100)
        self.name = ctk.CTkEntry(frame, placeholder_text="meno", width=150)
        self.name.place(x=120,y=100)

        surname_label = ctk.CTkLabel(frame, text="Priezvisko:")
        surname_label.place(x=305,y=100)
        self.surname = ctk.CTkEntry(frame, placeholder_text="priezvisko", width=150)
        self.surname.place(x=370,y=100)

        company_label = ctk.CTkLabel(frame, text="Firma:")
        company_label.place(x=550,y=100)
        self.company = ctk.CTkEntry(frame, placeholder_text="firma", width=150)
        self.company.place(x=590,y=100)

        arrival_label = ctk.CTkLabel(frame, text="Príchod:")
        arrival_label.place(x=70,y=150)
        self.arrival = ctk.CTkEntry(frame, placeholder_text="dd.mm.rrrr", width=150)
        self.arrival.place(x=120,y=150)

        departure_label = ctk.CTkLabel(frame, text="Odchod:")
        departure_label.place(x=318,y=150)
        self.departure = ctk.CTkEntry(frame, placeholder_text="dd.mm.rrrr", width=150)
        self.departure.place(x=370,y=150)

        filter = ctk.CTkButton(frame, text="Filter", command=lambda: self.filter_visitors(), width=150)
        filter.place(x=590, y=150)

        self.name_sort = ctk.CTkLabel(frame, text="Meno")
        self.name_sort.place(x=112, y=200)
        self.name_sort.bind("<Button-1>", lambda event: self.sort_by("name"))

        self.surname_sort = ctk.CTkLabel(frame, text="Priezvisko")
        self.surname_sort.place(x=232, y=200)
        self.surname_sort.bind("<Button-1>", lambda event: self.sort_by("surname"))

        self.company_sort = ctk.CTkLabel(frame, text="Firma")
        self.company_sort.place(x=382, y=200)
        self.company_sort.bind("<Button-1>", lambda event: self.sort_by("company"))

        self.arrival_sort = ctk.CTkLabel(frame, text="Príchod")
        self.arrival_sort.place(x=512, y=200)
        self.arrival_sort.bind("<Button-1>",lambda event:  self.sort_by("arrival"))

        self.departure_sort = ctk.CTkLabel(frame, text="Odchod")
        self.departure_sort.place(x=652, y=200)
        self.departure_sort.bind("<Button-1>",lambda event:  self.sort_by("departure"))

        refresh = ctk.CTkButton(frame, text="Vyčistiť filter", command=lambda: self.clear_entry(), width=150, height=40)
        refresh.place(x=230,y=500)

        button = ctk.CTkButton(frame, text="Naspäť", command=lambda: self.go_back(), width=150, height=40, fg_color="red", hover_color="darkred")
        button.place(x=420,y=500)

        self.error_application_image = ctk.CTkImage(Image.open(ICONS_PATH + "tablet_error.png"), None, (50, 50))
        self.error_cable_image = ctk.CTkImage(Image.open(ICONS_PATH + "connection_error.png"),  None, (50, 50))
        self.no_error_image = ctk.CTkImage(Image.new("RGBA", (50, 50), (0, 0, 0, 0)), None, (50, 50))

        self.error_cable = ctk.CTkLabel(self, text="", font=LARGE_FONT, image=self.error_cable_image)
        self.error_cable.place(relx=0, rely=0.8)

        self.error_application = ctk.CTkLabel(self, text="", font=LARGE_FONT, image=self.error_application_image)
        self.error_application.place(relx=0, rely=0.9)

        frame.pack()

        self.show_connection_status()

    def show_visitor(self,data):
        popup = ctk.CTkToplevel(self.controller)
        popup.geometry('600x400')
        if(self.filtered_visitors):
            visitor= self.filtered_visitors[data['row']]
        else:
            visitor = self.controller.mediator.allVisitors[data['row']]
        popup.grab_set()
        label = ctk.CTkLabel(popup, text="Meno: " + visitor.name, font=LARGE_FONT)
        label.pack()
        label2 = ctk.CTkLabel(popup, text="Priezvisko: " + visitor.surname, font=LARGE_FONT)
        label2.pack()
        label3 = ctk.CTkLabel(popup, text="Firma: " +visitor.company, font=LARGE_FONT)
        label3.pack()
        label4 = ctk.CTkLabel(popup, text="Príchod: " +visitor.arrival, font=LARGE_FONT)
        label4.pack()
        label5 = ctk.CTkLabel(popup, text="Odchod: " , font=LARGE_FONT)
        label5.pack()
        if visitor.departure:
            label5.configure(text="Odchod: " +visitor.departure)
        label6 = ctk.CTkLabel(popup, text="Id karty: " +visitor.cardId, font=LARGE_FONT)
        label6.pack()
        label7 = ctk.CTkLabel(popup, text="EČV: " +visitor.carTag, font=LARGE_FONT)
        label7.pack()
        label8 = ctk.CTkLabel(popup, text="Dôvod návštevy: " + visitor.reasonOfVisit, font=LARGE_FONT)
        label8.pack()
        if visitor.review:
            review = visitor.review
        else:
            review = "0"
        label9 = ctk.CTkLabel(popup, text="Recenzia: " + review + "\U00002B50", font=LARGE_FONT)
        label9.pack()
        popup.mainloop()

    def clear_label(self,label):
        if label == "meno":
            self.name_sort.configure(text="Meno")
        if label == "priezvisko":
            self.surname_sort.configure(text="Priezvisko")
        if label == "firma":
            self.company_sort.configure(text="Firma")
        if label == "prichod":
            self.arrival_sort.configure(text="Príchod")
        if label == "odchod":
            self.departure_sort.configure(text="Odchod")

    def sort_by(self,sort):
        if self.filtered_visitors:
            visitors = self.filtered_visitors
        else:
            visitors = self.list_visitors(self.controller.mediator.allVisitors)

        if self.sorted[0] != None:
            self.clear_label(self.sorted[0])
        if sort == "name":
            if self.sorted[1] == None or self.sorted == ["meno",DESC] or self.sorted[0] != "meno":
                self.table.update_values(sorted(visitors, key=lambda x: x[0]))
                self.name_sort.configure(text="Meno " + ASC)
                self.sorted = ["meno", ASC]
            elif self.sorted == ["meno", ASC] :
                self.table.update_values(sorted(visitors, key=lambda x: x[0], reverse=True))
                self.name_sort.configure(text="Meno " + DESC)
                self.sorted = ["meno", DESC]

        elif sort == "surname":
            if self.sorted[1] == None or self.sorted == ["priezvisko",DESC] or self.sorted[0] != "priezvisko":
                self.table.update_values(sorted(visitors, key=lambda x: x[1]))
                self.surname_sort.configure(text="Priezvisko " + ASC)
                self.sorted = ["priezvisko", ASC]
            elif self.sorted == ["priezvisko", ASC]:
                self.table.update_values(sorted(visitors, key=lambda x: x[1], reverse=True))
                self.surname_sort.configure(text="Priezvisko " + DESC)
                self.sorted = ["priezvisko", DESC]

        elif sort == "company":
            if self.sorted[1] == None or self.sorted == ["firma", DESC] or self.sorted[0] != "firma":
                self.table.update_values(sorted(visitors, key=lambda x: x[2]))
                self.company_sort.configure(text="Firma " + ASC)
                self.sorted = ["firma", ASC]
            elif self.sorted == ["firma", ASC]:
                self.table.update_values(sorted(visitors, key=lambda x: x[2], reverse=True))
                self.company_sort.configure(text="Firma " + DESC)
                self.sorted = ["firma", DESC]

        elif sort == "arrival":
            if self.sorted[1] == None or self.sorted == ["prichod", DESC] or self.sorted[0] != "prichod":
                self.table.update_values(sorted(visitors, key=lambda x: x[3]))
                self.arrival_sort.configure(text="Príchod " + ASC)
                self.sorted = ["prichod", ASC]
            elif self.sorted == ["prichod", ASC]:
                self.table.update_values(sorted(visitors, key=lambda x: x[3], reverse=True))
                self.arrival_sort.configure(text="Príchod " + DESC)
                self.sorted = ["prichod", DESC]

        elif sort == "departure":
            if self.sorted[1] == None or self.sorted == ["odchod", DESC] or self.sorted[0] != "odchod":
                self.table.update_values(sorted(visitors, key=lambda x: x[4]))
                self.departure_sort.configure(text="Odchod " + ASC)
                self.sorted = ["odchod", ASC]
            elif self.sorted == ["odchod", ASC]:
                self.table.update_values(sorted(visitors, key=lambda x: x[4], reverse=True))
                self.departure_sort.configure(text="Odchod " + ASC)
                self.sorted = ["odchod", DESC]

    def show_connection_status(self):
        if not self.controller.mediator.communication.is_device_connected:
            self.error_cable.configure(True, image=self.error_cable_image)
        else:
            self.error_cable.configure(True, image=self.no_error_image)

        if not self.controller.mediator.communication.is_application_running:
            self.error_application.configure(True, image=self.error_application_image)
        else:
            self.error_application.configure(True, image=self.no_error_image)
        self.after(1000, self.show_connection_status)

    def clear_entry(self):
        self.name.delete(0, 'end')
        self.surname.delete(0, 'end')
        self.company.delete(0, 'end')
        self.arrival.delete(0, 'end')
        self.departure.delete(0, 'end')
        if self.sorted[0] != None:
            self.clear_label(self.sorted[0])
        self.table.update_values(self.list_visitors())
        self.controller.update_tables()
        self.filter_visitors()

    def go_back(self):
        self.controller.show_frame(MainMenu)

    def filter_visitors(self):
        visitors = self.controller.mediator.filter(name=self.name.get(), surname=self.surname.get(), company=self.company.get(),
                 dateFrom=self.arrival.get(), dateTo=self.departure.get())
        visitors = self.list_visitors(visitors)
        self.filtered_visitors = visitors
        self.table.configure(rows=len(visitors))
        self.table.update_values(visitors)
    
    def set_default(self, row):
        if row % 2 == 0:
            self.table.edit_row(row, fg_color='gray21')
        else:
            self.table.edit_row(row, fg_color='gray17')

    def restore_table(self):
        for row in range(self.table.rows):
            self.set_default(row)
    def update_table(self):
        visitors = self.list_visitors()
        self.table.rows = len(visitors)
        self.table.update_values(visitors)
        self.restore_table()
    def is_good(self, string):
        if string:
             return string
        else:
            return ''

    def list_visitors(self, filtered=None):
        visitors = self.controller.mediator.allVisitors
        if filtered:
            visitors = filtered
        
        listofvisitors = []
        for v in visitors:

            name = self.is_good(v.name)
            surname = self.is_good(v.surname)
            company = self.is_good(v.company)
            arrival = self.is_good(v.arrival)
            departure = self.is_good(v.departure)
            listofvisitors.append(
                [name, surname, company,  arrival, departure])
        return listofvisitors

class Edit(ctk.CTkFrame):
    def __init__(self, parent, controller):
        self.controller = controller
        ctk.CTkFrame.__init__(self, parent)

        self.chosenVisitor = None

        frame = ctk.CTkFrame(self, width=400, height=400)

        label = ctk.CTkLabel(frame, text="Úprava Navstevy", font=VERY_LARGE_FONT)
        label.place(relx=0.3, y=10)

        lname = ctk.CTkLabel(frame, text="Meno:")
        lname.place(x=160, y=75)
        self.name = ctk.CTkEntry(frame, placeholder_text="meno")
        self.name.place(x=200, y=75)

        lsurname = ctk.CTkLabel(frame, text="Priezvisko:")
        lsurname.place(x=135, y=110)
        self.surname = ctk.CTkEntry(frame, placeholder_text="priezvisko")
        self.surname.place(x=200, y=110)

        lcard_id = ctk.CTkLabel(frame, text="Id karty:")
        lcard_id.place(x=150, y=145)
        self.card_id = ctk.CTkEntry(frame, placeholder_text="id karty")
        self.card_id.place(x=200, y=145)

        lcar_num = ctk.CTkLabel(frame, text="Spz:")
        lcar_num.place(x=170, y=180)
        self.car_num = ctk.CTkEntry(frame, placeholder_text="spz")
        self.car_num.place(x=200, y=180)

        lcompany = ctk.CTkLabel(frame, text="Firma:")
        lcompany.place(x=160, y=215)
        self.company = ctk.CTkEntry(frame, placeholder_text="firma")
        self.company.place(x=200, y=215)

        lgroup_size = ctk.CTkLabel(frame, text="Počet ľudí v skupine:")
        lgroup_size.place(x=80, y=250)
        self.group_size = ctk.CTkEntry(frame, placeholder_text="počet ľudí v skupine")
        self.group_size.place(x=200, y=250)

        lvisit_reason = ctk.CTkLabel(frame, text="Dôvod návštevy:")
        lvisit_reason.place(x=103, y=285)
        self.visit_reason = ctk.CTkOptionMenu(frame, values=self.controller.options)
        self.visit_reason.place(x=200, y=285)

        back = ctk.CTkButton(frame, text="Naspäť", height=40, command=lambda: self.go_back())
        back.place(x=250, y=350)

        submit = ctk.CTkButton(frame, text="Uložiť zmeny", height=40, command=lambda: self.save_info())
        submit.place(x=75, y=350)

        self.error_application_image = ctk.CTkImage(Image.open(ICONS_PATH + "tablet_error.png"), None, (50, 50))
        self.error_cable_image = ctk.CTkImage(Image.open(ICONS_PATH + "connection_error.png"),  None, (50, 50))
        self.no_error_image = ctk.CTkImage(Image.new("RGBA", (50, 50), (0, 0, 0, 0)), None, (50, 50))

        self.error_cable = ctk.CTkLabel(self, text="", font=LARGE_FONT, image=self.error_cable_image)
        self.error_cable.place(relx=0, rely=0.8)

        self.error_application = ctk.CTkLabel(self, text="", font=LARGE_FONT, image=self.error_application_image)
        self.error_application.place(relx=0, rely=0.9)

        frame.grid(padx=10, pady=10)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.show_connection_status()

    def show_connection_status(self):
        if not self.controller.mediator.communication.is_device_connected:
            self.error_cable.configure(True, image=self.error_cable_image)
        else:
            self.error_cable.configure(True, image=self.no_error_image)

        if not self.controller.mediator.communication.is_application_running:
            self.error_application.configure(True, image=self.error_application_image)
        else:
            self.error_application.configure(True, image=self.no_error_image)
        self.after(1000, self.show_connection_status)

    def go_back(self):
        self.clear_entry()
        self.controller.show_frame(Ongoing)

    def clear_entry(self):
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
        self.visit_reason.set(self.controller.options[0])

    def save_info(self):
        if self.checkInfo():
            name = self.name.get()
            surname = self.surname.get()
            card_id = int(self.card_id.get())
            car_num = self.car_num.get()
            company = self.company.get()
            group_size = int(self.group_size.get())
            visit_reason = self.visit_reason.get()
            self.controller.mediator.editVisitor(int(self.chosenVisitor[0].id),name, surname, card_id, car_num, company, group_size, visit_reason)
            self.controller.update_tables()

            popup = ctk.CTkToplevel(self.controller)
            popup.geometry('300x200')
            popup.attributes('-topmost', 'true')
            label = ctk.CTkLabel(popup, text="Navsteva uspesne pridana", font=LARGE_FONT)
            label.pack()
            popup.mainloop()

            self.chosenVisitor = [None,None]
            self.controller.frames[Ongoing].chosenVisitor  = [None,None]
            self.controller.frames[Ongoing].restore_table()

            self.go_back()

    def bad_entry(self, entry):
        entry.configure(fg_color='red')

    def goodEntry(self, entry):
        entry.configure(fg_color='#343638')

    def isInt(self, entry):
        try:
            int(self.group_size.get())
            return True
        except ValueError:
            return False

    def checkInfo(self):
        flag = True

        if (self.name.get() == ''):
            flag = False
            self.bad_entry(self.name)
        else:
            self.goodEntry(self.name)

        if (self.surname.get() == ''):
            flag = False
            self.bad_entry(self.surname)
        else:
            self.goodEntry(self.surname)

        if (self.card_id.get() == ''):
            flag = False
            self.bad_entry(self.card_id)
        elif not (self.isInt(self.card_id)):
            flag = False
            self.bad_entry(self.card_id)
        else:
            self.goodEntry(self.card_id)

        if (self.car_num.get() == ''):
            flag = False
            self.bad_entry(self.car_num)
        else:
            self.goodEntry(self.car_num)

        if (self.company.get() == ''):
            flag = False
            self.bad_entry(self.company)
        else:
            self.goodEntry(self.company)

        if (self.group_size.get() == ''):
            flag = False
            self.bad_entry(self.group_size)
        elif not (self.isInt(self.group_size)):
            flag = False
            self.bad_entry(self.group_size)
        else:
            self.goodEntry(self.group_size)

        return flag
    def enterVisitor(self):
        self.name.insert(0,self.chosenVisitor[0].name)
        self.surname.insert(0,self.chosenVisitor[0].surname)
        self.company.insert(0,self.chosenVisitor[0].company)
        self.car_num.insert(0,self.chosenVisitor[0].carTag)
        self.card_id.insert(0,self.chosenVisitor[0].cardId)
        self.group_size.insert(0,self.chosenVisitor[0].count)
        self.visit_reason.set(self.chosenVisitor[0].reasonOfVisit)

class Control(ctk.CTkFrame):
    
    def __init__(self, parent, controller):
        self.controller = controller
        ctk.CTkFrame.__init__(self, parent)
        self.label = ctk.CTkLabel(self, text="Prebieha kontrola zadaných údajov.", font=VERY_LARGE_FONT)
        self.label.pack(expand=True, fill='both', anchor='center')
        
        self.progressbar = ctk.CTkProgressBar(self)
        self.progressbar.set(0)

        end_presentation = ctk.CTkButton(self, text="Ukonči prezentáciu", height=40, command=lambda: self.send_end_presentation())
        end_presentation.pack(pady=20)

        back = ctk.CTkButton(self, text="Naspäť", height=40, command=lambda: self.go_back())
        back.pack(pady=20)

        self.error_application_image = ctk.CTkImage(Image.open(ICONS_PATH + "tablet_error.png"), None, (50, 50))
        self.error_cable_image = ctk.CTkImage(Image.open(ICONS_PATH + "connection_error.png"),  None, (50, 50))
        self.no_error_image = ctk.CTkImage(Image.new("RGBA", (50, 50), (0, 0, 0, 0)), None, (50, 50))

        self.error_cable = ctk.CTkLabel(self, text="", font=LARGE_FONT, image=self.error_cable_image)
        self.error_cable.place(relx=0, rely=0.8)

        self.error_application = ctk.CTkLabel(self, text="", font=LARGE_FONT, image=self.error_application_image)
        self.error_application.place(relx=0, rely=0.9)

        self.show_connection_status()

    def send_end_presentation(self):
        self.label.configure(True, text="Prezentácia bola ukončená")
        self.controller.mediator.endPresentation()
       

    def show_connection_status(self):
        if not self.controller.mediator.communication.is_device_connected:
            self.error_cable.configure(True, image=self.error_cable_image)
        else:
            self.error_cable.configure(True, image=self.no_error_image)

        if not self.controller.mediator.communication.is_application_running:
            self.error_application.configure(True, image=self.error_application_image)
        else:
            self.error_application.configure(True, image=self.no_error_image)
        self.after(1000, self.show_connection_status)

    def go_back(self):
        self.controller.show_frame(MainMenu)

    def showProgress(self, percentage):
        self.label.configure(text="Návšteva sa zoznamje s pravidlami prevádzky")
        self.progressbar.place(rely=0.7, relx=0.5, anchor="center")
        value = percentage / 100
        self.progressbar.set(value)
        self.progressbar.update()

    def waitForPresentation(self, name, surname, card_id, car_num, company, group_size, visit_reason):
        state, data = self.controller.mediator.addVisitor(self, name, surname, card_id, car_num, company, group_size, visit_reason)
        self.progressbar.set(0)

        if state == Communication.message_code["signature"]:
            self.controller.show_frame(MainMenu)
            self.controller.update_tables()
            self.controller.frames[Entry].clear_entry()
            self.go_back()

            signature: Image = data
            width, height = signature.size
            
            popup = ctk.CTkToplevel(self.controller)
            popup.geometry(f'{width}x{height + 100}')
            popup.attributes('-topmost', 'true')
            
            label = ctk.CTkLabel(popup, text="Navsteva bola zapisana", font=LARGE_FONT)
            label.pack()

            signature_image = ctk.CTkImage(signature, None, signature.size)
            image_label = ctk.CTkLabel(popup, image=signature_image, text="")
            image_label.pack(expand=True, fill="both")
            
            popup.mainloop()

        elif state == Communication.message_code["wrong_data"]:
            self.controller.show_frame(Entry)
            popup = ctk.CTkToplevel(self.controller)
            popup.geometry('300x200')
            popup.attributes('-topmost', 'true')
            label = ctk.CTkLabel(popup, text="Udaje boli zadane zle", font=LARGE_FONT)
            label.pack()
            popup.mainloop()

        elif state == Communication.message_code["presentation_end"]:
            self.controller.show_frame(Entry)
            popup = ctk.CTkToplevel(self.controller)
            popup.geometry('300x200')
            popup.attributes('-topmost', 'true')
            label = ctk.CTkLabel(popup, text="Prezentácia bola ukončená", font=LARGE_FONT)
            label.pack()
            popup.mainloop()

        
        else:
            self.controller.show_frame(Entry)
            popup = ctk.CTkToplevel(self.controller)
            popup.geometry('420x200')
            popup.title("Upozornenie")
            popup.attributes('-topmost', 'true')
            label = ctk.CTkLabel(popup, text="Nastala chyba, skontrolujte stav pripojeného zariadenia.", font=LARGE_FONT, text_color="red")
            label.place(x=12, y=75)
            popup.mainloop()

ctk.set_appearance_mode('dark')
mediator = med.Mediator()
app = MainScreen(mediator)
app.mainloop()