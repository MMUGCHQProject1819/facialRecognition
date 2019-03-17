import sys
import cv2
import face_recognition
import numpy
import json
import time
import imutils
from threading import Thread

if sys.version_info >= (3, 0): # import for python 3.x
    from queue import Queue
else:
    from Queue import Queue # import for python 2.7

from personDAO import *

class videoStream: # handles a thread that reads frames while other processes occur (speeding up the video)
    def __init__(self, path):
        self.queue = Queue(200)
        if path:
            self.stream = cv2.VideoCapture(path)
            self.running = True        

    def start(self):
        t = Thread(target=self.update,args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        while True:
            if not self.running: # stop the thread no longer running
                return 
            
            if not self.queue.full():
                (grabbed, frame) = self.stream.read()

                if not grabbed:
                    self.stop()
                    return

                self.queue.put(frame)

    def stop(self):
        self.running = False

    def read(self):
        return self.queue.get() # get next frame

    def more(self):
        return self.queue.qsize() > 0 # true if there are still frames left

    def webCamMode(self): # means more will always return true so can be used for webcam
        self.queue.put('1')


Encodings = {"encoding" : [], "name" : []}
face_cascade = cv2.CascadeClassifier('casc/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('casc/haarcascade_eye.xml')

def getEncoding(cv2Image):
    rgb = cv2.cvtColor(cv2Image, cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(rgb, model="hog") # hog or cnn these are face detection algorithms
    return face_recognition.face_encodings(rgb, boxes)

def addToEncoding(data):
    for x in data:
        Encodings["encoding"].append(json.loads(x[2]))
        Encodings["name"].append(x[1])

def faceDectImage(imagePath, DAO):
    names = []

    known = cv2.imread(imagePath)
    known_encoding = getEncoding(known) 
    
    rgb = cv2.cvtColor(known, cv2.COLOR_BGR2RGB)
    r = known.shape[1] / float(rgb.shape[1])

    boxes = face_recognition.face_locations(known, 1,"hog")

    for j in range(len(known_encoding)):
        counts = {}

        for x in range(len(Encodings["encoding"])):
            temp = numpy.asarray(Encodings["encoding"][x])

            result = face_recognition.compare_faces([known_encoding[j]], temp) #, tolerance = 0.6
        
            if result[0] == True:
                name = Encodings["name"][x]
                counts[name] = counts.get(name, 0) + 1

        if counts:
            name = max(counts, key=counts.get)
            names.append(name)
        else:
            names.append("unknown")

        for n in names:
            if n is not "unknown":
                print(DAO.getByName(n))

    gray = cv2.cvtColor(known, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for ((top, right, bottom, left), name) in zip(boxes, names):
		# rescale the face coordinates
        top = int(top * r)
        right = int(right * r)
        bottom = int(bottom * r)
        left = int(left * r)

		# draw the predicted face name on the image
        cv2.rectangle(known, (left, top), (right, bottom),
			(0, 255, 0), 2)
        y = top - 15 if top - 15 > 15 else top + 15
        cv2.putText(known, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
			0.75, (0, 255, 0), 2)

    cv2.imshow('ImageWindow',known)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def faceDectVideo(filePath, DAO):
    vStream = None
    vidStream = None
    mode = False

    printedNames = []
    names = []

    if filePath:
        mode = True
        vStream = videoStream(filePath)
        vStream.start() # start reading and queuing frames
        time.sleep(1.0) # make sure thread and first frame have started
    else:
        vidStream = cv2.VideoCapture(0)
        vStream = videoStream(None)
        vStream.webCamMode()

    writer = None

    while vStream.more():
        if mode:
            frame = vStream.read()
        else:
            (grabbed, frame) = vidStream.read()

        frame = imutils.resize(frame, width=450)

        known_encoding = getEncoding(frame) #face_recognition.face_encodings(known)[0]

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        r = frame.shape[1] / float(rgb.shape[1])

        boxes = face_recognition.face_locations(frame, 1,"hog")

        for j in range(len(known_encoding)):
            counts = {}

            for x in range(len(Encodings["encoding"])):
                temp = numpy.asarray(Encodings["encoding"][x])

                result = face_recognition.compare_faces([known_encoding[j]], temp) #, tolerance = 0.6
        
                if result[0] == True:
                    name = Encodings["name"][x]
                    counts[name] = counts.get(name, 0) + 1

            if counts:
                name = max(counts, key=counts.get)
                names.append(name)
            else:
                names.append("unknown")

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for n in names:
            if n is not "unknown":
                if n not in printedNames:
                    printedNames.append(n)
                    print(DAO.getByName(n))

        for ((top, right, bottom, left), name) in zip(boxes, names):
            top = int(top * r)
            right = int(right * r)
            bottom = int(bottom * r)
            left = int(left * r)

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2) 
            
            y = top - 15 if top - 15 > 15 else top + 15
            
            cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

            if writer is not None:
                writer.write(frame)
            

        cv2.imshow("Frame", frame)
            
        key = cv2.waitKey(1) & 0xFF
 
        if key == ord("q"):
           break

    cv2.destroyAllWindows()

    vidStream.release()
 
    if writer is not None:
        writer.release()