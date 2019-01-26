#!/usr/bin/env python
# -*- coding: utf-8 -*-

import globalFunctions
import re
import os
import logging


class OmgBeauPeep(object):
    def __init__(self, manga_url, download_directory, chapter_range, **kwargs):

        current_directory = kwargs.get("current_directory")
        conversion = kwargs.get("conversion")
        keep_files = kwargs.get("keep_files")
        self.logging = kwargs.get("log_flag")
        self.sorting = kwargs.get("sorting_order")
        self.comic_name = self.name_cleaner(manga_url)
        self.print_index = kwargs.get("print_index")

        splitter = list(str(manga_url).split("/"))

        # Since this website doesn't seem to have a dedicated page for series, I need to make a function just for the sake of range, huh. *sigh*
        # You need to pass the ABSOLUTE chapter number for this website though. Otherwise, it'll generate wrong links to chapter and won't download anything.
        # Please spare me such hard work.
        if chapter_range != "All":
            self.range_maker(manga_url=manga_url, chapter_range=chapter_range, download_directory=download_directory,
                             conversion=conversion, keep_files=keep_files)
        elif len(splitter) <= 5:
            self.full_series(manga_url, self.comic_name, download_directory, conversion=conversion,
                                keep_files=keep_files)
        else:
            self.single_chapter(manga_url, self.comic_name, download_directory, conversion=conversion,
                                keep_files=keep_files)

    def name_cleaner(self, url):
        initial_name = str(url).split("/")[4].strip()
        safe_name = re.sub(r"[0-9][a-z][A-Z]\ ", "", str(initial_name))
        manga_name = str(safe_name.title()).replace("_", " ")

        return manga_name

    def single_chapter(self, comic_url, comic_name, download_directory, conversion, keep_files):
        chapter_number = str(comic_url).split("/")[5].strip()

        source, cookies_main = globalFunctions.GlobalFunctions().page_downloader(manga_url=comic_url)

        last_page_number = int(re.search(r"</select> of (\d+) <a", str(source)).group(1))

        file_directory = globalFunctions.GlobalFunctions().create_file_directory(chapter_number, comic_name)
        # directory_path = os.path.realpath(file_directory)
        directory_path = os.path.realpath(str(download_directory) + "/" + str(file_directory))

        if self.print_index:
            for x in xrange(1, last_page_number + 1):
                print(str(x) + ": " + str(comic_url) + "/" + str(x))
            return

        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

        links = []
        file_names = []
        for x in range(1, last_page_number + 1):
            chapter_url = str(comic_url) + "/" + str(x)
            image_prefix = "http://www.omgbeaupeep.com/comics/mangas/"
            if "otakusmash" in comic_url:
                image_prefix = "https://www.otakusmash.com/read-comics/mangas/"
            source_new, cookies_new = globalFunctions.GlobalFunctions().page_downloader(manga_url=chapter_url)
            image_link = image_prefix + str(
                re.search(r'"mangas/(.*?)"', str(source_new)).group(1)).replace(" ", "%20")
            # file_name = "0" + str(x) + ".jpg"
            logging.debug("Chapter Url : %s" % chapter_url)
            logging.debug("Image Link : %s" % image_link)
            file_name = str(globalFunctions.GlobalFunctions().prepend_zeroes(x, last_page_number + 1)) + ".jpg"

            links.append(image_link)
            file_names.append(file_name)

        globalFunctions.GlobalFunctions().multithread_download(chapter_number, comic_name, comic_url, directory_path,
                                                               file_names, links, self.logging)

        globalFunctions.GlobalFunctions().conversion(directory_path, conversion, keep_files, comic_name,
                                                     chapter_number)

        return 0

    def range_maker(self, manga_url, chapter_range, download_directory, conversion, keep_files):
        starting = int(str(chapter_range).split("-")[0])
        ending = int(str(chapter_range).split("-")[1])
        for comic_chapter in range(starting, ending):
            chapter_number = str(manga_url).split("/")[5].strip()
            # Dirty Hack, 'cause I'm a HackerMan! (Dumb Joke)
            new_url = str(manga_url).replace(str(chapter_number), str(comic_chapter))
            self.single_chapter(new_url, self.comic_name, download_directory, conversion=conversion,
                                keep_files=keep_files)

    def full_series(self, manga_url, comic_name, download_directory, conversion, keep_files):
        source, cookies = globalFunctions.GlobalFunctions().page_downloader(manga_url=manga_url)
        chapters = source.findAll('select', {'name': 'chapter'})[0]
        bypass_first = "otakusmash" in manga_url
        for option in chapters.findAll('option'):
            if self.print_index:
                print('{}: {}'.format(option['value'], option.text))
            else:
                if bypass_first:  # Because this website lists the next chapter, which is NOT available.
                    bypass_first = False
                    continue
                try:
                    self.single_chapter(manga_url + "/" + str(option['value']), comic_name, download_directory, conversion=conversion,
                                    keep_files=keep_files)
                except Exception as ex:
                    logging.error("Error downloading : %s" % str(option['value']))
                    break  # break to continue processing other mangas
