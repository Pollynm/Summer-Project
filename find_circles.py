from get_level import *

im = cv2.imread('2021_07_23_11_46_35')
thresh, cont = find_contour(im)
cropped_im = crop_to_rotated_rectangular_contour(thresh, cont)
crop2 = crop_to_rotated_rectangular_contour(im, cont)
# images.display(crop2)
# images.CircleGui(cropped_im)
particles = images.find_circles(img=cropped_im, p1=220, p2=3, min_dist=19, min_rad=7, max_rad=10)
images.draw_circles(crop2, particles, (0, 0, 255), 5)
images.display(crop2)