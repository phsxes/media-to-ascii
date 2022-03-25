import numpy as np
import cv2


def get_ranges():
    symbols = " '`^\",:;Il!i><~+_-?][}{1)(|/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
    step = 255 / len(symbols)
    ranges = np.arange(0, 255 + step, step)
    ranges = dict(zip(ranges, symbols))
    return ranges


def generate_ascii(frame, ranges):

    # "Pixelating" reference media-to-ascii to smooth out busy images
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    height, width = gray.shape[:2]
    h, w = (int(height / 7), int(width / 5))
    temp = cv2.resize(gray, (w, h), interpolation=cv2.INTER_LINEAR)
    reference = cv2.resize(temp, (width, height), interpolation=cv2.INTER_NEAREST)

    # Generating empty result media-to-ascii and character to intensity mapping
    result = np.zeros((height, width, 3), np.uint8)

    # Iterating over reference media-to-ascii and defining "windows" to calculate
    # average intensity and apply a character
    for y in range(13, height, 13):
        for x in range(0, width, 10):
            window = reference[y:y + 13, x:x + 10]
            wdw_color = frame[y:y + 13, x:x + 10, :]
            colors, count = np.unique(wdw_color.reshape(-1, wdw_color.shape[-1]),
                                      axis=0, return_counts=True)
            bg_color = [int(i) for i in colors[count.argmax()]]
            avg = np.average(window)
            closest_key = min(ranges.keys(), key=lambda i: abs(i - avg))
            result = cv2.putText(result, ranges[closest_key], (x, y),
                                 cv2.FONT_HERSHEY_SIMPLEX, 0.3, bg_color, 1)
    return result
