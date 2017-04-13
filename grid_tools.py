from sys import argv
from sklearn.preprocessing import scale
from skimage.filters import gaussian
from PIL import Image, ImageFilter
import uuid
import os
from natsort import natsorted, ns
import matplotlib.pyplot as plt
import numpy as np
import scipy

RESIZE_HEIGHT = 256
RESIZE_WIDTH = 256
# RESIZE_MAX = 720
RESIZE_TUPLE = (32, 32)
SIGMA = 11
SLICE_SIZE = 256
OVERLAP = 128
NUM_OF_CROPS = 3

# OVERLAP = ((SLICE_SIZE*NUM_OF_CROPS) - RESIZE_MAX)/ NUM_OF_OVERLAPS
OVERLAP_AMOUNT = int(OVERLAP/2)
#CALCULATING OVERAPS
NUM_OF_OVERLAPS = NUM_OF_CROPS-1
RESIZE_MAX = SLICE_SIZE*NUM_OF_CROPS-(NUM_OF_OVERLAPS* OVERLAP)
print("OVERLAP AMOUNT", OVERLAP_AMOUNT)
print("OVERLAP AMOUNT", OVERLAP)
print("RESIZE_MAX", RESIZE_MAX)

def calc_overlap_min(j):
    return (j * SLICE_SIZE) - (j * OVERLAP)


def calc_overlap(j, width):
    if j < 0:
        return 0
    elif  j == 0:
        return SLICE_SIZE - OVERLAP_AMOUNT
    elif j == NUM_OF_CROPS - 1:
        return (j + 1) * SLICE_SIZE - ((j*2) * OVERLAP_AMOUNT)
    else:
        return (j + 1) * SLICE_SIZE - (((j*2)+1) * OVERLAP_AMOUNT)

def blur_f(img):
    return gaussian(img, sigma=SIGMA, preserve_range=True, multichannel=True)


def crop_overlap(infile,height,width):
    if isinstance(infile, str):
        im = Image.open(infile)
    else:
        im = Image.fromarray(infile)

    im = im.resize((RESIZE_MAX, RESIZE_MAX))
    im = im.filter(ImageFilter.GaussianBlur(radius=SIGMA))

    # imgwidth, imgheight = im.size
    for i in range(NUM_OF_CROPS):
        for j in range(NUM_OF_CROPS):
            x_min = calc_overlap_min(j)
            x_max = x_min + SLICE_SIZE
            y_min = calc_overlap_min(i)
            y_max = y_min + SLICE_SIZE
            # print('x_min', x_min, 'y_min', y_min, 'x_max', x_max, 'y_max', y_max)
            box = (x_min, y_min, x_max, y_max)
            yield im.crop(box)


