#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import print_function
from logging import debug, basicConfig, DEBUG
from re import search, compile, sub, findall
from os import path, makedirs
from cfscrape import create_scraper
from requests import session
from downloader.cookies_required import with_referer as FileDownloader


def single_chapter(url,current_directory, logger):
    headers = {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    }

    sess = session()
    sess = create_scraper(sess)
    s = sess.get(url, headers=headers).text.encode("utf-8")
    tasty_cookies = sess.cookies

    splitter = str(url).split("/")
    series_name = str(splitter[3]).replace("_"," ").title()
    debug("Series Name : %s" % series_name)
    # print(series_name)
    chapter_number = str(splitter[4])
    debug("Chapter Number : %s" % chapter_number)
    # print(chapter_number)

    # http://raw.senmanga.com/viewer/Strike_The_Blood/19/3
    image_url = "http://raw.senmanga.com/viewer/" + str(splitter[3]) + "/" + str(splitter[4]) + "/"
    debug("Image Url : %s" % image_url)
    page_referer = "http://raw.senmanga.com/" + str(splitter[3]) + "/" + str(splitter[4]) + "/"
    debug("Page Referer : %s" % page_referer)
    # print(image_url)
    # print(page_referer)

    try:
        total_pages = int(str(search(r'\<\/select\>\ of\ (.*?)\ \<a', str(s)).group(1)).strip())
    except Exception as e:
        debug("Error in Total Pages : %s" % e)
        print("Some error occured. Naming chapter as 0.")
        print("Run this script with --verbose option and send the error.log on repository of comic-d.")
        total_pages = 0
    # print(total_pages)

    Raw_File_Directory = str(series_name) + '/' + "Chapter " + str(chapter_number)

    File_Directory = sub('[^A-Za-z0-9\-\.\'\#\/ ]+', '',
                         Raw_File_Directory)  # Fix for "Special Characters" in The series name

    Directory_path = path.normpath(File_Directory)

    print('\n')
    print('{:^80}'.format('=====================================================================\n'))
    print('{:^80}'.format('%s - %s') % (series_name, chapter_number))
    print('{:^80}'.format('=====================================================================\n'))


    for x in range(0, total_pages + 1):
        if not path.exists(File_Directory):
            makedirs(File_Directory)
        file_name = str(x) + ".jpg"
        # print("File Name : %s" % file_name)
        ddl_image = str(image_url) + str(x)
        referer = str(page_referer) + str(x)
        # print(ddl_image)
        # print(page_referer)
        debug("DDL Image : %s" % ddl_image)
        FileDownloader(file_name, Directory_path, tasty_cookies, ddl_image, referer, logger)

    print('\n')
    print("Completed downloading ", series_name)

def whole_series(url, current_directory, logger, sortingOrder):

    headers = {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    }

    sess = session()
    sess = create_scraper(sess)
    s = sess.get(url, headers=headers).text.encode("utf-8")

    all_links = list(findall(r'\<td\>\<a\ href\=\"(.*?)\"\ title\=\"', str(s)))
    debug("All Links : %s" % all_links)

    if str(sortingOrder).lower() in ['new','desc','descending','latest']:
        for x in all_links:
            chapter_url = "http://raw.senmanga.com" + str(x).strip()
            single_chapter(url=chapter_url, current_directory=current_directory, logger=logger)

    elif str(sortingOrder).lower() in ['old','asc','ascending','oldest', 'a']:

        for x in all_links[::-1]:
            chapter_url = "http://raw.senmanga.com" + str(x).strip()
            single_chapter(url=chapter_url, current_directory=current_directory, logger=logger)

    print("Finished Downloading")


def raw_sen_Url_Check(input_url, current_directory, logger, sortingOrder):
    if logger == "True":
        basicConfig(format='%(levelname)s: %(message)s', filename="Error Log.log", level=DEBUG)

    raw_sen_single_regex = compile("https?://(?P<host>raw.senmanga.com)/(?P<Series_Name>[\d\w-]+)?/(?P<Chapter>[\d\w-]+)?")
    raw_sen_whole_regex = compile("https?://(?P<host>raw.senmanga.com)/(?P<Series_Name_whole>[\d\w-]+)?(|/)$")

    lines = input_url.split('\n')
    for line in lines:
        found = search(raw_sen_single_regex, line)
        if found:
            match = found.groupdict()
            if match['Chapter']:
                url = str(input_url)
                single_chapter(url, current_directory, logger)

            else:
                pass

        found = search(raw_sen_whole_regex, line)
        if found:
            match = found.groupdict()
            if match['Series_Name_whole']:
                url = str(input_url)
                whole_series(url, current_directory, logger, sortingOrder)
            else:
                pass
