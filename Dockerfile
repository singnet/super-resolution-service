## Create container using nvidia-docker and add shared memory size argument
FROM pytorch/pytorch:1.1.0-cuda10.0-cudnn7.5-runtime

ARG git_owner
ARG git_repo
ARG git_branch
ENV SINGNET_REPOS=/opt/singnet
ENV PROJECT_ROOT=${SINGNET_REPOS}/${git_repo}
ENV MODEL_PATH=${PROJECT_ROOT}/service/models

# Super resolution service specific:
ENV PYTHONPATH=${PROJECT_ROOT}/service/lib

# Updating and installing common dependencies
RUN apt-get update && \
    apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    git \
    wget \
    nano \
    sudo \
    unzip && \
    pip install --upgrade pip

# Installing snet-daemon + dependencies
RUN SNETD_VERSION=`curl -s https://api.github.com/repos/singnet/snet-daemon/releases/latest | grep -oP '"tag_name": "\K(.*)(?=")' || echo "v3.1.1"` && \
    echo 'version' $SNETD_VERSION && \
    wget https://github.com/singnet/snet-daemon/releases/download/${SNETD_VERSION}/snet-daemon-${SNETD_VERSION}-linux-amd64.tar.gz && \
    tar -xvf snet-daemon-${SNETD_VERSION}-linux-amd64.tar.gz && \
    sudo mv snet-daemon-${SNETD_VERSION}-linux-amd64/snetd /usr/bin/snetd

# Cloning service repository and downloading models
RUN mkdir -p ${SINGNET_REPOS} && \
    cd ${SINGNET_REPOS} &&\
    git clone -b ${git_branch} --single-branch https://github.com/${git_owner}/${git_repo}.git &&\
    cd ${MODEL_PATH} &&\
    wget --no-check-certificate https://snet-models.s3.amazonaws.com/bh/PreTrainedDNNModels/RRDB_ESRGAN_x4.pth

# Installing projects's original dependencies and building protobuf messages
RUN cd ${PROJECT_ROOT} &&\
    pip3 install -r requirements.txt &&\
    sh buildproto.sh

WORKDIR ${PROJECT_ROOT}
