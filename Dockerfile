## Create container using nvidia-docker and add shared memory size argument

FROM pytorch/pytorch:0.4.1-cuda9-cudnn7-runtime

ENV REPO_NAME=super-resolution-service
ENV PROJECT_ROOT=/root/${REPO_NAME}
ENV SERVICE_NAME=super-resolution
ENV PYTHONPATH=${PROJECT_ROOT}/service/lib
ENV SNETD_HOST=http://54.203.198.53
ENV SNETD_PORT=7017
ENV GRPC_HOST=http://localhost
ENV GRPC_PORT=7016
ENV SNETD_CONFIG=snetd.config.json

# Updating and installing common dependencies
RUN apt-get update
RUN apt-get install -y git wget unzip
RUN pip install --upgrade pip

# Cloning service repository to download models and install snet-cli and daemon
RUN cd /root/ &&\
    git clone https://github.com/ramongduraes/${REPO_NAME}.git &&\
    cd ${REPO_NAME} &&\
    . ./download_models.sh &&\
    . ./install_snet.sh

# Writing snetd.config.json
RUN cd ${PROJECT_ROOT} &&\
    sh -c "echo '{ \"PRIVATE_KEY\": \"1000000000000000000000000000000000000000000000000000000000000000\", \
                   \"DAEMON_LISTENING_PORT\": ${SNETD_PORT}, \
                   \"ETHEREUM_JSON_RPC_ENDPOINT\": \"https://kovan.infura.io\", \
                   \"PASSTHROUGH_ENABLED\": true, \
                   \"PASSTHROUGH_ENDPOINT\": \"${GRPC_HOST}:${GRPC_PORT}\", \
                   \"REGISTRY_ADDRESS_KEY\": \"0x2e4b2f2b72402b9b2d6a7851e37c856c329afe38\", \
                   \"DAEMON_END_POINT\": \"${SNETD_HOST}:${SNETD_PORT}\", \
                   \"IPFS_END_POINT\": \"http://ipfs.singularitynet.io:80\", \
                   \"ORGANIZATION_NAME\": \"snet\", \
                   \"SERVICE_NAME\": \"${SERVICE_NAME}\", \
                   \"LOG\": { \
                   \"LEVEL\": \"debug\", \
                   \"OUTPUT\": { \
                       \"TYPE\": \"stdout\" \
                       } \
                   } \
                }'" > ${SNETD_CONFIG}

# Installing projects's original dependencies and building protobuf messages
RUN cd ${PROJECT_ROOT} &&\
    pip3 install -r requirements.txt &&\
    sh buildproto.sh

WORKDIR ${PROJECT_ROOT}
