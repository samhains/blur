from PIL import Image, ImageFilter
import uuid
import os
import matplotlib.pyplot as plt
import numpy as np
import scipy
import scipy.misc
from natsort import natsorted, ns

# RESIZE_MAX = 720
PIX_2_PIX_CROP = False
SIGMA = 12
MONTAGE_SLICE_SIZE = 512
FINAL_SLICE_SIZE = MONTAGE_SLICE_SIZE
OVERLAP = int(FINAL_SLICE_SIZE/2)
NUM_OF_CROPS = 3

# OVERLAP = ((MONTAGE_SLICE_SIZE*NUM_OF_CROPS) - RESIZE_MAX)/ NUM_OF_OVERLAPS
OVERLAP_AMOUNT = int(OVERLAP/2)
# CALCULATING OVERAPS
NUM_OF_OVERLAPS = NUM_OF_CROPS-1
RESIZE_MAX = MONTAGE_SLICE_SIZE*NUM_OF_CROPS-(NUM_OF_OVERLAPS * OVERLAP)
print("OVERLAP AMOUNT", OVERLAP_AMOUNT)
print("OVERLAP", OVERLAP)
print("RESIZE_MAX", RESIZE_MAX)


def calc_overlap_min(j):
    return (j * MONTAGE_SLICE_SIZE) - (j * OVERLAP)


def calc_overlap(j):
    if j < 0:
        return 0
    elif j == 0:
        return MONTAGE_SLICE_SIZE - OVERLAP_AMOUNT
    elif j == NUM_OF_CROPS - 1:
        return (j + 1) * MONTAGE_SLICE_SIZE - ((j*2) * OVERLAP_AMOUNT)
    else:
        return (j + 1) * MONTAGE_SLICE_SIZE - (((j*2)+1) * OVERLAP_AMOUNT)


def crop_overlap(infile, height, width):
    if isinstance(infile, str):
        im = Image.open(infile)
    else:
        im = Image.fromarray(infile)

    im = im.resize((RESIZE_MAX, RESIZE_MAX))

    # imgwidth, imgheight = im.size
    for i in range(NUM_OF_CROPS):
        for j in range(NUM_OF_CROPS):
            x_min = calc_overlap_min(j)
            x_max = x_min + MONTAGE_SLICE_SIZE
            y_min = calc_overlap_min(i)
            y_max = y_min + MONTAGE_SLICE_SIZE
            box = (x_min, y_min, x_max, y_max)
            yield im.crop(box)


