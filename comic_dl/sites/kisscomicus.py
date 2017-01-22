#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cfscrape
import re
from bs4 import BeautifulSoup
import os
# from downloader.universal import main as FileDownloader
from downloader.cookies_required import main as FileDownloader
import requests
import logging

def single_chapter(url, directory, logger):

    sess = requests.session()
    sess = cfscrape.create_scraper(sess)
    s = sess.get(url)
    cookies = sess.cookies
    connection = s.text.encode('utf-8')

    soup = BeautifulSoup(connection, "html.parser")
    Series_Name_Finder = soup.findAll('ul', {'class': 'back-info'})
    for link in Series_Name_Finder:
        x = link.findAll('a')
        for a in x:
            raw_name = a['href']
            Series_Name = str(raw_name.split("/")[2]).replace(".html","").replace("-"," ").title().strip()
            # print("Series Name : %s" % Series_Name)
    chapter_number = int(str(url).split("-")[-1].replace(".html",""))
    # print("Chapter Number : %s" % chapter_number)

    Raw_File_Directory = str(Series_Name) + '/' + "Chapter " + str(chapter_number)

    File_Directory = re.sub('[^A-Za-z0-9\-\.\'\#\/ ]+', '',
                            Raw_File_Directory)  # Fix for "Special Characters" in The series name

    Directory_path = os.path.normpath(File_Directory)

    print('\n')
    print('{:^80}'.format('=====================================================================\n'))
    print('{:^80}'.format('%s - %s') % (Series_Name, chapter_number))
    print('{:^80}'.format('=====================================================================\n'))

    # soup = BeautifulSoup(connection, "html.parser")
    linkFinder = soup.findAll('ul', {'class': 'list-image'})
    logging.debug("Image Links : %s" % linkFinder)

    # print("Link Finder :s %s" % linkFinder)
    for link in linkFinder:
        x = link.findAll('img')
        for a in x:
            if not os.path.exists(File_Directory):
                os.makedirs(File_Directory)
            ddlLink = a['src']
            logging.debug("Final URL : %s" % ddlLink)
            fileName = str(ddlLink).split("/")[-1].strip()
            # print("Link : %s\nFile Name : %s" % (ddlLink, fileName))
            FileDownloader(File_Name_Final=fileName, Directory_path=File_Directory, tasty_cookies=cookies, ddl_image=ddlLink, logger=logger)

    print('\n')
    print("Completed downloading %s" % Series_Name)

def whole_series(url, directory, logger):

    scraper = cfscrape.create_scraper()
    connection = scraper.get(url).content

    soup = BeautifulSoup(connection, "html.parser")
    all_links = soup.findAll('div', {'class': 'list-chapter mCustomScrollbar'})

    for link in all_links:
        x = link.findAll('a')
        for a in x:
            # print(a['href'])
            url = "http://kisscomic.us" + a['href']
            logging.debug("Chapter URL : %s" % url)
            single_chapter(url, directory, logger)
    print("Finished Downloading")



def kissmcomicus_Url_Check(input_url, current_directory, logger):
    if logger == "True":
        logging.basicConfig(format='%(levelname)s: %(message)s', filename="Error Log.log", level=logging.DEBUG)
    kissmcomicus_single_regex = re.compile('https?://(?P<host>[^/]+)/chapters/(?P<comic>[\d\w-]+)(?:/Issue-)?')
    kissmcomicus_whole_regex = re.compile('https?://(?P<host>[^/]+)/comics/(?P<comic_name>[\d\w-]+)?')

    lines = input_url.split('\n')
    for line in lines:
        found = re.search(kissmcomicus_single_regex, line)
        if found:
            match = found.groupdict()
            if match['comic']:
                url = str(input_url)
                single_chapter(url, current_directory, logger)
            else:
                pass

        found = re.search(kissmcomicus_whole_regex, line)
        if found:
            match = found.groupdict()
            if match['comic_name']:
                url = str(input_url)
                whole_series(url, current_directory, logger)
            else:
                pass