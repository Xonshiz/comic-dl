#!/usr/bin/env python
# -*- coding: utf-8 -*-

import globalFunctions
import re
import os
import logging


class RawSenaManga(object):
    def __init__(self, manga_url, **kwargs):
        current_directory = kwargs.get("current_directory")
        self.logging = kwargs.get("log_flag")
        self.sorting = kwargs.get("sorting_order")
        self.comic_name = self.name_cleaner(manga_url)
        url_split = str(manga_url).split("/")

        if len(url_split) is 5:
            self.full_series(comic_url=manga_url, comic_name=self.comic_name, sorting=self.sorting)
        else:
            self.single_chapter(manga_url, self.comic_name)

    def name_cleaner(self, url):
        initial_name = str(url).split("/")[3].strip()
        safe_name = re.sub(r"[0-9][a-z][A-Z]\ ", "", str(initial_name))
        manga_name = str(safe_name.title()).replace("_", " ")

        return manga_name

    def single_chapter(self, comic_url, comic_name):
        chapter_number = str(comic_url).split("/")[4].strip()

        source, cookies_main = globalFunctions.GlobalFunctions().page_downloader(manga_url=comic_url)

        image_url = "http://raw.senmanga.com/viewer/" + str(comic_name).replace(" ", "-") + "/" + str(
            chapter_number) + "/"

        page_referer = "http://raw.senmanga.com/" + str(comic_name).replace(" ", "-") + "/" + str(chapter_number) + "/"

        last_page_number = int(str(re.search(r"</select> of (\d+) <a", str(source)).group(1)).strip())

        file_directory = str(comic_name) + '/' + str(chapter_number) + "/"

        directory_path = os.path.realpath(file_directory)

        globalFunctions.GlobalFunctions().info_printer(comic_name, chapter_number)

        if not os.path.exists(file_directory):
            os.makedirs(file_directory)

        for x in range(0, last_page_number + 1):
            if x is 0:
                pass
            else:
                file_name = "0" + str(x) + ".jpg"
                # print("File Name : %s" % file_name)
                ddl_image = str(image_url) + str(x)
                referer = str(page_referer) + str(x - 1)
                logging.debug("Image Link : %s" % ddl_image)
                globalFunctions.GlobalFunctions().downloader(ddl_image, file_name, referer, directory_path,
                                                             cookies=cookies_main, log_flag=self.logging)
        return 0

    def full_series(self, comic_url, comic_name, sorting, **kwargs):
        series_name_raw = str(comic_url).split("/")[3].strip()
        source, cookies = globalFunctions.GlobalFunctions().page_downloader(manga_url=comic_url)
        # a href="/Flying-Witch-Ishizuka-Chihiro/34/1"
        link_regex = "<td><a href=\"/" + str(series_name_raw) + "/(.*?)\""

        all_links = list(re.findall(link_regex, str(source)))
        logging.debug("All Links : %s" % all_links)

        if str(sorting).lower() in ['new', 'desc', 'descending', 'latest']:
            for link in all_links:
                chap_link = "http://raw.senmanga.com/" + str(series_name_raw) + "/" + str(
                    link).strip()
                self.single_chapter(comic_url=chap_link, comic_name=comic_name)

        elif str(sorting).lower() in ['old', 'asc', 'ascending', 'oldest', 'a']:
            for link in all_links[::-1]:
                chap_link = "http://raw.senmanga.com/" + str(series_name_raw) + "/" + str(
                    link).strip()
                self.single_chapter(comic_url=chap_link, comic_name=comic_name)
