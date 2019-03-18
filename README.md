# Facial Recognition

In this directory we will provide the entirety of the source code in Python for facial recognition on photos/videos/live videos.

## GUI

A GUI has been implemented with Tkinter which provides functionality for photos, video and webcams.

### Setting up the GUI scripts:

1. Clone this repository onto your local machine and install Python and MySQL if not already installed.
2. Using pip install the necessary python libraries (some may be default with your python installation):
- tkinter
- cv2
- face_recognition
- numpy
- json
- imutils
- base64
- PIL
- mysql-connector
3. Start mysqld, login to MySQL and run the 'mysqlDB.sql' SQL script (copy and paste works fine).
4. Start the GUI from the Gui.py script.

### Using the GUI

1. Once the GUI is running your going to want to add some people and images (or you'll only detect unknowns).
2. To add a person go to the database tab and select 'Add Person' fill out there details add a photo of them and submit.
3. If you want to add more photos of the same person select 'Add Photo', you'll only need there pid (Person ID) but there's an option to search by name, add a different photo and submit.   
4. You can also add footballers from the internet with the footballers.py script
5. **If a photo is in the database it isn't necessarily used in facial recognition** it needs to be encoded first to do this go to the database tab and select 'Run Encoder' if there are unencoded images in the database it will let you encode them.
6. On the main window select a video (need to change 'jpeg files' to 'all files' to see videos in the file explorer) or image then press the corresponding button to run it, or the webcam button which requires no input just a webcam.

## Fixes

- Video/Webcam still slow despite previous fixes
- GUI could be redesigned better
- GUI currently makes use of the debug console to show details of people detected in photo/video
- Currently no executable version
