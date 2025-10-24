# Building new image

```bash
# create a builder (of name "tiff-builder") and make it "the current builder" (--use)
sudo docker buildx create --name tiff-builder --use
#
# or, make sure to use the default builder
sudo docker buildx use default

# builds our receipe into the current local instance (--load)
sudo docker buildx build -f dockerfile.txt --load .

# same as above but give an explicit name (tag!) to the created image
sudo docker buildx build -t tiff:latest -f dockerfile.txt --load .
```


# Rename an existing image

- List images: `sudo docker images`
- Rename: `sudo docker tag a537bed1c1e6 tiff:latest`
  - Here, 'IMAGE ID' has been used, it is visible under the `images` command


# Run an existing image

The pattern is `sudo docker run --rm image_name params`, this implicitly creates
a container (which is an actual executable instance of the image), executes it,
and removes the container afterwards (this is due to the `--rm` parameter). Btw,
the existing containers (live running as well as finished ones) can be listed with
`sudo docker container ls -a`.

Following up the example above

`sudo docker run --rm tiff:latest /temp/input.tif`

and again with mapping a real `/temp` folder into a "virtual"
Docker folder `/tempX`; notice the parameter follows the "virtual" path

`sudo docker run --rm -v/temp:/tempX  tiff2:latest  /tempX/input2.tif`

Any command-line arguments will be passed to the containerized workhorse script.


# Interactive Mode

```bash
# Start an interactive shell in the container
docker run --rm -it \
    -v $(pwd)/test_data:/data \
    --entrypoint /bin/bash \
    tiff-processor:latest

# Inside the container, you can run the script manually:
python example_tiff_processor.py
```
# CLI

- docker_metrics run as CLI
```bash
docker run     -v "$(pwd)/tiff_images:/app/image"     -v "$(pwd)/output/output:/app/output" -v "$(pwd)/bin:/app/bin" -v "$(pwd)/output_metrics:/app/output_metrics"  metrics python "/app/bin/metrics.py"  --image_path "/app/image/604_img.tif"     --label_path "/app/output/604_img_mask.tif" --output_dir "app/output_metrics"
```
- cellpose 4 run inside a nextflow pipeline
# Troubleshooting

If you encounter permission issues with Docker:

```bash
# Run with user permissions
docker run --rm \
    -v $(pwd)/test_data:/data \
    -u $(id -u):$(id -g) \
    tiff-processor:latest
```

### Checking Container Contents

```bash
# Docker: list files in container
docker run --rm tiff-processor:latest ls -la /app
```

