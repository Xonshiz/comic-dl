#!/usr/bin/env python
# -*- coding: utf-8 -*-

import globalFunctions
import re
import sys
import os
import logging


class FoolSlide(object):
    def __init__(self, manga_url, download_directory, chapter_range, **kwargs):

        current_directory = kwargs.get("current_directory")
        conversion = kwargs.get("conversion")
        delete_files = kwargs.get("delete_files")
        self.logging = kwargs.get("log_flag")
        self.sorting = kwargs.get("sorting_order")

        self.manga_name = self.name_cleaner(manga_url)

        if "/reader/series/" in manga_url:
            self.full_manga(manga_url=manga_url, comic_name=self.manga_name, sorting=self.sorting,
                            download_directory=download_directory, chapter_range=chapter_range, conversion=conversion,
                            delete_files=delete_files)
        elif "/reader/read/" in manga_url:
            self.single_chapter(manga_url, self.manga_name, download_directory, conversion=conversion,
                                delete_files=delete_files)

    def single_chapter(self, chapter_url, comic_name, download_directory, conversion, delete_files):

        chapter_number = str(chapter_url).split("/")[8].strip()

        source, cookies = globalFunctions.GlobalFunctions().page_downloader(manga_url=chapter_url)
        img_links = self.image_links(source)
        logging.debug("Img Links : %s" % img_links)

        file_directory = str(comic_name) + '/' + "Chapter " + str(chapter_number) + "/"
        file_directory = file_directory.replace(":", "-")
        # directory_path = os.path.realpath(file_directory)
        directory_path = os.path.realpath(str(download_directory) + "/" + str(file_directory))

        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

        globalFunctions.GlobalFunctions().info_printer(comic_name, chapter_number, total_chapters=len(img_links))
        print("Img Links : {0}".format(img_links))
        print("LEN Img Links : {0}".format(str(len(img_links))))

        for current_chapter, link in enumerate(img_links):
            new_link = link.replace("\\", "")
            # file_name = str(img_links.index(link)) + ".jpg"
            current_chapter += 1
            file_name = str(globalFunctions.GlobalFunctions().prepend_zeroes(current_chapter, len(img_links))) + ".jpg"
            globalFunctions.GlobalFunctions().downloader(new_link, file_name, chapter_url, directory_path,
                                                         log_flag=self.logging)

        globalFunctions.GlobalFunctions().conversion(directory_path, conversion, delete_files, comic_name,
                                                     chapter_number)

        return 0

    def image_links(self, source_code):

        try:
            source_dict = re.search(r"\= \[(.*?)\]\;", str(source_code)).group(1)

            image_links = re.findall(r"\"url\"\:\"(.*?)\"", str(source_dict))
            # file_names = re.findall(r"\"filename\"\:\"(.*?)\"", str(source_dict))

        except Exception as ImageLinksNotFound:
            print("Links : %s" % ImageLinksNotFound)
            sys.exit()

        return image_links

    def name_cleaner(self, url):
        initial_name = str(url).split("/")[5].strip()
        safe_name = re.sub(r"[0-9][a-z][A-Z]\ ", "", str(initial_name))
        anime_name = str(safe_name.title()).replace("-", " ")

        return anime_name

    def full_manga(self, manga_url, comic_name, sorting, download_directory, chapter_range, conversion, delete_files):
        source, cookies = globalFunctions.GlobalFunctions().page_downloader(manga_url=manga_url)
        # print(source)
        chapter_text = source.findAll('div', {'class': 'title'})
        all_links = []

        for link in chapter_text:
            x = link.findAll('a')
            for a in x:
                url = a['href']
                all_links.append(url)
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
            for chap_link in all_links:
                self.single_chapter(chapter_url=chap_link, comic_name=comic_name, download_directory=download_directory,
                                    conversion=conversion, delete_files=delete_files)
                # if chapter range contains "__EnD__" write new value to config.json
                if chapter_range.split("-")[1] == "__EnD__":
                    globalFunctions.GlobalFunctions().addOne(comic_url)
        elif str(sorting).lower() in ['old', 'asc', 'ascending', 'oldest', 'a']:
            # print("Running this")
            for chap_link in all_links[::-1]:
                self.single_chapter(chapter_url=chap_link, comic_name=comic_name, download_directory=download_directory,
                                    conversion=conversion, delete_files=delete_files)
                # if chapter range contains "__EnD__" write new value to config.json
                if chapter_range.split("-")[1] == "__EnD__":
                    globalFunctions.GlobalFunctions().addOne(comic_url)

        print("Finished Downloading")
        return 0
