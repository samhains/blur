import os
import utils
import matplotlib.pyplot as plt
from skimage.transform import resize
from multiprocessing.dummy import Pool as ThreadPool 
from skimage.filters import gaussian
import numpy as np
import scipy

NUM_OF_THREADS = 1

filename = 'images'
dirname = './'+filename
BLUR_DIRNAME = dirname+'_blurred'
CROP_DIRNAME = dirname+'_cropped'

pool = ThreadPool(NUM_OF_THREADS) 

# Load every image file in the provided directory
filenames = [os.path.join(dirname, fname)
             for fname in os.listdir(dirname) if fname.endswith('.jpg')]

filnames = np.asarray(filenames)
filenames_split = np.array_split(filenames, NUM_OF_THREADS)

os.mkdir(BLUR_DIRNAME)
# os.mkdir(CROP_DIRNAME)

# Then resize the square image to 100 x 100 pixels
def save_cropped(filenames_arr):
    for fname in filenames_arr[:10]:
        img = scipy.misc.imread(fname)
        fname = fname.split('/')[-1]
        img = utils.imcrop_tosquare(img)
        img = resize(img, (256, 256))
        b_img = gaussian(img, sigma=9)
        filename = dirname.split('.')[-1]
        # a_fname = '{}/{}_{}'.format(CROP_DIRNAME, filename, fname)
        # print('a_filename', a_fname)
        b_fname = '{}/{}_{}'.format(BLUR_DIRNAME, filename, fname)
        scipy.misc.imsave(b_fname, b_img)
        # scipy.misc.imsave(a_fname, img)


pool.map(save_cropped, filenames_split)

#save_cropped(filenames_split)
