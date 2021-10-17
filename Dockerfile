# build with command:
# docker build -t comic-dl:py3.8-buster .
# run with alias
# alias comic_dl="docker run -it --rm -v $(pwd):/directory -w /directory comic-dl:py3.8-buster comic_dl -dd /directory"

# this builds the base image to run comic_dl
FROM python:3.8-slim-buster AS base
RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get -yq upgrade
# update system & install basisc stuff
#        and dependencies for phantomjs
# RUN DEBIAN_FRONTEND=noninteractive apt-get install -yq \
#     build-essential \
#     chrpath \
#     libssl-dev \
#     libxft-dev \
#     libfreetype6 \
#     libfreetype6-dev \
#     libfontconfig1 \
#     libfontconfig1-dev

ENV OWNER_UID=1000
ENV OWNER_GID=1000

COPY / /opt/comic-dl
RUN python -m pip install --upgrade pip && \
    python -m pip install -r /opt/comic-dl/requirements.txt && \
    chmod +x /opt/comic-dl/docker-init.sh && \
    ln -s /opt/comic-dl/docker-init.sh /usr/local/bin/comic_dl && \
    addgroup --gid ${OWNER_GID} comic-dl && \
    adduser --disabled-password -home /home/comic-dl --gid ${OWNER_GID} --uid ${OWNER_UID} --gecos "" comic-dl

USER comic-dl