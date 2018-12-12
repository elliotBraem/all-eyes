# file  -- inpaint.py --

from dlib import rectangle as rectangle


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

    return rectangle(l, t, r, b)
