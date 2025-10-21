# Building and Running TIFF Processor Containers

## Prerequisites

- Docker installed (for Docker container)
- Apptainer/Singularity installed (for Apptainer container)
- A test TIFF image file

## Building the Containers

### Docker

```bash
# Build the Docker image
docker build -t tiff-processor:latest .

# Verify the image was created
docker images | grep tiff-processor
```

### Apptainer/Singularity

```bash
# Build the Apptainer/Singularity image
# Option 1: Using fakeroot (recommended, no root needed)
apptainer build --fakeroot tiff_processor.sif tiff_processor.def

# Option 2: Using sudo (if fakeroot is not available)
sudo singularity build tiff_processor.sif tiff_processor.def

# Verify the image was created
ls -lh tiff_processor.sif
```

## Running the Containers

### Prepare Test Data

First, create a directory with your test TIFF image:

```bash
# Create a test directory
mkdir -p test_data

# Copy your TIFF image to the test directory and name it input.tif
cp /path/to/your/image.tif test_data/input.tif
```

### Run with Docker

```bash
# Run the Docker container with volume mount
docker run --rm \
    -v $(pwd)/test_data:/data \
    tiff-processor:latest

# Check the output
cat test_data/output.txt
```

### Run with Apptainer/Singularity

```bash
# Run the Apptainer container with bind mount
apptainer run \
    --bind $(pwd)/test_data:/data \
    tiff_processor.sif

# Or with singularity command
singularity run \
    --bind $(pwd)/test_data:/data \
    tiff_processor.sif

# Check the output
cat test_data/output.txt
```

## Alternative: Interactive Mode

### Docker Interactive

```bash
# Start an interactive shell in the container
docker run --rm -it \
    -v $(pwd)/test_data:/data \
    --entrypoint /bin/bash \
    tiff-processor:latest

# Inside the container, you can run the script manually:
python example_tiff_processor.py
```

### Apptainer Interactive

```bash
# Start an interactive shell in the container
apptainer shell \
    --bind $(pwd)/test_data:/data \
    tiff_processor.sif

# Inside the container, you can run the script manually:
python /app/example_tiff_processor.py
```

## Modifying the Hardcoded Path

If you want to use a different path instead of `/data/input.tif`, you have two options:

1. **Modify the script**: Edit `example_tiff_processor.py` and change the `IMAGE_PATH` variable
2. **Mount to different location**: Keep the script as-is and adjust your bind/volume mount

Example for option 2:

```bash
# Docker: mount your data to /data
docker run --rm -v /home/user/images:/data tiff-processor:latest

# Apptainer: mount your data to /data
apptainer run --bind /home/user/images:/data tiff_processor.sif
```

## Troubleshooting

### Permission Issues

If you encounter permission issues with Docker:

```bash
# Run with user permissions
docker run --rm \
    -v $(pwd)/test_data:/data \
    -u $(id -u):$(id -g) \
    tiff-processor:latest
```

### Apptainer Fakeroot Issues

If fakeroot doesn't work:

```bash
# Use remote build (requires network)
apptainer build --remote tiff_processor.sif tiff_processor.def

# Or use sudo
sudo singularity build tiff_processor.sif tiff_processor.def
```

### Checking Container Contents

```bash
# Docker: list files in container
docker run --rm tiff-processor:latest ls -la /app

# Apptainer: inspect the container
apptainer inspect tiff_processor.sif
```