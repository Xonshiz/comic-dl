#!/usr/bin/env python
# -*- coding: utf-8 -*-

import globalFunctions
import re
import os
import logging


class ComicNaver(object):
    def __init__(self, manga_url, download_directory, chapter_range, **kwargs):

        current_directory = kwargs.get("current_directory")
        conversion = kwargs.get("conversion")
        keep_files = kwargs.get("keep_files")
        self.logging = kwargs.get("log_flag")
        self.sorting = kwargs.get("sorting_order")
        self.comic_name = self.name_cleaner(manga_url)
        self.print_index = kwargs.get("print_index")
        if "list.nhn" in manga_url:
            self.full_series(manga_url, self.comic_name, self.sorting, download_directory, chapter_range=chapter_range,
                             conversion=conversion, keep_files=keep_files)

        elif "detail.nhn" in manga_url:
            self.single_chapter(manga_url, self.comic_name, download_directory, conversion=conversion,
                                keep_files=keep_files)

    def name_cleaner(self, url):
        manga_name = re.search(r"titleId=(\d+)", str(url)).group(1)

        return manga_name

    def single_chapter(self, comic_url, comic_name, download_directory, conversion, keep_files):
        # http: // comic.naver.com / webtoon / detail.nhn?titleId = 654817 & no = 100 & weekday = tue
        chapter_number = re.search(r"no=(\d+)", str(comic_url)).group(1)

        source, cookies = globalFunctions.GlobalFunctions().page_downloader(manga_url=comic_url)
        # https://image-comic.pstatic.net/webtoon/183559/399/20180810173548_ffbf217190f59dc04bd6fc538e11d64b_IMAG01_1.jpg
        img_regex = r'https?://(?:imgcomic\.naver\.net|image-comic\.pstatic\.net)/webtoon/\d+/\d+/.+?\.(?:jpg|png|gif|bmp|JPG|PNG|GIF|BMP)'
        image_list = list(re.findall(img_regex, str(source)))
        logging.debug("Image List : %s" % image_list)

        file_directory = globalFunctions.GlobalFunctions().create_file_directory(chapter_number, comic_name)
        # directory_path = os.path.realpath(file_directory)
        directory_path = os.path.realpath(str(download_directory) + "/" + str(file_directory))
        print("Directory Path : %s" % str(directory_path))

        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

        links = []
        file_names = []
        for current_chapter, image_link in enumerate(image_list):
            current_chapter += 1

            # Fix for #18
            file_name = str(globalFunctions.GlobalFunctions().prepend_zeroes(current_chapter, len(image_list))) + ".jpg"

            file_names.append(file_name)
            links.append(image_link)

        globalFunctions.GlobalFunctions().multithread_download(chapter_number, comic_name, comic_url, directory_path,
                                                               file_names, links, self.logging)
            
        globalFunctions.GlobalFunctions().conversion(directory_path, conversion, keep_files, comic_name,
                                                     chapter_number)

        return 0

    def full_series(self, comic_url, comic_name, sorting, download_directory, chapter_range, conversion, keep_files):
        source, cookies = globalFunctions.GlobalFunctions().page_downloader(manga_url=comic_url)
        # print(source)

        latest_chapter = re.findall(r"no=(\d+)\&", str(source))[1]

        all_links = []

        for x in range(1, int(latest_chapter) + 1):
            chapter_url = "http://comic.naver.com/webtoon/detail.nhn?titleId=%s&no=%s" % (comic_name, x)
            all_links.append(chapter_url)
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

        if self.print_index:
            idx = 0
            for chap_link in all_links:
                idx = idx + 1
                print(str(idx) + ": " + chap_link)
            return

        if str(sorting).lower() in ['new', 'desc', 'descending', 'latest']:
            for chap_link in all_links:
                self.single_chapter(comic_url=chap_link, comic_name=comic_name, download_directory=download_directory,
                                    conversion=conversion, keep_files=keep_files)
                # if chapter range contains "__EnD__" write new value to config.json
                if chapter_range != "All" and chapter_range.split("-")[1] == "__EnD__":
                    globalFunctions.GlobalFunctions().addOne(comic_url)
        elif str(sorting).lower() in ['old', 'asc', 'ascending', 'oldest', 'a']:
            # print("Running this")
            for chap_link in all_links[::-1]:
                self.single_chapter(comic_url=chap_link, comic_name=comic_name, download_directory=download_directory,
                                    conversion=conversion, keep_files=keep_files)
                # if chapter range contains "__EnD__" write new value to config.json
                if chapter_range != "All" and chapter_range.split("-")[1] == "__EnD__":
                    globalFunctions.GlobalFunctions().addOne(comic_url)

        return 0
