import os
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from tkinter import filedialog

from personDAO import *
from faceEncoding import *

root = None
DAO = None

class mainWindow(Tk):

    directory = None # defined here so can tell if directory has been selected or not

    def __init__(self):
        Tk.__init__(self)
        self.title("Face Recognition")
        self.back = Frame(self, width=50, height=100)
        self.back.grid()
        self.root_menu  = Menu(self)
        self.config(menu = self.root_menu)

        self.file_menu = Menu(self.root_menu)
        self.root_menu.add_cascade(label = "File", menu = self.file_menu)
        self.file_menu.add_command(label = "Exit", command = self.destroy)

        self.database_menu = Menu(self.root_menu)
        self.root_menu.add_cascade(label = "Database", menu = self.database_menu)
        self.database_menu.add_command(label = "Add Person", command=initAdd)        
        self.database_menu.add_command(label = "Add Photo", command=initPhoto)        
        self.database_menu.add_command(label = "Run Encoder", command=initEncode)
        
        self.filebtn = Button(self, text="Video/Image path", command=self.btnFile)
        self.filebtn.grid(row = 0, column = 0)
        self.filepath = Text(self, width = 30, height = 1,state= DISABLED)
        self.filepath.grid(row = 1, column = 0)
        self.runImage = Button(self, text="Run Image", command=self.btnImg)
        self.runImage.grid(row=0,column=1)
        self.runVideo = Button(self, text="Run Video", command=self.btnVideo)
        self.runVideo.grid(row=1,column=1)
        self.runWebcam = Button(self, text="Run Webcam", command=self.btnWebcam)
        self.runWebcam.grid(row=2,column=1)

    def btnFile(self):
        self.directory = filedialog.askopenfilename(initialdir = "C:\\",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        self.filepath.configure(state = NORMAL)
        self.filepath.insert(INSERT,"")
        self.filepath.insert(INSERT,str(os.path.basename(self.directory)))
        self.filepath.configure(state = DISABLED)

    def btnImg(self):
        if self.directory is not None:
            addToEncoding(DAO.getEncoded())
            faceDectImage(self.directory)
        else:
            messagebox.showerror("Error","No input image/video selected.")

    def btnVideo(self):
        if self.directory is not None:
            addToEncoding(DAO.getEncoded())
            faceDectVideo(self.directory)
        else:
            messagebox.showerror("Error","No input image/video selected.")

    def btnWebcam(self):
        addToEncoding(DAO.getEncoded())
        faceDectVideo(None)


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
            DAO.updateEncoding(x[0],encoding[0])
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
            newperson = Person(self.pid.get(),self.name.get().lower(),self.dob.get(),self.nationality.get(),self.height.get(),self.weight.get(),self.hair_colour.get(),self.hair_style.get(),self.skin_colour.get(),self.facial_hair.get())
            newphoto = Photo(self.pid.get(),  DAO.convertToBinaryB64(filename=str(self.directory)))
            DAO.insertPerson(newperson, newphoto)
        except Error as e:
            messagebox.showerror("Error", "Invaild input.")

    def btnFile(self):
        self.directory = filedialog.askopenfilename(initialdir = "C:\\", title = "Select file", filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        self.image.configure(state = NORMAL)
        self.image.insert(INSERT,str(os.path.basename(self.directory)))
        self.image.configure(state = DISABLED)

class addPhoto(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        Label(self, text = "Name").grid(row = 1) 
        self.name = Entry(self)
        self.name.grid(row = 1, column = 1) 
        self.namebtn = Button(self, text="Find PID", command=self.btnName)
        self.namebtn.grid(row = 1, column = 2)
        Label(self, text = "PID").grid(row = 2) 
        self.pid = Entry(self)
        self.pid.grid(row = 2, column = 1) 
        Label(self, text = "Image path").grid(row = 3) 
        self.image = Text(self, width = 30, height = 1,state= DISABLED)
        self.image.grid(row = 3, column = 1) 
        self.filebtn = Button(self, text="File path", command=self.btnFile)
        self.filebtn.grid(row = 3, column = 3)
       

        sumbitbtn = Button(self, text="Sumbit", command=self.btnClick).grid(row = 12)

    def btnClick(self):
        try:
            newphoto = Photo(self.pid.get(), DAO.convertToBinaryB64(filename=str(self.directory)))
            DAO.insertPhoto(newphoto)
        except Error as e:
            messagebox.showerror("Error", "Invaild input.")

    def btnName(self):
        try:
            pid = DAO.getName(self.name.get().lower())[0]
            self.pid.insert(INSERT,"")
            self.pid.insert(INSERT,pid)
        except Error as e:
            messagebox.showerror("Error", "Invaild input.")

    def btnFile(self):
        self.directory = filedialog.askopenfilename(initialdir = "C:\\", title = "Select file", filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
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

def initPhoto():
    ph = addPhoto()
    ph.mainloop()

if __name__ == "__main__":
    DAO = personDAO()
    initMain()