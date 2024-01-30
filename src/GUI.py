import customtkinter as ctk
import Mediator as med
import CTkTable as t
import Visitor
from Communication import Communication
import asyncio
from threading import Thread

BASE_FG_COLOR = '#343638'
LARGE_FONT = ("times new roman", 12)


class MainScreen(ctk.CTk):

    def __init__(self, mediator):
        ctk.CTk.__init__(self)

        self.geometry("1200x600")
        self.width = 1200
        self.height = 600
        self.mediator = mediator
        self.minsize(500, 500)

        self.visitors = mediator.allVisitors
        self.ongoingVisitors = mediator.visitors

        self.container = ctk.CTkFrame(self)
        self.container.pack(side="top", fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        #todo dorobit moznosti vyberu pre reason of visit

        self.frames = {}

        for F in (MainMenu, Entry, Ongoing, Visit_History, Edit):
            frame = F(self.container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainMenu)

    def show_frame(self, cont):
        if cont == Edit:
            self.frames[Edit].enterVisitor()
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

        # TODO umiestnit labels k entry
        self.lname = ctk.CTkLabel(self, text="meno")
        self.lname.pack()
        self.lsurname = ctk.CTkLabel(self, text="priezvisko")
        self.lsurname.pack()
        self.lcard_id = ctk.CTkLabel(self, text="id")
        self.lcard_id.pack()
        self.lcar_num = ctk.CTkLabel(self, text="spz")
        self.lcar_num.pack()
        self.lcompany = ctk.CTkLabel(self, text="firma")
        self.lcompany.pack()
        self.lgroup_size = ctk.CTkLabel(self, text="pocet ludi v skupine")
        self.lgroup_size.pack()

        self.name = ctk.CTkEntry(self, placeholder_text="meno")
        self.name.pack()
        self.surname = ctk.CTkEntry(self, placeholder_text="priezvisko")
        self.surname.pack()
        self.card_id = ctk.CTkEntry(self, placeholder_text="id")
        self.card_id.pack()
        self.car_num = ctk.CTkEntry(self, placeholder_text="spz")
        self.car_num.pack()
        self.company = ctk.CTkEntry(self, placeholder_text="firma")
        self.company.pack()
        self.group_size = ctk.CTkEntry(self, placeholder_text="pocet ludi v skupine")
        self.group_size.pack()

        self.options = [
            "navsteva manazera",
            "audit",
            "instalacia",
            "oprava zariadeni"
        ]
        # TODO pridat moznost Pomocou popup / remove moznost

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
            name = self.name.get()
            surname = self.surname.get()
            card_id = int(self.card_id.get())
            car_num = self.car_num.get()
            company = self.company.get()
            group_size = int(self.group_size.get())
            visit_reason = self.visit_reason.get()
            
            """
            ## komunikacia 
            mediator:med.Mediator = self.controller.mediator

            ## Posli start prezentacia
            temporary_visitor = Visitor.Visitor(0, name, surname, card_id, car_num, company, group_size, visit_reason)
            
            ## Cakaj odpovede z prezentacia a reaguj na to 
            state, data = mediator.communication.send_start_presentation(temporary_visitor)
            thread = Thread(target=mediator.communication.recieve()).start()
    
    
            
            while state == Communication.message_code["progress"]:
                ## TODO update progress bar
                state, data = mediator.communication.recieve()
            
            

            if state == Communication.message_code["wrong_data"]:
                ## TODO treba upravit udaje Visitora
                ...

            elif state == Communication.message_code["signature"]:
                ## TODO treba cosi spravit s obrazkom
                ## data == obrazok podpisu
                ...
            """


            ## Toto az po prezentacii
            self.controller.mediator.addVisitor(name, surname, card_id, car_num, company, group_size, visit_reason)
            # todo dorobit aby sa refreshli tables


            # TODO dorobit POPUP visitor sa prida az po odkontrolovani
            '''if checked():
                    self.goBack()
            '''

            # temporary
            self.goBack()

    def badEntry(self, entry):
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
            self.badEntry(self.name)
        else:
            self.goodEntry(self.name)

        if (self.surname.get() == ''):
            flag = False
            self.badEntry(self.surname)
        else:
            self.goodEntry(self.surname)

        if (self.card_id.get() == ''):
            flag = False
            self.badEntry(self.card_id)
        elif not (self.isInt(self.card_id)):
            flag = False
            self.badEntry(self.card_id)
        else:
            self.goodEntry(self.card_id)

        if (self.car_num.get() == ''):
            flag = False
            self.badEntry(self.car_num)
        else:
            self.goodEntry(self.car_num)

        if (self.company.get() == ''):
            flag = False
            self.badEntry(self.company)
        else:
            self.goodEntry(self.company)

        if (self.group_size.get() == ''):
            flag = False
            self.badEntry(self.group_size)
        elif not (self.isInt(self.group_size)):
            flag = False
            self.badEntry(self.group_size)
        else:
            self.goodEntry(self.group_size)

        return flag


class Ongoing(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        label = ctk.CTkLabel(self, text="Prebiehajuce Navstevy", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        self.controller = controller

        self.chosenVisitor = [None,None]

        # TODO upravit vzhladom na velkost obrazovky
        scrollable_frame = ctk.CTkScrollableFrame(self, width=600)
        scrollable_frame.pack()
        #todo dorobit farby table aby sedeli
        self.table = t.CTkTable(scrollable_frame, row=len(self.controller.ongoingVisitors),
                                column=4, values=self.listOngoing(),
                                command=self.on_row_clicked)
        self.table.pack()

        recenzia = ctk.CTkButton(self, text="Recenzia", command=lambda: self.review())
        recenzia.pack()
        submit = ctk.CTkButton(self, text="Odchod", command=lambda: self.submit())
        submit.pack()
        edit = ctk.CTkButton(self, text="Uprava", command=lambda: self.edit())
        edit.pack()
        button = ctk.CTkButton(self, text="Naspat", command=lambda: self.goBack())
        button.pack()

    def set_default(self, row):
        if row % 2 == 0:
            self.table.edit_row(row, fg_color='gray17')
        else:
            self.table.edit_row(row, fg_color='gray14')

    def restore_table(self):
        for row in range(self.table.rows):
            self.set_default(row)

    def on_row_clicked(self, data):
        if self.chosenVisitor[0]:
            self.set_default(self.chosenVisitor[1])
        self.chosenVisitor = [self.controller.ongoingVisitors[data['row']],data['row']]
        self.table.edit_row(self.chosenVisitor[1], fg_color='green')

    def goBack(self):
        if self.chosenVisitor:
            self.chosenVisitor = [None,None]
        self.restore_table()
        self.controller.show_frame(MainMenu)

    def edit(self):
        if self.chosenVisitor[0]:
            self.controller.frames[Edit].chosenVisitor = self.chosenVisitor
            self.controller.show_frame(Edit)
        else:
            self.notify()

    def review(self):
        if self.chosenVisitor[0]:
            #self.controller.mediator.review()
            # TODO popup na review a zapisanie review pre vybrateho visitora
            popup = ctk.CTkToplevel(self.controller)
            popup.geometry('300x200')
            popup.grab_set()
            label = ctk.CTkLabel(popup, text="Odoslane review", font=LARGE_FONT)
            label.pack()
            popup.mainloop()

        else:
            self.notify()

    def submit(self):
        if self.chosenVisitor[0]:
            visitorx = self.chosenVisitor
            self.controller.mediator.departureVisitor(visitorx)
            self.goBack()
        else:
            self.notify()
    def isGood(self,string):
        if string:
             return string
        else:
            return ''

    def listOngoing(self):
        visitors = self.controller.ongoingVisitors
        filtered = []
        for v in visitors:
            name = self.isGood(v.name)
            surname = self.isGood(v.surname)
            cardId = self.isGood(v.cardId)
            review = self.isGood(v.review)
            filtered.append([name, surname, cardId, review])
        return filtered

    def notify(self):
        popup = ctk.CTkToplevel(self.controller)
        popup.geometry('300x200')

        popup.grab_set()
        label = ctk.CTkLabel(popup, text="Vyberte navstevu", font=LARGE_FONT)
        label.pack()
        popup.mainloop()


class Visit_History(ctk.CTkFrame):
    def __init__(self, parent, controller):
        self.controller = controller
        ctk.CTkFrame.__init__(self, parent)
        label = ctk.CTkLabel(self, text="Historia Navstev", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        if self.controller.visitors is None:
            self.controller.visitors = self.listVisitors(m.allVisitors)
        # TODO priradit sort na labels
        self.lname = ctk.CTkLabel(self, text="meno")
        self.lname.pack()
        self.lsurname = ctk.CTkLabel(self, text="priezvisko")
        self.lsurname.pack()
        self.lcompany = ctk.CTkLabel(self, text="firma")
        self.lcompany.pack()
        self.larrival = ctk.CTkLabel(self, text="prichod")
        self.larrival.pack()
        self.ldeparture = ctk.CTkLabel(self, text="odchod")
        self.ldeparture.pack()

        self.name = ctk.CTkEntry(self, placeholder_text="meno")
        self.name.pack()
        self.surname = ctk.CTkEntry(self, placeholder_text="priezvisko")
        self.surname.pack()
        self.company = ctk.CTkEntry(self, placeholder_text="firma")
        self.company.pack()
        self.arrival = ctk.CTkEntry(self, placeholder_text="prichod")
        self.arrival.pack()
        self.departure = ctk.CTkEntry(self, placeholder_text="odchod")
        self.departure.pack()


        #todo relative height na table
        scrollable_frame = ctk.CTkScrollableFrame(self,width=800)
        scrollable_frame.pack()
        self.table = t.CTkTable(scrollable_frame, row=len(self.controller.visitors), column=9, values=self.listVisitors())
        self.table.pack()

        #TODO spravit na enter???
        filter = ctk.CTkButton(self, text="Filter", command=lambda: self.filterVisitors())
        filter.pack()

        refresh = ctk.CTkButton(self, text="Clear", command=lambda: self.clearEntry())
        refresh.pack()
        button = ctk.CTkButton(self, text="Back", command=lambda: self.goBack())
        button.pack()
        # todo buttons na prepinanie table

    def clearEntry(self):
        self.name.delete(0, 'end')
        self.surname.delete(0, 'end')
        self.company.delete(0, 'end')
        self.arrival.delete(0, 'end')
        self.departure.delete(0, 'end')
        self.controller.visitors = self.controller.mediator.allVisitors
        self.table.configure(rows=len(self.controller.visitors))
        self.table.update_values(self.listVisitors())





    def goBack(self):
        self.controller.show_frame(MainMenu)


    def filterVisitors(self):
        self.controller.visitors = m.filter(name=self.name.get(), surname=self.surname.get(), company=self.company.get(),
                 dateFrom=self.arrival.get(), dateTo=self.departure.get())

        visitors = self.listVisitors()
        self.table.configure(rows=len(visitors))
        self.table.update_values(visitors)
        self.controller.show_frame(Visit_History)
    def isGood(self,string):
        if string:
             return string
        else:
            return ''

    def listVisitors(self):
        visitors = self.controller.visitors
        listofvisitors = []
        for v in visitors:

            name = self.isGood(v.name)
            surname = self.isGood(v.surname)
            cardId = self.isGood(v.cardId)
            review = self.isGood(v.review)
            company = self.isGood(v.company)
            carTag = self.isGood(v.carTag)
            count = self.isGood(v.count)
            reasonOfVisit = self.isGood(v.reasonOfVisit)
            arrival = self.isGood(v.arrival)
            departure = self.isGood(v.departure)
            listofvisitors.append(

                [name, surname, company, cardId, carTag, count, reasonOfVisit, arrival, departure,
                 review])
        return listofvisitors

class Edit(ctk.CTkFrame):
    def __init__(self, parent, controller):
        self.controller = controller
        self.parent = parent
        ctk.CTkFrame.__init__(self, parent)

        self.chosenVisitor = None

        label = ctk.CTkLabel(self, text="Zapis Navstevy", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button = ctk.CTkButton(self, text="Naspat", command=lambda: self.goBack())
        button.pack()

        submit = ctk.CTkButton(self, text="Ulozit zmeny", command=lambda: self.saveInfo())
        submit.pack()

        # TODO umiestnit labels k entry
        self.lname = ctk.CTkLabel(self, text="meno")
        self.lname.pack()
        self.lsurname = ctk.CTkLabel(self, text="priezvisko")
        self.lsurname.pack()
        self.lcard_id = ctk.CTkLabel(self, text="id")
        self.lcard_id.pack()
        self.lcar_num = ctk.CTkLabel(self, text="spz")
        self.lcar_num.pack()
        self.lcompany = ctk.CTkLabel(self, text="firma")
        self.lcompany.pack()
        self.lgroup_size = ctk.CTkLabel(self, text="pocet ludi v skupine")
        self.lgroup_size.pack()

        self.name = ctk.CTkEntry(self, placeholder_text="meno")
        self.name.pack()
        self.surname = ctk.CTkEntry(self, placeholder_text="priezvisko")
        self.surname.pack()
        self.card_id = ctk.CTkEntry(self, placeholder_text="id")
        self.card_id.pack()
        self.car_num = ctk.CTkEntry(self, placeholder_text="spz")
        self.car_num.pack()
        self.company = ctk.CTkEntry(self, placeholder_text="firma")
        self.company.pack()
        self.group_size = ctk.CTkEntry(self, placeholder_text="pocet ludi v skupine")
        self.group_size.pack()

        self.options = [
            "navsteva manazera",
            "audit",
            "instalacia",
            "oprava zariadeni"
        ]
        # TODO pridat moznost Pomocou popup / remove moznost



        self.visit_reason = ctk.CTkOptionMenu(master=self, values=self.options)
        self.visit_reason.pack()

    def goBack(self):
        self.clearEntry()
        self.controller.show_frame(Ongoing)

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
            name = self.name.get()
            surname = self.surname.get()
            card_id = int(self.card_id.get())
            car_num = self.car_num.get()
            company = self.company.get()
            group_size = int(self.group_size.get())
            visit_reason = self.visit_reason.get()
            self.controller.mediator.editVisitor(int(self.chosenVisitor[0].id),name, surname, card_id, car_num, company, group_size, visit_reason)
            #Todo urobit aby sa to ulozilo a zobrazilo

            #todo dorobit aby sa refreshli tables

            self.chosenVisitor = [None,None]
            self.controller.frames[Ongoing].chosenVisitor  = [None,None]
            self.controller.frames[Ongoing].restore_table()

            # temporary
            self.goBack()

    def badEntry(self, entry):
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
            self.badEntry(self.name)
        else:
            self.goodEntry(self.name)

        if (self.surname.get() == ''):
            flag = False
            self.badEntry(self.surname)
        else:
            self.goodEntry(self.surname)

        if (self.card_id.get() == ''):
            flag = False
            self.badEntry(self.card_id)
        elif not (self.isInt(self.card_id)):
            flag = False
            self.badEntry(self.card_id)
        else:
            self.goodEntry(self.card_id)

        if (self.car_num.get() == ''):
            flag = False
            self.badEntry(self.car_num)
        else:
            self.goodEntry(self.car_num)

        if (self.company.get() == ''):
            flag = False
            self.badEntry(self.company)
        else:
            self.goodEntry(self.company)

        if (self.group_size.get() == ''):
            flag = False
            self.badEntry(self.group_size)
        elif not (self.isInt(self.group_size)):
            flag = False
            self.badEntry(self.group_size)
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
        self.visit_reason.set(0,self.chosenVisitor[0].reason)

ctk.set_appearance_mode('dark')
m = med.Mediator()
app = MainScreen(m)
app.mainloop()