# file  -- utils.py --

from scipy.spatial import distance as dist
import dlib


OPEN_THRESHOLD = 0.2
MATCH_DISTANCE = 30


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