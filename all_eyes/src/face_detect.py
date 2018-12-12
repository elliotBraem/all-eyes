# file  -- face_detect.py --

from imutils import face_utils
from dlib import rectangle as Rectangle
import numpy as np
import cv2
from .utils import swap_needed


class Image:
    def __init__(self):
        pass

    name = None
    image = None
    faces = []


class Face:
    def __init__(self):
        pass

    left_eye_image = None
    right_eye_image = None
    face_image = None
    left_eye_position = None
    right_eye_position = None
    left_eye_rect = None
    right_eye_rect = None
    face_position = None

    eyes_open = True


# takes an image and creates a face object to be used for swapping
def create_object_from_image(image, detector, predictor):
    current_object = Image()
    current_object.image = image

    # resize the image
    # image = imutils.resize(image, width=500)

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

        # isolate face position on original image
        face_object.face_position = rect

        (x, y, w, h) = face_utils.rect_to_bb(rect)
        face_object.face_image = image[y:y + h, x:x + w]

        # isolate right and left eye
        right_eye = shape[42:48]
        left_eye = shape[36:42]

        face_object.left_eye_position = left_eye
        face_object.right_eye_position = right_eye

        # gather shape and image of left eye
        (x, y, w, h) = cv2.boundingRect(np.array(left_eye))
        face_object.left_eye_image = image[y:y + h, x:x + w]

        face_object.left_eye_rect = Rectangle(x - face_object.face_position.left(),
                                                y - face_object.face_position.top(),
                                                x + w - face_object.face_position.left(),
                                                y + h - face_object.face_position.top())

        # gather shape and image of right eye
        (x, y, w, h) = cv2.boundingRect(np.array(right_eye))
        face_object.right_eye_image = image[y:y + h, x:x + w]
        face_object.right_eye_rect = Rectangle(x - face_object.face_position.left(),
                                               y - face_object.face_position.top(),
                                               x + w - face_object.face_position.left(),
                                               y + h - face_object.face_position.top())

        if swap_needed(left_eye, right_eye):
            face_object.eyes_open = False
        else:
            face_object.eyes_open = True

        image_faces.append(face_object)
    current_object.faces = image_faces
    return current_object
