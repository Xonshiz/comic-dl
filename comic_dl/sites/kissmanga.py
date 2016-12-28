#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import sys
from bs4 import BeautifulSoup
from downloader.universal import main as FileDownloader
import cfscrape


def single_chapter(url, current_directory):
    
    scraper = cfscrape.create_scraper()

    Page_Source = scraper.get(str(url)).content

    formatted = BeautifulSoup(Page_Source, "lxml")
    
    meta = formatted.findAll('title')
    
    meta_data = list(str(meta).split('\n'))
    

    try:
        Series_Name = str(meta_data[2])
    except Exception as e:
        print (e)
        Series_Name = "Unkown Series"

    try:
        # Getting the Volume Number from the page source.
        volume_number = int(
            str(re.search('Vol\.(.*)\ Ch', Page_Source).group(1)).strip())
    except Exception as e:
        volume_number = '0'

    try:
        chapter_number = int(str(meta_data[3]))

    except Exception as e:
        try:
            # Getting the Volume Number from the page source.
            chapter_number = int(
                str(re.search('Ch\.(.*)\:', Page_Source).group(1)).strip())
        except Exception as e:
            chapter_number = '0'

    all_links = re.findall('lstImages.push\(\"(.*)\"\)\;', str(formatted))
    
    if volume_number == '0':
        # Some series don't seem to have volumes mentioned. Let's assume
        # they're 0.
        Raw_File_Directory = str(Series_Name) + '/' + \
            "Chapter " + str(chapter_number)
    else:
        Raw_File_Directory = str(Series_Name) + '/' + "Volume " + \
            str(volume_number) + '/' + "Chapter " + str(chapter_number)

    # Fix for "Special Characters" in The series name
    File_Directory = re.sub(
        '[^A-Za-z0-9\-\.\'\#\/ \[\]]+',
        '',
        Raw_File_Directory)

    Directory_path = os.path.normpath(File_Directory)

    print ('\n')
    print('{:^80}'.format('%s - %s') % (Series_Name, chapter_number))
    print('{:^80}'.format('=====================================================================\n'))

    for elements in all_links:
        if not os.path.exists(File_Directory):
            os.makedirs(File_Directory)
        ddl_image = str(elements).strip()

        try:
            File_Name_Final = str(re.search(
                's0/(.*)\.([png]|[jpg])', ddl_image).group(1)).strip() + "." + str(ddl_image[-3:])
        except Exception as e:
            File_Name_Final = str(re.search(
                'title\=(.*)\_(\d+)\.([png]|[jpg])', ddl_image).group(1)).strip() + "." + str(ddl_image[-3:])
        FileDownloader(File_Name_Final, Directory_path, ddl_image)

    print('\n')
    print("Completed downloading ", Series_Name, ' - ', chapter_number)


def whole_series(url, current_directory):

    scraper = cfscrape.create_scraper()

    Page_Source = scraper.get(str(url)).content

    link_list = []

    soup = BeautifulSoup(Page_Source, "html.parser")
    all_links = soup.findAll('table', {'class': 'listing'})

    for link in all_links:
        x = link.findAll('a')
        for a in x:

            ddl_image = a['href']
            if "Manga" in ddl_image:
                final_url = "http://kissmanga.com" + ddl_image
                link_list.append(final_url)

    if int(len(link_list)) == '0':
        print("Sorry, I couldn't bypass KissManga's Hooman check. Please try again in a few minutes.")
        sys.exit()

    print("Total Chapters To Download : ", len(link_list))

    for item in link_list:
        url = str(item)
        single_chapter(url, current_directory)


def kissmanga_Url_Check(input_url, current_directory):

    kissmanga_single_regex = re.compile(
        'https?://(?P<host>kissmanga.com)/Manga/(?P<Series_Name>[\d\w-]+)?/((?P<Volume>[Vol\-\d]+)|(.*)(?P<Chapter>[Ch\-\d]+))\-(?P<Chap_Name>[\d\w-]+)\?(?P<id>[\=\d\w-]+)')
    kissmanga_whole_regex = re.compile(
        '^https?://(?P<host>kissmanga.com)/Manga/(?P<comic>[\d\w\-]+)?(\/|.)$')

    lines = input_url.split('\n')
    for line in lines:
        found = re.search(kissmanga_single_regex, line)
        if found:
            match = found.groupdict()
            if match['Chap_Name']:
                url = str(input_url)
                single_chapter(url, current_directory)
            else:
                pass

        found = re.search(kissmanga_whole_regex, line)
        if found:
            match = found.groupdict()
            if match['comic']:
                url = str(input_url)
                whole_series(url, current_directory)
            else:
                pass
