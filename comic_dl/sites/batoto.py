#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import sys
from  more_itertools import unique_everseen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from downloader.universal import main as FileDownloader


"""Bato serves the chapters in 2 ways :
1.) All the images on 1 page by default. However, only some of the series/chapters have this thing.
2.) Traditional 1 page 1 image thing.

We can check which kind of page this is by checking the "NEXT ARROW" kind of thing to move to the next page.

batoto_login function open a fresh instance of selenium webdriver and logs the user in by sending user name and password to batoto login page.
The session is maintained and that instance of selenium webdriver is used to browse the pages to maintain the session and see the pages without
any restriction.

The script should show error if the user is trying the access the page not visible to logged out users and quit. Some instances of pages to replicate these validations :

1.) Page not available to logged out users : http://bato.to/reader#1f018238b7e945ed
2.) Single Page with all images : http://bato.to/reader#cb22bfed948294cb
3.) Traditional Manga Page : http://bato.to/reader#e5fc75f0ca34bcd5

There are small portions in the code block to explain certain scenarios, so devs. please go through them if you're thinking of changing something.

The directory contains the name of the Scanlation group as well, because the script currently downloads jus the english chapters, but in future it
will download all the languages available. So, this one as a reminded (lol) and for consistency. Oh, let's not forget the group's hardwork as well.

Currently there is no way/hack to view all the images in one page manually or to bypass the not logged in user restriction.
This script pretty much does everything fine. However, should you encounter a bug/problem, please mention in the github issue.
All bug fixes and patches are welcomed.
"""

