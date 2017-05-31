from PIL import Image
import os
import numpy as np
import json
import math


filename = 'out'
dirname = './'+filename
CROP_DIRNAME = dirname+'_cropped'

if not os.path.exists(CROP_DIRNAME):
    os.mkdir(CROP_DIRNAME)


def crop_box(box, filename):
    img = Image.open('{}/{}.jpg'.format(dirname,filename))
    original_height = img.height
    original_width = img.width
    print('img', 'width:', img.width, 'height:', img.height)
    if box:
        x0 = box[0]
        y0 = box[1]
        x1 = box[2]
        y1 = box[3]

        width = x1-x0
        height = y1-y0

        diff = abs(width-height)
        half_diff = math.floor(diff/2)

        if height < width: 
            y0 = max(y0 - half_diff, 0)
            y1 = min(half_diff + y1, original_height)
        elif width < height:
            x0 = max(x0 - half_diff, 0)
            x1 = min(half_diff + x1, original_width)

    else:
        x0 = 0
        y0 = 0
        x1 = original_width
        y1 = original_height

    width = x1-x0
    height = y1-y0
    print('crop width', width, 'crop height', height)
    img_cropped = img.crop(box=(x0, y0, x1, y1))
    img_cropped.save('{}/{}.jpg'.format(CROP_DIRNAME, filename))
    print('cropped_img', 'width:', img_cropped.width, 'height:', img_cropped.height)


def get_crop_box_from_json(filename):
    try:
        with open('{}/{}.json'.format(dirname, filename)) as json_data:

            crop_details = json.load(json_data)[0]

        x0 = crop_details['topleft']['x']
        y0 = crop_details['topleft']['y']
        x1 = crop_details['bottomright']['x']
        y1 = crop_details['bottomright']['y']
        print('x0', x0, 'y0', y0, 'x1', x1, 'y1', y1,)
        return (x0, y0, x1, y1)
    except:
        print('error loading JSON')
        return None
# Load every image file in the provided directory
filenames = [ fname.split('.')[0] for fname in os.listdir(dirname) if fname.endswith('.jpg')]

filenames = np.asarray(filenames)

print(filenames)

for fname in filenames:
    box = get_crop_box_from_json(fname)
    crop_box(box, fname)

