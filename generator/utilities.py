from PIL import Image
from PIL import ImageTk
import cv2


def resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    # set initial dimensions, width and height
    d = None
    (h, w) = image.shape[:2]

    # return image if no params given
    if width is None and height is None:
        return image

    # determine ratio on whichever value was given
    if width is None:
        r = height / float(h)
        d = (int(w * r), height)
    else:
        r = width / float(w)
        d = (width, int(h * r))

    # return resized
    resized = cv2.resize(image, d, interpolation=inter)
    return resized


class TkImage:

    def __init__(self, path):
        self.path = path
        self.data = cv2.imread(path)

    def get_preview(self, w=None, h=None):
        resized = resize(self.data, width=w, height=h)
        img_color = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
        img_tk = Image.fromarray(img_color)
        image = ImageTk.PhotoImage(img_tk)
        return image
