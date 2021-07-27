import numpy as np
import cv2
from labvision import images
from labequipment import arduino
from labvision import camera
from serial_commands import SendSerialCommands


def get_level():
    # uneven = True
    cam = camera.Panasonic()
    # while uneven:
    im = cam.get_frame(delete=True)
    im = images.rotate(im, 180)
    threshold_im, contour = find_contour(im)
    cropped_im = crop_to_rotated_rectangular_contour(threshold_im, contour)
    com, midpoint = get_com_and_midpoint(cropped_im)
    colour_im = images.gray_to_bgr(cropped_im)
    colour_im = images.draw_circles(colour_im, (com[0], com[1], 15), color=[0, 0, 255], thickness=-1)
    colour_im = images.draw_circles(colour_im, (midpoint[0], midpoint[1], 15), color=[255, 0, 0], thickness=-1)
    images.display(colour_im)
    print(com, midpoint)
    move_com_to_midpoint(com, midpoint)


def find_contour(im):
    greyscale_im = images.bgr_to_gray(im)
    threshold_im = images.threshold(greyscale_im, 75)

    kernel = np.ones((50, 50), np.uint8)
    no_particles_im = cv2.morphologyEx(threshold_im, cv2.MORPH_CLOSE, kernel)

    contours = images.find_contours(no_particles_im)
    sorted_contours = images.sort_contours(contours)
    biggest_contour = sorted_contours[-1]

    return threshold_im, biggest_contour


def crop_to_rotated_rectangular_contour(img, contour):
    rect = cv2.minAreaRect(contour)
    # rotate img
    angle = rect[2]
    if angle > 0:  # angle needs to be negative
        angle -= 90
    rows, cols = img.shape[0], img.shape[1]
    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)
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


def get_com_and_midpoint(im):
    midpoint = (int(im.shape[0] / 2), int(im.shape[1] / 2))

    inverted_im = cv2.bitwise_not(im)
    com = images.center_of_mass(inverted_im)

    return com, midpoint


# def move_com_to_midpoint(com, midpoint, duration):
#     xdiff = midpoint[0] - com[0]
#     ydiff = midpoint[1] - com[1]
#     xduration = duration * np.abs(xdiff)
#     yduration = duration * np.abs(ydiff)
#     ratio = 24.5 / 19.5
#     if ydiff == 0 and xdiff == 0:
#         print('surface is level')
#         return False
#     else:
#         if xdiff > 0:
#             cartesian_coord_steps_to_motor_commands('+i', xduration, ratio)
#         if xdiff < 0:
#             cartesian_coord_steps_to_motor_commands('-i', xduration, ratio)
#         if ydiff < 0:
#             cartesian_coord_steps_to_motor_commands('+j', yduration, ratio)
#         if ydiff > 0:
#             cartesian_coord_steps_to_motor_commands('-j', yduration, ratio)
#         return True


# def cartesian_coord_steps_to_motor_commands(command, duration, ratio):
#     motors = SendSerialCommands()
#     if command == '+i':
#         motors.move_motors([1, 3], 'f', duration)
#     if command == '-i':
#         motors.move_motors([2], 'f', duration * ratio)
#     if command == '+j':
#         motors.move_motors([1], 'b', duration * ratio)
#         motors.move_motors([2], 'b', duration * ratio ** 2)
#     if command == '-j':
#         motors.move_motors([3], 'b', duration * ratio)
#         motors.move_motors([2], 'b', duration * ratio ** 2)


def move_com_to_midpoint(com, midpoint):
    xdiff = midpoint[0] - com[0]
    ydiff = midpoint[1] - com[1]
    if ydiff == 0 and xdiff == 0:
        print('surface is level')
        return False
    else:
        coord_diffs_to_serial_commands(xdiff, ydiff)
        return True


def coord_diffs_to_serial_commands(xdiff, ydiff):
    scaling = 0.0001
    xduration = scaling * np.abs(xdiff)**2
    yduration = scaling * np.abs(ydiff)**2
    ratio = 24.5 / 19.5
    duration = [0, 0, 0, 0]
    if xdiff > 0:
        duration[1] += xduration
        duration[3] += xduration
    if xdiff < 0:
        duration[2] += xduration * ratio
    if ydiff < 0:
        duration[1] -= yduration * ratio
        duration[2] -= yduration * ratio ** 2
    if ydiff > 0:
        duration[3] -= yduration * ratio
        duration[2] -= yduration * ratio ** 2
    print(duration)
    motors = SendSerialCommands()
    motors.move_motors([1, 2, 3], duration)
