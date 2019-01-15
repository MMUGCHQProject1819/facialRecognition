import numpy as np
import cv2
#Loading the instructions
face_cascade = cv2.CascadeClassifier('casc/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('casc/haarcascade_eye.xml')

#loading the image
img = cv2.imread('img/test.jpg')

#converting to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

faces = face_cascade.detectMultiScale(gray, 1.3, 5)

#Calculations to draw the rectangle on face
for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
    roi_gray = gray[y:y+h, x:x+w]
    roi_color = img[y:y+h, x:x+w]
    #detect eyes
    eyes = eye_cascade.detectMultiScale(roi_gray)
    #draw circle on eyes
    for (ex, ey, ew, eh) in eyes:
        cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

cv2.imshow('img', img)
cv2.waitKey(0)
cv2.destroyAllWindows()