import cv2
import numpy as np
from labvision import images
from moviepy.editor import *


def format_im(im):
    greyscale_im = images.bgr_to_gray(im)
    blurred_im = images.median_blur(greyscale_im, 7)
    threshold_im = images.threshold(blurred_im, 88)
    threshold_im = np.uint32(threshold_im)
    return threshold_im


def trim_video(vid, start, stop):
    clip = VideoFileClip(vid).subclip(start, stop)
    clip.write_videofile("cropped_vid.mp4")


# def combine_boxes(video):
#     cap = cv2.VideoCapture(video)
#     i = 0
#     im1 = np.zeros((1270, 1450), dtype=int)
#     combined = im1
#     white_pixel_percentage = np.array([])
#
#     while cap.isOpened():
#         ret, frame = cap.read()
#         if ret == False:
#             break
#
#         im2 = format_im(frame)
#         both = im2 * im1
#         both = np.uint8(both / np.max(both) * 255)
#         combined += both
#         combined = images.threshold(combined / 255, 0.9)
#         images.display(combined)
#         no_white_pixels = np.sum(combined == 255)
#         percentage = no_white_pixels/combined.size
#         white_pixel_percentage = np.append(white_pixel_percentage, percentage)
#         im1 = im2
#         i += 1
#
#     cap.release()
#     cv2.destroyAllWindows()


def crop_video_into_grid(im, rows, cols):
    imwidth, imheight = im.shape
    box_height = int(imheight / rows)
    box_width = int(imwidth / cols)
    for i in range(0, imheight - box_height, box_height):
        for j in range(0, imwidth - box_width, box_width):
            cropped = im[j:j + box_width, i:i + box_height]
            combine_boxes(cropped)


def format_video_frame(im, frame_no, rows, cols):
    imwidth, imheight = im.shape
    box_height = int(imheight / rows)
    height_remainder = imheight % rows
    if height_remainder == 0:
        imheight += 1
    box_width = int(imwidth / cols)
    width_remainder = imwidth % rows
    if width_remainder == 0:
        imwidth += 1
    global white_pixel_percentage_array
    a = 0
    for i in range(0, imheight - box_height, box_height):
        b = 0
        for j in range(0, imwidth - box_width, box_width):
            cropped = im[j:j + box_width, i:i + box_height]
            if white_pixel_percentage_array[a][b] <= 99:
                no_white_pixels = np.sum(cropped == 255)
                white_pixel_percentage = (no_white_pixels / cropped.size)*100
                white_pixel_percentage_array[a][b] = white_pixel_percentage
                if white_pixel_percentage_array[a][b] >= 99:
                    white_pixel_percentage_array[a][b] = frame_no

            b += 1
        a += 1


def combine_boxes(video, rows, cols):
    cap = cv2.VideoCapture(video)
    i = 0
    im1 = np.zeros((1270, 1450), dtype=int)
    combined = im1
    frame_no = 100

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_no += 1
        im2 = format_im(frame)
        both = im2 * im1
        both = np.uint8(both / np.max(both) * 255)
        combined += both
        combined = images.threshold(combined / 255, 0.9)
        format_video_frame(combined, frame_no=frame_no, rows=rows, cols=cols)
        im1 = im2
        i += 1

    cap.release()

    cv2.destroyAllWindows()

    print(white_pixel_percentage_array - 100)


np.seterr(divide='ignore', invalid='ignore')
white_pixel_percentage_array = np.ones((10, 10))
combine_boxes('particles_annotate.mp4', 10, 10)
