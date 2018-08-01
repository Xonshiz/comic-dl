#!/usr/bin/env python
# -*- coding: utf-8 -*-

import globalFunctions
import re
import os
import logging

from multiprocessing.dummy import Pool as ThreadPool
from functools import partial

class RawSenaManga(object):
    def __init__(self, manga_url, download_directory, chapter_range, **kwargs):
        current_directory = kwargs.get("current_directory")
        conversion = kwargs.get("conversion")
        delete_files = kwargs.get("delete_files")
        self.logging = kwargs.get("log_flag")
        self.sorting = kwargs.get("sorting_order")
        self.comic_name = self.name_cleaner(manga_url)
        url_split = str(manga_url).split("/")

        if len(url_split) is 5:
            self.full_series(comic_url=manga_url, comic_name=self.comic_name, sorting=self.sorting,
                             download_directory=download_directory, chapter_range=chapter_range, conversion=conversion,
                             delete_files=delete_files)
        else:
            self.single_chapter(manga_url, self.comic_name, download_directory, conversion=conversion,
                                delete_files=delete_files)

    def name_cleaner(self, url):
        initial_name = str(url).split("/")[3].strip()
        safe_name = re.sub(r"[0-9][a-z][A-Z]\ ", "", str(initial_name))
        manga_name = str(safe_name.title()).replace("_", " ")

        return manga_name

    def single_chapter(self, comic_url, comic_name, download_directory, conversion, delete_files):
        chapter_number = str(comic_url).split("/")[4].strip()

        source, cookies_main = globalFunctions.GlobalFunctions().page_downloader(manga_url=comic_url)

        image_url = "http://raw.senmanga.com/viewer/" + str(comic_name).replace(" ", "-") + "/" + str(
            chapter_number) + "/"

        page_referer = "http://raw.senmanga.com/" + str(comic_name).replace(" ", "-") + "/" + str(chapter_number) + "/"

        last_page_number = int(str(re.search(r"</select> of (\d+) <a", str(source)).group(1)).strip())

        file_directory = str(comic_name) + '/' + str(chapter_number) + "/"
        file_directory = file_directory.replace(":", "-")
        # directory_path = os.path.realpath(file_directory)
        directory_path = os.path.realpath(str(download_directory) + "/" + str(file_directory))

        globalFunctions.GlobalFunctions().info_printer(comic_name, chapter_number, total_chapters=last_page_number)

        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

        links = []
        file_names = []
        for x in range(0, last_page_number + 1):
            if x is 0:
                pass
            else:
                # file_name = "0" + str(x) + ".jpg"
                # print("File Name : %s" % file_name)
                ddl_image = str(image_url) + str(x)
                referer = str(page_referer) + str(x - 1)
                logging.debug("Image Link : %s" % ddl_image)

                file_name = str(
                    globalFunctions.GlobalFunctions().prepend_zeroes(x, last_page_number + 1)) + ".jpg"
                    
                links.append(ddl_image)
                file_names.append(file_name)
                    
        pool = ThreadPool(4)
        pool.map(partial(globalFunctions.GlobalFunctions().downloader, referer=comic_url, directory_path=directory_path, log_flag=self.logging), zip(links,file_names))

        globalFunctions.GlobalFunctions().conversion(directory_path, conversion, delete_files, comic_name,
                                                     chapter_number)

        return 0

    def full_series(self, comic_url, comic_name, sorting, download_directory, chapter_range, conversion, delete_files):
        series_name_raw = str(comic_url).split("/")[3].strip()
        source, cookies = globalFunctions.GlobalFunctions().page_downloader(manga_url=comic_url)
        # a href="/Flying-Witch-Ishizuka-Chihiro/34/1"
        link_regex = "<td><a href=\"/" + str(series_name_raw) + "/(.*?)\""

        all_links = list(re.findall(link_regex, str(source)))
        logging.debug("All Links : %s" % all_links)

        # Uh, so the logic is that remove all the unnecessary chapters beforehand
        #  and then pass the list for further operations.
        if chapter_range != "All":
            # -1 to shift the episode number accordingly to the INDEX of it. List starts from 0 xD!
            starting = int(str(chapter_range).split("-")[0]) - 1

            if str(chapter_range).split("-")[1].isdigit():
                ending = int(str(chapter_range).split("-")[1])
            else:
                ending = len(all_links)

            indexes = [x for x in range(starting, ending)]

            all_links = [all_links[x] for x in indexes][::-1]
        else:
            all_links = all_links

        if str(sorting).lower() in ['new', 'desc', 'descending', 'latest']:
            for link in all_links:
                chap_link = "http://raw.senmanga.com/" + str(series_name_raw) + "/" + str(
                    link).strip()
                self.single_chapter(comic_url=chap_link, comic_name=comic_name, download_directory=download_directory,
                                    conversion=conversion, delete_files=delete_files)
                # if chapter range contains "__EnD__" write new value to config.json
                if chapter_range != "All" and chapter_range.split("-")[1] == "__EnD__":
                    globalFunctions.GlobalFunctions().addOne(comic_url)

        elif str(sorting).lower() in ['old', 'asc', 'ascending', 'oldest', 'a']:
            for link in all_links[::-1]:
                chap_link = "http://raw.senmanga.com/" + str(series_name_raw) + "/" + str(
                    link).strip()
                self.single_chapter(comic_url=chap_link, comic_name=comic_name, download_directory=download_directory,
                                    conversion=conversion, delete_files=delete_files)
                # if chapter range contains "__EnD__" write new value to config.json
                if chapter_range != "All" and chapter_range.split("-")[1] == "__EnD__":
                    globalFunctions.GlobalFunctions().addOne(comic_url)
