#!/usr/bin/env bash

MODELSDIR=./models
mkdir -p $MODELSDIR

##################################
# Pretrained Models
##################################

# ProSR
wget https://www.dropbox.com/s/3fjp5dd70wuuixl/proSR.zip?dl=0 -O /tmp/proSR.zip
unzip -j /tmp/proSR.zip -d $MODELSDIR && rm /tmp/proSR.zip

# ProSRGAN
wget https://www.dropbox.com/s/ulkvm4yt5v3vxd8/proSRGAN.zip?dl=0 -O /tmp/proSRGAN.zip
unzip -j /tmp/proSRGAN.zip -d $MODELSDIR && rm /tmp/proSRGAN.zip