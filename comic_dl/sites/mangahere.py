#!/usr/bin/env python
# -*- coding: utf-8 -*-

from requests import session
from cfscrape import create_scraper
from re import search, compile, sub
from logging import debug, basicConfig, DEBUG
from bs4 import BeautifulSoup
from downloader.cookies_required import main as FileDownloader
from os import path, makedirs


def single_chapter(url, directory, logger):
    debug("Downloading Single Chapter")
    sess = session()
    sess = create_scraper(sess)
    s = sess.get(url)
    cookies = sess.cookies
    connection = s.text.encode('utf-8')

    soup = BeautifulSoup(connection, "html.parser")
    lastChapter = str(search(r'total_pages\ \=\ (.*?) \;', str(soup)).group(1)).strip()
    Series_Name = str(search(r'series_name\ \=\ \"(.*?)\"\;', str(soup)).group(1)).strip().replace("_"," ").title()
    chapter_number = str(search(r'current_chapter\ \=\ \"(.*?)\"\;', str(soup)).group(1)).strip().replace("c","")
    Raw_File_Directory = str(Series_Name) + '/' + "Chapter " + str(chapter_number)

    File_Directory = sub('[^A-Za-z0-9\-\.\'\#\/ ]+', '',Raw_File_Directory)  # Fix for "Special Characters" in The series name

    print('\n')
    print('{:^80}'.format('=====================================================================\n'))
    print('{:^80}'.format('%s - %s') % (Series_Name, chapter_number))
    print('{:^80}'.format('=====================================================================\n'))

    for chapCount in range(1, int(lastChapter)+1):
        # print(chapCount)
        chapURL = str(url) + '/%s.html' % chapCount
        # print(chapURL)
        newConnection = sess.get(url=chapURL, cookies=cookies)
        # print(newConnection.text)
        soupNew = BeautifulSoup(newConnection.text, "html.parser")
        Series_Name_Finder = soupNew.findAll('section', {'class': 'read_img'})
        for link in Series_Name_Finder:
            x = link.findAll('img')
            for a in x:
                if not path.exists(File_Directory):
                    makedirs(File_Directory)
                ddlLink = a['src']
                debug("ddlLink : %s" % ddlLink)
                if ddlLink in ['http://www.mangahere.co/media/images/loading.gif']:
                    pass
                else:
                    # print(ddlLink)
                    FileDownloader(File_Name_Final=str(chapCount) + '.jpg', Directory_path=File_Directory, tasty_cookies=cookies, ddl_image=ddlLink, logger=logger)
    print('\n')
    print("Completed downloading %s" % Series_Name)

def whole_series(url, directory, logger, sortingOrder):
    # print("Need Time!")
    debug("Downloading Whole Series")
    sess = session()
    sess = create_scraper(sess)
    s = sess.get(url)
    cookies = sess.cookies
    connection = s.text.encode('utf-8')

    soup = BeautifulSoup(connection, "html.parser")
    all_links = soup.findAll('a', {'class': 'color_0077'})
    debug("all_links : %s" % all_links)
    # print(all_links)
    chapterLinks = []

    for link in all_links:
        links = link['href']
        if 'mangahere.co/manga/' in links:
            chapterLinks.append(links)
        else:
            pass
    chapterLinks.pop(0)
    # print(chapterLinks)
    if str(sortingOrder).lower() in ['new','desc','descending','latest']:
        for chapLink in chapterLinks:
            single_chapter(url=chapLink, directory=directory, logger=logger)
    elif str(sortingOrder).lower() in ['old','asc','ascending','oldest', 'a']:
        for chapLink in chapterLinks[::-1]:
            single_chapter(url=chapLink, directory=directory, logger=logger)
    print("Finished Downloading")



def mangahere_Url_Check(input_url, current_directory, logger, sortingOrder):
    debug("Input URL : %s" % input_url)
    if logger == "True":
        basicConfig(format='%(levelname)s: %(message)s', filename="Error Log.log", level=DEBUG)
    mangahere_single_regex = compile('https?://(?P<host>[^/]+)/manga/(?P<comic>[\d\w-]+)/(?P<chapter>[\d\w-]+).$')
    mangahere_whole_regex = compile('https?://(?P<host>[^/]+)/manga/(?P<comic>[\d\w-]+).$')

    lines = input_url.split('\n')
    for line in lines:
        found = search(mangahere_single_regex, line)
        if found:
            match = found.groupdict()
            if match['chapter']:
                url = str(input_url)
                single_chapter(url, current_directory, logger)
            else:
                pass

        found = search(mangahere_whole_regex, line)
        if found:
            match = found.groupdict()
            if match['comic']:
                url = str(input_url)
                whole_series(url, current_directory, logger, sortingOrder)
            else:
                pass