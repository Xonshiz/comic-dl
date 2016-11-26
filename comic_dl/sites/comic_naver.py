#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import re
import sys
import os
import requests
from downloader.cookies_required import with_referer as FileDownloader

"""Thanks to puilp0502 for his repo : https://github.com/puilp0502/comic-downloader
I got stuck at getting the images to download from the links. Then I went through puilp's script to see that I was missing referer in my requests module.
"""


def single_chapter(url, current_directory):

    s = requests.Session()
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}
    req = s.get(url, headers=headers)
    cookies = req.cookies
    page_source_1 = req.text.encode('utf-8')

    try:
        #Korean_Name = re.search(r'<h2>(.*?)<span class="wrt_nm">',str(page_source)).group(1)
        Series_Name = re.search(r'titleId=(\d+)', url).group(1)
    except Exception as e:
        Series_Name = "Unknown"

    try:
        #chapter_number = int(re.search(r'\<span\ class\=\"total\"\>(.\d+)\<\/span\>',page_source_1).group(1))
        chapter_number = re.search(r'&no=(\d+)', url).group(1)
    except Exception as e:
        print e
        chapter_number = 0

    img_regex = r'http://imgcomic.naver.net/webtoon/\d+/\d+/.+?\.(?:jpg|png|gif|bmp|JPG|PNG|GIF|BMP)'

    img_links = list(re.findall(img_regex, page_source_1))

    Raw_File_Directory = str(Series_Name).decode(
        'utf-8') + '/' + "Chapter " + str(chapter_number)

    # Fix for "Special Characters" in The series name
    File_Directory = re.sub('[^A-Za-z0-9\-\.\'\#\/ ]+', '', Raw_File_Directory)

    Directory_path = os.path.normpath(File_Directory)

    print '\n'
    print '{:^80}'.format('=====================================================================\n')
    print '{:^80}'.format('%s - %s') % (Series_Name, chapter_number)
    print '{:^80}'.format('=====================================================================\n')

    for x, items in enumerate(img_links):
        if not os.path.exists(File_Directory):
            os.makedirs(File_Directory)
        FileDownloader(
            str(x + 1) + str(items[-4:]), Directory_path, cookies, items, url)

    print '\n'
    print "Completed downloading ", Series_Name


def whole_series(url, current_directory):

    s = requests.Session()
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}
    req = s.get(url, headers=headers)
    cookies = req.cookies
    page_source_1 = req.text.encode('utf-8')

    titleId = re.search(r'titleId=(\d+)', url).group(1)

    try:
        first_link = int(
            re.search(
                r'\/webtoon\/detail\.nhn\?titleId\=%s\&no\=(\d+)\&weekday\=tue' %
                (titleId),
                page_source_1).group(1))
    except Exception as e:
        first_link = input("Please Enter the Last chapter of the series : ")
        if not first_link:
            print "You failed to enter the last chapter count. Script will exit now."
            sys.exit()

    for x in range(1, int(first_link)):
        Chapter_Url = "http://comic.naver.com/webtoon/detail.nhn?titleId=%s&no=%s" % (
            titleId, x)
        single_chapter(Chapter_Url, current_directory)


def comic_naver_Url_Check(input_url, current_directory):

    comic_naver_single_regex = re.compile(
        'https?://(?P<host>comic.naver.com)/webtoon/(?P<detail>detail.nhn)\?titleId\=(?P<extra_characters>[\d]+)?(\/|.)')
    comic_naver_whole_regex = re.compile(
        'https?://(?P<host>comic.naver.com)/webtoon/(?P<list>list.nhn)\?titleId\=(?P<extra_characters>[\d]+)?(\/|.)')

    lines = input_url.split('\n')
    for line in lines:
        found = re.search(comic_naver_single_regex, line)
        if found:
            match = found.groupdict()
            if match['detail']:
                url = str(input_url)
                single_chapter(url, current_directory)

            else:
                pass

        found = re.search(comic_naver_whole_regex, line)
        if found:
            match = found.groupdict()
            if match['list']:
                url = str(input_url)
                whole_series(url, current_directory)
            else:
                pass
