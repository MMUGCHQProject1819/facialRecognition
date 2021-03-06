import os
import sys
import io
import base64
import json
from PIL import Image
import PIL.Image
import mysql.connector
from datetime import datetime
from mysql.connector import Error
from mysql.connector import errorcode

class Person:
    def __init__(self, pid, name = None, dob = None, nationality = None, height = 0, weight = 0, hair_colour = None, hair_style = None, skin_colour = None, facial_hair = None):
        self.pid = pid
        self.name = name 
        self.dob = self.rec(dob)
        self.nationality = self.rec(nationality)
        self.height = height
        self.weight = weight
        self.hair_colour = self.rec(hair_colour)
        self.hair_style = self.rec(hair_style)
        self.skin_colour = self.rec(skin_colour)
        self.facial_hair = self.rec(facial_hair)

    def __str__(self): # equivalent to override toString()
        return "PID: {0}\nName: {1}\nDOB: {2}\nNationality: {3}\nHeight: {4}\nWeight: {5}\nHair colour: {6}\nHair style: {7}\nSkin Colour: {8}\nFacial hair: {9}\n".format(str(self.pid), self.name, self.dob, self.nationality, self.rec(self.height), self.rec(self.weight), self.hair_colour, self.hair_style, self.skin_colour, self.facial_hair)
      
    def rec(self, record): # db record to string 
        if record is None:
            return "N/A"
        else:
            return str(record)

class Photo:
    def __init__(self, pid, image = None, encoding = None, encoded = None):
        self.pid = pid
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

    def insertPerson(self, person, photo): # p = person object
        try:
            self.mydb = self.connectToMysql()
            self.mycursor = self.mydb.cursor()
            self.mycursor.execute("INSERT INTO person (pid, name, dob, nationality, height, weight, hair_colour, hair_style, skin_colour,facial_hair) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (int(person.pid),person.name,person.dob,person.nationality,int(person.height),int(person.weight),person.hair_colour,person.hair_style,person.skin_colour,person.facial_hair))
            self.mycursor.execute("INSERT INTO photos (pid,image,encoding,encoded) VALUES ('%s','%s','%s','%s')" % (int(photo.pid),photo.image,'','0'))
            self.mydb.commit()
        except Error as e:
            if "10053" in str(e):
                print("File to big, this can be fixed in the mysql config just google the error message.")
            print(e)
        finally:
            self.mycursor.close()
            self.mydb.close()

    def insertPhoto(self, photo): # p = person object
        try:
            self.mydb = self.connectToMysql()
            self.mycursor = self.mydb.cursor()
            self.mycursor.execute("INSERT INTO photos (pid,image,encoding,encoded) VALUES ('%s','%s','%s','%s')" % (int(photo.pid),photo.image,'','0'))
            self.mydb.commit()
        except Error as e:
            if "10053" in str(e):
                print("File to big, this can be fixed in the mysql config just google the error message.")
            print(e)
        finally:
            self.mycursor.close()
            self.mydb.close()

    def updateEncoding(self, pid, encoding): 
        try:
            self.mydb = self.connectToMysql()
            self.mycursor = self.mydb.cursor()
            temp = json.dumps(encoding.tolist())
            self.mycursor.execute("UPDATE photos SET encoding='%s', encoded='1' WHERE pid='%s'" % (temp,pid))
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
            self.mycursor.execute("SELECT pid,image FROM photos WHERE encoded ='0'")
            self.result = self.mycursor.fetchall()
            self.mydb.commit()
        except Error as e:
            print(e)
        else:
            return self.result
        finally:
            self.mycursor.close()
            self.mydb.close()

    def getEncoded(self): 
        try:
            self.mydb = self.connectToMysql()
            self.mycursor = self.mydb.cursor()
            self.mycursor.execute("SELECT photos.pid,person.name,photos.encoding FROM photos INNER JOIN person ON photos.pid = person.pid WHERE photos.encoded ='1'")
            self.result = self.mycursor.fetchall()
            self.mydb.commit()
        except Error as e:
            print(e)
        else:
            return self.result
        finally:
            self.mycursor.close()
            self.mydb.close()

    def getByName(self, name): 
        try:
            self.mydb = self.connectToMysql()
            self.mycursor = self.mydb.cursor()
            self.mycursor.execute("SELECT * FROM person WHERE name='%s'" % (name))
            self.result = self.mycursor.fetchall()
            self.mydb.commit()
        except Error as e:
            print(e)
        else:
            p = self.result[0]
            return Person(p[0],p[1],p[2],p[3],p[4],p[5],p[6],p[7],p[8],p[9])
        finally:
            self.mycursor.close()
            self.mydb.close()
