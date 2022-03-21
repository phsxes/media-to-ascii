from PIL import Image as PILImage
from PIL import ImageTk
import numpy as np
import cv2


class Image:

    def __init__(self, path):
        self.path = path
        self.data = cv2.imread(path)

    def resize(self, width=None, height=None):
        # setting initial variables
        d = None
        inter = cv2.INTER_AREA
        (h, w) = self.data.shape[:2]

        # returning image if no sizing param is given
        if width is None and height is None:
            return self.data

        # determine ratio on whichever value was given
        if width is None:
            r = height / float(h)
            d = (int(w * r), height)
        else:
            r = width / float(w)
            d = (width, int(h * r))

        # return resized numpy array
        resized = cv2.resize(self.data, d, interpolation=inter)
        return resized

    def preview(self, w=None, h=None):

        # Resizing image to fit preview panel
        resized = self.resize(width=w, height=h)

        # converting numpy array to Tk image
        pil_array = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
        img_tk = PILImage.fromarray(pil_array)
        image = ImageTk.PhotoImage(img_tk)
        return image


def get_ranges():
    symbols = " '`^\",:;Il!i><~+_-?][}{1)(|/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
    step = 255/len(symbols)
    ranges = np.arange(0, 255+step, step)
    ranges = dict(zip(ranges, symbols))
    return ranges


class Ascii(Image):

    def __init__(self, path):
        super().__init__(path)
        self.data = self.generate_ascii()

    def generate_ascii(self):
        image = self.data

        # "Pixelating" reference image to smooth out busy images
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        height, width = gray.shape[:2]
        h, w = (int(height / 13), int(width / 10))
        temp = cv2.resize(gray, (w, h), interpolation=cv2.INTER_LINEAR)
        reference = cv2.resize(temp, (width, height), interpolation=cv2.INTER_NEAREST)

        # Generating empty result image and character to intensity mapping
        result = np.zeros((height, width), np.uint8)
        ranges = get_ranges()

        # Iterating over reference image and defining "windows" to calculate
        # average intensity and apply a character
        for y in range(13, height, 13):
            for x in range(0, width, 10):
                window = reference[y:y + 13, x:x + 10]
                wdw_color = image[y:y + 13, x:x + 10, :]
                colors, count = np.unique(wdw_color.reshape(-1, wdw_color.shape[-1]), axis=0, return_counts=True)
                bg_color = [int(i) for i in colors[count.argmax()]]
                avg = np.average(window)
                closest_key = min(ranges.keys(), key=lambda i: abs(i - avg))
                result = cv2.putText(result, ranges[closest_key], (x, y),
                                     cv2.FONT_HERSHEY_SIMPLEX, 0.3, bg_color, 1)
        return result

    def save(self):
        cv2.imwrite("ASCII.png", self.data)
