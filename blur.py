from grid_tools import slice_img, slice_overlap, sort_and_montage, prepare_p2p, retrieve_p2p
from sys import argv

script, arg1, arg2, arg3  = argv

print ("The script is called:", script)
print ("Your arg1 variable is:", arg1)

if arg1 == 'slice':
    slice_img(arg2, arg3)

# if arg1 == 'slice_overlap':
#     slice_overlap(arg2, arg3)

if arg1 == 'slice_overlap':
    slice_overlap(arg2, arg3)

if arg1 == 'slice_overlap_p2p':
    slice_overlap(arg2, arg3, pix2pix=True)

if arg1 == 'montage':
    sort_and_montage(arg2, arg3)

if arg1 == 'prepare_p2p':
    prepare_p2p(arg2, arg3)

if arg1 == 'retrieve_p2p':
    retrieve_p2p(arg2, arg3)

# if arg1 == 'dir_montage':
#     imgs = slice_img(arg2, arg3)
    # imgs = arr_slice_overlap(imgs)
    # sort_and_montage(arg2, arg3)

