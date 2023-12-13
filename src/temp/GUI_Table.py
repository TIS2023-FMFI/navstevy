import customtkinter as ctk
import CTkTable as t
LARGE_FONT = ("Verdana", 12)
BASE_FG_COLOR = '#343638'

'''
    Sposob na zobrazenie informacii o navsteve
    z listu sa zoberu data a tie sa zobrazia v CTkTable
    '''

root = ctk.CTk()
radio_var = ctk.IntVar(0)

def radiobutton_event():
    print("radiobutton toggled, current value:", radio_var.get())

radiobutton_1 = ctk.CTkRadioButton(master=root, text='',
                                             command=radiobutton_event, variable= radio_var, value=1)
radiobutton_2 = ctk.CTkRadioButton(master=root, text='',
                                             command=radiobutton_event, variable= radio_var, value=2)

radiobutton_1.pack(padx=20, pady=10)
radiobutton_2.pack(padx=20, pady=10)
value = [[1,2,3,4,5],
         [1,2,3,4,5],
         [1,2,3,4,5],
         [1,2,3,4,5],
         [1,2,3,4,5]]

table = t.CTkTable(master=root, row=5, column=5, values=value)
table.pack(expand=True, fill="both", padx=20, pady=20)
root.mainloop()
