#!/usr/bin/env python
# -*- coding: utf-8 -*-

import globalFunctions
import requests
import cfscrape
from bs4 import BeautifulSoup
import sys
import re
import os


class Batoto:
    def __init__(self, manga_url, download_directory, chapter_range, **kwargs):
        user_name = kwargs.get("username")
        password = kwargs.get("password")
        comic_language = kwargs.get("comic_language")
        current_directory = kwargs.get("current_directory")
        conversion = kwargs.get("conversion")
        delete_files = kwargs.get("delete_files")
        self.logging = kwargs.get("log_flag")
        self.sorting = kwargs.get("sorting_order")

        if "/reader#" in  str(manga_url):
            self.single_chapter(comic_url=manga_url, download_directory=download_directory, conversion=conversion,
                                delete_files=delete_files, user_name=user_name, user_password=password)
        else:
            self.full_series(comic_url=manga_url, sorting=self.sorting, download_directory=download_directory,
                             chapter_range=chapter_range, conversion=conversion, delete_files=delete_files,
                             user_name=user_name, user_password=password, manga_language=comic_language)

    def user_login(self, username, password, **kwargs):
        session_cookie = ""

        headers = kwargs.get("headers")
        if not headers:
            headers = {
                'User-Agent':
                    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
                'Accept-Encoding': 'gzip, deflate',
                'referer': 'https://bato.to/'
            }
        print("Getting Auth Token...")
        page_source, update_cookie = globalFunctions.GlobalFunctions().page_downloader(
            manga_url="https://bato.to/forums/index.php?app=core&module=global&section=login")

        soup_parse = page_source.find_all('input', {'type': 'hidden'})
        auth_token = str([x['value'] for x in soup_parse][0]).strip()

        payload = {
            'auth_key': auth_token,
            'ips_username': username,
            'ips_password': password,
            'rememberMe': '1'
        }

        sess = requests.session()
        sess = cfscrape.create_scraper(sess)

        print('Trying To Log In...')
        connection = sess.post("https://bato.to/forums/index.php?app=core&module=global&section=login&do=process",
                               headers=headers, data=payload, cookies=kwargs.get("cookies"))
        if connection.status_code != 200:
            print("Whoops! Seems like I can't connect to website.")
            print("It's showing : %s" % connection)
            print("Run this script with the --verbose argument and report the issue along with log file on Github.")
            sys.exit(1)
        else:
            page_source = BeautifulSoup(connection.text.encode("utf-8"), "html.parser")
            if "logout" in str(page_source):
                print("Successfully Logged In!")
            else:
                print("Couldn't Log You In. Please Check Your Credentials Again!")
            session_cookie = sess.cookies

        return session_cookie

    def name_cleaner(self, scrapped_name):
        return re.sub('[^A-Za-z0-9.\-\+\' ]+', '', ' '.join([str(word).strip().title() for word in str(scrapped_name).split("-")[:-1]]))

    def single_chapter(self, comic_url, download_directory, conversion, delete_files, comic_name=None, user_name=None,
                       user_password=None, **kwargs):
        chapter_id = str(str(comic_url).split("#")[-1]).replace("/", "")
        temp_cookies = kwargs.get("session_cookies")


        if str(user_name) != "None" and str(user_password) != "None":
            print("Trying To Log You In...")
            temp_cookies = self.user_login(username=user_name, password=user_password)

        """next_page denotes whether there will be a next page or not. Basically, it's like a flag to know whether we're
        on the last page or not.
        page_count starts from 0 and will add 1 to it in every iteration, which will in turn give us page number.
        TRULY GENIUS! <3
        """
        comic_name = ""
        chapter_number = ""
        file_directory = ""
        directory_path = ""
        next_page = True
        page_count = 1

        headers = {
            'User-Agent':
                'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate',
            'referer': 'https://bato.to/reader'
        }

        while next_page:
            batoto_reader_url = "https://bato.to/areader?id=" + str(chapter_id) + "&p=" + str(page_count)
            page_source, temp_cookies = globalFunctions.GlobalFunctions().page_downloader(manga_url=batoto_reader_url,
                                                                                          headers=headers,
                                                                                          cookies=temp_cookies)
            if not comic_name or not chapter_number or not file_directory:
                comic_name = self.name_cleaner(re.search(r'https://bato.to/comic/_/comics/(.*?)">', str(page_source)).group(1))
                chapter_number = re.sub('[^0-9]+', '', str(re.search(r'Ch\.(.*?)\:', str(page_source)).group(1)))
                file_directory = str(comic_name) + os.sep + str(chapter_number) + os.sep
                file_directory = file_directory.replace(":", "-")
                directory_path = os.path.realpath(str(download_directory) + os.sep + str(file_directory))

                if not os.path.exists(directory_path):
                    os.makedirs(directory_path)

                globalFunctions.GlobalFunctions().info_printer(comic_name, chapter_number)

            img_link = page_source.find_all("img", {"id": "comic_page"})

            current_image_url = ""

            for x in img_link:
                current_image_url = str(x['src']).strip()

            globalFunctions.GlobalFunctions().downloader(current_image_url, str(page_count) +
                                                         str(current_image_url)[-4:],
                                                         comic_url, directory_path, log_flag=self.logging)
            try:
                page_count = int(str(re.search(r"next_page = '(.*?)';", str(page_source)).group(1)).split("_")[-1])
                next_page = True
            except Exception as LastPage:
                next_page = False
                pass
        globalFunctions.GlobalFunctions().conversion(directory_path, conversion, delete_files,
                                                     comic_name, chapter_number)

    def full_series(self, comic_url, sorting, download_directory, chapter_range, conversion, delete_files,
                    user_name=None, user_password=None, **kwargs):
        all_links = []
        session_cookie = None

        headers = {
            'User-Agent':
                'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate',
            'referer': 'https://bato.to/'
        }
        if str(user_name) != "None" and str(user_password) != "None":
            print("Trying To Log You In...")
            session_cookie = self.user_login(username=user_name, password=user_password)
        else:
            print("You are not logged in. You might not be able to download all the listed chapters from Batoto.")

        print("")

        manga_language = kwargs.get("manga_language")

        page_source, update_cookie = globalFunctions.GlobalFunctions().page_downloader(manga_url=comic_url,
                                                                                       headers=headers,
                                                                                       cookies=session_cookie)

        class_name = "row lang_{0} chapter_row".format(manga_language)

        raw_chapters_table = page_source.find_all('tr', {'class': class_name})
        for table_data in raw_chapters_table:
            x = table_data.findAll('a')
            for a in x:
                if "/reader#" in str(a['href']):
                    all_links.append(str(a['href']).strip())

        if chapter_range != "All":
            # -1 to shift the episode number accordingly to the INDEX of it. List starts from 0 xD!
            starting = int(str(chapter_range).split("-")[0]) - 1

            if (str(chapter_range).split("-")[1]).decode().isdecimal():
                ending = int(str(chapter_range).split("-")[1])
            else:
                ending = len(all_links)

            indexes = [x for x in range(starting, ending)]
            # [::-1] in sub_list in beginning to start this from the 1st episode and at the last,
            # it is to reverse the list again, because I'm reverting it again at the end.
            all_links = [all_links[x] for x in indexes][::-1]
            #if chapter range contains "__EnD__" write new value to config.json
            if chapter_range.split("-")[1] == "__EnD__":
                globalFunctions.GlobalFunctions().saveNewRange(comic_url,len(all_links))
        else:
            all_links = all_links

        if str(sorting).lower() in ['new', 'desc', 'descending', 'latest']:
            for chap_link in all_links:
                self.single_chapter(comic_url=chap_link, download_directory=download_directory, conversion=conversion,
                                    delete_files=delete_files, session_cookies=session_cookie)

        elif str(sorting).lower() in ['old', 'asc', 'ascending', 'oldest', 'a']:
            for chap_link in all_links[::-1]:
                self.single_chapter(comic_url=chap_link, download_directory=download_directory, conversion=conversion,
                                    delete_files=delete_files, session_cookies=session_cookie)

        print("Finished Downloading")
        return 0
