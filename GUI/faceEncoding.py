import cv2
import face_recognition
import numpy
import json

Encodings = {"encoding" : [], "name" : []}
face_cascade = cv2.CascadeClassifier('casc/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('casc/haarcascade_eye.xml')

def getEncoding(cv2Image):
    rgb = cv2.cvtColor(cv2Image, cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(rgb, model="hog") # hog or cnn these are face detection algorithms
    return face_recognition.face_encodings(rgb, boxes)

def addToEncoding(data):
    for x in data:
        print("Printing: {0}".format(x))
        Encodings["encoding"].append(json.loads(x[2]))
        Encodings["name"].append(x[1])

def faceDectImage(imagePath):
    names = []

    known = cv2.imread(imagePath)
    known_encoding = getEncoding(known) #face_recognition.face_encodings(known)[0]

    rgb = cv2.cvtColor(known, cv2.COLOR_BGR2RGB)
    #rgb = imutils.resize(rgb, width=750)
    r = known.shape[1] / float(rgb.shape[1])

    boxes = face_recognition.face_locations(known, 1,"hog")

    print(Encodings)
    print(boxes)

    for j in range(len(known_encoding)):
        counts = {}

        for x in range(len(Encodings["encoding"])):
            print("Known encoding: {0}  {1}".format(type(known_encoding[j]), known_encoding[j]))
            print("Encoding:  {0}   {1}".format(type(Encodings["encoding"][x]), Encodings["encoding"][x]))
            temp = numpy.asarray(Encodings["encoding"][x])
            print("Encoding:  {0}   {1}".format(type(temp), temp))

            print("J: {0}".format(str(j)))
            print("X: {0}".format(str(x)))

            print(numpy.array_equal(known_encoding[j],temp))

            result = face_recognition.compare_faces([known_encoding[j]], temp) #, tolerance = 0.6
            print(result)
        
            if result[0] == True:
                name = Encodings["name"][x]
                counts[name] = counts.get(name, 0) + 1

        if counts:
            name = max(counts, key=counts.get)

            names.append(name)

            print(counts)
            print(name)
        else:
            names.append("unknown")

    gray = cv2.cvtColor(known, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    #names.reverse()

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


def faceDectVideo(filePath):
    names = []
    count = 0

    if filePath is None:
        vidStream = cv2.VideoCapture(0)
    else:
        vidStream = cv2.VideoCapture(filePath)

    writer = None

    while True:
        count += 1

        if count % 30 == 0:
            (grabbed, frame) = vidStream.read()

            if not grabbed: # if we havent got a frame were at the end of the video
                break

            known_encoding = getEncoding(frame) #face_recognition.face_encodings(known)[0]

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            r = frame.shape[1] / float(rgb.shape[1])

            boxes = face_recognition.face_locations(frame, 1,"hog")

            #print(boxes)

            for j in range(len(known_encoding)):
                counts = {}

                for x in range(len(Encodings["encoding"])):
                    #print("Known encoding: {0}  {1}".format(type(known_encoding[j]), known_encoding[j]))
                    #print("Encoding:  {0}   {1}".format(type(Encodings["encoding"][x]), Encodings["encoding"][x]))
                    temp = numpy.asarray(Encodings["encoding"][x])
                    #print("Encoding:  {0}   {1}".format(type(temp), temp))

                    #print("J: {0}".format(str(j)))
                    #print("X: {0}".format(str(x)))

                    #print(numpy.array_equal(known_encoding[j],temp))

                    result = face_recognition.compare_faces([known_encoding[j]], temp) #, tolerance = 0.6
        
                    if result[0] == True:
                        name = Encodings["name"][x]
                        counts[name] = counts.get(name, 0) + 1

                if counts:
                    name = max(counts, key=counts.get)
                    names.append(name)
                else:
                    names.append("unknown")

                #print(counts)
                #print(name)

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            names.reverse()

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