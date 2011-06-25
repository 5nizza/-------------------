#!/bin/sh

DIRECTORY=3rd_party
if [ -d "$DIRECTORY" ]; then
    echo $DIRECTORY already exist, remove it first
    exit
fi

mkdir $DIRECTORY
tmp_file=3rd_party/3rd_party.tar.gz
echo "downloading.."
wget "http://dl.dropbox.com/u/444947/3rd_party.tar.gz" -O $tmp_file
echo "unpacking.."
tar -xf $tmp_file -C 3rd_party/
rm $tmp_file

echo "done"
