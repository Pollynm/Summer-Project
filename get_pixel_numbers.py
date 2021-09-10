import numba as np
from labvision import video
from test_crop import *
import matplotlib.pyplot as plt


@profile
def get_white_pixel_no(vid_fname, stop=2, rows=10, cols=5):
    '''
    :param vid_fname: video to analyse
    :param stop: timestamp to stop analysis (s)
    :param rows: number of rows to split video into
    :param cols: number of columns
    :return: a 3d array containing the number of white pixels in each box of the video grid
    '''

    im1 = np.ones((10, 5, 1), dtype=np.int32)
    max_frame = int(stop * 50)
    cap = video.ReadVideo(vid_fname)
    frame_no = 0
    for frame in cap:
        if frame_no == 0:
            shape = frame[:, :, 0].reshape(rows, cols, -1).shape
            cumulative_im = np.zeros(shape)
        if frame_no > max_frame:
            break
        cumulative_im, im1 = combine_boxes(im1=im1, frame=frame, cumulative_im=cumulative_im, rows=rows, cols=cols)
        frame_no += 1
    cv2.destroyAllWindows()
    white_pixel_no = np.count_nonzero(cumulative_im, axis=2)
    return white_pixel_no


def get_pixels_and_graph(vid_fname, stop=0.5, rows=10, cols=5):
    '''
    same as get_white_pixel_no but displays the process of the video frames being combined and plots the time evolution
    of white pixel number for each box - much slower
    '''
    im1 = np.ones((10, 5, 1), dtype=np.int32)
    max_frame = int(stop * 50)
    white_pixel_no = np.zeros((max_frame + 1, rows, cols))
    cap = video.ReadVideo(vid_fname)
    frame_no = 0
    disp = images.Displayer('')
    for frame in cap:
        if frame_no == 0:
            shape = frame[:, :, 0].reshape(rows, cols, -1).shape
            cumulative_im = np.zeros(shape)
        if frame_no > max_frame:
            break
        cumulative_im, im1 = combine_boxes(im1=im1, frame=frame, cumulative_im=cumulative_im, rows=rows, cols=cols)
        show_pixel_evolution(disp=disp, cumulative_im=cumulative_im)
        white_pixel_no[frame_no] = np.count_nonzero(cumulative_im, axis=2)
        frame_no += 1
    cv2.destroyAllWindows()
    plot_pixel_graph()
    return white_pixel_no


def format_im(im):
    '''
    makes images binary
    '''
    greyscale_im = images.bgr_to_gray(im)
    threshold_im = images.threshold(greyscale_im, 88)
    threshold_im = np.uint32(threshold_im)
    return threshold_im


# @profile
def combine_boxes(im1, frame, cumulative_im, rows, cols):
    '''
    makes video frames binary, splits them into a grid, combines current frames with the previous ones and adds the
    result to a cumulative image
    '''
    im2 = format_im(frame)
    im2 = im2.reshape(rows, cols, -1)
    im1 += 1
    im1 = np.where(im1 < 2, im1, 0)
    combined_image = im2 * im1
    cumulative_im += combined_image
    return cumulative_im, im2


def show_pixel_evolution(disp, cumulative_im):
    '''
    displays the cumulative image combination as video frames are being added to it
    '''
    display_im = cumulative_im.reshape(1270, 1450)
    display_im = np.uint8(display_im / np.max(display_im) * 255)
    display_im = images.threshold(display_im, 1)
    disp.update_im(display_im)


def plot_pixel_graph():
    '''
    plots a graph of white pixel number versus time for every box in the video grid
    '''
    t = np.arange(0, 0.52, 0.02)
    pixel_no = get_white_pixel_no('particles_annotate.mp4')
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xscale('log')

    for i in range(np.shape(pixel_no)[1]):
        for j in range(np.shape(pixel_no)[2]):
            ax.plot(t, pixel_no[:, i, j])

    plt.show()


a = get_white_pixel_no('particles_annotate.mp4')



