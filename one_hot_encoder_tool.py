import pickle
import os
import scipy.misc
import numpy as np


def get_filenames(dirname):
    return [os.path.join(dirname, fname)
            for fname in os.listdir(dirname) if fname.endswith('.jpg')]


def get_directories(dirname):
    return [x[0] for x in os.walk(dirname)][1:]

def create_one_hot_data(d):
    dirs = get_directories(d)

    images = []
    one_hot_arr_total = []
    for i, dirname in enumerate(dirs):

        one_hot_arr = np.zeros(len(dirs))
        one_hot_arr[i] = 1

        filenames = get_filenames(dirname)
        for fname in filenames:
            img = scipy.misc.imread(fname)
            images.append(img)
            one_hot_arr_total.append(one_hot_arr)

    return [np.array(images), np.array(one_hot_arr_total)]


with open('data.pickle', 'wb') as f:
    data = create_one_hot_data('./')
    pickle.dump(data, f)

# with open('data.pickle', 'rb') as f:
     # data = pickle.load(f)
