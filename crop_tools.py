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
             for fname in os.listdir(dirname) if fname.endswith('.png') or fname.endswith('.jpg')]

filenames = np.asarray(filenames)
filenames_split = np.array_split(filenames, NUM_OF_THREADS)

print(filenames)

if not os.path.exists(BLUR_DIRNAME):
    os.mkdir(BLUR_DIRNAME)

if not os.path.exists(CROP_DIRNAME):
    os.mkdir(CROP_DIRNAME)

def save_cropped(filenames_arr):
    for fname in filenames_arr:
        img = scipy.misc.imread(fname)
        fname = fname.split('/')[-1]
        img = utils.imcrop_tosquare(img)
        img = resize(img, (512, 512))
        b_img = gaussian(img, sigma=11, mode='constant')
        filename = dirname.split('.')[-1]
        b_fname = '{}/{}_{}'.format(BLUR_DIRNAME, filename, fname)
        scipy.misc.imsave(b_fname, b_img)
        # a_fname = '{}/{}_{}'.format(CROP_DIRNAME, filename, fname)
        # print('a_filename', a_fname)
        # scipy.misc.imsave(a_fname, img)
        # scipy.misc.imsave(b_fname, b_img)


pool.map(save_cropped, filenames_split)

#save_cropped(filenames_split)
