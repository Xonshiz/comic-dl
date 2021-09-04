#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from comic_dl.comic_dl import ComicDL
from comic_dl import sites
from comic_dl import manga_eden

if __name__ == "__main__":
    ComicDL(sys.argv[1:])