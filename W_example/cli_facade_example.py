import click

@click.command()
@click.option('--in_file_path',  type=click.STRING, help='Path to the input image')
@click.option('--out_file_path', type=click.STRING, help='Path to the output image')
def cli_wrapper(in_file_path:str, out_file_path:str):
    """
    An CLI-friendly wrapper to test my own 'image_processing' directly
    and locally on some user-given input image. For BIOMERO dockerized
    solution, for example, this file is not required.
    """

    # just a sanity check, with an attempt to advise...
    if not in_file_path or not out_file_path:
        import sys
        print("Not happy with the parameters...\n")
        ctx = click.core.Context(cli_wrapper, info_name=sys.argv[0])
        print(cli_wrapper.get_help(ctx))
        return


    # from here follows the real utilization of the 'image_processing' code
    import tifffile as TIFF
    import image_processing as IP

    IP.initiate_resources(42, 24)

    img_i = TIFF.imread(in_file_path)
    img_o = IP.process([img_i])[0]     # notice the "list wrappings"
    TIFF.imwrite(out_file_path,img_o)

    # no point for releasing when this process code is going to an end anyway
    # ...still we release for the demo
    IP.release_resources()


if __name__ == '__main__':
    cli_wrapper()

