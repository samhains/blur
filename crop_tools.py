import os
from PIL import Image, ImageFilter
import uuid
import utils
import matplotlib.pyplot as plt
from skimage.transform import resize
from multiprocessing.dummy import Pool as ThreadPool 
from skimage.filters import gaussian
import numpy as np
import scipy

NUM_OF_THREADS = 1
FINAL_SLICE_SIZE = 512

filename = 'insta_images'
dirname = './'+filename
BLUR_DIRNAME = dirname+'_blurred'
CROP_DIRNAME = dirname+'_cropped'

pool = ThreadPool(NUM_OF_THREADS) 

# Load every image file in the provided directory
filenames = [os.path.join(dirname, fname)
             for fname in os.listdir(dirname) if fname.endswith('.png') or fname.endswith('.jpg')]

filenames = np.asarray(filenames)
filenames_split = np.array_split(filenames, NUM_OF_THREADS)


if not os.path.exists(BLUR_DIRNAME):
    os.mkdir(BLUR_DIRNAME)

if not os.path.exists(CROP_DIRNAME):
    os.mkdir(CROP_DIRNAME)

def save_cropped(filenames_arr):
    for fname in filenames_arr:
        img = scipy.misc.imread(fname)
        fname = fname.split('/')[-1]
        img = utils.imcrop_tosquare(img)
        img = resize(img, (FINAL_SLICE_SIZE, FINAL_SLICE_SIZE))
        img = gaussian(img, sigma=12, mode='constant')*255
        img = img.astype('uint8') 
        new_img = Image.new('RGB', (FINAL_SLICE_SIZE*2, FINAL_SLICE_SIZE))
        img = Image.fromarray(img)
        new_img.paste(img, (0, 0))
        # new_img.paste(img)
        img = new_img
        # filename = dirname.split('.')[-1]
        b_fname = '{}/_{}.png'.format(BLUR_DIRNAME, uuid.uuid4())
        print(b_fname)
        print(b_fname)
        scipy.misc.imsave(b_fname, img)
        # a_fname = '{}/{}_{}'.format(CROP_DIRNAME, filename, fname)
        # print('a_filename', a_fname)
        # scipy.misc.imsave(a_fname, img)
        # scipy.misc.imsave(b_fname, b_img)


pool.map(save_cropped, filenames_split)

#save_cropped(filenames_split)
