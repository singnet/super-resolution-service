#!/usr/bin/env bash

echo "Installing snet components."

# Can take a programming language as input to run additional setup steps
LANGUAGE="$1"

# Set environment
export SINGNET_REPOS=/opt/singnet
export GOPATH=${SINGNET_REPOS}/go
export PATH=${GOPATH}/bin:${PATH}

mkdir -p ${GOPATH}

# Dependencies and utilities
apt-get update && \
apt-get install -y \
        apt-utils \
        nano \
        git \
        wget \
        curl \
        zip \
        libudev-dev \
        libusb-1.0-0-dev

# Install nodejs npm and python3
apt-get install -y nodejs npm
apt-get install -y python3 python3-pip

# Install snet-cli
cd ${SINGNET_REPOS} && \
git clone https://github.com/singnet/snet-cli && \
cd snet-cli && \
./scripts/blockchain install && \
pip3 install -e .

# Install snet-daemon
cd ${SINGNET_REPOS} && \
mkdir snet-daemon && \
cd snet-daemon && \
wget -q https://github.com/singnet/snet-daemon/releases/download/v0.1.2/snetd-0.1.2.tar.gz && \
tar -xvf snetd-0.1.2.tar.gz && \
mv snetd-0.1.2/snetd-linux-amd64 /usr/bin/snetd

# Language dependent extra installation steps
if [[ "$LANGUAGE" = "cpp" ]]; then
    apt-get install -y build-essential autoconf libtool pkg-config libgflags-dev libgtest-dev clang libc++-dev
    git clone -b $(curl -L https://grpc.io/release) https://github.com/grpc/grpc
    cd grpc
    git submodule update --init
    make
    make install
    apt-get install -y openjdk-8-jdk
    echo "deb [arch=amd64] http://storage.googleapis.com/bazel-apt stable jdk1.8" | tee /etc/apt/sources.list.d/bazel.list
    curl https://bazel.build/bazel-release.pub.gpg | apt-key add -
    apt-get update
    apt-get install -y bazel
    apt-get upgrade -y bazel
    bazel build :all
    make install
    cd third_party/protobuf
    make
    make install
elif [[ "$LANGUAGE" = "go" ]]; then
    apt-get install -y golang go-dep golang-goprotobuf-dev golint
    go get -v -u google.golang.org/grpc
elif [[ "$LANGUAGE" = "java" ]]; then
    apt-get install -y unzip openjdk-8-jdk
    curl -OL https://github.com/google/protobuf/releases/download/v3.6.1/protoc-3.6.1-linux-x86_64.zip
    unzip protoc-3.6.1-linux-x86_64.zip -d protoc3
    mv protoc3/bin/* /usr/local/bin/
    mv protoc3/include/* /usr/local/include/
    rm -rf protoc3
    rm protoc-3.6.1-linux-x86_64.zip
    curl -OL http://central.maven.org/maven2/io/grpc/protoc-gen-grpc-java/1.16.1/protoc-gen-grpc-java-1.16.1-linux-x86_64.exe
    mv protoc-gen-grpc-java-1.16.1-linux-x86_64.exe /usr/local/bin/protoc-gen-grpc-java
    chmod +x /usr/local/bin/protoc-gen-grpc-java
else
    echo "Optional argument (programming language) not specified or not recognized (should be go, cpp or java)."
fi

echo "Snet components successfully installed."
