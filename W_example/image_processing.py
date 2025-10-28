import sys
sys.path.append("../W_prototypes")
from prototypes import PrototypeImgToImg
import numpy as np

class MyAwesomeImgProcessing(PrototypeImgToImg):

    # TODO: add types
    def __init__(self, param1, param2):
        self.param1 = param1
        self.param2 = param2

        print(f"initiating with param1 = {param1}")
        print(f"initiating with param2 = {param2}")


    # TODO: add types for numpy-like arrays
    def execute(self, img):
        print(f"doing fake work on an image of size: {img.shape}, and using params {self.param1}, {self.param2}")
        return img


    def release_resources(self):
        print("just reporting that I'm now releasing my resources")


import click
@click.command()
@click.option('--param1', default=1, help='Info for param1')
@click.option('--param2', help='Foo and blah for param2')
def cli_wrapper(param1,param2):
    imgproc = MyAwesomeImgProcessing(param1,param2)

    img = np.zeros((10,10))
    imgproc.execute(img)
    imgproc.execute(img)
    # no point for releasing when this process code is going to an end anyway


if __name__ == '__main__':
    cli_wrapper()

