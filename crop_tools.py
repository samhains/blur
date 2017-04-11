import os
import utils
import matplotlib.pyplot as plt
from skimage.transform import resize
from multiprocessing.dummy import Pool as ThreadPool 
import numpy as np

NUM_OF_THREADS=100

pool = ThreadPool(NUM_OF_THREADS) 
dirname = './images'

# Load every image file in the provided directory
filenames = [os.path.join(dirname, fname)
             for fname in os.listdir(dirname) if fname.endswith('.jpg')]

filnames = np.asarray(filenames)
filenames_split = np.array_split(filenames, NUM_OF_THREADS)

#os.mkdir('cropped')
# Then resize the square image to 100 x 100 pixels
def save_cropped(filenames_arr):
    for fname in filenames_arr:
        img = plt.imread(fname)
        fname = fname.split('/')[-1]
        if(img.shape[0] > 256 and img.shape[1] > 256):
            img = utils.imcrop_tosquare(img)
            img = resize(img, (256, 256))
            fname = './cropped/'+fname

            plt.imsave(fname, arr=img)

#os.mkdir('ordered')
def order(filenames):
    i = 1
    for fname in filenames:
        img = plt.imread(fname)
        plt.imsave("./ordered/{}.jpg".format(i), arr=img)
        i = i + 1

#results = pool.map(save_cropped, filenames_split)
order(filenames)
