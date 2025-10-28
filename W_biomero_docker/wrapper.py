import numpy as np


def biomero_entry_point(args):

    from image_processing import MyAwesomeImgProcessing
    imgproc = MyAwesomeImgProcessing(2,3)

    # loop here
    img = np.zeros((30,20))
    imgproc.execute(img)
    imgproc.execute(img)

    imgproc.release_resources()


if __name__ == '__main__':
    biomero_entry_point([])

