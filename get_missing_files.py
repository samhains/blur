import os

BASE_DIR = '/home/paperspace/Code/pix2pix'
PIX_2_PIX_OUTPUT_DIR = BASE_DIR+'/results/nolikes256/latest_net_G_val/images/output_old'
INPUT_DIR = BASE_DIR+'/data/val_old/'
VAL_2_DIR = BASE_DIR+'/data/val_2/'

if not os.path.exists('./val_2'):
    os.mkdir('./val_2')


def diff(first, second):
    second = set(second)
    return [INPUT_DIR+item for item in first
            if item.split('/')[-1] not in second]


def get_filenames(dir_name):
    return [fname
            for fname in os.listdir(dir_name)
            if fname.endswith('.png')]


input_filenames = get_filenames(INPUT_DIR)
p2p_filenames = get_filenames(PIX_2_PIX_OUTPUT_DIR)

missing_filenames = diff(input_filenames, p2p_filenames)

for filename in missing_filenames:
    new_name = VAL_2_DIR + filename.split('/')[-1]
    print('moving from', filename, 'moving to', new_name )
    os.rename(filename, new_name)