def create_driver():
    
    desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
    desired_capabilities['phantomjs.page.customHeaders.User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) ' \
                                                                  'AppleWebKit/537.36 (KHTML, like Gecko) ' \
                                                                  'Chrome/39.0.2171.95 Safari/537.36'
    driver = webdriver.PhantomJS(desired_capabilities=desired_capabilities,service_args=['--load-images=no'])
    return driver

def single_chapter(driver,url,current_directory,User_Name,User_Password):
    
    """This little block checks whether the user has provided the arguments for password or username.
    If the user has provided something, then check that both UserName and Password has been provided.
    Filling either of them won't work. If the user has provided both, the username and password, send
    that info to batoto_login function which will create a logged in session and return us that instance
    of the selenium webdriver.
    """

    if str(User_Name) not in ["N"] or str(User_Password) not in ["N"]:
        if str(User_Name) in ["N"] or str(User_Password) in ["N"]:
            print "Username or Password cannot be empty."
            sys.exit()
        print "Authenticating Your Username and Password ..."
        
        batoto_login(driver,User_Name,User_Password)
        print "Logged in successfully"
    """Selenium was navigating to the new url, but the old page still had its resources loaded, which made selenium
    think that the page was already loaded. So, it started taking 'Stale Elements' and threw the same exception.
    So, refreshing the page seemed to do the job.
    """    
    driver.get(url)
    driver.refresh()

    """Let's wait till the 'comic wrap' element has been loaded. This element contains the actual
    image for the comic. This element doesn't load in the beginning, so Selenium could be tricked
    into the false alarm that the page has been loaded. Half loaded page will seem like fully loaded
    page and selenium will start executing the search operation, which will cause the script to break
    in case everything 'Comic Image' has been loaded.
    """
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "comic_wrap"))
        )
                
    except Exception, e:
        pass
    page_title = str(driver.title)
    
    """Batoto doesn't provide shit in the source code of the web page. Hence, we'll be using the outer HTML
    to scrap all the info we need.
    """
    elem = driver.find_element_by_xpath("//*")
    Page_Source = elem.get_attribute("outerHTML").encode('utf-8')

    """As mentioned above, batoto won't let the user watch/read the older entries/chapters if you're not logged in.
    So, if any user tries to download any such page, let's show the user the error and close the instance of selenium
    webdriver, and quit the script entirely without wasting anymore resources.
    """
    try:
        access_check = driver.find_element_by_xpath('//*[@id="reader"]/div/span').text
        
        if access_check in ["ERROR [10030]: The thing you're looking for is unavailable. It may be due to:"]:
            print "You cannot access this page. You'll need to log in to download this page."
            driver.quit()
            sys.exit()
        
        else:
            pass
        
    except Exception as e:
        pass


    try:
        Series_Name = str(re.search('^(.*)\ \-', page_title).group(1)).strip().replace('_',' ').title() # Getting the Series Name from the <title></title> tags of the web page.
    except Exception as e:
        Series_Name = "Unkown Series"
    
    try:
        volume_number = int(str(re.search('vol (\d+)', page_title).group(1)).strip()) # Getting the Series Name from the <title></title> tags of the web page.
    except Exception as e:
        volume_number = '0'
    
    try:
        chapter_number = int(str(re.search('ch (\d+)', page_title).group(1)).strip()) # Getting the Series Name from the <title></title> tags of the web page.
    except Exception as e:
        chapter_number = '0'
    
    try:
        Group_Name_Finder = str(driver.find_element_by_xpath('//*[@id="reader"]/div[1]/ul/li[3]/select').text).replace("/"," ").strip() # Used to find translation group's name from the 'Drop Down Menu'.
        
    except Exception as e:
        Group_Name_Finder = str('No Group') # Some entries on batoto don't have a name. So, if we get to any such occassion, let's be prepared.

    try:
        page_list = driver.find_element_by_id('page_select') # This is a check which tells us if this particular web page is a traditional way or one page all image thing.
        
    except Exception as e:
        
        page_list = False # If we cannot find the 'page_select' element, it means that this chapter is showing all the images in one page.

    if volume_number == 0:
        Raw_File_Directory = str(Series_Name)+'/'+"Chapter "+str(chapter_number)+" ["+str(Group_Name_Finder)+" ]" # Some series don't seem to have volumes mentioned. Let's assume they're 0.
    else:
        Raw_File_Directory = str(Series_Name)+'/'+"Volume "+str(volume_number)+'/'+"Chapter "+str(chapter_number)+" ["+str(Group_Name_Finder)+" ]"
    
    File_Directory = re.sub('[^A-Za-z0-9\-\.\'\#\/ \[\]]+', '', Raw_File_Directory) # Fix for "Special Characters" in The series name
    
    Directory_path = os.path.normpath(File_Directory)
    
    print '\n'
    print '{:^80}'.format('%s - %s')%(Series_Name,chapter_number)
    print '{:^80}'.format('=====================================================================\n')

    if page_list: # If batoto is serving 1 image per page, we'll be using this part.
        """We will be grabbing all the values in the drop down menu that has page numbers and take the very last value
        and extract the integer from it and use it to know what is the last page number for this chapter.
        Batoto follow a very simple linking syntax for serving the images, so let's exploit that to get the images
        without hitting batoto for each and every page of the chapter.
        URL Syntax : http://img.bato.to/comics/2016/11/02/s/read58196cffb13dd/img000001.jpg
        Look at the last number for the image. Manipulate that and we have what we need.
        """
        items_list = page_list.find_elements_by_tag_name("option")
        
        for item in items_list:
            list_of_pages = item.text
                
        lst_pag = str(list_of_pages)
        
        Last_Page_number = int(str(re.search('(\d+)', lst_pag).group(1)).strip())
        
        img_link = driver.find_element_by_id('comic_page').get_attribute('src')
        
        for i in range(1,Last_Page_number+1):
            if not os.path.exists(File_Directory):
                os.makedirs(File_Directory)
            if len(str(i)) == 1:
                
                ddl_image = str(img_link).replace('img000001','img00000%s')%(i)
                
            else:
                
                ddl_image = str(img_link).replace('img000001','img0000%s')%(i)
                
            File_Name_Final = str(i).strip()+"."+str(re.search('\d\.(.*?)$', ddl_image).group(1)).strip()
            FileDownloader(File_Name_Final,Directory_path,ddl_image)

        print '\n'
        print "Completed downloading ",Series_Name,' - ',chapter_number
        #driver.close()


    
    if not page_list: # If Batoto is serving all the images in one page, we'll follow this block.
        """Since all the image links are in one place, we don't have to rack our brains. Grab all the links
        to the images and download them one by one.
        """

        soup = BeautifulSoup(Page_Source,"html.parser")
        Image_Links = soup.findAll('div',{'style':'text-align:center;'})
        
        for link in Image_Links:
            if not os.path.exists(File_Directory):
                os.makedirs(File_Directory)
            x = link.findAll('img')
            for a in x:
                ddl_image = a['src']
                
                File_Name_Final = str(re.search('img0000(\d+)\.([jpg]|[png])', ddl_image).group(1)).strip()+"."+str(re.search('\d\.(.*?)$', ddl_image).group(1)).strip()
                FileDownloader(File_Name_Final,Directory_path,ddl_image)
        
        print '\n'
        print "Completed Downloading ",Series_Name,' - ',chapter_number
                
