import numpy as np
import cv2

#loading the image
img = cv2.imread("faces.jpeg", 1)

#Convert the image to gray-scale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#Load the instructions
path = "haarcascade_eye.xml"

eye_cascade = cv2.CascadeClassifier(path)

#Object = path.Detect multiple variants (make it gray, set the size of the detection, minimum detections that can be near it, make the size to be as small as 10,10 px.
eyes = eye_cascade.detectMultiScale(gray, scaleFactor=1.02, minNeighbors=5, minSize=(10, 10))

print(len(eyes))

#Calculations to draw the circle on eyes
for(x, y, w, h) in eyes:
    xc = (x + x+w)/2
    yc = (y + y+h)/2
    #Radius
    radius = w/2
    #Drawing the circle
    cv2.circle(img, (int(xc), int(yc)), int(radius), (255, 0, 0), 2)

#Display the image
cv2.imshow("Eyes", img)

cv2.waitKey(0)
cv2.destroyAllWindows()

#NOTE: the eye detection isn't perfect, we need to implement more training for the .xml file to better focus on what an eye is.
#(You can modify the scaleFactor & minSize to try and improve the Accuracy.