#!/usr/bin/env bash

echo "Downloading models."

MODELSDIR=./service/models

mkdir -p $MODELSDIR/proSR
mkdir -p $MODELSDIR/proSRGAN

##################################
####### Pretrained Models ########
##################################

# ProSR
wget -q https://www.dropbox.com/s/3fjp5dd70wuuixl/proSR.zip?dl=0 -O /tmp/proSR.zip
unzip -j /tmp/proSR.zip -d $MODELSDIR/proSR/ && rm /tmp/proSR.zip

# ProSRGAN
wget -q https://www.dropbox.com/s/ulkvm4yt5v3vxd8/proSRGAN.zip?dl=0 -O /tmp/proSRGAN.zip
unzip -j /tmp/proSRGAN.zip -d $MODELSDIR/proSRGAN/ && rm /tmp/proSRGAN.zip

echo "Models successfully downloaded."
