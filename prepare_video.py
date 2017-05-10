import cv2
import os
import utils
import numpy as np
from skimage.transform import resize

VIDEONAME = '1'
def vid_cap():
    vidcap = cv2.VideoCapture(VIDEONAME+'.mp4')
    success,image = vidcap.read()
    count = 0
    success = True
    if not os.path.exists(VIDEONAME+'_frames'):
        os.mkdir(VIDEONAME+'_frames')
    while success:
      success, image = vidcap.read()
      img = np.array(image)
      img = utils.imcrop_tosquare(image)
      img = resize(img, (256, 256), mode="constant")*255
      print('Read a new frame: ', success)
      cv2.imwrite("video_frames/frame%d.jpg" % count, img)     # save frame as JPEG file
      count += 1
