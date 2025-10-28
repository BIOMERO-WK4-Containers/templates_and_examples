import sys
sys.path.append("../W_prototypes")
from prototypes import PrototypeImgToImg

import click

class MyAwesomeImgProcessing(PrototypeImgToImg):

	 # TODO: add types
    def __init__(self, param1, param2):
        print(f"initiating with param1 = {param1}")
        print(f"initiating with param2 = {param2}")


	 # TODO: add types for numpy-like arrays
    def execute(img):
        print(f"doing fake work on an image of size: {img.shape}")
        return img


    def release_resources():
        print("just reporting that I'm now releasing my resources")


@click.command()
@click.option('--param1', default=1, help='Info for param1')
@click.option('--param2', help='Foo and blah for param2')
def cli_wrapper(param1,param2):
	imgproc = MyAwesomeImgProcessing(param1,param2)
	imgproc.execute()
	# no point for releasing when this process code is going to an end anyway


if __name__ == '__main__':
	cli_wrapper()

