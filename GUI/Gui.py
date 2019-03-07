import os
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog

from personDAO import *
from faceEncoding import *

root = None
DAO = None

class mainWindow(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("Face Recognition")
        self.root_menu  = Menu(self)
        self.config(menu = self.root_menu)

        self.file_menu = Menu(self.root_menu)
        self.root_menu.add_cascade(label = "File", menu = self.file_menu)
        self.file_menu.add_command(label = "Exit", command = self.destroy)
        #self.file_menu.add_separator() 

        self.database_menu = Menu(self.root_menu)
        self.root_menu.add_cascade(label = "Database", menu = self.database_menu)
        self.database_menu.add_command(label = "Add Person", command=initAdd)        
        self.database_menu.add_command(label = "Run Encoder", command=initEncode)

class encodeWindow(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.result = DAO.getUnencoded()
        if len(self.result) != 0: 
            self.frac = 100 / len(self.result) # zero check needed
            Label(self, text = "Amount of unencoded database entries: " + str(len(self.result)) + "").grid(row = 1, column= 1) 
            self.prog = Progressbar(self,orient=HORIZONTAL,length=200,mode='determinate')
            self.prog.grid(row=2, column=1)
            self.updateBtn = Button(self, text="Sumbit", command=self.btnUpdate).grid(row = 3,column=1)
        else:
            Label(self, text = "No database entries to encode.").grid(row = 1, column= 1) 

    def btnUpdate(self):
        for x in self.result:
            img = DAO.convertFromBinaryB64(x[1])
            img.save('img/temp/image.png')
            encoding = getEncoding(cv2.imread('img/temp/image.png'))
            DAO.updateEncoding(x[0],encoding)
            self.prog['value'] += self.frac
            self.update_idletasks()
        
class addWindow(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        Label(self, text = "PID").grid(row = 1) 
        self.pid = Entry(self)
        self.pid.grid(row = 1, column = 1) 
        Label(self, text = "Name").grid(row = 2) 
        self.name = Entry(self)
        self.name.grid(row = 2, column = 1) 
        Label(self, text = "DOB (YYYY-MM-DD)").grid(row = 3) 
        self.dob = Entry(self)
        self.dob.grid(row = 3, column = 1) 
        Label(self, text = "Nationality").grid(row = 4) 
        self.nationality = Entry(self)
        self.nationality.grid(row = 4, column = 1) 
        Label(self, text = "Height").grid(row = 5) 
        self.height = Entry(self)
        self.height.grid(row = 5, column = 1) 
        self.height.insert(INSERT, "0")
        Label(self, text = "Weight").grid(row = 6) 
        self.weight = Entry(self)
        self.weight.grid(row = 6, column = 1) 
        self.weight.insert(INSERT, "0")
        Label(self, text = "Hair colour").grid(row = 7) 
        self.hair_colour = Entry(self)
        self.hair_colour.grid(row = 7, column = 1) 
        Label(self, text = "Hair Style").grid(row = 8) 
        self.hair_style = Entry(self)
        self.hair_style.grid(row = 8, column = 1) 
        Label(self, text = "Skin colour").grid(row = 9) 
        self.skin_colour = Entry(self)
        self.skin_colour.grid(row = 9, column = 1) 
        Label(self, text = "Facial hair").grid(row = 10) 
        self.facial_hair = Entry(self)
        self.facial_hair.grid(row = 10, column = 1) 
        Label(self, text = "Image path").grid(row = 11) 
        self.image = Text(self, width = 30, height = 1,state= DISABLED)
        self.filebtn = Button(self, text="File path", command=self.btnFile)
        self.filebtn.grid(row = 11, column = 3)
        self.image.grid(row = 11, column = 1) 

        sumbitbtn = Button(self, text="Sumbit", command=self.btnClick).grid(row = 12)

    def btnClick(self):
        try:
            newperson = Person(self.pid.get(),self.name.get(),self.dob.get(),self.nationality.get(),self.height.get(),self.weight.get(),self.hair_colour.get(),self.hair_style.get(),self.skin_colour.get(),self.facial_hair.get(), DAO.convertToBinaryB64(filename=str(self.directory)))
            DAO.insertPerson(newperson)
        except Error as e:
            messagebox.showerror("Error", "Invaild input.")

    def btnFile(self):
        self.directory = filedialog.askopenfilename(initialdir = "C:\\",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        self.image.configure(state = NORMAL)
        self.image.insert(INSERT,str(os.path.basename(self.directory)))
        self.image.configure(state = DISABLED)

def initAdd():
    ad = addWindow()
    ad.mainloop()

def initEncode():
    en = encodeWindow()
    en.mainloop()

def initMain():
    root = mainWindow()
    root.mainloop()


if __name__ == "__main__":
    DAO = personDAO()
    initMain()
    
