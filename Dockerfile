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
RUN SNETD_VERSION=`curl -s https://api.github.com/repos/singnet/snet-daemon/releases/latest | grep -oP '"tag_name": "\K(.*)(?=")'` && \
    cd /tmp && \
    wget https://github.com/singnet/snet-daemon/releases/download/${SNETD_VERSION}/snet-daemon-${SNETD_VERSION}-linux-amd64.tar.gz && \
    tar -xvf snet-daemon-${SNETD_VERSION}-linux-amd64.tar.gz && \
    mv snet-daemon-${SNETD_VERSION}-linux-amd64/snetd /usr/bin/snetd

# Cloning service repository and downloading models
RUN mkdir -p ${SINGNET_REPOS} && \
    cd ${SINGNET_REPOS} &&\
    git clone -b ${git_branch} --single-branch https://github.com/${git_owner}/${git_repo}.git &&\
    cd ${SERVICE_DIR} &&\
    . ./download_models.sh

# Installing projects's original dependencies and building protobuf messages
RUN cd ${PROJECT_ROOT} &&\
    pip3 install -r requirements.txt &&\
    sh buildproto.sh

WORKDIR ${PROJECT_ROOT}
