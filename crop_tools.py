from sys import argv
from PIL import Image
import os
from natsort import natsorted, ns
import utils
import matplotlib.pyplot as plt
from skimage.transform import resize
import numpy as np

dirname = path

# Load every image file in the provided directory
filenames = [os.path.join(dirname, fname)
             for fname in os.listdir(dirname) if fname.endswith('.jpg')]

os.mkdir('cropped')
# Then resize the square image to 100 x 100 pixels
for fname in filenames:
    img = plt.imread(fname)
    if(img.shape[0] > 256 and img.shape[1] > 256):
        img = utils.imcrop_tosquare(img)
        img = resize(img, (256, 256))
        fname = './cropped'+fname.split('/')[-1]
        plt.imsave(fname, arr=img)
