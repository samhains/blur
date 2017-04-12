from sys import argv
from skimage.filters import gaussian
from PIL import Image
import os
from natsort import natsorted, ns
import matplotlib.pyplot as plt
import numpy as np
import scipy

RESIZE_HEIGHT = 256
RESIZE_WIDTH = 256
RESIZE_MAX = 740
RESIZE_TUPLE = (32, 32)
SIGMA = 3
SLICE_SIZE = 256
NUM_OF_CROPS = 3

#CALCULATING OVERAPS
NUM_OF_OVERLAPS = NUM_OF_CROPS-1
OVERLAP = ((SLICE_SIZE*NUM_OF_CROPS) - RESIZE_MAX)/ NUM_OF_OVERLAPS
OVERLAP_AMOUNT = int(OVERLAP/2)
print("OVERLAP AMOUNT", OVERLAP_AMOUNT)

def crop(infile,height,width):
    print(height, width)
    im = Image.open(infile)
    im = im.resize((RESIZE_MAX, RESIZE_MAX))
    # imgwidth, imgheight = im.size
    for i in range(NUM_OF_CROPS):
        for j in range(NUM_OF_CROPS):
            print('i', i, 'j', j)
            x_min = calc_overlap_min(i)
            x_max = x_min + SLICE_SIZE
            y_min = calc_overlap_min(j)
            y_max = y_min + SLICE_SIZE
            box = (x_min, y_min, x_max, y_max)
            box = (j*width, i*height, (j+1)*width, (i+1)*height)
            yield im.crop(box)

def calc_overlap_min(j):
    return (j * SLICE_SIZE) - (j * OVERLAP)

def calc_min(j, val):
    return calc_min_overlap(j*val)

def calc_max(j, val):
    return calc_max_overlap((j+1)*val)

def calc_min_overlap(i):
    return i * RESIZE_HEIGHT - (i * OVERLAP_AMOUNT)

def calc_max_overlap(j):
    if j == NUM_OF_CROPS - 1:
        return (j + 1) * RESIZE_HEIGHT
    else:
        return (j + 1) * RESIZE_HEIGHT - ((j+1) * OVERLAP_AMOUNT)



def calc_overlap(j, width):
    if j < 0:
        return 0
    elif  j == 0:
        return SLICE_SIZE - OVERLAP_AMOUNT
    elif j == NUM_OF_CROPS - 1:
        return (j + 1) * SLICE_SIZE - ((j*2) * OVERLAP_AMOUNT)
    else:
        return (j + 1) * SLICE_SIZE - (((j*2)+1) * OVERLAP_AMOUNT)


def crop_2(infile,height,width):
    im = Image.open(infile)
    imgwidth, imgheight = im.size
    for i in range(imgheight//height):
        for j in range(imgwidth//width):
            box = (j*width, i*height, (j+1)*width, (i+1)*height)
            yield im.crop(box)

def blur_f(img):
    return gaussian(img, sigma=SIGMA, preserve_range=True, multichannel=True)

def slice_img(infile, folder_dir='./clean_img', height=SLICE_SIZE, width=SLICE_SIZE, start_num=0, blur=False):
    imgs = []
    if not os.path.exists(folder_dir):
        os.mkdir(folder_dir)
    for k,piece in enumerate(crop(infile,height,width),start_num):
        img = Image.new('RGB', (height,width), 255)
        img.paste(piece)
        path = os.path.join(folder_dir,"IMG-%s.png" % k)
        print('saving to path', path)
        img = img.resize((RESIZE_HEIGHT, RESIZE_WIDTH))
        img = np.asarray(img)
        # if blur:
        #     img = blur_f(img)
        #imgs.append(img)
        print('shape', img.shape)
        scipy.misc.imsave(path, img)
    return imgs

def slice_blur(infile, folder_dir):
    if not os.path.exists(folder_dir):
        os.mkdir(folder_dir)
    slice_img(infile, folder_dir=folder_dir, height=SLICE_SIZE, width=SLICE_SIZE, blur=False)


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
    crop_amount = OVERLAP/2
    width, height = img.size
    if min_val == 0:
        return img.crop((0, crop_amount, width, height))
    if max_val == RESIZE_MAX:
        return img.crop((0, 0, width, height - crop_amount))
    else:
        return img.crop((0, crop_amount, width, height - crop_amount))



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

            print('xmin', x_min, 'xmax', x_max, 'y_min', y_min, 'y_max', y_max)
            if this_filter < images.shape[0]:
                this_img = images[this_filter]

                this_img = overlap_crop_x(this_img, y_min, y_max)
                this_img = overlap_crop_y(this_img, x_min, x_max)
                this_img = np.asarray(this_img, np.uint8)
                m[x_min:x_max,
                  y_min:y_max
                  ] = this_img

    plt.imsave(arr=m, fname=saveto)
    return m


def sort_and_montage(folder_dir, file_name):
    # Load every image file in the provided directory
    filenames = [os.path.join(folder_dir, fname)
                 for fname in os.listdir(folder_dir) if fname.endswith('.jpg') or fname.endswith('.png')]

    filenames = natsorted(filenames, alg=ns.IGNORECASE)
    imgs = [plt.imread(fname)[..., :3] for fname in filenames]
    imgs = np.array(imgs).astype(np.float32)
    # montage(imgs)
    montage(imgs, saveto=file_name)

script, first, file_name, save_dir  = argv

print ("The script is called:", script)
print ("Your first variable is:", first)

if first == 'slice':
    slice_img(file_name, save_dir)

# if first == 'slice_overlap':
#     slice_overlap(file_name, save_dir)

if first == 'slice_blur':
    slice_blur(file_name, save_dir)

if first == 'montage':
    sort_and_montage(file_name, save_dir)


# def blur(img, resize_tuple):
#     img = img.blur(resize_tuple)
#     return img.blur((RESIZE_WIDTH, RESIZE_HEIGHT))

# def montage_2(images, saveto='montage.png'):
#     if isinstance(images, list):
#         images = np.array(images)
#     img_h = images.shape[1]
#     img_w = images.shape[2]
#     n_plots = int(np.ceil(np.sqrt(images.shape[0])))
#     if len(images.shape) == 4 and images.shape[3] == 3:
#         m = np.ones(
#             (images.shape[1] * n_plots,
#              images.shape[2] * n_plots, 3)) * 0.5
#         print(m.shape)
#     else:
#         m = np.ones(
#             (images.shape[1] * n_plots + 1,
#              images.shape[2] * n_plots + n_plots + 1)) * 0.5
#     for i in range(n_plots):
#         for j in range(n_plots):
#             this_filter = i * n_plots + j
#             lower_x = i * img_h
#             upper_x = (i + 1) * img_h
#             lower_y = j * img_w
#             upper_y = (j + 1) * img_w
#             if this_filter < images.shape[0]:
#                 this_img = images[this_filter]
#                 m[lower_x:upper_x,
#                   lower_y:upper_y] = this_img
#     plt.imsave(arr=m, fname=saveto)
#     return m
