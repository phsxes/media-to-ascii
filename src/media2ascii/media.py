from moviepy.editor import ImageSequenceClip
from moviepy.editor import VideoFileClip
import media2ascii.ascii
from tqdm import tqdm
import logging
import os.path
import cv2

# Logger
log = logging.getLogger(__name__)


def _get_frames_from_media(data):
    frame_number, frame_list = 0, []
    while True:
        frames_left, frame_array = data.read()
        frame_list.append(frame_array)
        if not frames_left:
            return frame_list
        frame_number += 1


def validate(path):
    ext = os.path.splitext(path)[1]
    media_type = {'img': False, 'video': False}
    img = cv2.imread(path)

    if img is not None and ext.lower() != '.gif':
        media_type['img'] = True
        return media_type

    vid = cv2.VideoCapture(path)
    if vid is not None:
        media_type['video'] = True
    return media_type


def get_ascii_from_image(path):
    log.info(f"Reading {path.split('/')[-1]}...")
    img = cv2.imread(path)
    ext = os.path.splitext(path)[1]
    ranges = media2ascii.ascii.get_ranges()
    ascii_img = media2ascii.ascii.generate_ascii(img, ranges)
    log.info(f"ASCII image generated. Saving...")
    cv2.imwrite(f'ascii{ext}', ascii_img)
    log.info(f"Done.")


def get_ascii_from_media(path):
    name, ext = os.path.splitext(path)
    log.info(f"Starting conversion of {path.split('/')[-1]}...")
    data = cv2.VideoCapture(path)
    fps = VideoFileClip(path).fps
    frames = _get_frames_from_media(data)
    ranges = media2ascii.ascii.get_ranges()
    result = []

    for frame in tqdm(frames):
        if frame is None:
            continue
        generated_frame = media2ascii.ascii.generate_ascii(frame, ranges)
        rgb_frame = cv2.cvtColor(generated_frame, cv2.COLOR_BGR2RGB)
        result.append(rgb_frame)

    log.info(f"ASCII media generated. Saving...")
    with ImageSequenceClip(result, fps=int(fps)) as clip:
        clip.write_gif(f'ASCII{ext}')
    log.info(f"Done.")
