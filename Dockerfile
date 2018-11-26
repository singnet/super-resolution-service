## Create container using nvidia-docker and add shared memory size argument

FROM pytorch/pytorch:0.4.1-cuda9-cudnn7-runtime

ENV REPO_NAME=super-resolution-service
ENV PROJECT_ROOT=/root/${REPO_NAME}
ENV PYTHONPATH=${PROJECT_ROOT}/lib
ENV SNETD_PORT=7027

RUN apt-get update
RUN apt-get install -y wget unzip
RUN pip install --upgrade pip

# Installing original repository dependencies
RUN yes | pip install scikit-image easydict
#                   torchvision==0.1.8 Cython html / maybe visdom dominate -c conda-forge

# Cloning service repository to download models and install snet-cli and daemon
RUN git clone https://github.com/ramongduraes/${REPO_NAME}.git &&\
    cd ${REPO_NAME} &&\
    . ./download_models.sh &&\
    . ./install_snet.sh
