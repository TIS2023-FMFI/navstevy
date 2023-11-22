import tkinter as tk
LARGE_FONT = ("Verdana", 12)


'''using frames in  main class we can add classes of gui as individual frames and change between them
    this can be used with main windows and popups.
    
     how to get window info:
        self.winfo_height() 
        self.winfo_width()
'''
class MainScreen(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry("1200x900")
        self.minsize(500, 500)

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand = True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (Uvod, Prichod, Prebiehajuce, Historia):

            frame = F(self.container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Uvod)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.configure(width=1000, height=1000)
        frame.tkraise()


'''This are gonna be the classes that will have the buttons and functions that will change the screen and create popups'''
class Uvod(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Uvod", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button = tk.Button(self, text="Prichod", command=lambda: controller.show_frame(Prichod))
        button.pack()

        button2 = tk.Button(self, text="Prebiehajuce", command=lambda: controller.show_frame(Prebiehajuce))
        button2.pack()

        button3 = tk.Button(self, text="Historia", command=lambda: controller.show_frame(Historia))
        button3.pack()

class Prichod(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Prichod", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button = tk.Button(self, text="Back", command=lambda: controller.show_frame(Uvod))
        button.pack()

        button2 = tk.Button(self, text="PopUp", command=self.popup)
        button2.pack()
    '''this will be a similar class for popups as for the main screen'''
    def popup(self):
        root = tk.Tk()
        root.configure(width=100, height=100, background="black", highlightcolor="Red")
        root.title("PopUp")
        root.mainloop()

class Prebiehajuce(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Prebiehajuce", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button = tk.Button(self, text="Back", command=lambda: controller.show_frame(Uvod))
        button.pack()

class Historia(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Historia", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button = tk.Button(self, text="Back", command=lambda: controller.show_frame(Uvod))
        button.pack()


app = MainScreen()
app.mainloop()