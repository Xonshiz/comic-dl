#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import print_function
from re import search,sub,compile, findall
from os import path,makedirs
from sys import exit
from logging import debug, basicConfig, DEBUG
from requests import Session,cookies
from downloader.cookies_required import with_referer as FileDownloader
from six.moves import range
from six.moves import input


def single_chapter(url,current_directory, logger):
    
    s = Session()
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}
    req = s.get(url,headers=headers)
    cookies = req.cookies
    page_source_1 = str(req.text.encode('utf-8'))
    
    try:
        #Korean_Name = search(r'<h2>(.*?)<span class="wrt_nm">',str(page_source)).group(1)
        Series_Name = search(r'titleId=(\d+)',url).group(1)
    except Exception as e:
        debug("Error in Series Name : %s" % e)
        Series_Name = "Unknown"

    try:
        #chapter_number = int(search(r'\<span\ class\=\"total\"\>(.\d+)\<\/span\>',page_source_1).group(1))
        chapter_number = search(r'&no=(\d+)',url).group(1)
    except Exception as e:
        # print(e)
        debug("Error in Chapter Number : %s" % e)
        chapter_number = 0
    
    img_regex = r'http://imgcomic.naver.net/webtoon/\d+/\d+/.+?\.(?:jpg|png|gif|bmp|JPG|PNG|GIF|BMP)'

    img_links = list(findall(img_regex,page_source_1))
    debug("Image Links : %s" % img_links)
    
    Raw_File_Directory = str(Series_Name) +'/'+"Chapter "+str(chapter_number)

    File_Directory = sub('[^A-Za-z0-9\-\.\'\#\/ ]+', '', Raw_File_Directory) # Fix for "Special Characters" in The series name

    Directory_path = path.normpath(File_Directory)

    print('\n')
    print('{:^80}'.format('=====================================================================\n'))
    print('{:^80}'.format('%s - %s')%(Series_Name,chapter_number))
    print('{:^80}'.format('=====================================================================\n'))

    for x,items in enumerate(img_links):
        if not path.exists(File_Directory):
            makedirs(File_Directory)
        FileDownloader(str(x+1)+str(items[-4:]),Directory_path,cookies,items,url, logger)

    print('\n')
    print("Completed downloading ",Series_Name)




def whole_series(url, current_directory, logger, sortingOrder):
    
    
    
    s = Session()
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}
    req = s.get(url,headers=headers)
    cookies = req.cookies
    page_source_1 = req.text.encode('utf-8')
    
    titleId = search(r'titleId=(\d+)',url).group(1)
    
    try:
        first_link = int(search(r'\/webtoon\/detail\.nhn\?titleId\=%s\&no\=(\d+)\&weekday\=tue' %(titleId),page_source_1).group(1))
    except Exception as e:
        first_link = eval(input("Please Enter the Last chapter of the series : "))
        if not first_link:
            print("You failed to enter the last chapter count. Script will exit now.")
            exit()
    all_links = []
    for x in range(1,int(first_link)):
        Chapter_Url = "http://comic.naver.com/webtoon/detail.nhn?titleId=%s&no=%s" %(titleId,x)
        debug("Chapter URL : %s" % Chapter_Url)
        all_links.append(Chapter_Url)
    # print(all_links)
    if str(sortingOrder).lower() in ['new','desc','descending','latest']:
        for chapLink in all_links[::-1]:
            single_chapter(chapLink, current_directory, logger)
    elif str(sortingOrder).lower() in ['old','asc','ascending','oldest', 'a']:
        # print("Running this")
        for chapLink in all_links:
            single_chapter(chapLink, current_directory, logger)
    print("Finished Downloading")



def comic_naver_Url_Check(input_url, current_directory, logger, sortingOrder):
    if logger == "True":
        basicConfig(format='%(levelname)s: %(message)s', filename="Error Log.log", level=DEBUG)

    comic_naver_single_regex = compile(
        'https?://(?P<host>comic.naver.com)/webtoon/(?P<detail>detail.nhn)\?titleId\=(?P<extra_characters>[\d]+)?(\/|.)')
    comic_naver_whole_regex = compile(
        'https?://(?P<host>comic.naver.com)/webtoon/(?P<list>list.nhn)\?titleId\=(?P<extra_characters>[\d]+)?(\/|.)')

    lines = input_url.split('\n')
    for line in lines:
        found = search(comic_naver_single_regex, line)
        if found:
            match = found.groupdict()
            if match['detail']:
                url = str(input_url)
                single_chapter(url, current_directory, logger)
                
            else:
                pass

        found = search(comic_naver_whole_regex, line)
        if found:
            match = found.groupdict()
            if match['list']:
                url = str(input_url)
                whole_series(url, current_directory, logger, sortingOrder)
            else:
                pass
