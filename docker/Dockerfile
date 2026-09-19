FROM ubuntu:noble
LABEL org.opencontainers.image.title="marinholab-sas-core build environment"
LABEL authors="murilomarinho"
SHELL ["/bin/bash", "-c"]

ENV DEBIAN_FRONTEND=noninteractive

# Build tooling, C++ dependencies and the Python toolchain.
# libdqrobotics (headers + shared library) is not in the Ubuntu repositories;
# it is provided by the DQ Robotics PPA (noble, amd64/arm64).
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential g++ cmake make pkg-config ninja-build \
        python3-dev python3-pip \
        libeigen3-dev \
        software-properties-common ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN add-apt-repository -y ppa:dqrobotics-dev/development \
    && apt-get update \
    && apt-get install -y --no-install-recommends libdqrobotics \
    && rm -rf /var/lib/apt/lists/*

# The dqrobotics headers use <Eigen/Dense> (without the eigen3/ prefix);
# provide the conventional include path for them.
RUN ln -s /usr/include/eigen3/Eigen /usr/include/Eigen

# Build-time Python packages (used with `pip install --no-build-isolation`).
RUN python3 -m pip install --no-cache-dir --break-system-packages \
        setuptools wheel ninja setuptools-git-versioning

WORKDIR /opt/sas_py
# `COPY .` includes the populated git-submodule trees (submodules/sas_cpp,
# submodules/pybind11) from the build context. No `git submodule update` is
# needed inside the image because CMake consumes them as plain source trees
# (via add_subdirectory), not via git.
COPY . /opt/sas_py

CMD ["bash", "/opt/sas_py/docker/build.sh"]
