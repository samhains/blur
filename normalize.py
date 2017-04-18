import os
import matplotlib.pyplot as plt
from natsort import natsorted, ns
import numpy as np
from sys import argv

script, arg1  = argv

 
BASE_DIR = '/home/paperspace/Code/pix2pix/results/{}/latest_net_G_val/images'.format(arg1)
# BASE_DIR = '.'
PROCESS_DIR = BASE_DIR + '/processed'
if not os.path.exists(PROCESS_DIR):
    os.mkdir(PROCESS_DIR)
INPUT_DIR = BASE_DIR + '/input'
OUTPUT_DIR = BASE_DIR + '/output'


def get_filenames(folder_dir):
    return [os.path.join(folder_dir, fname)
            for fname in os.listdir(folder_dir)
            if fname.endswith('.jpg') or fname.endswith('.png')]


def get_images(filenames):
    print('getting images')
    imgs = [plt.imread(fname)[..., :3] for fname in filenames]
    return np.array(imgs)


def normalize(input_filenames, output_filenames, batch_num):
    output_imgs = get_images(output_filenames)
    input_imgs = get_images(input_filenames)

    filenames = get_filenames(OUTPUT_DIR)
    filenames = natsorted(filenames, alg=ns.IGNORECASE)

    for idx, (input_img, output_img) in enumerate(
            zip(input_imgs, output_imgs)):
        input_mean = input_img.mean()
        output_mean = output_img.mean()
        difference = input_mean - output_mean
        adjusted_output = output_img + difference
        adjusted_output = np.clip(adjusted_output, 0, 1)
        fname = "{}-{}".format(batch_num, filenames[idx].split('/')[-1])
        print(fname)
        plt.imsave(PROCESS_DIR+"/{}".format(fname), adjusted_output)


def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]

batch_num = 0
input_dir = INPUT_DIR
output_dir = OUTPUT_DIR
input_filenames = get_filenames(input_dir)
input_filenames = natsorted(input_filenames, alg=ns.IGNORECASE)
output_filenames = get_filenames(output_dir)
output_filenames = natsorted(output_filenames, alg=ns.IGNORECASE)

for i, o in zip(batch(input_filenames, 1000), batch(output_filenames, 1000)):
    batch_num = batch_num+1
    normalize(i, o, batch_num)
