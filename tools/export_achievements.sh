#!/bin/bash

for filename in ../assets/achievements/*.svg; do
    echo $filename
    echo $(basename "$filename")
    inkscape -h 512 ../achievements/$filename -o "../app/static/img/achievements/$(basename "$filename" .svg).png"
done
