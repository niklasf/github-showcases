#!/bin/bash -e

# Clone all repositories.

tail -n +2 showcases.tsv | while read URL META
do
    OWNER=$(echo $URL | cut -d/ -f4)
    mkdir -p "mirror/$OWNER"
    cd "mirror/$OWNER"
    git clone "$URL"
    cd ../..
done
