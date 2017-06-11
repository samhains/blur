import os
import utils
import matplotlib.pyplot as plt
from skimage.transform import resize
from PIL import Image, ImageFilter
from multiprocessing.dummy import Pool as ThreadPool 
from skimage.filters import gaussian
import numpy as np
import scipy

NUM_OF_THREADS = 1
SIGMA = 12
FINAL_SLICE_SIZE = 512

filename = 'k'
dirname = './'+filename
BLUR_DIRNAME = dirname+'_blurred'
CROP_DIRNAME = dirname+'_cropped'

pool = ThreadPool(NUM_OF_THREADS) 

# Load every image file in the provided directory
filenames = [os.path.join(dirname, fname)
             for fname in os.listdir(dirname) if fname.endswith('.jpg')]

filenames = np.asarray(filenames)
filenames_split = np.array_split(filenames, NUM_OF_THREADS)

print(filenames)

if not os.path.exists(BLUR_DIRNAME):
    os.mkdir(BLUR_DIRNAME)

if not os.path.exists(CROP_DIRNAME):
    os.mkdir(CROP_DIRNAME)


def simple_crop(filenames_arr):

    for fname in filenames_arr:
        try:
            img = scipy.misc.imread(fname)
            fname = fname.split('/')[-1]
            img = utils.imcrop_tosquare(img)
            img = resize(img, (FINAL_SLICE_SIZE, FINAL_SLICE_SIZE))*255
            img = img.astype('uint8')
            img = Image.fromarray(img)
            filename = dirname.split('.')[-1]
            fname = '{}/{}_{}'.format(CROP_DIRNAME, filename, fname)
            img.save(fname)
        except:
            print('Thats not an image!', fname)



def simple_blur(filenames_arr):
    for fname in filenames_arr:
        img = scipy.misc.imread(fname)
        fname = fname.split('/')[-1]
        img = utils.imcrop_tosquare(img)
        img = resize(img, (FINAL_SLICE_SIZE, FINAL_SLICE_SIZE))*255
        img = img.astype('uint8')
        img = Image.fromarray(img)
        img = img.filter(ImageFilter.GaussianBlur(SIGMA))
        filename = dirname.split('.')[-1]
        fname = '{}/{}_{}'.format(BLUR_DIRNAME, filename, fname)
        img.save(fname)


def pix2pix_blur(filenames_arr):
    for fname in filenames_arr:
        img = scipy.misc.imread(fname)
        fname = fname.split('/')[-1]
        img = utils.imcrop_tosquare(img)
        img = resize(img, (FINAL_SLICE_SIZE, FINAL_SLICE_SIZE))*255
        img = img.astype('uint8')
        img = Image.fromarray(img)
        img = img.filter(ImageFilter.GaussianBlur(SIGMA))
        new_img = Image.new('RGB', (FINAL_SLICE_SIZE*2, FINAL_SLICE_SIZE))
        new_img.paste(img)
        filename = dirname.split('.')[-1]
        fname = '{}/{}_{}_{}'.format(BLUR_DIRNAME, filename,SIGMA, fname)
        new_img.save(fname)


pool.map(simple_crop, filenames_split)

#save_cropped(filenames_split)


