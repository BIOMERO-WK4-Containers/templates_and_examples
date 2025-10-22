cd apptainer
for i in ../*.py; do ln -v $i; done

cd ../docker
for i in ../*.py; do ln -v $i; done

cd ..
