# file  -- core.py --

import argparse
import dlib
import os
import cv2
from .utils import determine_base
from .replace_eye import do_swaps
from .face_detect import create_object_from_image
import os

IMAGES_PATH = "all_eyes/resources/images/"
PREDICTOR_PATH = "all_eyes/resources/shape_predictor_68_face_landmarks.dat"


# loads images from a folder and returns a list of these images
def load_images(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder, filename))
        if img is not None:
            images.append(img)
    return images

def main():
    # construct argument parser and parse the arguments
    ap = argparse.ArgumentParser()

    ap.add_argument("-b", "--base-image", required=False, help="image to use as base")
    args = vars(ap.parse_args())

    # load the images
    images = load_images(IMAGES_PATH)

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
        base_image = create_object_from_image(cv2.imread(IMAGES_PATH + "/" + args["base_image"]), detector, predictor)
    else:
        base_image = determine_base(image_objects)

    do_swaps(base_image, image_objects)

    cv2.imshow("Completed Image", base_image.image)
    cv2.waitKey(0)