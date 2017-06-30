#!/usr/bin/env python
# -*- coding: utf-8 -*-

import globalFunctions
import re
import os
import logging


class ComicNaver(object):
    def __init__(self, manga_url, download_directory, **kwargs):

        current_directory = kwargs.get("current_directory")
        self.logging = kwargs.get("log_flag")
        self.sorting = kwargs.get("sorting_order")
        self.comic_name = self.name_cleaner(manga_url)
        if "list.nhn" in manga_url:
            self.full_series(manga_url, self.comic_name, self.sorting, download_directory)

        elif "detail.nhn" in manga_url:
            self.single_chapter(manga_url, self.comic_name, download_directory)

    def name_cleaner(self, url):
        manga_name = re.search(r"titleId=(\d+)", str(url)).group(1)

        return manga_name

    def single_chapter(self, comic_url, comic_name, download_directory):
        # http: // comic.naver.com / webtoon / detail.nhn?titleId = 654817 & no = 100 & weekday = tue
        chapter_number = re.search(r"no=(\d+)", str(comic_url)).group(1)

        source, cookies = globalFunctions.GlobalFunctions().page_downloader(manga_url=comic_url)

        img_regex = r'http://imgcomic.naver.net/webtoon/\d+/\d+/.+?\.(?:jpg|png|gif|bmp|JPG|PNG|GIF|BMP)'

        image_list = list(re.findall(img_regex, str(source)))
        logging.debug("Image List : %s" % image_list)

        file_directory = str(comic_name) + '/' + str(chapter_number) + "/"

        # directory_path = os.path.realpath(file_directory)
        directory_path = os.path.realpath(str(download_directory) + "/" + str(file_directory))
        print("Directory Path : %s" % str(directory_path))

        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

        globalFunctions.GlobalFunctions().info_printer(comic_name, chapter_number)

        for link in image_list:
            # link = link.replace("\\", "")
            # file_name = str(link).split("/")[-1].strip()
            file_name = "0" + str(image_list.index(link)) + ".jpg"  # 0 for #18 (Leading 0s)
            globalFunctions.GlobalFunctions().downloader(link, file_name, comic_url, directory_path, log_flag=self.logging)

    def full_series(self, comic_url, comic_name, sorting, download_directory, **kwargs):
        source, cookies = globalFunctions.GlobalFunctions().page_downloader(manga_url=comic_url)
        # print(source)

        latest_chapter = re.findall(r"no=(\d+)\&", str(source))[1]

        all_links = []

        for x in range(1, int(latest_chapter) + 1):
            chapter_url = "http://comic.naver.com/webtoon/detail.nhn?titleId=%s&no=%s" % (comic_name, x)
            all_links.append(chapter_url)
        logging.debug("All Links : %s" % all_links)

        if str(sorting).lower() in ['new', 'desc', 'descending', 'latest']:
            for chap_link in all_links:
                self.single_chapter(comic_url=chap_link, comic_name=comic_name, download_directory=download_directory)
        elif str(sorting).lower() in ['old', 'asc', 'ascending', 'oldest', 'a']:
            # print("Running this")
            for chap_link in all_links[::-1]:
                self.single_chapter(comic_url=chap_link, comic_name=comic_name, download_directory=download_directory)

        print("Finished Downloading")
        return 0
