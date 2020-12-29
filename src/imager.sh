#!/bin/sh

if [ -d images]
then
    echo "images exist"
else
    mkdir images
fi

cd "example set"

counter=0
for f in *.mp3
do    
    bettername=${f::-4}
    echo $f
    echo $bettername

    yes | ffmpeg -i "${f}" "../images/${bettername}.jpg"
done