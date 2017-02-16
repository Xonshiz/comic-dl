#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import print_function
from re import search,sub,compile, findall
from os import path,makedirs
from sys import exit
from bs4 import BeautifulSoup
from downloader.universal import main as FileDownloader
from cfscrape import create_scraper
from logging import debug, basicConfig, DEBUG


def single_chapter(url, current_directory, logger):
    
    scraper = create_scraper()

    Page_Source = scraper.get(str(url)).content

    formatted = BeautifulSoup(Page_Source, "lxml")
    
    meta = formatted.findAll('title')
    
    meta_data = list(str(meta).split('\n'))
    # print(meta_data)
    

    try:
        Series_Name = str(meta_data[2])
    except Exception as e:
        # print (e)
        debug("Error in Series Name : %s" % e)
        Series_Name = "Unkown Series"

    try:
        # Getting the Volume Number from the page source.
        volume_number = int(
            str(search('Vol\.(.*)\ Ch', Page_Source).group(1)).strip())
    except Exception as e:
        debug("Error in Volume Number : %s" % e)
        volume_number = '0'

    try:
        chapter_number = str(meta_data[3])

    except Exception as e:
        debug("Error in Chapter Number : %s\nTrying Something else." % e)
        try:
            # Getting the Volume Number from the page source.
            chapter_number = str(search('Ch\.(.*)\:', str(Page_Source)).group(1)).strip()
        except Exception as e:
            debug("Error in Chapter Number : %s" % e)
            chapter_number = str('0')

    all_links = findall('lstImages.push\(\"(.*)\"\)\;', str(formatted))
    debug("Image Links : %s" % all_links)
    
    if volume_number == '0':
        # Some series don't seem to have volumes mentioned. Let's assume
        # they're 0.
        Raw_File_Directory = str(Series_Name) + '/' + \
            "Chapter " + str(chapter_number)
    else:
        debug("Found the Volume. Making a directory.")
        Raw_File_Directory = str(Series_Name) + '/' + "Volume " + \
            str(volume_number) + '/' + "Chapter " + str(chapter_number)

    # Fix for "Special Characters" in The series name
    File_Directory = sub(
        '[^A-Za-z0-9\-\.\'\#\/ \[\]]+',
        '',
        Raw_File_Directory)

    Directory_path = path.normpath(File_Directory)

    print ('\n')
    print('{:^80}'.format('%s - %s') % (Series_Name, chapter_number))
    print('{:^80}'.format('=====================================================================\n'))

    for elements in all_links:
        sane_url = str(elements).replace("%3a",":").replace("%2f","/").replace("&imgmax=30000","").replace("https://images1-focus-opensocial.googleusercontent.com/gadgets/proxy?container=focus&gadget=a&no_expand=1&resize_h=0&rewriteMime=image%2F*&url=","")
        # print(sane_url)
        if not path.exists(File_Directory):
            makedirs(File_Directory)
        ddl_image = str(sane_url).strip()

        try:
            File_Name_Final = str(search(
                's0/(.*)\.([png]|[jpg])', ddl_image).group(1)).strip() + "." + str(ddl_image[-3:])
        except Exception as e:
            debug("Error in File Name : %s" % e)
            try:
                File_Name_Final = str(search(
                    'title\=(.*)\_(\d+)\.([png]|[jpg])', ddl_image).group(1)).strip() + "." + str(ddl_image[-3:])
            except Exception as e:
                debug("Error inside Error : %s" % e)
                File_Name_Final = str(ddl_image[-6:])
        # print(File_Name_Final)
        FileDownloader(File_Name_Final, Directory_path, ddl_image, logger)

    print('\n')
    print("Completed downloading ", Series_Name, ' - ', chapter_number)


def whole_series(url, current_directory, logger):

    scraper = create_scraper()

    Page_Source = scraper.get(str(url)).content

    link_list = []

    soup = BeautifulSoup(Page_Source, "html.parser")
    all_links = soup.findAll('table', {'class': 'listing'})
    debug("Chapter Links : %s" % all_links)

    for link in all_links:
        x = link.findAll('a')
        for a in x:

            ddl_image = a['href']
            if "Manga" in ddl_image:
                final_url = "http://kissmanga.com" + ddl_image
                link_list.append(final_url)
                debug("%s added in the bag!" % final_url)

    if int(len(link_list)) == '0':
        print("Sorry, I couldn't bypass KissManga's Hooman check. Please try again in a few minutes.")
        exit()

    print("Total Chapters To Download : ", len(link_list))

    for item in link_list:
        url = str(item)
        debug("Chapter Links : %s" % url)
        single_chapter(url, current_directory, logger)


def kissmanga_Url_Check(input_url, current_directory, logger):
    if logger == "True":
        basicConfig(format='%(levelname)s: %(message)s', filename="Error Log.log", level=DEBUG)

    kissmanga_single_regex = compile(
        'https?://(?P<host>kissmanga.com)/Manga/(?P<Series_Name>[\d\w-]+)?/((?P<Volume>[Vol\-\d]+)|(.*)(?P<Chapter>[Ch\d\w-]+))\-(?P<Chap_Name>[\d\w-]+)\?(?P<id>[\=\d\w-]+)')
    kissmanga_whole_regex = compile(
        '^https?://(?P<host>kissmanga.com)/Manga/(?P<comic>[\d\w\-]+)?(\/|.)$')

    lines = input_url.split('\n')
    # print(lines)
    for line in lines:
        found = search(kissmanga_single_regex, line)
        # print(found)
        if found:
            match = found.groupdict()
            if match['Chap_Name']:
                url = str(input_url)
                # print("Here inside!")
                single_chapter(url, current_directory, logger)
                # print("Passed it")
            else:
                pass

        found = search(kissmanga_whole_regex, line)
        # print(found)
        if found:
            match = found.groupdict()
            if match['comic']:
                url = str(input_url)
                whole_series(url, current_directory, logger)
            else:
                pass
