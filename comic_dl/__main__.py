#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
sys.path.append("..")


from comic_dl.__version__ import __version__
from comic_dl.sites import *
from comic_dl.manga_eden import *
from comic_dl.readcomiconline import *
from comic_dl.comic_dl import ComicDL

if __name__ == "__main__":
    ComicDL(sys.argv[1:])


def main():
    ComicDL(sys.argv[1:])