def crop(infile, height, width):
    if isinstance(infile, str):
        im = Image.open(infile)
    else:
        im = Image.fromarray(infile)

    imgwidth, imgheight = im.size

    for i in range(imgheight//height):
        for j in range(imgwidth//width):
            box = (j*width, i*height, (j+1)*width, (i+1)*height)
            yield im.crop(box)


def slice_img(
        infile,
        folder_dir='./clean_img',
        height=MONTAGE_SLICE_SIZE,
        width=MONTAGE_SLICE_SIZE,
        start_num=0,
        blur=False,
        resize=False,
        pix2pix=False,
        crop_f=crop,
        save=True,
        montage_n=1):
    imgs = []
    print('slicing image')
    if not os.path.exists(folder_dir):
        os.mkdir(folder_dir)
    for k, piece in enumerate(crop_f(infile, height, width), start_num):
        img = Image.new('RGB', (height, width), 255)
        img.paste(piece)
        path = os.path.join(
                folder_dir, "s{}_{}_{}.png".format(SIGMA, montage_n, k))
        if pix2pix:
            new_img = Image.new('RGB', (FINAL_SLICE_SIZE*2, FINAL_SLICE_SIZE))
            img = img.resize((FINAL_SLICE_SIZE, FINAL_SLICE_SIZE))
            img = img.filter(ImageFilter.GaussianBlur(SIGMA))
            new_img.paste(img)
            new_img.paste(img)
            img = new_img
        img = np.asarray(img)
        img = img.astype('uint8')
        imgs.append(img)
        if save:
            print('saving to path', path)
            scipy.misc.imsave(path, img)

    return imgs


def slice_overlap(infile, folder_dir, pix2pix=False):
    if not os.path.exists(folder_dir):
        os.mkdir(folder_dir)
    slice_img(
        infile,
        folder_dir=folder_dir,
        height=MONTAGE_SLICE_SIZE,
        width=MONTAGE_SLICE_SIZE,
        blur=False,
        crop_f=crop_overlap, resize=True, pix2pix=pix2pix)


def overlap_crop_x(img, min_val, max_val):
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

            x_min = calc_overlap(i-1)
            x_max = calc_overlap(i)
            y_min = calc_overlap(j-1)
            y_max = calc_overlap(j)

            if this_filter < images.shape[0]:
                this_img = images[this_filter]
                this_img = np.clip(this_img, 0, 1)
                this_img = overlap_crop_x(this_img, y_min, y_max)
                this_img = overlap_crop_y(this_img, x_min, x_max)
                this_img = np.asarray(this_img, np.uint8)
                m[x_min:x_max,
                  y_min:y_max
                  ] = this_img

    plt.imsave(arr=m, fname=saveto)
    return m


def get_filenames(folder_dir):
    return [
        os.path.join(folder_dir, fname)
        for fname in os.listdir(folder_dir)
        if fname.endswith('.jpg') or fname.endswith('.png')]


def save_image(fname):
    print(fname)
    return plt.imread(fname)[..., :3]


def sort_and_montage(filenames, file_name):
    # Load every image file in the provided directory

    filenames = natsorted(filenames, alg=ns.IGNORECASE)
    imgs = [save_image(fname) for fname in filenames]
    imgs = np.array(imgs).astype(np.float32)
    if(imgs[0][0][0][0] > 1):
        imgs = imgs/255.0
    montage(imgs, saveto=file_name)


def prepare_p2p(input_dir, output_dir, overlap=True):
    i = 0

    filenames = get_filenames(input_dir)
    print(filenames[:10])
    filenames = natsorted(filenames, alg=ns.IGNORECASE)

    for filename in filenames:
        i = i+1
        slice_img(
            filename,
            folder_dir=output_dir,
            height=MONTAGE_SLICE_SIZE,
            width=MONTAGE_SLICE_SIZE,
            blur=True,
            crop_f=crop_overlap,
            resize=True,
            pix2pix=PIX_2_PIX_CROP,
            montage_n=i)


def prepare_p2p_grid(input_dir, output_dir, overlap=True):
    i = 0

    filenames = get_filenames(input_dir)
    print(filenames[:10])
    filenames = natsorted(filenames, alg=ns.IGNORECASE)
    print(filenames[:10])
    imgs_arr = [slice_img(filename, save=False) for filename in filenames]

    for imgs in imgs_arr:
        for img in imgs:
            print('imgs', img)
            i = i+1
            slice_img(
                img,
                folder_dir=output_dir,
                height=MONTAGE_SLICE_SIZE,
                width=MONTAGE_SLICE_SIZE,
                blur=True,
                crop_f=crop_overlap,
                resize=True,
                pix2pix=PIX_2_PIX_CROP,
                montage_n=i)


def retrieve_p2p(folder_dir, dest_dir):
    i = 0
    print('fold', folder_dir, dest_dir)
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)
    img_filenames = get_filenames(folder_dir)
    img_filenames = natsorted(img_filenames, alg=ns.IGNORECASE)
    img_filenames = np.array(img_filenames)
    num_of_montages = 1
    num_of_images = len(img_filenames)/9
    print(num_of_images)
    chunked_montages = np.split(img_filenames, num_of_montages)
    for k, montage_filenames in enumerate(chunked_montages):
        chunked_filenames = np.split(montage_filenames, num_of_images)
        for filenames in chunked_filenames:
            i = i+1
            sort_and_montage(
                filenames, './{}/s8_{}_{}.png'.format(dest_dir, k, i))
