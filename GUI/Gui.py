import os
import sys
import tkinter

root = None

class mainWindow(tkinter.Tk):
    def __init__(self):
        tkinter.Tk.__init__(self)


class addWindow(tkinter.Toplevel):
    def __init__(self):
        tkinter.Toplevel.__init__(self)
        tkinter.Label(self, text = "PID").grid(row = 1) 
        self.pid = tkinter.Entry(self)
        self.pid.grid(row = 1, column = 1) 
        tkinter.Label(self, text = "Name").grid(row = 2) 
        self.name = tkinter.Entry(self)
        self.name.grid(row = 2, column = 1) 
        tkinter.Label(self, text = "DOB").grid(row = 3) 
        self.dob = tkinter.Entry(self)
        self.dob.grid(row = 3, column = 1) 
        tkinter.Label(self, text = "Nationality").grid(row = 4) 
        self.nationality = tkinter.Entry(self)
        self.nationality.grid(row = 4, column = 1) 
        tkinter.Label(self, text = "Height").grid(row = 5) 
        self.height = tkinter.Entry(self)
        self.height.grid(row = 5, column = 1) 
        tkinter.Label(self, text = "Weight").grid(row = 6) 
        self.weight = tkinter.Entry(self)
        self.weight.grid(row = 6, column = 1) 
        tkinter.Label(self, text = "Hair colour").grid(row = 7) 
        self.hair_colour = tkinter.Entry(self)
        self.hair_colour.grid(row = 7, column = 1) 
        tkinter.Label(self, text = "Hair Style").grid(row = 8) 
        self.hair_style = tkinter.Entry(self)
        self.hair_style.grid(row = 8, column = 1) 
        tkinter.Label(self, text = "Skin colour").grid(row = 9) 
        self.skin_colour = tkinter.Entry(self)
        self.skin_colour.grid(row = 9, column = 1) 
        tkinter.Label(self, text = "Facial hair").grid(row = 10) 
        self.facial_hair = tkinter.Entry(self)
        self.facial_hair.grid(row = 10, column = 1) 
        tkinter.Label(self, text = "Image (path to?)").grid(row = 11) 
        self.image = tkinter.Entry(self)
        self.image.grid(row = 11, column = 1) 

        sumbitbtn = tkinter.Button(self, text="Sumbit", command=self.exc).grid(row = 12)

    def exc(self):
        print("button pressed")
        print(self)
        print(self.pid.get())
        print(self.height.get())

def initAdd():
    ad = addWindow()
    ad.mainloop()


if __name__ == "__main__":
    root = tkinter.Tk()
    root.title("Face Recognition")

    root_menu  = tkinter.Menu(root)
    root.config(menu = root_menu)

    file_menu = tkinter.Menu(root_menu)
    root_menu.add_cascade(label = "File", menu = file_menu)
    file_menu.add_command(label = "Exit", command = root.destroy)
    file_menu.add_separator() 

    database_menu = tkinter.Menu(root_menu)
    root_menu.add_cascade(label = "Database", menu = database_menu)
    database_menu.add_command(label = "Add Person", command=initAdd)

    #tkinter.Label(self, text="works")

    root.mainloop()