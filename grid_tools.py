from sys import argv
from PIL import Image
import os
from natsort import natsorted, ns
import matplotlib.pyplot as plt
import numpy as np

def crop(infile,height,width):
    im = Image.open(infile)
    imgwidth, imgheight = im.size
    for i in range(imgheight//height):
        for j in range(imgwidth//width):
            box = (j*width, i*height, (j+1)*width, (i+1)*height)
            yield im.crop(box)




def resize(img, resize_tuple):
    img = img.resize(resize_tuple)
    return img.resize((200, 200))

def slice_img(infile, folder_dir='./clean_img', height=200, width=200, start_num=0, resize_tuple=(200,200)):
    imgs = []
    if not os.path.exists(folder_dir):
        os.mkdir(folder_dir)
    for k,piece in enumerate(crop(infile,height,width),start_num):
        img = Image.new('RGB', (height,width), 255)
        img.paste(piece)
        path = os.path.join(folder_dir,"IMG-%s.png" % k)
        print('saving to path', path)
        img = resize(img, resize_tuple)
        imgs.append(np.asarray(img))
        img.save(path)
    return imgs

def slice_resize(infile, folder_dir):
    if not os.path.exists(folder_dir):
        os.mkdir(folder_dir)
    slice_img(infile, folder_dir=folder_dir, height=100, width=100, resize_tuple=(25,25))


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

if first == 'slice_resize':
    slice_resize(file_name, save_dir)

if first == 'montage':
    sort_and_montage(file_name, save_dir)
