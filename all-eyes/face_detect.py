from imutils import face_utils
from scipy.spatial import distance as dist
import numpy as np
import argparse
import imutils
import dlib
import os
import cv2

OPEN_THRESHOLD = 0.2
PREDICTOR_PATH = "resources/shape_predictor_68_face_landmarks.dat"


class Image:
    def __init__(self):
        pass

    image = None
    faces = None


class Face:
    def __init__(self):
        pass

    left_eye_image = None
    right_eye_image = None
    face_image = None
    left_eye_position = None
    right_eye_position = None
    face_position = None

    eyes_open = None


def determine_base(image_objs):
    base = None
    num_open = 0

    for obj in image_objs:
        current_open = 0
        for face in obj.faces:
            if face.eyes_open is True:
                current_open = current_open + 1
        if current_open > num_open:
            base = obj
            num_open = current_open
    return base


def load_images(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder, filename))
        if img is not None:
            images.append(img)
    return images


def swap_needed(left_eye, right_eye):
    left_open = is_eye_open(left_eye)
    right_open = is_eye_open(right_eye)

    if not right_open or not left_open:
        return True
    else:
        return False


def is_eye_open(eye):
    # euclidean distances between vertical pairs.
    a = dist.euclidean(eye[1], eye[5])
    b = dist.euclidean(eye[2], eye[4])

    # euclidean distance between horizontal pair
    c = dist.euclidean(eye[0], eye[3])

    # compute the eye aspect ratio
    ratio = (a + b) / (2.0 * c)

    # return the eye aspect ratio
    return ratio >= OPEN_THRESHOLD


def create_object_from_image(image, detector, predictor):
    current_object = Image()
    current_object.image = image

    # resize it
    image = imutils.resize(image, width=500)

    # convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # detect faces in the grayscale image
    # second param is number of pyramid layers/ increases resolution of image
    rects = detector(gray, 2)

    image_faces = []
    # loop over the face detections
    for (i, rect) in enumerate(rects):
        face_object = Face()
        # determine the facial landmarks for the face region, then
        # convert the facial landmark (x, y)-coordinates to a NumPy
        # array
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        # clone the original image
        #    clone = img.copy()

        face_object.face_position = rect

        (x, y, w, h) = face_utils.rect_to_bb(rect)
        face_object.face_image = image[y:y + h, x:x + w]

        left_eye = shape[42:48]
        right_eye = shape[36:42]

        face_object.left_eye_position = left_eye
        face_object.right_eye_position = right_eye

        (x, y, w, h) = cv2.boundingRect(np.array(left_eye))
        face_object.left_eye_image = image[y:y + h, x:x + w]

        (x, y, w, h) = cv2.boundingRect(np.array(right_eye))
        face_object.right_eye_image = image[y:y + h, x:x + w]

        if swap_needed(left_eye, right_eye):
            face_object.eyes_open = False
        else:
            face_object.eyes_open = True

        image_faces.append(face_object)
        current_object.faces = image_faces
    return current_object


# construct argument parser and parse the arguments
# this may be changed to constants
ap = argparse.ArgumentParser()
# ap.add_argument("-p", "--shape-predictor", required=True, help="path to facial landmark predictor")
# ap.add_argument("-i", "--image", required=True, help="path to input image")
ap.add_argument("-b", "--base-image", required=False, help="image to use as base image")
ap.add_argument("-f", "--folder", required=True, help="folder containing input images")
args = vars(ap.parse_args())

images = load_images(args["folder"])
image_objects = []
base_image = None

# initialize dlib's face detector (HOG-based)
detector = dlib.get_frontal_face_detector()
# create the facial landmark predictor
predictor = dlib.shape_predictor(PREDICTOR_PATH)

if images is not None:
    for image in images:
        image_objects.append(create_object_from_image(image, detector, predictor))

if args["base_image"] is not None:
    base_image = create_object_from_image(cv2.imread(args["base_image"]), detector, predictor)
else:
    base_image = determine_base(image_objects)

cv2.imshow("ok", base_image.image)
cv2.waitKey(0)

# if images is not None:
#    output = begin(images, base_image)
#    cv2.imshow("Output", output)
#    cv2.waitKey(0)
# else:
#    print("No images in given source folder.")
