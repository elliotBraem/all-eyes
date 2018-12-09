from imutils import face_utils
from scipy.spatial import distance as dist
from dlib import rectangle as Rectangle
import numpy as np
import argparse
import imutils
import dlib
import os
import cv2

OPEN_THRESHOLD = 0.2
PREDICTOR_PATH = "resources/shape_predictor_68_face_landmarks.dat"
MATCH_DISTANCE = 30


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


# takes a list of image objects and determines best base (number of faces with eyes open)
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


# loads images from a folder and returns a list of these images
def load_images(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder, filename))
        if img is not None:
            images.append(img)
    return images


# if either eye is closed, we will determine that a swap is needed.
def swap_needed(left_eye, right_eye):
    left_open = is_eye_open(left_eye)
    right_open = is_eye_open(right_eye)

    if not right_open or not left_open:
        return True
    else:
        return False


# determines if the eye is open or closed based on a ratio of top and bottom to sides of the eye
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


# checks the center of the faces, if they are within the threshold to match, we return that they are the same.
def matches(face1, face2):
    dif_center = dlib.rectangle.center(face1.face_position) - dlib.rectangle.center(face2.face_position)
    if abs(dif_center.x) > MATCH_DISTANCE:
        return False
    elif abs(dif_center.y) > MATCH_DISTANCE:
        return False
    else:
        return True


# takes an image, overlay image, and bounds to draw overlay, places this over image
# todo: make this better
def blend(image, overlay, rect):
    x1 = rect.left()
    x2 = rect.right()
    y1 = rect.top()
    y2 = rect.bottom()

    image[y1:y2, x1:x2] = overlay
    return


# creates a new rectangle shifted by a movement vector
def shift_it(rect, vector):
    l = rect.left() + vector.x
    t = rect.top() + vector.y
    r = rect.right() + vector.x
    b = rect.bottom() + vector.y

    return Rectangle(l, t, r, b)


# performs a swap of a face onto the base face, gets a face with eyes closed and a matching face with eyes open
def swap(base_face, face):

    # create new face object, this will have same image as base_face for now.
    new_face = Face()
    new_face.face_image = base_face.face_image

    # find difference between left and right eye based on center
    left_dif = base_face.left_eye_rect.center() - face.left_eye_rect.center()
    right_dif = base_face.right_eye_rect.center() - face.right_eye_rect.center()

    # create location of new eyes based on shape of new eyes and position of old eyes
    new_left_location = shift_it(face.left_eye_rect, left_dif)
    new_right_location = shift_it(face.right_eye_rect, right_dif)

    # draw the new eyes onto the new face
    blend(new_face.face_image, face.left_eye_image, new_left_location)
    blend(new_face.face_image, face.right_eye_image, new_right_location)

    # set data for new face and return
    new_face.face_position = base_face.face_position
    new_face.eyes_open = True
    new_face.left_eye_rect = new_left_location
    new_face.right_eye_rect = new_right_location
    new_face.left_eye_image = face.left_eye_image
    new_face.right_eye_image = face.right_eye_image

    return new_face


# returns a 2d matrix with the first index of each being the base_image image and the rest
# as matched faces to that image
def do_swaps(base_image, images):
    # loop through faces in base image looking for replacements
    for base_face_obj in base_image.faces:
        if not base_face_obj.eyes_open:

            # look through images to find replacement
            for image_obj in images:

                # only calling a match if they have same number of faces, this could be removed
                if len(image_obj.faces) == len(base_image.faces):
                    for face_obj in image_obj.faces:
                        # if the faces are a match and replaement has eyes open
                        if matches(base_face_obj, face_obj) and face_obj.eyes_open is True:
                            new_face_obj = swap(base_face_obj, face_obj)

                            # draw new face on image below
                            blend(base_image.image, new_face_obj.face_image, new_face_obj.face_position)
                            break


# takes an image and creates a face object to be used for swapping
def create_object_from_image(image, detector, predictor):
    current_object = Image()
    current_object.image = image

    # resize it
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

        # face position on original image
        face_object.face_position = rect

        (x, y, w, h) = face_utils.rect_to_bb(rect)
        face_object.face_image = image[y:y + h, x:x + w]

        right_eye = shape[42:48]
        left_eye = shape[36:42]

        face_object.left_eye_position = left_eye
        face_object.right_eye_position = right_eye

        (x, y, w, h) = cv2.boundingRect(np.array(left_eye))
        face_object.left_eye_image = image[y:y + h, x:x + w]

        # todo just use shiftit for this...
        face_object.left_eye_rect = Rectangle(x - face_object.face_position.left(),
                                                y - face_object.face_position.top(),
                                                x + w - face_object.face_position.left(),
                                                y + h - face_object.face_position.top())

        (x, y, w, h) = cv2.boundingRect(np.array(right_eye))
        face_object.right_eye_image = image[y:y + h, x:x + w]
        # todo and this
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

do_swaps(base_image, image_objects)

cv2.imshow("Finished", base_image.image)
cv2.waitKey(0)
