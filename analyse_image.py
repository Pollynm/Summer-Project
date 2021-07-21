import numpy as np
import cv2
import matplotlib.pyplot as plt
from labvision import images

original_image = cv2.imread('box')
images.display(original_image)
greyscale_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
threshold_image = images.threshold(greyscale_image, 75)

contours = images.find_contours(threshold_image)
sorted_contours = images.sort_contours(contours)
biggest_contour = sorted_contours[-1]

original_image = images.draw_contours(original_image, biggest_contour, thickness=5)
images.display(original_image)

# get circles
# particles = images.find_circles(threshold_image, 30, cv2.HOUGH_GRADIENT, 1.2, 3, 10)
# images.draw_circles(original_image, particles, (0, 0, 255), 5)

# method 1 (rotation)
rect = cv2.minAreaRect(biggest_contour)


def crop_minAreaRect(img, rect):
    # rotate img
    angle = rect[2]
    rows, cols = img.shape[0], img.shape[1]
    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)
    M[3] -= 90
    img_rot = cv2.warpAffine(img, M, (cols, rows))

    # rotate bounding box
    rect0 = (rect[0], rect[1], 0.0)
    box = cv2.boxPoints(rect0)
    pts = np.int0(cv2.transform(np.array([box]), M))[0]
    pts[pts < 0] = 0

    # crop
    img_crop = img_rot[pts[1][1]:pts[0][1], pts[1][0]:pts[2][0]]

    img_crop = img_crop[18:-18, 18:-18]

    return img_crop


cropped_im = crop_minAreaRect(threshold_image, rect)
colour_cropped = crop_minAreaRect(original_image, rect)

images.display(cropped_im)

# method 2 (no rotation)
corners, midpoint = images.find_contour_corners(biggest_contour, 4)
# for index in corners:
#     print(biggest_contour[index])
# crop_img = original_image[258:3625, 992:4360]
# images.display(crop_img)

inverted_im = cv2.bitwise_not(cropped_im)
com = images.center_of_mass(inverted_im)

print(com)
print(midpoint)
com_on_image = cv2.circle(colour_cropped, com, radius=10, color=(0, 0, 255), thickness=-1)
images.display(com_on_image)
