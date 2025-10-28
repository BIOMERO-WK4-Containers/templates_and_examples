class PrototypeImgToImg:

    def execute(img):
        """
        This method is meant to be overridden by downstream
        code and it is here where the image processing shall happen.

        The method must return an image.
        (There will be another classes that would request
        that different types are returned, e.g. pandas or
        writing csv files directly or such...)
        """
        return img

    def release_resources():
        """
        This method is intended to have a unique way to
        ask one's own image processing routine to close itself,
        that said, release its resources etc.

        An object **must not** be used anymore after
        this method is called.
        """
        pass


class PrototypeImgToList:

    def execute(img):
        """
        This method is meant to be overridden by downstream
        code and it is here where the image processing shall happen.

        The method shall return a list of values -- measurements
        on the input image.
        (There will be another classes that would request
        that different types are returned...)
        """
        return img

    def release_resources():
        """
        This method is intended to have a unique way to
        ask one's own image processing routine to close itself,
        that said, release its resources etc.

        An object **must not** be used anymore after
        this method is called.
        """
        pass