def whole_series(driver,url,current_directory,User_Name,User_Password):
    #print "Whole Series : ",url
    """This little block checks whether the user has provided the arguments for password or username.
    If the user has provided something, then check that both UserName and Password has been provided.
    Filling either of them won't work. If the user has provided both, the username and password, send
    that info to batoto_login function which will create a logged in session and return us that instance
    of the selenium webdriver.
    """
    
    if str(User_Name) not in ["N"] or str(User_Password) not in ["N"]:
        if str(User_Name) in ["N"] or str(User_Password) in ["N"]:
            print "Username or Password cannot be empty."
            sys.exit()
        print "Authenticating Your Username and Password ..."
        
        batoto_login(driver,User_Name,User_Password)
        print "Logged in successfully"

        driver.get(url)
        """Let's wait till the 'content' element has been loaded. This element contains the list of all the
        chapters related to a particular manga. This element doesn't load in the beginning, so Selenium could 
        be tricked into the false alarm that the page has been loaded. Half loaded page will seem like fully 
        loaded page and selenium will start executing the search operation, which will cause the script to 
        break in case everything 'Comic Image' has been loaded.
        """
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "content"))
            )
                
        except Exception, e:
            pass
        elem = driver.find_element_by_xpath("//*")
        Page_Source = elem.get_attribute("outerHTML").encode('utf-8')
        """Basic idea is to grab all the 'a href' links found in the `row lang_English chapter_row` class
        and put them inside a lit. Later, for each element of the list, call the 'single_chapter' function to
        do the rest of the job.
        """
        
        link_list = []

        soup = BeautifulSoup(Page_Source,"html.parser")
        all_links = soup.findAll('tr',{'class':'row lang_English chapter_row'})       
        

        for link in all_links:
            x = link.findAll('a')
            for a in x:
                ddl_image = a['href']
                if "reader" in ddl_image:
                    
                    link_list.append(ddl_image)

        print "Total Chapters To Download : ",len(link_list)

        for item in link_list:
            url = str(item)
            User_Name = 'N'
            User_Password = 'N'
            single_chapter(driver,url,current_directory,User_Name,User_Password)


        
    else:
        # If the user hasn't supplied any logging information, we'll do this.
        driver.get(url)
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "content"))
            )
                
        except Exception, e:
            pass
        elem = driver.find_element_by_xpath("//*")
        Page_Source = elem.get_attribute("outerHTML").encode('utf-8')
        
        link_list = []

        soup = BeautifulSoup(Page_Source,"html.parser")
        all_links = soup.findAll('tr',{'class':'row lang_English chapter_row'})       
        
        for link in all_links:
            x = link.findAll('a')
            for a in x:
                ddl_image = a['href']
                if "reader" in ddl_image:
                    link_list.append(ddl_image)

        print "Total Chapters To Download : ",len(link_list)
        print link_list

        for x in link_list:
            url = str(x)
            User_Name = 'N'
            User_Password = 'N'
            single_chapter(driver,url,current_directory,User_Name,User_Password)

        
def batoto_login(driver,User_Name,User_Password):
    
    driver.get("https://bato.to/forums/index.php?app=core&module=global&section=login")
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ips_password"))
        )
                
    except Exception, e:
        #driver.save_screenshot('Single_exception.png')
        pass
    LoggedOut_Title = driver.title
    driver.find_element_by_id('ips_username').send_keys(User_Name)
    driver.find_element_by_id('ips_password').send_keys(User_Password)
    
    driver.find_element_by_xpath('//*[@id="login"]/fieldset[2]/input').click()
    LoggedIn_Title = driver.title

    """A little check to see whether we've logged in or not. Comparing the titles of the before and after logging
    pages.
    """

    if str(LoggedIn_Title).strip() == str(LoggedOut_Title).strip():
        print "Couldn't log you in. Please check your credentials."
        driver.quit()
        sys.exit()
    

def batoto_Url_Check(input_url,current_directory,User_Name,User_Password):
    
    batoto_single_regex = re.compile('https?://(?P<host>bato.to)/reader\#(?P<extra_characters>[\d\w-]+)?(\/|.)')
    batoto_whole_regex = re.compile('^https?://(?P<host>bato.to)/comic/\_/comics/(?P<comic>[\d\w-]+)?(\/|.)$')

    lines = input_url.split('\n')
    for line in lines:
        found = re.search(batoto_single_regex, line)
        if found:
            match = found.groupdict()
            if match['extra_characters']:
                url = str(input_url)
                driver = create_driver()
                single_chapter(driver,url,current_directory,User_Name,User_Password)
                driver.quit()
            else:
                pass
                

        
        found = re.search(batoto_whole_regex, line)
        if found:
            match = found.groupdict()
            if match['comic']:
                url = str(input_url)
                driver = create_driver()
                whole_series(driver,url,current_directory,User_Name,User_Password)
                driver.quit()
            else:
                pass


