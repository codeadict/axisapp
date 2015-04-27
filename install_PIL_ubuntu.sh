#!/bin/bash
#Install libraries PIL needs
sudo apt-get -y install python-dev libjpeg-dev libfreetype6-dev zlib1g-dev

#Create the links
sudo ln -s /usr/lib/`uname -i`-linux-gnu/libfreetype.so /usr/lib/
sudo ln -s /usr/lib/`uname -i`-linux-gnu/libjpeg.so /usr/lib/
sudo ln -s /usr/lib/`uname -i`-linux-gnu/libz.so /usr/lib/
ln -s /usr/include/freetype2 /usr/include/freetype

#Install PIL
pip install PIL --allow-external PIL --allow-unverified PIL

