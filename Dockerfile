# build with command:
# docker build -t comic-dl:py3.8-buster .
# run with alias
# alias comic_dl="docker run -it --rm -e PGID=$(id -g) -e PUID=$(id -u) -v $(pwd):/directory:rw -w /directory comic-dl:py3.8-buster comic_dl -dd /directory"

# for armv7,
# cross build it (it takes a few hours on x86_64), or be prepared to wait an eternity
# build with command:
# docker build -t comic-dl:py3.8-buster-armv7 --platform linux/arm/v7 .
# export with command
# docker save -o comic-dl.tar comic-dl:py3.8-buster-armv7
# import on arm machine with command:
# docker load --input comic-dl.tar
# run with alias:
# alias comic_dl="docker run -it --rm -e PGID=$(id -g) -e PUID=$(id -u) -v $(pwd):/directory:rw -w /directory comic-dl:py3.8-buster-armv7 comic_dl -dd /directory"

FROM --platform=linux/amd64 python:3.8-slim-buster as stage-amd64
RUN DEBIAN_FRONTEND=noninteractive apt-get update && DEBIAN_FRONTEND=noninteractive apt-get -yq upgrade
ARG TARGETOS
ARG TARGETARCH
ARG TARGETVARIANT
RUN echo "I'm building for $TARGETOS/$TARGETARCH/$TARGETVARIANT"

FROM --platform=linux/arm/v7 python:3.8-slim-buster as stage-armv7
ARG TARGETOS
ARG TARGETARCH
ARG TARGETVARIANT
RUN echo "I'm building for $TARGETOS/$TARGETARCH/$TARGETVARIANT"

ENV LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    LANGUAGE=en_US:en

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

## qpdf and pikepdf need to be built from source on armv7
RUN set -x && \
    TEMP_PACKAGES=() && \
    KEPT_PACKAGES=() && \
    # Packages only required during build
    TEMP_PACKAGES+=(git) && \
    TEMP_PACKAGES+=(make) && \
    TEMP_PACKAGES+=(build-essential) && \
    TEMP_PACKAGES+=(libssl-dev) && \
    TEMP_PACKAGES+=(libfreetype6-dev) && \
    TEMP_PACKAGES+=(libfontconfig1-dev) && \
    TEMP_PACKAGES+=(libjpeg-dev) && \
    TEMP_PACKAGES+=(libqpdf-dev) && \
    TEMP_PACKAGES+=(libxft-dev) && \
    TEMP_PACKAGES+=(libxml2-dev) && \
    TEMP_PACKAGES+=(libxslt1-dev) && \
    TEMP_PACKAGES+=(zlib1g-dev) && \
    # Packages kept in the image
    KEPT_PACKAGES+=(bash) && \
    KEPT_PACKAGES+=(ca-certificates) && \
    KEPT_PACKAGES+=(locales) && \
    KEPT_PACKAGES+=(locales-all) && \
    KEPT_PACKAGES+=(python3) && \
    TEMP_PACKAGES+=(python3-dev) && \
    KEPT_PACKAGES+=(python3-pip) && \
    KEPT_PACKAGES+=(chrpath) && \
    KEPT_PACKAGES+=(libfreetype6) && \
    KEPT_PACKAGES+=(libfontconfig1) && \
    KEPT_PACKAGES+=(python3-wheel) && \
    # Install packages
    DEBIAN_FRONTEND=noninteractive apt-get update -y && apt-get -yq upgrade && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        ${KEPT_PACKAGES[@]} \
        ${TEMP_PACKAGES[@]} \
        && \
    git config --global advice.detachedHead false && \
    # Install required python modules
    python -m pip install --upgrade pip && \
    python -m pip install --no-cache-dir pybind11 && \
    ## qpdf and pikepdf need to be built from source on armv7
    cd /opt \
    && git clone --branch release-qpdf-10.6.3 https://github.com/qpdf/qpdf.git \
    && git clone --branch v5.1.1 https://github.com/pikepdf/pikepdf.git \
    && cd /opt/qpdf \
    && ./configure \
    && make \
    && make install \
    && cd /opt/pikepdf \
    && pip install . && \
    # Clean-up
    DEBIAN_FRONTEND=noninteractive apt-get remove -y ${TEMP_PACKAGES[@]} && \
    DEBIAN_FRONTEND=noninteractive apt-get autoremove -y && \
    DEBIAN_FRONTEND=noninteractive apt-get clean -y && \
    rm -rf /var/lib/apt/lists/* /tmp/* /src /opt/qpdf /opt/pikepdf

# Select final stage based on TARGETARCH ARG
FROM stage-${TARGETARCH}${TARGETVARIANT} as final

COPY / /opt/comic-dl
RUN python -m pip install --upgrade pip && \
    python -m pip install -r /opt/comic-dl/requirements.txt && \
    chmod +x /opt/comic-dl/docker-init.sh && \
    ln -s /opt/comic-dl/docker-init.sh /usr/local/bin/comic_dl && \
    cat /opt/comic-dl/comic_dl/__version__.py | grep version | awk '{print $3}' | sed 's/"//g' > /IMAGE_VERSION
