#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cfscrape
import requests
import json
import sys
import os
import globalFunctions


class MangaChapterDownload():
    def __init__(self, page_id, download_directory, **kwargs):
        self.page_id = str(page_id).strip()
        self.manga_name = str(kwargs.get("manga_name"))
        self.chapter_number = str(kwargs.get("chapter_number"))

        self.logging = kwargs.get("log_flag")
        self.conversion = kwargs.get("conversion")
        self.delete_files = kwargs.get("delete_files")

        self.json_content = self.json_download(page_id=self.page_id)
        self.image_links = self.link_lookup(json_source=self.json_content)

        if self.manga_name == "" or self.chapter_number == "":
            try:
                self.manga_name = raw_input("Please Enter Manga Name : ")
                self.chapter_number = raw_input("Please Enter Chapter Number : ")
            except Exception as WrongInputType:
                # If python3, then raw_input() won't work.
                self.manga_name = input("Please Enter Manga Name : ")
                self.chapter_number = input("Please Enter Chapter Number : ")
        else:
            pass

        file_directory = str(self.manga_name) + '/' + str(self.chapter_number) + "/"

        directory_path = os.path.realpath(str(download_directory) + "/" + str(file_directory))

        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

        globalFunctions.GlobalFunctions().info_printer(self.manga_name, self.chapter_number)

        for image in self.image_links:
            file_name = str(image) + str(self.image_links[image][-4:])
            file_name_number = file_name.split(".")[0]
            file_name_ext = file_name.split(".")[1]
            file_name = str(globalFunctions.GlobalFunctions().prepend_zeroes(file_name_number, len(
                self.image_links))) + "." + file_name_ext
            globalFunctions.GlobalFunctions().downloader(image_ddl=self.image_links[image],
                                                         file_name=file_name,
                                                         referer=None, directory_path=directory_path,
                                                         log_flag=self.logging)
        globalFunctions.GlobalFunctions().conversion(directory_path, self.conversion, self.delete_files,
                                                     self.manga_name, self.chapter_number)



    def json_download(self, page_id):
        headers = {
            'User-Agent':
                'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate'
        }

        sess = requests.session()
        sess = cfscrape.create_scraper(sess)

        search_url = "http://www.mangaeden.com/api/chapter/{0}/".format(page_id)

        connection = sess.get(search_url, headers=headers)
        if connection.status_code != 200:
            print("Whoops! Seems like I can't connect to website.")
            print("It's showing : %s" % connection)
            print("Run this script with the --verbose argument and report the issue along with log file on Github.")
            sys.exit(1)
        else:
            json_data = connection.content

            return json_data

    def link_lookup(self, json_source):
        image_links = {}

        """ the images's urls and sizes of the chapter are received via this API
        """
        page_json = json.loads(json_source)
        # print(page_json["images"])
        list_of_pages = list(page_json["images"])

        for page in list_of_pages:
            # print(page)
            image_links[page[0]] = "https://cdn.mangaeden.com/mangasimg/" + str(page[1])

        # Let's sort this dictionary based on the chapter count (KEYS).
        sorted(image_links.items(), key=lambda s: s[0])

        if image_links:
            return image_links
        else:
            return None
