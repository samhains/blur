import cv2
import os
import image_utils as utils
import numpy as np
from skimage.transform import resize
from PIL import Image, ImageFilter


dirname = './videos'
SIGMA = 11
NUM_FRAMES = 50

# Load every image file in the provided directory
images = [os.path.join(dirname, fname)
          for fname in os.listdir(dirname) if fname.endswith('.mp4')]

if not os.path.exists('video_frames'):
    os.mkdir('video_frames')

def vid_cap(video_path, video_count):
    video_path = video_path.split('.')[1]
    print('VIDEONAME', video_path)
    vidcap = cv2.VideoCapture('.'+video_path+'.mp4')
    success, image = vidcap.read()
    length = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    MOD_NUM = int(length/NUM_FRAMES)
    count = 0
    while success:
        success, image = vidcap.read()
        count += 1
        if success and count % MOD_NUM == 0:
            img = np.array(image)
            print(img)
            # img = img.astype('uint8')
            img = Image.fromarray(img)
            img.save("video_frames/{}frame{}.jpg".format(video_count, count))

video_count = 0
for fname in images:
    video_count += 1
    vid_cap(fname, video_count)
