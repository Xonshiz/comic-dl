#!/usr/bin/env python
# -*- coding: utf-8 -*-

from logging import debug, basicConfig, DEBUG
from re import search, compile, sub, findall
from os import path, makedirs
from cfscrape import create_scraper
from requests import session
from downloader.cookies_required import main as FileDownloader


def single_chapter(url, current_directory, logger):
    headers = {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    }

    sess = session()
    sess = create_scraper(sess)
    s = sess.get(url, headers=headers).text.encode("utf-8")
    tasty_cookies = sess.cookies

    splitter = str(url).split("/")
    series_name = str(splitter[4]).replace("_", " ").title()
    debug("Series Name : %s" % series_name)
    # print(series_name)
    chapter_number = str(splitter[5]).lstrip("0")
    debug("Chapter Number : %s" % chapter_number)
    # print(chapter_number)

    # http://www.omgbeaupeep.com/comics/mangas/Beau%20Peep/001%20-%20Beau%20Peep%20Book%201/Beau-Peep-Book-1-Page-001.jpg
    imageLink = "http://www.omgbeaupeep.com/comics/mangas/" + str(search(r'"mangas/(.*?)" alt', str(s)).group(1)).replace(" ", "%20")
    # print(imageLink)

    lastPage = int(str(search(r'</select> of (.*?) <a', str(s)).group(1)).strip())
    # print(lastPage)

    Raw_File_Directory = str(series_name) + '/' + "Chapter " + str(chapter_number)

    File_Directory = sub('[^A-Za-z0-9\-\.\'\#\/ ]+', '',
                         Raw_File_Directory)  # Fix for "Special Characters" in The series name

    Directory_path = path.normpath(File_Directory)

    print('\n')
    print('{:^80}'.format('=====================================================================\n'))
    print('{:^80}'.format('%s - %s') % (series_name, chapter_number))
    print('{:^80}'.format('=====================================================================\n'))
    
    """Seems like there is some weird file naming convention going on in this website.
    If the chapter number is Single Digit, ex : 9, then the image links are like :
    Page 1 = http://www.omgbeaupeep.com/comics/mangas/Beau%20Peep/009%20-%20Beau%20Peep%20Book%209/Beau-Peep-Book-9-Page-001.jpg
    Page 10 = http://www.omgbeaupeep.com/comics/mangas/Beau%20Peep/009%20-%20Beau%20Peep%20Book%209/Beau-Peep-Book-9-Page-010.jpg
    
    But, if the page number is Double Digit, ex : 10, then the image links are like :
    Page 1 = http://www.omgbeaupeep.com/comics/mangas/Beau%20Peep/010%20-%20Beau%20Peep%20Book%2010/Beau-Peep-Book-10-Page-01.jpg
    Page 10 = http://www.omgbeaupeep.com/comics/mangas/Beau%20Peep/010%20-%20Beau%20Peep%20Book%2010/Beau-Peep-Book-10-Page-10.jpg
    
    Notice the file names. 001 and 010 for Single digits(Chapter Number) and 01 & 10 for Double digits (Chapter Number).
    """
    for pageNumber in range(1, lastPage + 1):
        # print(chapter_number)
        if len(str(chapter_number)) == 1:
            if len(str(pageNumber)) == 1:
                pageNumber = "00" + str(pageNumber)
            elif len(str(pageNumber)) == 2:
                pageNumber = "0" + str(pageNumber)

        elif len(str(chapter_number)) == 2:
            # print(chapter_number)
            if len(str(pageNumber)) == 1:
                pageNumber = "0" + str(pageNumber)
            elif len(str(pageNumber)) == 2:
                pageNumber = str(pageNumber)

        if not path.exists(File_Directory):
            makedirs(File_Directory)

        ddl_image = imageLink.replace(".jpg", "").replace(".png", "")[:-len(imageLink.replace(".jpg", "").replace(".png", "").split("-")[-1])] + str(pageNumber) + ".jpg"
        # tempBreaker = imageLink
        # print(ddl_image)
        debug("DDL Image : %s" % ddl_image)

        fileName = str(pageNumber) + ".jpg"

        FileDownloader(fileName, Directory_path, tasty_cookies, ddl_image, logger)

    print('\n')
    print("Completed downloading ", series_name)

def whole_series(url, current_directory, logger, sortingOrder):
    print("Nothing for this section on this website.")

def omgbeaupeep_Url_Check(input_url, current_directory, logger, sortingOrder):
    if logger == "True":
        basicConfig(format='%(levelname)s: %(message)s', filename="Error Log.log", level=DEBUG)

    url = str(input_url).replace("www.", "")
    # print(url)
    # print(len(url.split("/")))
    if len(url.split("/")) < 7:
        url = str(url) + "001"
    # print(url)
    single_chapter(url, current_directory, logger)
