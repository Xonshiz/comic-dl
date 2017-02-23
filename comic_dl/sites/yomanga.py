#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function
import requests
from  more_itertools import unique_everseen
from re import search,sub,compile, findall
from os import path,makedirs
from sys import exit
from bs4 import BeautifulSoup
from downloader.cookies_required import main as FileDownloader
from logging import debug, basicConfig, DEBUG
from requests import Session,cookies


def single_chapter(url, current_directory, logger):
    
    if not url:
        print("Couldn't get the URL. Please report it on Github Repository.")
        exit(0)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
        
    }
    
    s = Session()
    response = s.get(url, headers=headers)
    tasty_cookies = response.cookies
    
    Page_source = str(response.text.encode('utf-8'))
    
    Series_Name = str(search('\/read\/(.*?)/', url).group(1)).strip().replace('_',' ').title() # Getting the Series Name from the URL itself for naming the folder/dicrectories.
    
    try:
        chapter_number = int(str(search('0\/(.*?)/', url).group(1)).strip().replace('0','').replace('/','')) # Getting the chapter count from the URL itself for naming the folder/dicrectories in integer.
    except Exception as e:
        debug("Error in Chapter Number : %s" % e)
        chapter_number = 0 # Name the chapter 0 if nothing INTEGER type comes up
   
    Raw_File_Directory = str(Series_Name)+'/'+"Chapter "+str(chapter_number)
    File_Directory = sub('[^A-Za-z0-9\-\.\'\#\/ ]+', '', Raw_File_Directory) # Fix for "Special Characters" in The series name
    Directory_path = path.normpath(File_Directory)
   
    
    ddl_image_list = findall('comics(.*?)\"', Page_source)
    
    ddl_list = list(unique_everseen(ddl_image_list))
    debug("Image Links : %s" % ddl_list)

    print('\n')
    print('{:^80}'.format('%s - %s')%(Series_Name,chapter_number))
    print('{:^80}'.format('=====================================================================\n'))

    for i in ddl_list:
        if not path.exists(File_Directory):
                        makedirs(File_Directory)
        ddl_image = "http://yomanga.co/reader/content/comics"+str(i).replace('"','').replace('\\','')
        debug("Image Download Link : %s" % ddl_image)
        
        File_Name_Final = str(findall('\/(\d+)\.[jpg]|[png]', i)).replace("[","").replace("]","").replace("'","").replace(",","").strip()+"."+str(findall('\d\.(.*?)$', str(i))).replace(",","").replace("[","").replace("]","").replace("'","").strip()
        FileDownloader(File_Name_Final,Directory_path,tasty_cookies,ddl_image, logger)
        
    print('\n')
    print("Completed downloading ",Series_Name)

def whole_series(url, current_directory, logger, sortingOrder):
    if not url:
        print("Couldn't get the URL. Please report it on Github Repository.")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
        
    }
    
    s = Session()
    response = s.get(url, headers=headers)
    tasty_cookies = response.cookies
    
    Page_source = str(response.text.encode('utf-8'))

    Series_Name = str(search('\/series\/(.*?)/', url).group(1)).strip().replace('_',' ').title() # Getting the Series Name from the URL itself for naming the folder/dicrectories.
    
    soup = BeautifulSoup(Page_source, 'html.parser')

    chapter_text = soup.findAll('div',{'class':'title'})
    debug("Chapter Text : %s" % chapter_text)
    all_links = []

    for link in chapter_text:
        x = link.findAll('a')
        for a in x:
            url = a['href']
            debug("Chapter URL : %s" % url)
            all_links.append(url)

    if str(sortingOrder).lower() in ['new','desc','descending','latest']:
        for chapLink in all_links[::-1]:
            single_chapter(chapLink, current_directory, logger)
    elif str(sortingOrder).lower() in ['old','asc','ascending','oldest']:
        # print("Running this")
        for chapLink in all_links[::-1]:
            single_chapter(chapLink, current_directory, logger)
    print("Finished Downloading")
            
def yomanga_Url_Check(input_url, current_directory, logger, sortingOrder):
    if logger == "True":
        basicConfig(format='%(levelname)s: %(message)s', filename="Error Log.log", level=DEBUG)
    
    yomanga_single_regex = compile('https?://(?P<host>yomanga.co)/reader/read/(?P<comic_single>[\d\w-]+)/en/(?P<volume>\d+)?/(?P<Chapter>\d+)?()|(/page/(?P<PageNumber>\d+)?)')
    yomanga_whole_regex = compile('^https?://(?P<host>yomanga.co)/reader/(?P<series>series)?/(?P<comic>[\d\w-]+)?(\/|.)$')
    
    lines = input_url.split('\n')
    for line in lines:
        found = search(yomanga_single_regex, line)
        if found:
            match = found.groupdict()
            if match['Chapter']:
                url = str(input_url)
                single_chapter(url, current_directory, logger)
            else:
                pass
                

        
        found = search(yomanga_whole_regex, line)
        if found:
            match = found.groupdict()
            if match['comic']:
                url = str(input_url)
                whole_series(url, current_directory, logger, sortingOrder)
            else:
                pass







