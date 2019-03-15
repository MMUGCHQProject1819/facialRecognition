import cv2
import face_recognition
#import time
from imutils.video import VideoStream

Encodings = {"encoding" : [], "name" : []}
face_cascade = cv2.CascadeClassifier('casc/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('casc/haarcascade_eye.xml')
output = "img/output.mjpg"

def getEncoding(cv2Image):
    rgb = cv2.cvtColor(cv2Image, cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(rgb, model="hog") # hog or cnn these are face detection algorithms
    return face_recognition.face_encodings(rgb, boxes)

def createNameEncodingDict(NameEncoding):
    tempName = []
    tempEncoding = []

    for x in NameEncoding:
        temp = getEncoding(NameEncoding[x])
        for y in temp:
            tempName.append(x)
            tempEncoding.append(temp)

    return {"encoding" : tempEncoding, "name" : tempName}

def greatestOccurrence(inArray): # this could have terrible effiecency for long lists O(n^2)
    n = []
    for x in inArray:
        count = 0
        for i in inArray:
            if x == i:
                count += 1
        n[x] = count
    return max(n)

def addToEncoding(name, path):
    Encodings["encoding"].append(getEncoding(cv2.imread(path)))
    Encodings["name"].append(name)

if __name__ == "__main__":
    img = {}
    names = []

    addToEncoding("nixon", "img/nixon1.jpg")
    addToEncoding("nixon", "img/nixon2.jpg")

    vidStream = cv2.VideoCapture("img/nixon.mp4")
    writer = None


    while True: #cut out rest of the video (use opencv to cut faces out)

        (grabbed, frame) = vidStream.read() # skip a certain number of frames

        if not grabbed: # if we havent got a frame were at the end of the video
            break

        known_encoding = getEncoding(frame) #face_recognition.face_encodings(known)[0]

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        r = frame.shape[1] / float(rgb.shape[1])

        boxes = face_recognition.face_locations(frame, 1,"hog")

        print(boxes)

        for j in range(len(known_encoding)):
            counts = {}

            for x in range(len(Encodings["encoding"])):
                result = face_recognition.compare_faces(known_encoding[j - 1], Encodings["encoding"][x])
                print(result)

                if result[0] == True:
                    name = Encodings["name"][x]
                    counts[name] = counts.get(name, 0) + 1

            if len(counts) != 0:
                name = max(counts, key=counts.get)
                names.append(name)

            print(counts)
            print(name)

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