def crop(infile,height,width):
    im = Image.open(infile)
    imgwidth, imgheight = im.size
    for i in range(imgheight//height):
        for j in range(imgwidth//width):
            box = (j*width, i*height, (j+1)*width, (i+1)*height)
            yield im.crop(box)


def slice_img(infile, folder_dir='./clean_img', height=SLICE_SIZE, width=SLICE_SIZE, start_num=0, blur=False, resize=False, pix2pix=False, crop_f=crop, save=True, montage_n=1):
    imgs = []
    if not os.path.exists(folder_dir):
        os.mkdir(folder_dir)
    for k,piece in enumerate(crop_f(infile,height,width),start_num):
        img = Image.new('RGB', (height,width), 255)
        img.paste(piece)
        path = os.path.join(folder_dir,"{}-IMG-{}.png".format(montage_n, k) )
        if pix2pix:
            new_img = Image.new('RGB', (512, 256))
            new_img.paste(img)
            new_img.paste(img)
            img = new_img
        img = np.asarray(img)
        # if blur:
        #     img = blur_f(img)
        imgs.append(img)
        if save:
            print('saving to path', path)
            scipy.misc.imsave(path, img)

    return imgs


def slice_overlap(infile, folder_dir, pix2pix=False):
    if not os.path.exists(folder_dir):
        os.mkdir(folder_dir)
    slice_img(infile, folder_dir=folder_dir, height=SLICE_SIZE, width=SLICE_SIZE, blur=False, crop_f=crop_overlap, resize=True, pix2pix=pix2pix)


def overlap_crop_x(img, min_val, max_val):
    # Left upper right lower
    # img = np.asarray(img*255, np.uint8)
    # img = Image.fromarray(img)
    if type(img) == np.ndarray:
        img = np.asarray(img*255, np.uint8)
        img = Image.fromarray(img)

    width, height = img.size
    crop_amount = OVERLAP_AMOUNT
    if min_val == 0:
        return img.crop((0, 0, width - crop_amount, height))
    if max_val == RESIZE_MAX:
        return img.crop((crop_amount, 0, width, height))
    else:
        return img.crop((crop_amount, 0, width - crop_amount, height))

def overlap_crop_y(img, min_val, max_val):

    # Left upper right lower

    if type(img) == np.ndarray:
        img = np.asarray(img*255, np.uint8)
        img = Image.fromarray(img)
    width, height = img.size
    if min_val == 0:
        return img.crop((0, 0, width, height-OVERLAP_AMOUNT))
    if max_val == RESIZE_MAX:
        return img.crop((0, OVERLAP_AMOUNT, width, height))
    else:
        # print('cropping Y', min_val, max_val)
        return img.crop((0, OVERLAP_AMOUNT, width, height - OVERLAP_AMOUNT))

def montage(images, saveto='montage.png'):
    if isinstance(images, list):
        images = np.array(images)
    m = np.ones(
        (RESIZE_MAX,
            RESIZE_MAX, 3), np.uint8)
    for i in range(NUM_OF_CROPS):
        for j in range(NUM_OF_CROPS):
            this_filter = i * NUM_OF_CROPS + j

            x_min = calc_overlap(i-1, SLICE_SIZE)
            x_max = calc_overlap(i, SLICE_SIZE)
            y_min = calc_overlap(j-1, SLICE_SIZE)
            y_max = calc_overlap(j, SLICE_SIZE)

            # print('x_min', x_min, 'y_min', y_min, 'x_max', x_max, 'y_max', y_max)
            first_img = images[0]
            if this_filter < images.shape[0]:
                this_img = images[this_filter]
                try:
                    y = images[this_filter+1]
                except:
                    y = this_img
                try:
                    z = images[this_filter+3]
                except:
                    z = this_img

                this_img = np.clip(this_img, 0, 1)
                # print(this_img.max(), this_img.min())
                this_img = overlap_crop_x(this_img, y_min, y_max)
                this_img = overlap_crop_y(this_img, x_min, x_max)
                this_img = np.asarray(this_img, np.uint8)
                m[x_min:x_max,
                  y_min:y_max
                  ] = this_img

    plt.imsave(arr=m, fname=saveto)
    return m

def get_filenames(folder_dir):
    return [os.path.join(folder_dir, fname)
                 for fname in os.listdir(folder_dir) if fname.endswith('.jpg') or fname.endswith('.png')]

def sort_and_montage(filenames, file_name):
    # Load every image file in the provided directory

    filenames = natsorted(filenames, alg=ns.IGNORECASE)
    imgs = [plt.imread(fname)[..., :3] for fname in filenames]
    imgs = np.array(imgs).astype(np.float32)
    if(imgs[0][0][0][0] > 1):
        imgs = imgs/255.0
    montage(imgs, saveto=file_name)

def prepare_p2p_folder(input_dir, dest_dir):
    filenames = get_filenames(input_dir)


def prepare_p2p(file_name, folder_dir):
    i = 0
    imgs = slice_img(file_name, save=False)
    for img in imgs:
        i = i+1
        print(i)
        slice_img(img, folder_dir=folder_dir, height=SLICE_SIZE, width=SLICE_SIZE, blur=False, crop_f=crop_overlap, resize=True, pix2pix=True, montage_n=i)

def retrieve_p2p(folder_dir, dest_dir):
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)
    img_filenames = get_filenames(folder_dir)
    img_filenames = natsorted(img_filenames, alg=ns.IGNORECASE)
    img_filenames = np.array(img_filenames)
    chunked_filenames = np.split(img_filenames, 64)
    i = 1
    for filenames in chunked_filenames:
        sort_and_montage(filenames, './{}/{}.png'.format(dest_dir,uuid.uuid4()))
        i = i + 1
