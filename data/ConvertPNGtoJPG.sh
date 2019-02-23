#!/bin/bash

for IMAGE in *.png
do
    IMAGE="${IMAGE%.*}"
    echo $IMAGE
    convert "$IMAGE".png "$IMAGE".jpg
    rm "$IMAGE".png
done