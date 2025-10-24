# Building new image

...is as simple as this: `apptainer build  --fakeroot sandbox.sif singularity.def`

It creates an executable file `sandbox.sif` that just works as long as the hosting
OS contains a binary `run-singularity`.

You can also build your container as a slurm job like this `sbatch apptainer_build.slurm`

**nota bene: depending on the cluster you build the container in [SCRATCHDIR](SLURM/apptainer_build_tier1.slurm) or in [TMPDIR](SLURM/apptainer_build_tier2k.slurm) and copy it back to SCRATCHDIR**

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

Alternatively, you can also run your container as a slurm job: `sbatch apptainer_run.slurm`

***Nota bene: you need to check if you need to mount the [folders](SLURM/apptainer_run_tier2k.slurm) or the folders are already [mounted](SLURM/apptainer_run_tier1.slurm)

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

# Or if sudo is not allowed (i.e. HPC), use fakeroot
```

### Checking Container Contents

```bash
# Apptainer: inspect the container
apptainer inspect tiff_processor.sif
```

### Container folder contents

#### apptainer

- cellpose3_cuda121.def without [gui](https://github.com/vib-bic-training/HPC_bioimage_analysis/blob/main/Chapters/chapter6.md#use-case)
- cellpose4_cuda121.def with GUI and would be started using a desktop on a Open On Demand instance using `apptainer run cellpose4_cuda121.sif cellpose`
- metrics.def within [a nextflow pipeline](https://github.com/vib-bic-training/HPC_bioimage_analysis/blob/main/Chapters/chapter6.md#use-case)
- napari_empanada_devbio.def using a gui and starting from a nvidia pytorch cuda image 

