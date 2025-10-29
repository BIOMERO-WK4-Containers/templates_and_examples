import numpy as np
# TODO: add type declarations

# initial default values
my_param1 = 1
my_param2 = 2


def initiate_resources(param1, param2):
    """
    Example of (optional!) special function to one-time(!) pre-allocate
    resources so that the main workhorse code 'process()' need to do it...

    In this lame example, two parameters are taken and memorized to show
    one way of passing them for later 'process()'-ing.
    """
    global my_param1, my_param2
    my_param1 = param1
    my_param2 = param2

    print(f"initiating with param1 = {param1}")
    print(f"initiating with param2 = {param2}")


def process(input_tuple):
    """
    Example function that processes one processing unit of input.

    This "unit of input" can be a single image, but it is not limited to it and
    the unit can very well be a list/tuple, e.g., [image,aux_info,specific_params]
    where 'image' is the image to be processed taking into account additional
    (non-image?) data 'aux_info' with processing tailoring 'specific_params',
    which is specific to this data pair ('image'+'aux_info'). Another example
    could be a pair of [raw_image,mask_image] to collect average intensity
    in each mask, for example.

    Similarly, a list of (heterogenous) items should be returned as a result
    of the processing. The output list can also be empty '[]'.

    In this lame example, the code is assuming that a single image
    is provided, and that image is returned back as a fake result.
    Notice the un-/wrapping with lists.
    """

    # unpack the image from the input tuple
    img = input_tuple[0]

    # process the image
    print(f"doing fake work on an image of size: {img.shape}, and using params {my_param1}, {my_param2}")
    m = np.max(img) # just to touch the image pixels for the sake of fun

    # return the output as a list of results
    return [img]


def release_resources():
    print("just reporting that I'm now releasing my resources")

