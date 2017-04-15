import os
import utils
import matplotlib.pyplot as plt
from skimage.transform import resize
from multiprocessing.dummy import Pool as ThreadPool 
from skimage.filters import gaussian
import numpy as np
import scipy

NUM_OF_THREADS=10

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
        print(fname)
        img = scipy.misc.imread(fname)
        fname = fname.split('/')[-1]
        if(img.shape[0] > 256 and img.shape[1] > 256):
            img = utils.imcrop_tosquare(img)
            img = resize(img, (256, 256))
            b_fname = './blurred/'+fname
            img = resize(img, (32, 32))
            img = resize(img, (256, 256))
            scipy.misc.imsave(b_fname, img)


pool.map(save_cropped, filenames_split)
#save_cropped(filenames_split)
