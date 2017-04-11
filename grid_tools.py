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
RESIZE_MAX = 750
RESIZE_TUPLE = (32, 32)
SIGMA = 3
SLICE_HEIGHT = 256
SLICE_WIDTH = 256
NUM_OF_CROPS = 3
OVERLAP = 7


def crop(infile,height,width):
    im = Image.open(infile)
    im = im.resize((RESIZE_MAX, RESIZE_MAX))
    imgwidth, imgheight = im.size
    # add overlap to width or height unless this would make the y<0, x<0, or y> RESIZE_HEIGHT, x>RESIZE_WIDTH
    for i in range(NUM_OF_CROPS):
        for j in range(NUM_OF_CROPS):
            x_min = calc_x_min(j, width)
            x_max = calc_x_max(j, width)
            y_min = calc_y_min(i, height)
            y_max = calc_y_max(i, height)
            box = (x_min, y_min, x_max, y_max)
            # box = (j*width, i*height, (j+1)*width, (i+1)*height)
            yield im.crop(box)

def calc_min_overlap(val):
    if val - OVERLAP < 0:
        return val - OVERLAP
    else:
        return val

def calc_max_overlap(val):
    if val + OVERLAP > RESIZE_MAX:
        return val
    else:
        return val + OVERLAP


def calc_x_min(j, width):
    return calc_min_overlap(j*width)

def calc_y_min(i, height):
    return calc_min_overlap(i*height)

def calc_x_max(j, width):
    return calc_max_overlap((j+1)*width)

def calc_y_max(i, height):
    return calc_max_overlap((i+1)*height)

def crop_2(infile,height,width):
    im = Image.open(infile)
    imgwidth, imgheight = im.size
    for i in range(imgheight//height):
        for j in range(imgwidth//width):
            box = (j*width, i*height, (j+1)*width, (i+1)*height)
            yield im.crop(box)

def blur_f(img):
    return gaussian(img, sigma=SIGMA, preserve_range=True, multichannel=True)

# def blur(img, resize_tuple):
#     img = img.blur(resize_tuple)
#     return img.blur((RESIZE_WIDTH, RESIZE_HEIGHT))

def slice_img(infile, folder_dir='./clean_img', height=RESIZE_HEIGHT, width=RESIZE_WIDTH, start_num=0, blur=False):
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
        if False:
            img = blur_f(img)
        #imgs.append(img)
        print(img.shape)
        scipy.misc.imsave(path, img)
    return imgs

def slice_blur(infile, folder_dir):
    if not os.path.exists(folder_dir):
        os.mkdir(folder_dir)
    slice_img(infile, folder_dir=folder_dir, height=SLICE_HEIGHT, width=SLICE_WIDTH, blur=True)


def montage(images, saveto='montage.png'):
    """Draw all images as a montage separated by 1 pixel borders.

    Also saves the file to the destination specified by `saveto`.

    Parameters
    ----------
    images : numpy.ndarray
        Input array to create montage of.  Array should be:
        batch x height x width x channels.
    saveto : str
        Location to save the resulting montage image.

    Returns
    -------
    m : numpy.ndarray
        Montage image.
    """
    if isinstance(images, list):
        images = np.array(images)
    img_h = images.shape[1]
    img_w = images.shape[2]
    n_plots = int(np.ceil(np.sqrt(images.shape[0])))
    if len(images.shape) == 4 and images.shape[3] == 3:
        m = np.ones(
            (images.shape[1] * n_plots,
             images.shape[2] * n_plots, 3)) * 0.5
        print(m.shape)
    else:
        m = np.ones(
            (images.shape[1] * n_plots + 1,
             images.shape[2] * n_plots + n_plots + 1)) * 0.5
    for i in range(n_plots):
        for j in range(n_plots):
            this_filter = i * n_plots + j
            lower_x = i * img_h
            upper_x = (i + 1) * img_h
            lower_y = j * img_w
            upper_y = (j + 1) * img_w
            if this_filter < images.shape[0]:
                this_img = images[this_filter]
                m[lower_x:upper_x,
                  lower_y:upper_y] = this_img
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

if first == 'slice_overlap':
    slice_overlap(file_name, save_dir)

if first == 'slice_blur':
    slice_blur(file_name, save_dir)

if first == 'montage':
    sort_and_montage(file_name, save_dir)
