#!/usr/bin/env python
# -*- coding: utf-8 -*-

import globalFunctions
import json
import re
import os
import glob


class MangaRock():
    def __init__(self, manga_url, download_directory, chapter_range, **kwargs):
        current_directory = kwargs.get("current_directory")
        conversion = kwargs.get("conversion")
        keep_files = kwargs.get("keep_files")
        self.logging = kwargs.get("log_flag")
        self.sorting = kwargs.get("sorting_order")
        self.manga_url = manga_url
        self.print_index = kwargs.get("print_index")

        if len(str(manga_url).split("/")) is 5:
            self.comic_id = str(str(manga_url).split("/")[-1])
            self.full_series(comic_id=self.comic_id, sorting=self.sorting,
                             download_directory=download_directory, chapter_range=chapter_range, conversion=conversion,
                             keep_files=keep_files)
        else:
            self.chapter_id = str(str(manga_url).split("/")[-1])
            self.comic_name, self.chapter_number = self.name_cleaner(url=manga_url, chapter_id=self.chapter_id)
            self.single_chapter(chapter_id=self.chapter_id, comic_name=self.comic_name, chapter_number=self.chapter_number,
                                download_directory=download_directory, conversion=conversion, keep_files=keep_files)

    def name_cleaner(self, url, chapter_id):
        print("Fetching The Chapter Data...")
        info_json_url = "https://api.mangarockhd.com/query/web401/info?oid=" + str(str(url).split("/")[4])

        source, cookies = globalFunctions.GlobalFunctions().page_downloader(manga_url=info_json_url)
        json_parse = json.loads(str(source))
        comic_name = str(json_parse["data"]["name"])
        chapter_number_value = ""

        print("")

        for chapter_number in json_parse["data"]["chapters"]:
            if str(chapter_id) in str(chapter_number.values()):
                chapter_number_value = chapter_number["name"]
            else:
                pass
        return comic_name, re.sub('[^A-Za-z0-9.\-\+\' ]+', '', chapter_number_value.replace(":", " -"))

    def file_decryption(self, path_to_files):
        """
        A REALLY BIG THANKS TO 'dradzenglor' for decrypting the files! Amazing work!
        Follow The Thread On Reddit : https://www.reddit.com/r/codes/comments/7mdx70/need_help_decrypting_this_string/
        """
        for mri_file in glob.glob(os.path.abspath(path_to_files) + os.sep + "*.mri"):
            data = open(mri_file, "rb").read()

            n = len(data) + 7

            header = [82, 73, 70, 70, 255 & n, n >> 8 & 255, n >> 16 & 255, n >> 24 & 255, 87, 69, 66, 80, 86, 80, 56]
            data = [x ^ 101 for x in data]

            open(str(mri_file).replace(".mri", ".jpg"), 'wb').write(bytes(header + data))

            # Let's delete the .mri file
            os.remove(mri_file)

    def single_chapter(self, chapter_id, comic_name, chapter_number, download_directory, conversion, keep_files):
        image_api_link = "https://api.mangarockhd.com/query/web401/pages?oid=" + str(chapter_id)
        source, cookies = globalFunctions.GlobalFunctions().page_downloader(manga_url=image_api_link)
        json_parse = json.loads(str(source))

        file_directory = globalFunctions.GlobalFunctions().create_file_directory(chapter_number, comic_name)

        directory_path = os.path.realpath(str(download_directory) + os.sep + str(file_directory))

        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

        links = []
        file_names = []
        for current_chapter, image_link in enumerate(json_parse["data"]):
            # file_name = str(json_parse["data"].index(image_link)) + ".mri"
            current_chapter += 1
            file_name = str(globalFunctions.GlobalFunctions().prepend_zeroes(current_chapter, len(json_parse["data"]))) + ".mri"
   
            file_names.append(file_name)
            links.append(image_link)

        globalFunctions.GlobalFunctions().multithread_download(chapter_number, comic_name, None, directory_path,
                                                               file_names, links, self.logging)
            
        print("Decrypting Files...")
        self.file_decryption(path_to_files=directory_path) # Calling the method that does the magic!

        globalFunctions.GlobalFunctions().conversion(directory_path, conversion, keep_files, comic_name,
                                                     chapter_number)

        return 0

    def full_series(self, comic_id, sorting, download_directory, chapter_range, conversion, keep_files):
        chapters_dict = {}
        api_url = "https://api.mangarockhd.com/query/web401/info?oid=" + str(comic_id)

        source, cookies = globalFunctions.GlobalFunctions().page_downloader(manga_url=api_url)
        json_parse = json.loads(str(source))
        comic_name = str(json_parse["data"]["name"])

        if chapter_range != "All":
            # -1 to shift the episode number accordingly to the INDEX of it. List starts from 0 xD!
            starting = int(str(chapter_range).split("-")[0])
            total_chapters = int(json_parse["data"]["total_chapters"])
            if str(chapter_range).split("-")[1].isdigit():
                ending = int(str(chapter_range).split("-")[1])
            else:
                ending = total_chapters

            if ending > total_chapters:
                ending = total_chapters

            for range_value in range(starting, ending + 1):
                chapters_dict[str(json_parse["data"]["chapters"][int(range_value) - 1]["oid"])] = re.sub('[^A-Za-z0-9.\-\+\' ]+', '', json_parse["data"]["chapters"][int(range_value) - 1]["name"].replace(":", " -"))
        else:
            for chapter in json_parse["data"]["chapters"]:
                chapters_dict[str(chapter["oid"])] = re.sub('[^A-Za-z0-9.\-\+\' ]+', '', chapter["name"].replace(":", " -"))

        if self.print_index:
            chapters_ = json_parse["data"]["chapters"]
            for chapter in chapters_:
                print(str(chapter["order"] + 1) + ": " + chapter["name"].encode('utf-8'))
            return

        for single_chapter in chapters_dict:
            try:
                self.single_chapter(chapter_id=str(single_chapter), comic_name=comic_name,
                                    chapter_number=str(chapters_dict[single_chapter]).strip().title(),
                                    download_directory=download_directory, conversion=conversion,
                                    keep_files=keep_files)
            except Exception as ex:
                break  # break to continue processing other mangas
                # @Chr1st-oo - modified condition due to some changes on automatic download and config.
                if chapter_range != "All" and (chapter_range.split("-")[1] == "__EnD__" or len(chapter_range.split("-")) == 3):
                    globalFunctions.GlobalFunctions().addOne(self.manga_url)

        return 0
