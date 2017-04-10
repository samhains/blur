from sys import argv
from PIL import Image
import os
from natsort import natsorted, ns
import matplotlib.pyplot as plt
import utils
import numpy as np

def crop(infile,height,width):
    im = Image.open(infile)
    imgwidth, imgheight = im.size
    for i in range(imgheight//height):
        for j in range(imgwidth//width):
            box = (j*width, i*height, (j+1)*width, (i+1)*height)
            yield im.crop(box)



def slice_img(infile, folder_name='clean_img', height=200, width=200, start_num=0, resize=lambda a: a):
    imgs = []
    print(folder_name)
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
    for k,piece in enumerate(crop(infile,height,width),start_num):
        img = Image.new('RGB', (height,width), 255)
        img.paste(piece)
        path = os.path.join('./'+folder_name,"IMG-%s.png" % k)
        print('saving to path', path)
        img = resize(img)
        imgs.append(np.asarray(img))
        img.save(path)
    return imgs


def slice_resize(infile, folder_name):
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
    slice_img(infile, folder_name=folder_name, height=25, width=25, resize=lambda a: a.resize((200,200)))

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
            (images.shape[1] * n_plots + n_plots + 1,
             images.shape[2] * n_plots + n_plots + 1, 3)) * 0.5
    else:
        m = np.ones(
            (images.shape[1] * n_plots + n_plots + 1,
             images.shape[2] * n_plots + n_plots + 1)) * 0.5
    for i in range(n_plots):
        for j in range(n_plots):
            this_filter = i * n_plots + j
            if this_filter < images.shape[0]:
                this_img = images[this_filter]
                m[1 + i + i * img_h:1 + i + (i + 1) * img_h,
                  1 + j + j * img_w:1 + j + (j + 1) * img_w] = this_img
    plt.imsave(arr=m, fname=saveto)
    return m


def sort_and_montage(folder_name, file_name='montage.png'):
    # Load every image file in the provided directory
    filenames = [os.path.join(folder_name, fname)
                for fname in os.listdir(folder_name)]

    filenames = natsorted(filenames, alg=ns.IGNORECASE)
    # Make sure we have exactly 100 image files!
    imgs = [plt.imread(fname)[..., :3] for fname in filenames]

    # # Crop every image to a square
    # imgs = [utils.imcrop_tosquare(img_i) for img_i in imgs]

    # # Then resize the square image to 100 x 100 pixels
    # imgs = [resize(img_i, (100, 100)) for img_i in imgs]

    # # Finally make our list of 3-D images a 4-D array with the first dimension the number of images:
    imgs = np.array(imgs).astype(np.float32)
    # montage(imgs)
    montage(imgs, saveto=file_name)

script, first, file_name  = argv

if first == 'slice':
    slice_img(file_name)

if first == 'slice_resize':
    file_name_no_ext = file_name.split('.')[0]
    slice_resize('./clean_img/'+file_name_no_ext, file_name)

if first == 'montage':
    sort_and_montage('./'+file_name)
