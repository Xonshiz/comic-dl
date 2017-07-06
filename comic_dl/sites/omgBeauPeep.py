#!/usr/bin/env python
# -*- coding: utf-8 -*-

import globalFunctions
import re
import os
import logging


class OmgBeauPeep(object):
    def __init__(self, manga_url, download_directory, chapter_range, **kwargs):

        current_directory = kwargs.get("current_directory")
        self.logging = kwargs.get("log_flag")
        self.sorting = kwargs.get("sorting_order")
        self.comic_name = self.name_cleaner(manga_url)

        # Since this website doesn't seem to have a dedicated page for series, I need to make a function just for the sake of range, huh. *sigh*
        # You need to pass the ABSOLUTE chapter number for this website though. Otherwise, it'll generate wrong links to chapter and won't download anything.
        # Please spare me such hard work.
        if chapter_range != "All":
            self.range_maker(manga_url=manga_url, chapter_range=chapter_range, download_directory=download_directory)
        else:
            self.single_chapter(manga_url, self.comic_name, download_directory)

    def name_cleaner(self, url):
        initial_name = str(url).split("/")[4].strip()
        safe_name = re.sub(r"[0-9][a-z][A-Z]\ ", "", str(initial_name))
        manga_name = str(safe_name.title()).replace("_", " ")

        return manga_name

    def single_chapter(self, comic_url, comic_name, download_directory):
        chapter_number = str(comic_url).split("/")[5].strip()

        source, cookies_main = globalFunctions.GlobalFunctions().page_downloader(manga_url=comic_url)

        last_page_number = int(re.search(r"</select> of (\d+) <a", str(source)).group(1))

        file_directory = str(comic_name) + '/' + str(chapter_number) + "/"

        # directory_path = os.path.realpath(file_directory)
        directory_path = os.path.realpath(str(download_directory) + "/" + str(file_directory))

        globalFunctions.GlobalFunctions().info_printer(comic_name, chapter_number)

        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

        for x in range(1, last_page_number + 1):
            chapter_url = str(comic_url) + "/" + str(x)
            source_new, cookies_new = globalFunctions.GlobalFunctions().page_downloader(manga_url=chapter_url)
            image_link = "http://www.omgbeaupeep.com/comics/mangas/" + str(
                re.search(r'"mangas/(.*?)"', str(source_new)).group(1)).replace(" ", "%20")
            file_name = "0" + str(x) + ".jpg"
            logging.debug("Chapter Url : %s" % chapter_url)
            logging.debug("Image Link : %s" % image_link)
            globalFunctions.GlobalFunctions().downloader(image_link, file_name, chapter_url, directory_path, log_flag=self.logging)

    def range_maker(self, manga_url, chapter_range, download_directory):
        starting = int(str(chapter_range).split("-")[0])
        ending = int(str(chapter_range).split("-")[1])
        for comic_chapter in range(starting, ending):
            chapter_number = str(manga_url).split("/")[5].strip()
            # Dirty Hack, 'cause I'm a HackerMan! (Dumb Joke)
            new_url = str(manga_url).replace(str(chapter_number), str(comic_chapter))
            self.single_chapter(new_url, self.comic_name, download_directory)