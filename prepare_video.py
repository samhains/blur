import cv2
import os
import utils
import numpy as np
from skimage.transform import resize
from skimage.filters import gaussian


dirname = './videos'

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
    count = 0
    while success:
        success, image = vidcap.read()
        if success:
            img = np.array(image)
            img = utils.imcrop_tosquare(img)
            img = resize(img, (512, 512), mode="constant")

            img = gaussian(img, sigma=12, multichannel=True)*255
            print('Read a new frame: ', success)
            cv2.imwrite("video_frames/{}frame{}.jpg".format(video_count, count), img)     # save frame as JPEG file
            count += 1

video_count = 0
for fname in images:
    video_count += 1
    vid_cap(fname, video_count)
