FROM python:3.6.5-stretch
RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get -yq upgrade
# update system & install basisc stuff
#        and dependencies for phantomjs
RUN DEBIAN_FRONTEND=noninteractive apt-get install -yq \
    build-essential chrpath libssl-dev libxft-dev \
         libfreetype6 libfreetype6-dev libfontconfig1 libfontconfig1-dev \
    wget git
# install phantomjs and symlink to /usr/local/bin/
RUN wget -q https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2 && \
    tar xvjf phantomjs-2.1.1-linux-x86_64.tar.bz2 -C /usr/local/share/ && \
    ln -s /usr/local/share/phantomjs-2.1.1-linux-x86_64/bin/phantomjs /usr/local/bin/
# install comic-dl
RUN python -m pip install -r requirements.txt && \
    git -C /opt/ clone https://github.com/kidpixo/comic-dl.git && \
    chmod +x /opt/comic-dl/comic_dl/__main__.py  && \
    ln -s /opt/comic-dl/comic_dl/__main__.py /usr/local/bin/comic_dl
    

