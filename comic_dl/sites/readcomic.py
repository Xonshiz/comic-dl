#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import print_function
from builtins import str
from downloader.universal import main as FileDownloader
from re import search,sub,compile, findall
from os import path,makedirs
from sys import exit
from bs4 import BeautifulSoup
from cfscrape import create_scraper
from logging import debug, basicConfig, DEBUG


def readcomic_Url_Check(input_url, current_directory, logger, sortingOrder):
    if logger == "True":
        basicConfig(format='%(levelname)s: %(message)s', filename="Error Log.log", level=DEBUG)

    Issue_Regex = compile('https?://(?P<host>[^/]+)/Comic/(?P<comic>[\d\w-]+)(?:/Issue-)?(?P<issue>\d+)?')
    Annual_Regex = compile('https?://(?P<host>[^/]+)/Comic/(?P<comic>[\d\w-]+)(?:/Annual-)?(?P<issue>\d+)?')
    lines = input_url.split('\n')
    for line in lines:
        found = search(Issue_Regex, line)
        if found:
            match = found.groupdict()
            if match['issue']:
                Edited_Url = str(input_url) + '?&readType=1'
                url = str(Edited_Url)
                Single_Issue(url, current_directory, logger)

            else:
                url = str(input_url)
                Whole_Series(url, current_directory, logger, sortingOrder)

        found = search(Annual_Regex, line)
        if found:
            match = found.groupdict()

            if match['issue']:
                Edited_Url = str(input_url) + '?&readType=1'
                url = str(Edited_Url)
                Single_Issue(url, current_directory, logger)
            else:
                print()
                'Uh, please check the link'

        if not found:
            print()
            'Please Check Your URL one again!'
            exit()

def Single_Issue(url, current_directory, logger):

    scraper = create_scraper()
    connection = scraper.get(url).content

    Series_Name_Splitter = url.split('/')
    Series_Name = str(Series_Name_Splitter[4]).replace('-', ' ')
    Issue_Number_Splitter = str(Series_Name_Splitter[5])
    Issue_Or_Annual_Split = str(Issue_Number_Splitter).split("?")
    Issue_Or_Annual = str(Issue_Or_Annual_Split[0]).replace("-", " ").strip()
    reg = findall(r'[(\d)]+', Issue_Number_Splitter)

    Issue_Number = str(reg[0])

    Raw_File_Directory = str(Series_Name) + '/' + "Chapter " + str(Issue_Or_Annual)

    File_Directory = sub('[^A-Za-z0-9\-\.\'\#\/ ]+', '',
                            Raw_File_Directory)  # Fix for "Special Characters" in The series name

    Directory_path = path.normpath(File_Directory)

    print('\n')
    print('{:^80}'.format('=====================================================================\n'))
    print('{:^80}'.format('%s - %s') % (Series_Name, Issue_Or_Annual))
    print('{:^80}'.format('=====================================================================\n'))

    linksList = findall('lstImages.push\(\"(.*?)\"\)\;', str(connection))
    debug("Image Links : %s" % linksList)

    for link in linksList:
        if not path.exists(File_Directory):
            makedirs(File_Directory)
        fileName = str(linksList.index(link)) + ".jpg"
        # debug("Name of File : %s" % fileName)
        FileDownloader(fileName, Directory_path, link, logger)

def Whole_Series(url, current_directory, logger, sortingOrder):

    scraper = create_scraper()
    connection = scraper.get(url).content

    soup = BeautifulSoup(connection, "html.parser")
    # debug("Soup : %s" % soup)
    all_links = soup.findAll('table', {'class': 'listing'})
    # debug("Issue Links : %s" % all_links)

    final_links = []
    for link in all_links:
        # debug("link : %s" % link)
        x = link.findAll('a')
        debug("Actual Link : %s" % x)
        for a in x:
            url = "http://readcomiconline.to" + a['href']
            debug("Final URL : %s" % url)
            final_links.append(url)
    print(final_links)
    if str(sortingOrder).lower() in ['new', 'desc', 'descending', 'latest']:
        for chapLink in final_links:
            Single_Issue(chapLink, current_directory=current_directory, logger=logger)
    elif str(sortingOrder).lower() in ['old', 'asc', 'ascending', 'oldest', 'a']:
        # print("Running this")
        for chapLink in final_links[::-1]:
            Single_Issue(chapLink, current_directory=current_directory, logger=logger)
    print("Finished Downloading")

