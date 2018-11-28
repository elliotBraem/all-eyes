from imutils import face_utils
import numpy as np
import argparse
import imutils
import dlib
import cv2

# construct argument parser and parse the arguments
# this may be changed to constants
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", required =True, help="path to facial landmark predictor")
ap.add_argument("-i", "--image", required=True, help="path to input image")
args = vars(ap.parse_args())

# initialize dlib's face detector (HOG-based)
detector = dlib.get_frontal_face_detector()
# create the facial landmark predictor
predictor = dlib.shape_predictor(args["shape_predictor"])

# load the input image
img = cv2.imread(args["image"])
# resize it
img = imutils.resize(img, width=500)
# convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# detect faces in the grayscale image
# second param is number of pyramid layers/ increases resolution of image
rects = detector(gray, 2)

# loop over the face detections
for (i, rect) in enumerate(rects):
    # determine the facial landmarks for the face region, then
    # convert the facial landmark (x, y)-coordinates to a NumPy
    # array
    shape = predictor(gray, rect)
    shape = face_utils.shape_to_np(shape)

    # convert dlib's rectangle to a OpenCV-style bounding box
    # [i.e., (x, y, w, h)], then draw the face bounding box
    (x, y, w, h) = face_utils.rect_to_bb(rect)
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # show the face number
    cv2.putText(img, "Face #{}".format(i + 1), (x - 10, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # loop over the (x, y)-coordinates for the facial landmarks
    # and draw them on the image
    for (x, y) in shape:
        cv2.circle(img, (x, y), 1, (0, 0, 255), -1)

# show the output image with the face detections + facial landmarks
cv2.imshow("Output", img)
cv2.waitKey(0)

#
# # Path to the input image
# imgPath = 'elliot-family-test.jpg'
#
# # Paths to the XML classifiers
# faceCascPath = "resources/haarcascade_frontalface_default.xml"
# eyeCascPath = "resources/haarcascade_eye.xml"
#
# # Load the required XML classifiers
# face_cascade = cv2.CascadeClassifier(faceCascPath)
# eye_cascade = cv2.CascadeClassifier(eyeCascPath)
#
# # Load the image
# img = cv2.imread(imgPath)
# # Convert to grayscale
# img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#
# # Detect faces in the image
# faces = face_cascade.detectMultiScale(
#     img_gray,
#     scaleFactor=1.3,
#     minNeighbors=5
# )
# # For each face found (x,y are coordinates, w,h are width and height)
# for (x,y,w,h) in faces:
#     # Draw a rectangle around the face
#     img = cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
#     # Create a ROI (region of interest) for the face
#     roi_gray = img_gray[y:y+h, x:x+w]
#     roi_color = img[y:y+h, x:x+w]
#     # Detect the eyes on the face
#     eyes = eye_cascade.detectMultiScale(roi_gray)
#     # For each eye found
#     for (ex,ey,ew,eh) in eyes:
#         cv2.rectangle(roi_color, (ex,ey), (ex+ew, ey+eh), (0,255,0), 2)
#
# # Show results
# cv2.imshow("Face & Eye Detection Results", img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
