# build with command:
# docker build -t comic-dl:py3.8-buster .
# run with alias
# alias comic_dl="docker run -it --rm -e PGID=$(id -g) -e PUID=$(id -u) -v $(pwd):/directory:rw -w /directory comic-dl:py3.8-buster comic_dl -dd /directory"

# for armv7,
# cross build it (it takes a few hours on x86_64)
# build with command:
# docker build -t comic-dl:py3.8-buster-armv7 --platform linux/arm/v7 .
# export with command
# docker save -o comic-dl.tar comic-dl:py3.8-buster-armv7
# import on arm machine with command:
# docker load --input comic-dl.tar
# run with alias:
# alias comic_dl="docker run -it --rm -e PGID=$(id -g) -e PUID=$(id -u) -v $(pwd):/directory:rw -w /directory comic-dl:py3.8-buster-armv7 comic_dl -dd /directory"

FROM ghcr.io/darodi/docker-py3.8-slim-buster-pikepdf:latest

COPY / /opt/comic-dl
RUN python -m pip install --upgrade pip && \
    python -m pip install -r /opt/comic-dl/requirements.txt && \
    chmod +x /opt/comic-dl/docker-init.sh && \
    ln -s /opt/comic-dl/docker-init.sh /usr/local/bin/comic_dl && \
    cat /opt/comic-dl/comic_dl/__version__.py | grep version | awk '{print $3}' | sed 's/"//g' > /IMAGE_VERSION
