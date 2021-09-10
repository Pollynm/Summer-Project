from PIL import Image
import cv2
from labvision import images

# def crop(path, input, height, width, k, page, area):
#     im = Image.open(input)
#     imgwidth, imgheight = im.size
#     for i in range(0, imgheight, height):
#         for j in range(0, imgwidth, width):
#             box = (j, i, j + width, i + height)
#             a = im.crop(box)
#             try:
#                 o = a.crop(area)
#                 o.save(os.path.join(path, "PNG", "%s" % page, "IMG-%s.png" % k))
#             except:
#                 pass
#             k += 1
#
#
def crop(filename, rows, cols):
    im = cv2.imread(filename)
    imwidth, imheight, channel = im.shape
    box_height = int(imheight/rows)
    box_width = int(imwidth/cols)
    for i in range(0, imheight, box_height):
        for j in range(0, imwidth, box_width):
            cropped = im[j:j + box_width, i:i + box_height]
            images.display(cropped)


crop('kang0.jpg', 1000, 1000)

# cap = cv2.VideoCapture('particles_annotate.mp4')
# i = 0
# while cap.isOpened():
#     ret, frame = cap.read()
#     if ret == False:
#         break
#     cv2.imwrite('kang' + str(i) + '.jpg', frame)
#     i += 1
#
# cap.release()
# cv2.destroyAllWindows()

