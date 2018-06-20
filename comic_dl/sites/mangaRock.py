#!/usr/bin/env python
# -*- coding: utf-8 -*-

import globalFunctions
import json
import re
import os
import glob

from multiprocessing.dummy import Pool as ThreadPool 
from functools import partial

class MangaRock():
    def __init__(self, manga_url, download_directory, chapter_range, **kwargs):
        current_directory = kwargs.get("current_directory")
        conversion = kwargs.get("conversion")
        delete_files = kwargs.get("delete_files")
        self.logging = kwargs.get("log_flag")
        self.sorting = kwargs.get("sorting_order")

        if len(str(manga_url).split("/")) is 5:
            self.comic_id = str(str(manga_url).split("/")[-1])
            self.full_series(comic_id=self.comic_id, sorting=self.sorting,
                             download_directory=download_directory, chapter_range=chapter_range, conversion=conversion,
                             delete_files=delete_files)
        else:
            self.chapter_id = str(str(manga_url).split("/")[-1])
            self.comic_name, self.chapter_number = self.name_cleaner(url=manga_url, chapter_id=self.chapter_id)
            self.single_chapter(chapter_id=self.chapter_id, comic_name=self.comic_name, chapter_number=self.chapter_number,
                                download_directory=download_directory, conversion=conversion, delete_files=delete_files)


    def name_cleaner(self, url, chapter_id):
        print("Fetching The Chapter Data...")
        info_json_url = "https://api.mangarockhd.com/query/web400/info?oid=" + str(str(url).split("/")[4])

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

            data = map(lambda x: ord(x) ^ 101, data)

            open(str(mri_file).replace(".mri", ".jpg"), 'wb').write(''.join(map(chr, header + data)))

            # Let's delete the .mri file
            os.remove(mri_file)

    def single_chapter(self, chapter_id, comic_name, chapter_number, download_directory, conversion, delete_files):
        image_api_link = "https://api.mangarockhd.com/query/web400/pages?oid=" + str(chapter_id)
        source, cookies = globalFunctions.GlobalFunctions().page_downloader(manga_url=image_api_link)
        json_parse = json.loads(str(source))

        file_directory = str(comic_name) + os.sep + str(chapter_number) + os.sep
        file_directory = file_directory.replace(":", "-")

        directory_path = os.path.realpath(str(download_directory) + os.sep + str(file_directory))

        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

        globalFunctions.GlobalFunctions().info_printer(comic_name, chapter_number, total_chapters=len(json_parse["data"]))

        links = []
        file_names = []
        for current_chapter, image_link in enumerate(json_parse["data"]):
            # file_name = str(json_parse["data"].index(image_link)) + ".mri"
            current_chapter += 1
            file_name = str(globalFunctions.GlobalFunctions().prepend_zeroes(current_chapter, len(json_parse["data"]))) + ".mri"
   
            file_names.append(file_name)
            links.append(image_link)

        pool = ThreadPool(4)
        pool.map(partial(globalFunctions.GlobalFunctions().downloader, referer=None, directory_path=directory_path), zip(links,file_names))
            
        print("Decrypting Files...")
        self.file_decryption(path_to_files=directory_path) # Calling the method that does the magic!

        globalFunctions.GlobalFunctions().conversion(directory_path, conversion, delete_files, comic_name,
                                                     chapter_number)

        return 0

    def full_series(self, comic_id, sorting, download_directory, chapter_range, conversion, delete_files):
        chapters_dict = {}
        api_url = "https://api.mangarockhd.com/query/web400/info?oid=" + str(comic_id)

        source, cookies = globalFunctions.GlobalFunctions().page_downloader(manga_url=api_url)
        json_parse = json.loads(str(source))
        comic_name = str(json_parse["data"]["name"])

        if chapter_range != "All":
            # -1 to shift the episode number accordingly to the INDEX of it. List starts from 0 xD!
            starting = int(str(chapter_range).split("-")[0])

            if str(chapter_range).split("-")[1].isdigit():
                ending = int(str(chapter_range).split("-")[1])
            else:
                ending = str(json_parse["data"]["total_chapters"])

            for range_value in range(starting, ending + 1):
                chapters_dict[str(json_parse["data"]["chapters"][int(range_value)]["oid"])] = re.sub('[^A-Za-z0-9.\-\+\' ]+', '', json_parse["data"]["chapters"][int(range_value)]["name"].replace(":", " -"))
        else:
            for chapter in json_parse["data"]["chapters"]:
                chapters_dict[str(chapter["oid"])] = re.sub('[^A-Za-z0-9.\-\+\' ]+', '', chapter["name"].replace(":", " -"))

        for single_chapter in chapters_dict:
            self.single_chapter(chapter_id=str(single_chapter), comic_name=comic_name,
                                chapter_number=str(chapters_dict[single_chapter]).strip().title(),
                                download_directory=download_directory, conversion=conversion,
                                delete_files=delete_files)

        print("Finished Downloading")
        return 0
