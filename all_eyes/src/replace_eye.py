# file  -- replace_eye.py --

from .face_detect import Face
from .utils import matches
from .inpaint import blend, shift_it


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
