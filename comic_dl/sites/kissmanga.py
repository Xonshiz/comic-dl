#!/usr/bin/env python
# -*- coding: utf-8 -*-

import globalFunctions
import re
import os


class KissManga(object):
    def __init__(self, manga_url, download_directory, **kwargs):
        print("Currently Under Development")
        # current_directory = kwargs.get("current_directory")
        # self.logging = kwargs.get("logger")
        # self.sorting = kwargs.get("sorting_order")
        # self.comic_name = self.name_cleaner(manga_url)
        # self.single_chapter(manga_url, self.comic_name)

    def name_cleaner(self, url):
        initial_name = re.search(r"/Manga/(.*?)/", str(url)).group(1)
        # initial_name = str(url).split("/")[4].strip()
        safe_name = re.sub(r"[0-9][a-z][A-Z]\ ", "", str(initial_name))
        anime_name = str(safe_name.title()).replace("-", " ")

        return anime_name

    def single_chapter(self, comic_url, comic_name, download_directory):
        chapter_number = re.search("(\d+)", str(comic_url)).group(1)
        # print(chapter_number)

        source, cookies = globalFunctions.GlobalFunctions().page_downloader(manga_url=comic_url)
        # print(source)
        image_list = re.findall(r"lstImages\.push\(wrapKA\(\"(.*?)\"\)\);", str(source))
        #
        file_directory = str(comic_name) + '/' + str(chapter_number) + "/"
        file_directory = file_directory.replace(":", "-")
        directory_path = os.path.realpath(file_directory)

        if not os.path.exists(file_directory):
            os.makedirs(file_directory)

        globalFunctions.GlobalFunctions().info_printer(comic_name, chapter_number)
        print(image_list)

        links = []
        file_names = []
        for link in image_list:
            link_edited = "http://2.bp.blogspot.com/" + link.replace("\\", "") + ".png"
            print(link_edited)
            # file_name = str(link).split("/")[-1].strip()
            file_name = str(image_list.index(link)) + ".jpg"
            print(file_name)
            
            file_names.append(file_name)
            links.append(link_edited)

        globalFunctions.GlobalFunctions().multithread_download(chapter_number, comic_name, comic_url, directory_path,
                                                               file_names, links)
        # globalFunctions.GlobalFunctions().multithread_download(chapter_number, comic_name, comic_url, directory_path,
        #                                                        file_names, links, self.logging)

        return 0
