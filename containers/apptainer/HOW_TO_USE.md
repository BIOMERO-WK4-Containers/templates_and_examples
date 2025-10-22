# Building new image

...is as simple as this: `apptainer build  --fakeroot sandbox.sif singularity.def`

It creates an executable file `sandbox.sif` that just works as long as the hosting
OS contains a binary `run-singularity`.


# Rename an existing image

Renaming the `.sif` file should just do it... I guess, haven't tested.


# Run an existing image

One way is to execute the created `.sif` file directly (by standard means
of the OS), e.g., as `./sandbox.sif`. Any command-line arguments will be
passed to the containerized workhorse script.

Alternatively, the same thing can be achieved "explicitly"
with the `apptainer` application:

`apptainer run sandbox.sif /temp/input.tif`

The example passes a path as an argument to the script. This path is
evaluated within the container, and can be made to overlay a real path:

`apptainer run --bind /temp:/tempQW sandbox.sif /tempQW/input.tif`


# Interactive Mode

```bash
# Start an interactive shell in the container
apptainer shell \
    --bind $(pwd)/test_data:/data \
    tiff_processor.sif

# Inside the container, you can run the script manually:
python /app/example_tiff_processor.py
```

# Troubleshooting

If fakeroot doesn't work:

```bash
# Use remote build (requires network)
apptainer build --remote tiff_processor.sif tiff_processor.def

# Or use sudo
sudo singularity build tiff_processor.sif tiff_processor.def
```

### Checking Container Contents

```bash
# Apptainer: inspect the container
apptainer inspect tiff_processor.sif
```

