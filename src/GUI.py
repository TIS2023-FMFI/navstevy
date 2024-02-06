import customtkinter as ctk
import Mediator as med
import CTkTable as t

BASE_FG_COLOR = '#343638'
LARGE_FONT = ("times new roman", 18)
VERY_LARGE_FONT = ("times new roman", 32)


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
        self.options = [
            "návšteva manažéra",
            "audit",
            "inštalácia",
            "oprava zariadení"
        ]

        self.frames = {}

        for F in (MainMenu, Entry, Ongoing, Visit_History, Edit, Control):
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
        frame = ctk.CTkFrame(self,width=300,height=400)

        label = ctk.CTkLabel(frame, text="Úvod", font=VERY_LARGE_FONT)
        label.place(relx=0.4,rely=0.1)

        button = ctk.CTkButton(frame, text="Príchod",font=LARGE_FONT,width=200,height=50, command=lambda: controller.show_frame(Entry))
        button.place(relx=0.2, rely=0.3)

        button2 = ctk.CTkButton(frame, text="Prebiehajúce návštevy",font=LARGE_FONT,width=200,height=50, command=lambda: controller.show_frame(Ongoing))
        button2.place(relx=0.2, rely=0.5)

        button3 = ctk.CTkButton(frame, text="História návštev",font=LARGE_FONT,width=200,height=50, command=lambda: controller.show_frame(Visit_History))
        button3.place(relx=0.2, rely=0.7, )

        frame.grid(padx=10,pady=10)
        self.grid_rowconfigure(0,weight=1)
        self.grid_columnconfigure(0, weight=1)
