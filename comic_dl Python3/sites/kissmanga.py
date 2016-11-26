#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function
import re
import os
import sys
from bs4 import BeautifulSoup
from downloader.universal import main as FileDownloader
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By



def create_driver():
    
    desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
    desired_capabilities['phantomjs.page.customHeaders.User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) ' \
                                                                  'AppleWebKit/537.36 (KHTML, like Gecko) ' \
                                                                  'Chrome/39.0.2171.95 Safari/537.36'
    driver = webdriver.PhantomJS(desired_capabilities=desired_capabilities,service_args=['--load-images=no'])
    return driver

def single_chapter(driver,url,current_directory):

    try:
        Series_Name = str(re.search('Manga/(.*)/([Vol]|[Ch])', url).group(1)).strip().replace('-',' ').title() # Getting the Series Name from the url itself.
    except Exception as e:
        Series_Name = "Unkown Series"
    
    try:
        volume_number = int(str(re.search('Vol\-(.*)\-Ch', url).group(1)).strip()) # Getting the Volume Number from the url itself.
    except Exception as e:
        volume_number = '0'
    
    try:
        chapter_number = int(str(re.search('Ch\-(.*)\-\-', url).group(1)).strip()) # Getting the Chapter Number from the url itself.
        
    except Exception as e:
        chapter_number = '0'

    driver.get(url)
    driver.refresh()

    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "divImage"))
        )
                
    except Exception as e:
        pass

    elem = driver.find_element_by_xpath("//*")
    Page_Source = elem.get_attribute("outerHTML")

    all_links = re.findall('lstImages.push\(\"(.*)\"\)\;',Page_Source)
    
    if volume_number == '0':
        Raw_File_Directory = str(Series_Name)+'/'+"Chapter "+str(chapter_number) # Some series don't seem to have volumes mentioned. Let's assume they're 0.
    else:
        Raw_File_Directory = str(Series_Name)+'/'+"Volume "+str(volume_number)+'/'+"Chapter "+str(chapter_number)
    
    File_Directory = re.sub('[^A-Za-z0-9\-\.\'\#\/ \[\]]+', '', Raw_File_Directory) # Fix for "Special Characters" in The series name
    
    Directory_path = os.path.normpath(File_Directory)

    print('\n')
    print('{:^80}'.format('%s - %s')%(Series_Name,chapter_number))
    print('{:^80}'.format('=====================================================================\n'))


    for element in all_links:
        if not os.path.exists(File_Directory):
                os.makedirs(File_Directory)
        ddl_image = str(element).strip()
        
        try:
            File_Name_Final = str(re.search('s0/(.*)\.([png]|[jpg])',ddl_image).group(1)).strip()+"."+str(ddl_image[-3:])
        except Exception as e:
            File_Name_Final = str(re.search('title\=(.*)\_(\d+)\.([png]|[jpg])',ddl_image).group(1)).strip()+"."+str(ddl_image[-3:])

        
        FileDownloader(File_Name_Final,Directory_path,ddl_image)
    
    print('\n')
    print("Completed downloading ",Series_Name,' - ',chapter_number)

def whole_series(driver,url,current_directory):
    
    driver.get(url)
    
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "leftside"))
        )
                
    except Exception as e:
        driver.save_screenshot("error.png")
        print("Couldn't load the element. I'll try to move ahead in any case.")
        print('\n')
        print("I took a screenshot, please attach it in the issue you open in the repository.")
        pass
    

    
    elem = driver.find_element_by_xpath("//*")
    Page_Source = elem.get_attribute("outerHTML").encode('utf-8')

    link_list = []

    soup = BeautifulSoup(Page_Source,"html.parser")
    all_links = soup.findAll('table',{'class':'listing'})       
    
    for link in all_links:
        x = link.findAll('a')
        for a in x:
            
            ddl_image = a['href']
            if "Manga" in ddl_image:
                #print (ddl_image)
                #sys.exit()
                final_url = "http://kissmanga.com"+ddl_image
                link_list.append(final_url)
    #print (link_list)            
    
    
    if int(len(link_list)) == '0':
        print("Sorry, I couldn't bypass KissManga's Hooman check. Please try again in a few minutes.")
        sys.exit()

    print("Total Chapters To Download : ",len(link_list))

    for item in link_list:
            url = str(item)
            #print (url)
            single_chapter(driver,url,current_directory)

def kissmanga_Url_Check(input_url,current_directory):
    
    kissmanga_single_regex = re.compile('https?://(?P<host>kissmanga.com)/Manga/(?P<Series_Name>[\d\w-]+)?/((?P<Volume>[Vol\-\d]+)|(.*)(?P<Chapter>[Ch\-\d]+))\-(?P<Chap_Name>[\d\w-]+)\?(?P<id>[\=\d\w-]+)')
    kissmanga_whole_regex = re.compile('^https?://(?P<host>kissmanga.com)/Manga/(?P<comic>[\d\w\-]+)?(\/|.)$')

    lines = input_url.split('\n')
    for line in lines:
        found = re.search(kissmanga_single_regex, line)
        if found:
            match = found.groupdict()
            if match['Chap_Name']:
                url = str(input_url)
                driver = create_driver()
                try:
                    single_chapter(driver,url,current_directory)
                except Exception as e:
                    print(e)
                    driver.quit()
                driver.quit()
            else:
                pass
                

        
        found = re.search(kissmanga_whole_regex, line)
        if found:
            match = found.groupdict()
            if match['comic']:
                url = str(input_url)
                driver = create_driver()
                try:
                    whole_series(driver,url,current_directory)
                except Exception as e:
                    print(e)
                    driver.quit()
                driver.quit()
            else:
                pass

