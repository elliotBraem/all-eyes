# coding: utf-8
from imutils import face_utils
from scipy.spatial import distance as dist
import numpy as np
import argparse
import imutils
import dlib
import cv2

OPEN_THRESHOLD = 0.2

def is_open(eye):
    # euclidean distances between vertical pairs.
    a = dist.euclidean(eye[1], eye[5])
    b = dist.euclidean(eye[2], eye[4])

    # euclidean distance between horizontal pair
    c = dist.euclidean(eye[0], eye[3])

    # compute the eye aspect ratio
    ratio = (a + b) / (2.0 * c)

    print(ratio)

    # return the eye aspect ratio
    return ratio >= OPEN_THRESHOLD

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

    # clone the original image
    clone = img.copy()

    # draw the right eye
    for (x, y) in shape[36:42]:
        cv2.circle(clone, (x, y), 1, (0, 0, 255), -1)

    left_eye = is_open(shape[36:42])
    right_eye = is_open(shape[42:48])

    print(left_eye)
    print(right_eye)

    # extract the ROI of the face region as a separate image
    (x, y, w, h) = cv2.boundingRect(np.array([shape[36:42]]))
    roi = img[y:y + h, x:x + w]
    roi = imutils.resize(roi, width=250, inter=cv2.INTER_CUBIC)

    # show the particular face part
    cv2.imshow("ROI", roi)
    cv2.imshow("Image", clone)
    cv2.waitKey(0)

    # clone the original image
    clone = img.copy()

    # draw the left eye
    for (x, y) in shape[42:48]:
        cv2.circle(clone, (x, y), 1, (0, 0, 255), -1)

    # extract the ROI of the face region as a separate image
    (x, y, w, h) = cv2.boundingRect(np.array([shape[42:48]]))
    roi = img[y:y + h, x:x + w]
    roi = imutils.resize(roi, width=250, inter=cv2.INTER_CUBIC)

    # show the particular face part
    cv2.imshow("ROI", roi)
    cv2.imshow("Image", clone)
    cv2.waitKey(0)

#     # visualize all facial landmarks with a transparent overlay
#    output = face_utils.visualize_facial_landmarks(img, shape)
#    cv2.imshow("Image", output)
#    cv2.waitKey(0)
#
cv2.waitKey(0)