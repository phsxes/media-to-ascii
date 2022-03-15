from PIL import Image as PILImage
from PIL import ImageTk
import numpy as np
import cv2


class Image:

    def __init__(self, path):
        self.path = path
        self.data = cv2.imread(path)

    def resize(self, width=None, height=None):
        # set initial dimensions, width and height
        d = None
        inter = cv2.INTER_AREA
        (h, w) = self.data.shape[:2]

        # return image if no params given
        if width is None and height is None:
            return self.data

        # determine ratio on whichever value was given
        if width is None:
            r = height / float(h)
            d = (int(w * r), height)
        else:
            r = width / float(w)
            d = (width, int(h * r))

        # return resized
        resized = cv2.resize(self.data, d, interpolation=inter)
        return resized

    def preview(self, w=None, h=None):
        resized = self.resize(width=w, height=h)
        pil_array = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
        img_tk = PILImage.fromarray(pil_array)
        image = ImageTk.PhotoImage(img_tk)
        return image


class Ascii(Image):

    def __init__(self, path):
        super().__init__(path)
        self.data = self.generate_ascii()

    def generate_ascii(self):

        image = self.data
        height, width = image.shape[:2]
        h, w = (int(height/13), int(width/10))
        temp = cv2.resize(image, (w, h), interpolation=cv2.INTER_LINEAR)
        output = cv2.resize(temp, (width, height), interpolation=cv2.INTER_NEAREST)
        final = self.print_ascii(output)
        return final

    def print_ascii(self, reference):
        result = np.zeros((reference.shape[0], reference.shape[1], 3), np.uint8)
        for i in range(13, reference.shape[0], 13):
            for j in range(0, reference.shape[1], 10):
                result = cv2.putText(result, 'A', (j, i), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        return result
