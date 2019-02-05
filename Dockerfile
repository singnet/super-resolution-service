## Create container using nvidia-docker and add shared memory size argument

FROM pytorch/pytorch:0.4.1-cuda9-cudnn7-runtime

ENV GITHUB_ACCOUNT=ramongduraes
ENV REPO_NAME=super-resolution-service
ENV PROJECT_ROOT=/root/${REPO_NAME}
ENV SERVICE_DIR=${PROJECT_ROOT}/service
ENV SERVICE_NAME=super-resolution
ENV PYTHONPATH=${PROJECT_ROOT}/service/lib

# Updating and installing common dependencies
RUN apt-get update
RUN apt-get install -y git wget unzip
RUN pip install --upgrade pip

# Installing SNET (snet-cli and snet-daemon + dependencies)
RUN mkdir snet-daemon && \
    cd snet-daemon && \
    wget -q https://github.com/singnet/snet-daemon/releases/download/v0.1.6/snet-daemon-v0.1.6-linux-amd64.tar.gz && \
    tar -xvf snet-daemon-v0.1.6-linux-amd64.tar.gz  && \
    mv ./snet-daemon-v0.1.6-linux-amd64/snetd /usr/bin/snetd && \
    cd .. && \
    rm -rf snet-daemon

# Cloning service repository and downloading models
RUN cd /root/ &&\
    git clone https://github.com/${GITHUB_ACCOUNT}/${REPO_NAME}.git &&\
    cd ${SERVICE_DIR} &&\
    . ./download_models.sh

# Installing projects's original dependencies and building protobuf messages
RUN cd ${PROJECT_ROOT} &&\
    pip3 install -r requirements.txt &&\
    sh buildproto.sh

WORKDIR ${PROJECT_ROOT}