class Entry(ctk.CTkFrame):
    def __init__(self, parent, controller):
        self.controller = controller
        self.parent = parent
        ctk.CTkFrame.__init__(self, parent)

        frame = ctk.CTkFrame(self,width=400,height=400)

        label = ctk.CTkLabel(frame, text="Zapis Navstevy", font=VERY_LARGE_FONT)
        label.place(relx=0.3,y=10)

        self.lname = ctk.CTkLabel(frame, text="Meno:")
        self.lname.place(x=160,y=75)
        self.name = ctk.CTkEntry(frame, placeholder_text="meno")
        self.name.place(x=200,y=75)

        self.lsurname = ctk.CTkLabel(frame, text="Priezvisko:")
        self.lsurname.place(x=135,y=110)
        self.surname = ctk.CTkEntry(frame, placeholder_text="priezvisko")
        self.surname.place(x=200,y=110)

        self.lcard_id = ctk.CTkLabel(frame, text="Id karty:")
        self.lcard_id.place(x=150,y=145)
        self.card_id = ctk.CTkEntry(frame, placeholder_text="id karty")
        self.card_id.place(x=200,y=145)

        self.lcar_num = ctk.CTkLabel(frame, text="Spz:")
        self.lcar_num.place(x=170,y=180)
        self.car_num = ctk.CTkEntry(frame, placeholder_text="spz")
        self.car_num.place(x=200,y=180)

        self.lcompany = ctk.CTkLabel(frame, text="Firma:")
        self.lcompany.place(x=160,y=215)
        self.company = ctk.CTkEntry(frame, placeholder_text="firma")
        self.company.place(x=200,y=215)

        self.lgroup_size = ctk.CTkLabel(frame, text="Počet ľudí v skupine:")
        self.lgroup_size.place(x=80,y=250)
        self.group_size = ctk.CTkEntry(frame, placeholder_text="počet ľudí v skupine")
        self.group_size.place(x=200,y=250)

        self.lvisit_reason = ctk.CTkLabel(frame, text="Dôvod návštevy:")
        self.lvisit_reason.place(x=103, y=285)
        self.visit_reason = ctk.CTkOptionMenu(frame, values=self.controller.options)
        self.visit_reason.place(x=200,y=285)

        back = ctk.CTkButton(frame, text="Naspäť",height=40, command=lambda: self.goBack())
        back.place(x=250,y=350)

        submit = ctk.CTkButton(frame, text="Spustiť prezentáciu",height=40, command=lambda: self.saveInfo())
        submit.place(x=75,y=350)

        frame.grid(padx=10, pady=10)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)




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
        self.visit_reason.set(self.controller.options[0])

    def saveInfo(self):
        if self.checkInfo():
            name = self.name.get()
            surname = self.surname.get()
            card_id = int(self.card_id.get())
            car_num = self.car_num.get()
            company = self.company.get()
            group_size = int(self.group_size.get())
            visit_reason = self.visit_reason.get()
            state = self.controller.mediator.addVisitor(name, surname, card_id, car_num, company, group_size, visit_reason)
            # visitor je úspešne pridaný 
            if state == "signature":
                print("Visitor and signature saved.")
            # visitor sa nepridal
            elif state == "error":
                # TODO nastala nejaká chyba
                # data je dôvod chyby, ktorý stačí niekde vypísať
                # Bud chyba spojenia
                # alebo timout 60s  
                print("Error...")
            elif state == "wrong_data":
                # TODO treba upraviť zadané info a znova poslať na kontrolu
                print("Wrong data...")
            # TODO dorobit POPUP visitor sa prida az po odkontrolovani
            '''if checked():
                    self.goBack()
            '''
            self.controller.show_frame(Control)

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
    #TODO upravenie farieb, velkost
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.chosenVisitor = [None,None]

        frame = ctk.CTkFrame(self, width=600, height=600)

        label = ctk.CTkLabel(frame, text="Prebiehajúce Návštevy", font=VERY_LARGE_FONT)
        label.place(relx=0.3, y=10)

        name = ctk.CTkLabel(frame, text="Meno")
        name.place(x=78, y=85)
        surname = ctk.CTkLabel(frame, text="Priezvisko" )
        surname.place(x=205, y=85)
        company = ctk.CTkLabel(frame, text="Firma")
        company.place(x=360, y=85)
        review = ctk.CTkLabel(frame, text="Číslo karty")
        review.place(x=485, y=85)

        submit = ctk.CTkButton(frame, text="Odchod", command=lambda: self.submit())
        submit.place(x=50,y=500)
        edit = ctk.CTkButton(frame, text="Úprava", command=lambda: self.edit())
        edit.place(x=200,y=500)
        button = ctk.CTkButton(frame, text="Naspäť", command=lambda: self.goBack())
        button.place(x=350,y=500)

        scrollable_frame = ctk.CTkScrollableFrame(frame, width=600)
        scrollable_frame.place(relx=0,rely=0.2)

        self.table = t.CTkTable(scrollable_frame, row=len(self.controller.ongoingVisitors),
                                column=4, values=self.listOngoing(),
                                command=self.on_row_clicked)
        self.table.pack()

        frame.grid(padx=10, pady=10)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)



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



    def submit(self):
        if self.chosenVisitor[0]:
            visitorx = self.chosenVisitor
            self.controller.mediator.departureVisitor(visitorx)
            #todo dorobit review
            '''
            idea
            popup = ctk.CTkToplevel(self.controller)
            popup.geometry('300x200')
            popup.grab_set()
            label = ctk.CTkLabel(popup, text="Odoslane review", font=LARGE_FONT)
            label.pack()
            popup.mainloop()
            '''
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
            company = self.isGood(v.company)
            cardId = self.isGood(v.cardId)
            filtered.append([name, surname,company, cardId])
        return filtered

    def notify(self):
        popup = ctk.CTkToplevel(self.controller)
        popup.geometry('300x200')

        popup.grab_set()
        label = ctk.CTkLabel(popup, text="Vyberte navstevu", font=LARGE_FONT)
        label.pack()
        popup.mainloop()


class Visit_History(ctk.CTkFrame):
    #TODO celkovo dizajn
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


        scrollable_frame = ctk.CTkScrollableFrame(self,width=800)
        scrollable_frame.pack()
        self.table = t.CTkTable(scrollable_frame, row=len(self.controller.visitors), column=9, values=self.listVisitors())
        self.table.pack()

        filter = ctk.CTkButton(self, text="Filter", command=lambda: self.filterVisitors())
        filter.pack()

        refresh = ctk.CTkButton(self, text="Clear", command=lambda: self.clearEntry())
        refresh.pack()
        button = ctk.CTkButton(self, text="Back", command=lambda: self.goBack())
        button.pack()


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
    #TODO upravit ako ENTRY
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



        self.visit_reason = ctk.CTkOptionMenu(master=self, values=self.controller.options)
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
        self.visit_reason.set(self.controller.options[0])

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
        self.visit_reason.set(self.chosenVisitor[0].reasonOfVisit)

class Control(ctk.CTkFrame):
    # TODO dorobit frame co sa deje po spusteni prezentacie
    def __init__(self, parent, controller):
        self.controller = controller
        ctk.CTkFrame.__init__(self, parent)
        label = ctk.CTkLabel(self, text="Prebieha kontrola zadaných údajov.", font=VERY_LARGE_FONT)
        label.pack(expand=True, fill='both', anchor='center')

ctk.set_appearance_mode('dark')
m = med.Mediator()
app = MainScreen(m)
app.mainloop()