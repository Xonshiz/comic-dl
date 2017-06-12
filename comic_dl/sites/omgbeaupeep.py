#!/usr/bin/env python
# -*- coding: utf-8 -*-

import globalFunctions
import re
import os
import logging


class OmgBeauPeep(object):
    def __init__(self, manga_url, **kwargs):

        current_directory = kwargs.get("current_directory")
        self.logging = kwargs.get("log_flag")
        self.sorting = kwargs.get("sorting_order")
        self.comic_name = self.name_cleaner(manga_url)
        self.single_chapter(manga_url, self.comic_name)

    def name_cleaner(self, url):
        initial_name = str(url).split("/")[4].strip()
        safe_name = re.sub(r"[0-9][a-z][A-Z]\ ", "", str(initial_name))
        manga_name = str(safe_name.title()).replace("_", " ")

        return manga_name

    def single_chapter(self, comic_url, comic_name):
        chapter_number = str(comic_url).split("/")[5].strip()

        source, cookies_main = globalFunctions.GlobalFunctions().page_downloader(manga_url=comic_url)

        last_page_number = int(re.search(r"</select> of (\d+) <a", str(source)).group(1))

        file_directory = str(comic_name) + '/' + str(chapter_number) + "/"

        directory_path = os.path.realpath(file_directory)

        globalFunctions.GlobalFunctions().info_printer(comic_name, chapter_number)

        if not os.path.exists(file_directory):
            os.makedirs(file_directory)

        for x in range(1, last_page_number + 1):
            chapter_url = str(comic_url) + "/" + str(x)
            source_new, cookies_new = globalFunctions.GlobalFunctions().page_downloader(manga_url=chapter_url)
            image_link = "http://www.omgbeaupeep.com/comics/mangas/" + str(
                re.search(r'"mangas/(.*?)"', str(source_new)).group(1)).replace(" ", "%20")
            file_name = "0" + str(x) + ".jpg"
            logging.debug("Chapter Url : %s" % chapter_url)
            logging.debug("Image Link : %s" % image_link)
            globalFunctions.GlobalFunctions().downloader(image_link, file_name, chapter_url, directory_path, log_flag=self.logging)
