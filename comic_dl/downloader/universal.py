#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module serves as a universal downloader for downloading Images.
Note that this module does not support handling of cookies, for that you
need to refer to `cookies_required` module.
This module needs a File_Name for the file to be downloaded,
Directory_path which is the directory path where you want to download the file,
ddl_image is the direct link to the image itself.
"""

import os
import urllib2
import urllib
import shutil
from urllib2 import URLError
import sys


def main(File_Name_Final, Directory_path, ddl_image):
    File_Check_Path = str(Directory_path) + '/' + str(File_Name_Final)

    if os.path.isfile(File_Check_Path):
        print '[Comic-dl] File Exist! Skipping ', File_Name_Final, '\n'
        pass

    if not os.path.isfile(File_Check_Path):
        print '[Comic-dl] Downloading : ', File_Name_Final
        urllib.urlretrieve(ddl_image, File_Name_Final)
        File_Path = os.path.normpath(File_Name_Final)
        try:
            shutil.move(File_Path, Directory_path)
        except Exception as e:
            print e, '\n'
            os.remove(File_Path)
            pass


if __name__ == '__main__':
    main()
