import os
import sys
import io
import base64
from PIL import Image
import PIL.Image
import mysql.connector
from datetime import datetime
from mysql.connector import Error
from mysql.connector import errorcode

class Person:
    def __init__(self, pid, name = None, dob = None, nationality = None, height = 0, weight = 0, hair_colour = None, hair_style = None, skin_colour = None, facial_hair = None, image = None, encoding = None, encoded = None):
        self.pid = pid
        self.name = name 
        self.dob = dob
        self.nationality = nationality
        self.height = height 
        self.weight = weight
        self.hair_colour = hair_colour
        self.hair_style = hair_style
        self.skin_colour = skin_colour
        self.facial_hair = facial_hair
        self.image = image
        self.encoding = encoding
        self.encoded = encoded 

class personDAO:
    def __init__(self):
        pass

    def connectToMysql(self):
        return mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="project"
        )

    def convertToBinaryB64(self, filename):
        with open(filename, 'rb') as file:
            binaryData = file.read() # read the file binary (unicode bytes) from image
        file = base64.b64encode(binaryData) # convert to base64 (shorter so takes less space in the db)
        return str(file)[2:][:-1] # remove leading and trailing single qoute character which messes with the SQL

    def convertFromBinaryB64(self, data):
        imgbyte = base64.b64decode(data)
        return Image.open(io.BytesIO(imgbyte))

    def insertPerson(self, p): # p = person object
        try:
            self.mydb = self.connectToMysql()
            self.mycursor = self.mydb.cursor()
            self.mycursor.execute("INSERT INTO person (pid, name, dob, nationality, height, weight, hair_colour, hair_style, skin_colour,facial_hair,image,encoding,encoded) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (int(p.pid),p.name,p.dob,p.nationality,int(p.height),int(p.weight),p.hair_colour,p.hair_style,p.skin_colour,p.facial_hair,p.image,'','0'))
            self.mydb.commit()
        except Error as e:
            print(e)
        finally:
            self.mycursor.close()
            self.mydb.close()

    def updateEncoding(self, pid, encoding): 
        try:
            self.mydb = self.connectToMysql()
            self.mycursor = self.mydb.cursor()
            self.mycursor.execute("UPDATE person SET encoding='%s', encoded='1' WHERE pid='%s'" % (encoding,pid))
            self.mydb.commit()
        except Error as e:
            print(e)
        finally:
            self.mycursor.close()
            self.mydb.close()

    def getUnencoded(self): 
        try:
            self.mydb = self.connectToMysql()
            self.mycursor = self.mydb.cursor()
            self.mycursor.execute("SELECT pid,image FROM person WHERE encoded ='0'")
            self.result = self.mycursor.fetchall()
            self.mydb.commit()
        except Error as e:
            print(e)
        else:
            return self.result
        finally:
            self.mycursor.close()
            self.mydb.close()
