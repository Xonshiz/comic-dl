#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module serves as a universal downloader for downloading Images.
Note that this module does not support handling of cookies, for that you
need to refer to `cookies_required` module.
This module needs a File_Name for the file to be downloaded,
Directory_path which is the directory path where you want to download the file,
ddl_image is the direct link to the image itself.
"""

from __future__ import absolute_import
from __future__ import print_function
from os import path, remove
from shutil import move
import urllib
from logging import debug, basicConfig, DEBUG

def main(File_Name_Final,Directory_path,ddl_image, logger):
    if logger == "True":
        basicConfig(format='%(levelname)s: %(message)s', filename="Error Log.log", level=DEBUG)
    File_Check_Path = str(Directory_path)+'/'+str(File_Name_Final)
    debug("File Check Path : %s" % File_Check_Path)
            
    if path.isfile(File_Check_Path):
        print('[Comic-dl] File Exist! Skipping ',File_Name_Final,'\n')
        pass

    if not path.isfile(File_Check_Path): 
        print('[Comic-dl] Downloading : ',File_Name_Final)
        urllib.request.URLopener.version = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
        try:
            urllib.request.urlretrieve(ddl_image, File_Name_Final)
        except Exception as e:
            debug("Error in retrieving image : %s" % e)
        #filename, headers = urllib.urlretrieve(ddl_image,File_Name_Final)
        #print "File Name : ",filename
        #print "Headers : ",headers
        File_Path = path.normpath(File_Name_Final)
        try:
            move(File_Path,Directory_path)
        except Exception as e:
            print(e,'\n')
            remove(File_Path)
            pass



if __name__ == '__main__':
    main()