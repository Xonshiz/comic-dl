#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""This python module decides which URL should be assigned to which other module from the site package.
"""



from __future__ import absolute_import
from __future__ import print_function
#import urllib as urllib2
from urllib.parse import urlparse
from sites.yomanga import yomanga_Url_Check
from sites.gomanga import gomanga_Url_Check
from sites.mangafox import mangafox_Url_Check
from sites.batoto import batoto_Url_Check
from sites.kissmanga import kissmanga_Url_Check
from sites.comic_naver import comic_naver_Url_Check
from downloader import universal,cookies_required





def url_checker(input_url, current_directory, User_Name, User_Password):
    
    domain = urlparse(input_url).netloc

    if domain in ['mangafox.me']:
        mangafox_Url_Check(input_url, current_directory)
        
    elif domain in ['yomanga.co']:
        yomanga_Url_Check(input_url, current_directory)
        
    elif domain in ['gomanga.co']:
        gomanga_Url_Check(input_url, current_directory)
        
    elif domain in ['bato.to']:
        batoto_Url_Check(input_url, current_directory, User_Name, User_Password)
        
    elif domain in ['kissmanga.com']:
        kissmanga_Url_Check(input_url, current_directory)
        
    elif domain in ['comic.naver.com']:
        comic_naver_Url_Check(input_url, current_directory)
        
    elif domain in ['']:
        print('You need to specify at least 1 URL. Please run : comic-dl -h')
    else:
        print("%s is unsupported at the moment. Please request on Github repository."%(domain))
