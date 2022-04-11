Installation
============

After installing and setting up all the dependencies in your Operating
System, you’re good to go and use this script. The instructions for all
the OS would remain same. Download
`THIS REPOSITORY <https://github.com/Xonshiz/comic-dl/archive/master.zip>`__
and put it somewhere in your system. Move over to the ``comic_dl``
folder.

**Windows users**, it’s better to not place it places where it requires
administrator privileges. Good example would be ``C:\Windows``. This
goes for both, the Python script and the windows binary file (.exe).

**Linux/Debian** users make sure that this script is executable.just run
this command, if you run into problem(s) :

``chmod +x cli.py``

and then, execute with this :

``./cli.py``

Docker
------

With docker, you can get the whole dependencies enclosed in a container
and use the ``comic_dl`` from your system.

You need an up and running Docker client running, follow the `Docker
Documentation <https://docs.docker.com/install/>`__.

`Docker images are available
here <https://github.com/Xonshiz/comic-dl/pkgs/container/comic-dl/>`__

Define a handy alias on your system with some docker tricks. This mounts
the local directory under ``/directory`` in the container. This works on
\*NIX systems, and also under Windows Linux subsystem.

You can change the value of PGID and PUID with the value for the user
needed in your download directory.

.. code:: bash

   alias comic_dl="docker run -it --rm -e PGID=$(id -g) -e PUID=$(id -u) -v $(pwd):/directory:rw -w /directory ghcr.io/xonshiz/comic-dl:latest comic_dl -dd /directory"

Run it on your system. This actually starts a container on request and
stop&delete it when finished.

.. code:: bash

   usage: comicdl [-h] [--version] [-s SORTING] [-a] [-c]
                  [-dd DOWNLOAD_DIRECTORY] [-rn RANGE] [--convert CONVERT]
                  [--keep KEEP] [--quality QUALITY] [-i INPUT] [--comic]
                  [-comic-search SEARCH_COMIC] [-comic-info COMIC_INFO]
                  [--update UPDATE] [--print-index] [-find SEARCH]
                  [-ml MANGA_LANGUAGE] [-sc SKIP_CACHE] [-cid CHAPTER_ID]
                  [-pid PAGE_ID] [-fd] [-p PASSWORD] [-u USERNAME] [-v]
   [...]
