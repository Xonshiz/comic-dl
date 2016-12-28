#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module serves as a universal downloader for downloading Images.
This module supports handling of cookies.
This module needs a File_Name for the file to be downloaded,
Directory_path which is the directory path where you want to download the file,
tasty_cookies refer to the `cookies` you fetch from your session.
ddl_image is the direct link to the image itself.

This module uses `requests` library to achieve the handling of cookies.
"""

from __future__ import absolute_import
from __future__ import print_function
import os
import requests
import shutil
from downloader.universal import main as FileDownloader

def main(File_Name_Final,Directory_path,tasty_cookies,ddl_image):
    File_Check_Path = str(Directory_path)+'/'+str(File_Name_Final)

    if os.path.isfile(File_Check_Path):
        print('[Comic-dl] File Exist! Skipping ',File_Name_Final,'\n')
        pass

    if not os.path.isfile(File_Check_Path): 
        print('[Comic-dl] Downloading : ',File_Name_Final)
    
        response = requests.get(ddl_image, stream=True,cookies=tasty_cookies)
        try:
            with open(File_Name_Final, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            File_Path = os.path.normpath(File_Name_Final)
        except Exception as e:
            print("Couldn't download file from : ",ddl_image)
            pass
        try:
            shutil.move(File_Path,Directory_path)
        except Exception as e:
            print(e,'\n')
            pass


def with_referer(File_Name_Final,Directory_path,tasty_cookies,ddl_image,referer):
    File_Check_Path = str(Directory_path)+'/'+str(File_Name_Final)

    if os.path.isfile(File_Check_Path):
        print('[Comic-dl] File Exist! Skipping ',File_Name_Final,'\n')
        pass

    if not os.path.isfile(File_Check_Path): 
        print('[Comic-dl] Downloading : ',File_Name_Final)
        headers = {'Referer': referer}    
        response = requests.get(ddl_image, stream=True,cookies=tasty_cookies,headers=headers)
        try:
            with open(File_Name_Final, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            File_Path = os.path.normpath(File_Name_Final)
        except Exception as e:
            print("Couldn't download file from : ",ddl_image)
            pass
        try:
            shutil.move(File_Path,Directory_path)
        except Exception as e:
            print(e,'\n')
            pass


if __name__ == '__main__':
    main()