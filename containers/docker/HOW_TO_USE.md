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

