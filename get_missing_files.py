import os

PIX_2_PIX_OUTPUT_DIR = './2/'
INPUT_DIR = './1/'
VAL_2_DIR = './val_2/'

if not os.path.exists('./val_2'):
    os.mkdir('./val_2')


def diff(first, second):
    second = set(second)
    return [INPUT_DIR+item for item in first
            if item.split('/')[-1] not in second]


def get_filenames(dir_name):
    return [fname
            for fname in os.listdir(dir_name)
            if fname.endswith('.ong')]


input_filenames = get_filenames(INPUT_DIR)
p2p_filenames = get_filenames(PIX_2_PIX_OUTPUT_DIR)

print('input', input_filenames, 'output', p2p_filenames)

missing_filenames = diff(input_filenames, p2p_filenames)

for filename in missing_filenames:
    new_name = VAL_2_DIR + filename.split('/')[-1]
    print('moving to', new_name)
    os.rename(filename, new_name)
