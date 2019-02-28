## Create container using nvidia-docker and add shared memory size argument
FROM pytorch/pytorch:0.4.1-cuda9-cudnn7-runtime

ARG git_owner
ARG git_repo
ARG git_branch
ENV SINGNET_REPOS=/opt/singnet
ENV PROJECT_ROOT=${SINGNET_REPOS}/${git_repo}
ENV SERVICE_DIR=${PROJECT_ROOT}/service

# Super resolution service specific:
ENV PYTHONPATH=${PROJECT_ROOT}/service/lib

# Updating and installing common dependencies
RUN apt-get update && \
    apt-get install -y \
    git \
    wget \
    unzip && \
    pip install --upgrade pip

# Installing snet-daemon + dependencies
RUN mkdir snet-daemon && \
    cd snet-daemon && \
    wget -q https://github.com/singnet/snet-daemon/releases/download/v0.1.7/snet-daemon-v0.1.7-linux-amd64.tar.gz && \
    tar -xvf snet-daemon-v0.1.7-linux-amd64.tar.gz  && \
    mv ./snet-daemon-v0.1.7-linux-amd64/snetd /usr/bin/snetd && \
    cd .. && \
    rm -rf snet-daemon

# Cloning service repository and downloading models
RUN mkdir -p ${SINGNET_REPOS} && \
    cd ${SINGNET_REPOS} &&\
    git clone https://github.com/${git_owner}/${git_repo}.git &&\
    cd ${SERVICE_DIR} &&\
    . ./download_models.sh

# Installing projects's original dependencies and building protobuf messages
RUN cd ${PROJECT_ROOT} &&\
    pip3 install -r requirements.txt &&\
    sh buildproto.sh

WORKDIR ${PROJECT_ROOT}
