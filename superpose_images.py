from get_level import *


def get_square_im(cam):
    im = cam.get_frame()
    threshold_im, contour = find_contour(im)
    cropped_im = crop_to_rotated_rectangular_contour(threshold_im, contour)
    square_im = cv2.resize(cropped_im, (2910, 2980))
    square_im = cv2.bitwise_not(square_im)
    return square_im


def superpose_images(cam, number_of_photos=5):
    im = get_square_im(cam=cam)
    loops_run = 1
    while loops_run < number_of_photos:
        im2 = get_square_im(cam)
        combined = cv2.addWeighted(im, 1, im2, 1, 0)
        combined = cv2.bitwise_not(combined)
        images.display(combined)
        im = cv2.bitwise_not(combined)
        loops_run += 1


import pandas
print(pandas.__version__)
