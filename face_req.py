import numpy as np #importing a libary
import cv2 #importing a libary

img = cv2.imread("hqdefault.jpg", 1)  #Reads in the file
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)  #Converts the colour of the image
path = "haarcascade_frontalface_default.xml"  #The library path of faces

face_cascade = cv2.CascadeClassifier(path) #loading the cascade file

faces = face_cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=5, minSize=(40,40)) #detects the multiple greys
print(len(faces)) #amount of items in the object being printed

for (x, y, w, h) in faces: #all positions on the face
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.imshow("Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()