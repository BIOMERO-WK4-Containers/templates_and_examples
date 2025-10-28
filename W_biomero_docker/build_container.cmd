cd ..
sudo docker buildx build -t "template_biomero_container" -f $OLDPWD/Docker --load .
cd -
