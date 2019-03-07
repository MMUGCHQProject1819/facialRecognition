import cv2
import face_recognition

def getEncoding(cv2Image):
    rgb = cv2.cvtColor(cv2Image, cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(rgb, model="hog") # hog or cnn these are face detection algorithms
    return face_recognition.face_encodings(rgb, boxes)
