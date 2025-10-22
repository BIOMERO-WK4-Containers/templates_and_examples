# Containerization of Python scripts

This is an example project of a naive TIFF image file reader and reporter of the images parameters.

The script may have an optional parameter, which is a image file path to be examined.
The script writes `/temp/output.txt` file with again some image parameters.

## No-container testing

Below is a pixi project file `pixi.toml` that allows to test the scripts directly
in the host environment. Just start it by:

```bash
pixi shell
python ...
```

## Wrapping into containers, and testing

Currently the Docker and Apptainer containerization platforms are supported,
and their configuration/definition files as well as respective `HOW_TO_USE.md`
files are to be found in the respective sub-folders.

The very step, however, is to create hard-links of python scripts from
this "root" folder in the two sub-folders, simply by running:

```bash
source hardlink_py_files_to_inside_containers.cmd
```

The sub-folders are then ready and self-contained.

# TODOs

**1.** Extract commonalities from the containers' definition files and extract them,
and prepare a script (wizard?) that prepares the respective definition files
so that both containers differ really only in the containerization technique itself.


**2.** Add a layer, or specific layers, that connect the script (and perhaps also
the containers) to a particular system such as Nextflow or BIOMERO.

