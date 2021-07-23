import numpy as np
import cv2
from labvision import images
from labequipment import arduino
from labvision import camera
from serial_commands import SendSerialCommands


def get_level(duration=3):
    uneven = True
    cam = camera.Panasonic()
    while uneven:
        im = cam.get_frame(delete=True)
        threshold_im, contour = find_contour(im)
        cropped_im = crop_to_rotated_rectangular_contour(threshold_im, contour)
        com, midpoint = get_com_and_midpoint(cropped_im)
        uneven = move_com_to_midpoint(com, midpoint, duration)


def find_contour(im):
    greyscale_im = images.bgr_to_gray(im)
    threshold_im = images.threshold(greyscale_im, 75)

    contours = images.find_contours(threshold_im)
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


def move_com_to_midpoint(com, midpoint, duration):
    xdiff = midpoint[0] - com[0]
    ydiff = midpoint[1] - com[1]
    magnitude = np.sqrt(xdiff ** 2 + ydiff ** 2)
    duration = duration * (magnitude / 1000)
    ratio = 24.5 / 19.5
    if ydiff == 0 and xdiff == 0:
        print('surface is level')
        return False
    else:
        if xdiff > 0:
            cartesian_coord_steps_to_motor_commands('+i', duration, ratio)
        if xdiff < 0:
            cartesian_coord_steps_to_motor_commands('-i', duration, ratio)
        if ydiff < 0:
            cartesian_coord_steps_to_motor_commands('+j', duration, ratio)
        if ydiff > 0:
            cartesian_coord_steps_to_motor_commands('-j', duration, ratio)
        return True


def cartesian_coord_steps_to_motor_commands(command, duration, ratio):
    motors = SendSerialCommands()
    if command == '+i':
        motors.move_motors([1, 2], 'f', duration)
    if command == '-i':
        motors.move_motors([3], 'f', duration * ratio)
    if command == '+j':
        motors.move_motors([2], 'b', duration * ratio)
        motors.move_motors([3], 'b', duration * ratio ** 2)
    if command == '-j':
        motors.move_motors([1], 'b', duration * ratio)
        motors.move_motors([3], 'b', duration * ratio ** 2)
