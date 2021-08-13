import time

import numpy as np
import cv2
from labvision import images
from labvision import camera
from serial_commands import SendSerialCommands


def get_level(threshold=85, tau=60):
    """
    Top-level function. When called this calls daughter functions and levels the system

    :param threshold: Defines cutoff between particles and background

    :return: Returns true once levelled, false if errors.
    """
    try:
        not_level = True
        cam = camera.Panasonic()
        while not_level:
            im = cam.get_frame(delete=True)
            im = images.rotate(im, 180)
            threshold_im, contour = find_contour(im, threshold=threshold)
            crop_rot_im = crop_to_rotated_rectangular_contour(threshold_im, contour)
            com, midpoint = get_com_and_midpoint(crop_rot_im)
            print(com, midpoint)
            not_level = level(com, midpoint)
            time.sleep(tau)
        return True
    except:
        return False

def find_contour(im, threshold=85):
    """
    Finds boundary of light square surface

    :param im:
    :param threshold:
    :return: thresholded image and biggest contour
    """
    greyscale_im = images.bgr_to_gray(im)
    threshold_im = images.threshold(greyscale_im, threshold)

    kernel = np.ones((50, 50), np.uint8)
    no_particles_im = cv2.morphologyEx(threshold_im, cv2.MORPH_CLOSE, kernel)

    contours = images.find_contours(no_particles_im)
    sorted_contours = images.sort_contours(contours)
    biggest_contour = sorted_contours[-1]

    return threshold_im, biggest_contour


def crop_to_rotated_rectangular_contour(threshold_im, contour):
    """
    Rotates and crops thresholded img
    :param img:
    :param contour:
    :return:
    """
    rect = cv2.minAreaRect(contour)
    # rotate img
    angle = rect[2]
    if angle > 0:  # angle needs to be negative
        angle -= 90
    rows, cols = threshold_im.shape[0], threshold_im.shape[1]
    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)
    img_rot = cv2.warpAffine(threshold_im, M, (cols, rows))

    # rotate bounding box
    rect0 = (rect[0], rect[1], 0.0)
    box = cv2.boxPoints(rect0)
    pts = np.int0(cv2.transform(np.array([box]), M))[0]
    pts[pts < 0] = 0

    # crop
    img_crop_rot = img_rot[pts[1][1]:pts[0][1], pts[1][0]:pts[2][0]]
    img_crop_rot = img_crop_rot[18:-18, 18:-18]

    return img_crop_rot


def get_com_and_midpoint(im):
    midpoint = (int(im.shape[0] / 2), int(im.shape[1] / 2))

    inverted_im = cv2.bitwise_not(im)
    com = images.center_of_mass(inverted_im) #assumes dark

    return com, midpoint


def level(com, midpoint):
    """
    one iteration of levelling in response to image analysis

    :param com:
    :param midpoint:
    :return:
    """
    xdiff = midpoint[0] - com[0]
    ydiff = midpoint[1] - com[1]
    if abs(ydiff) <= 20 and abs(xdiff) <= 20:
        print('surface is level')
        return False
    else:
        coord_diffs_to_serial_commands(xdiff, ydiff)
        return True


def coord_diffs_to_serial_commands(xdiff, ydiff):
    """
    Communicates with arduino and tells it how to move the motors

    :param xdiff: Difference between COM and midpoint on x
    :param ydiff: Difference between COM and midpoint on y
    :return:
    """
    scaling = 0.015
    xmove = scaling * np.abs(xdiff)
    ymove = scaling * np.abs(ydiff)
    ratio = 24.5 / 19.5
    move = [0, 0, 0]
    if xdiff > 20:
        move[0] += xmove
        move[2] += xmove
    if xdiff < -20:
        move[1] += xmove * ratio
    if ydiff < -20:
        move[0] -= ymove * ratio
        move[1] -= ymove * ratio ** 2
    if ydiff > 20:
        move[2] -= ymove * ratio
        move[1] -= ymove * ratio ** 2
    print(move)
    motors = SendSerialCommands()
    motors.move_motors([1, 2, 3], move)
