#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import os
import re
import sys
import urllib2
import urllib
import shutil
from bs4 import BeautifulSoup
from urllib2 import URLError
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from downloader.universal import main as FileDownloader


def create_driver():
    
    desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
    desired_capabilities['phantomjs.page.customHeaders.User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) ' \
                                                                  'AppleWebKit/537.36 (KHTML, like Gecko) ' \
                                                                  'Chrome/39.0.2171.95 Safari/537.36'
    driver = webdriver.PhantomJS(desired_capabilities=desired_capabilities,service_args=['--load-images=no'])
    return driver

def single_chapter(driver,url,current_directory):
    
    try:
        Series_Name = str(re.search('manga\/(.*?)/v', url).group(1)).strip().replace('_',' ').title() # Getting the Series Name from the URL itself for naming the folder/dicrectories.
    except Exception as e:
        Series_Name = str(re.search('manga\/(.*?)/c', url).group(1)).strip().replace('_',' ').title() # Getting the Series Name from the URL itself for naming the folder/dicrectories.
    
    try:
        volume_number = "Volume " + str(re.search('v(.*?)/c', url).group(1)).strip() # Getting the volume count from the URL itself for naming the folder/dicrectories.
    except Exception as e:
        volume_number = "Volume 01"
    
    try:
        chapter_number = int(str(re.search('\/c(.*?)/\d', url).group(1)).strip()) # Getting the chapter count from the URL itself for naming the folder/dicrectories in integer.
    except Exception as e:
        chapter_number = float(str(re.search('\/c(.*?)/\d', url).group(1)).strip()) # Getting the chapter count from the URL itself for naming the folder/dicrectories in float.
    
    if volume_number == '0':
        Raw_File_Directory = str(Series_Name)+'/'+"Chapter "+str(chapter_number) # Some series don't seem to have volumes mentioned. Let's assume they're 0.
    else:
        Raw_File_Directory = str(Series_Name)+'/'+str(volume_number)+'/'+"Chapter "+str(chapter_number)
    
    File_Directory = re.sub('[^A-Za-z0-9\-\.\'\#\/ \[\]]+', '', Raw_File_Directory) # Fix for "Special Characters" in The series name
    
    Directory_path = os.path.normpath(File_Directory)

    driver.get(url)

    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "image"))
        )
                
    except Exception, e:
        driver.save_screenshot("error.png")
        print "Couldn't load the element. I'll try to move ahead in any case."
        print '\n'
        print "I took a screenshot, please attach it in the issue you open in the repository."
        pass

    elem = driver.find_element_by_xpath("//*")
    Page_Source = elem.get_attribute("outerHTML").encode('utf-8')

    First_chapter_link = str(re.search('http://(.*?)/(.*?)/manga/(.*?)/(.*?)/compressed/(.*?)\.jpg', Page_Source).group(0)).strip() # Fix if they change the CDN all of a sudden.
    
    current_chapter_count = int(str(re.search('current_page\=(.*?)\;', Page_Source).group(1)).strip()) # Getting the last chapter number from the URL itself for naming the folder/dicrectories.
    
    last_chapter_count = int(str(re.search('total_pages\=(.*?)\;', Page_Source).group(1)).strip()) # Getting the last chapter number from the URL itself for naming the folder/dicrectories.
    
    print '\n'
    print '{:^80}'.format('%s - %s')%(Series_Name,chapter_number)
    print '{:^80}'.format('=====================================================================\n')

    if not os.path.exists(File_Directory):
        os.makedirs(File_Directory)
     
    for x in range(current_chapter_count,last_chapter_count+1):
        
        driver.refresh()
        File_Name_Final = str(x)+'.jpg'
        link_container = driver.find_element_by_xpath('//*[@id="image"]')
        ddl_image = str(link_container.get_attribute('src'))
        FileDownloader(File_Name_Final,Directory_path,ddl_image)
        driver.find_element_by_xpath('//*[@id="top_bar"]/div/a[2]').click()
        
    print '\n'
    print "Completed downloading ",Series_Name,' - ',chapter_number


def whole_series(url,current_directory):
    
    if not url:
        print "Couldn't get the URL. Please report it on Github Repository."

    try:
        Series_Name = str(re.search('manga\/(.*?)/', url).group(1)).strip() # Getting the Series Name from the URL itself for naming the folder/dicrectories.
    except Exception as e:
        print 'Check if the URL is correct or not. Report on Github.'
    
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
        
    }
    
    response = requests.get(url, headers=headers)
    Page_source = str(response.text.encode('utf-8'))
    
    try:
        chapter_link_format = "http://mangafox.me/manga/"+str(Series_Name)+"/v"
        links = re.findall('{0}(.*?)html'.format(chapter_link_format),Page_source)
        
        if len(links) == 0:
            chapter_link_format = "http://mangafox.me/manga/"+str(Series_Name)+"/c"
            #print chapter_link_format
            links = re.findall('{0}(.*?)html'.format(chapter_link_format),Page_source)


    except Exception as e:
       print "Error : ",e,'\n',"Please report this error on Github repository."

    driver = create_driver()
    
    for x in links:
        chapter_link = str(str(chapter_link_format)+str(x)+"html").strip()
        
        try:
            single_chapter(driver,chapter_link,current_directory)
        except Exception as e:
            print e
            driver.quit()
    driver.quit()

def mangafox_Url_Check(input_url,current_directory):
    
    mangafox_single_regex = re.compile('https?://(?P<host>mangafox.me)/manga/(?P<comic>[\d\w-]+)(?P<Volume>(/v\d+)|(.))/(?P<chapter>c\d+(\.\d)?)?/(?P<issue>\d+)?\.html')
    mangafox_whole_regex = re.compile('^https?://(?P<host>mangafox.me)/manga/(?P<comic_series>[\d\w-]+)?|(\/)$')

    lines = input_url.split('\n')
    for line in lines:
        found = re.search(mangafox_single_regex, line)
        if found:
            match = found.groupdict()
            if match['issue']:
                url = str(input_url)
                driver = create_driver()
                try:
                    single_chapter(driver,url,current_directory)
                except Exception as e:
                    print e
                    driver.quit()
                driver.quit()
                sys.exit()
            else:
                pass
                

        
        found = re.search(mangafox_whole_regex, line)
        if found:
            match = found.groupdict()
            if match['comic_series']:
                url = str(input_url)
                #driver = create_driver()
                try:
                    whole_series(url,current_directory)
                except Exception as e:
                    print e
                sys.exit()
            else:
                pass
