from get_level import *

im = cv2.imread('box')
thresh, cont = find_contour(im)
cropped_im = crop_to_rotated_rectangular_contour(thresh, cont)
crop2 = crop_to_rotated_rectangular_contour(im, cont)
# images.CircleGui(cropped_im)
particles = images.find_circles(img=cropped_im, p1=200, p2=5, min_dist=10, min_rad=7, max_rad=15)
images.draw_circles(crop2, particles, (0, 0, 255), 5)
images.display(crop2)