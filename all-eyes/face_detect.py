import numpy as np
import cv2
import sys

# Path to the input image
imgPath = 'abba.png'

# Paths to the XML classifiers
faceCascPath = "resources/haarcascade_frontalface_default.xml"
eyeCascPath = "resources/haarcascade_eye.xml"

# Load the required XML classifiers
face_cascade = cv2.CascadeClassifier(faceCascPath)
eye_cascade = cv2.CascadeClassifier(eyeCascPath)

# Load the image
img = cv2.imread(imgPath)
# Convert to grayscale
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detect faces in the image
faces = face_cascade.detectMultiScale(
    img_gray,
    scaleFactor=1.3,
    minNeighbors=5
)
# For each face found (x,y are coordinates, w,h are width and height)
for (x,y,w,h) in faces:
    # Draw a rectangle around the face
    img = cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
    # Create a ROI (region of interest) for the face
    roi_gray = img_gray[y:y+h, x:x+w]
    roi_color = img[y:y+h, x:x+w]
    # Detect the eyes on the face
    eyes = eye_cascade.detectMultiScale(roi_gray)
    # For each eye found
    for (ex,ey,ew,eh) in eyes:
        cv2.rectangle(roi_color, (ex,ey), (ex+ew, ey+eh), (0,255,0), 2)

# Show results
cv2.imshow("Face & Eye Detection Results", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
