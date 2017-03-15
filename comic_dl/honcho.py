#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""This python module decides which URL should be assigned to which other module from the site package.
"""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import

from future import standard_library
standard_library.install_aliases()

#import urllib as urllib2
import logging
from sites.yomanga import yomanga_Url_Check
from sites.gomanga import gomanga_Url_Check
from sites.mangafox import mangafox_Url_Check
from sites.batoto import batoto_Url_Check
from sites.kissmanga import kissmanga_Url_Check
from sites.comic_naver import comic_naver_Url_Check
from sites.readcomic import readcomic_Url_Check
from sites.kisscomicus import kissmcomicus_Url_Check
from sites.mangahere import mangahere_Url_Check
from sites.rawsen import raw_sen_Url_Check
from downloader import universal,cookies_required
from urllib.parse import urlparse




def url_checker(input_url, current_directory, User_Name, User_Password, logger, sortingOrder):

    if logger == "True":
        logging.basicConfig(format='%(levelname)s: %(message)s', filename="Error Log.log", level=logging.DEBUG)
        logging.debug("Your URL : %s" % input_url)

    domain = urlparse(input_url).netloc
    logging.debug("Domain : %s" % domain)
    # print(domain)

    if domain in ['mangafox.me', 'www.mangafox.me']:
        mangafox_Url_Check(input_url, current_directory, logger)

    elif domain in ['yomanga.co', 'www.yomanga.co']:
        yomanga_Url_Check(input_url, current_directory, logger, sortingOrder)

    elif domain in ['gomanga.co', 'www.gomanga.co']:
        gomanga_Url_Check(input_url, current_directory, logger, sortingOrder)

    elif domain in ['bato.to', 'www.bato.to']:
        batoto_Url_Check(input_url, current_directory, User_Name, User_Password, logger)

    elif domain in ['kissmanga.com', 'www.kissmanga.com']:
        kissmanga_Url_Check(input_url, current_directory, logger, sortingOrder)

    elif domain in ['comic.naver.com', 'www.comic.naver.com']:
        comic_naver_Url_Check(input_url, current_directory, logger, sortingOrder)

    elif domain in ['readcomiconline.to', 'www.readcomiconline.to']:
        readcomic_Url_Check(input_url, current_directory, logger, sortingOrder)

    elif domain in ['kisscomic.us', 'www.kisscomic.us']:
        kissmcomicus_Url_Check(input_url, current_directory, logger, sortingOrder)

    elif domain in ['mangahere.co','www.mangahere.co']:
        mangahere_Url_Check(input_url, current_directory, logger, sortingOrder)

    elif domain in ['raw.senmanga.com','www.raw.senmanga.com']:
        raw_sen_Url_Check(input_url, current_directory, logger, sortingOrder)
        
    elif domain in ['']:
        print('You need to specify at least 1 URL. Please run : comic-dl -h')
    else:
        print("%s is unsupported at the moment. Please request on Github repository."%(domain))
