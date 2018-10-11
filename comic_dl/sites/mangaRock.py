#!/usr/bin/env python
# -*- coding: utf-8 -*-

import globalFunctions
import json
import re
import os
import glob

from PIL import Image


class MangaRock():
    def __init__(self, manga_url, download_directory, chapter_range, **kwargs):
        current_directory = kwargs.get("current_directory")
        conversion = kwargs.get("conversion")
        delete_files = kwargs.get("delete_files")
        self.logging = kwargs.get("log_flag")
        self.sorting = kwargs.get("sorting_order")
        self.manga_url = manga_url

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

    @staticmethod
    def file_decryption(path_to_files, conversion):
        """
        A REALLY BIG THANKS TO 'dradzenglor' for decrypting the files! Amazing work!
        Follow The Thread On Reddit : https://www.reddit.com/r/codes/comments/7mdx70/need_help_decrypting_this_string/
        """
        for mri_file in glob.glob(os.path.abspath(path_to_files) + os.sep + "*.mri"):
            data = open(mri_file, "rb").read()

            n = len(data) + 7

            header = [82, 73, 70, 70, 255 & n, n >> 8 & 255, n >> 16 & 255, n >> 24 & 255, 87, 69, 66, 80, 86, 80, 56]

            data = map(lambda x: ord(x) ^ 101, data)

            webp_file = str(mri_file).replace(".mri", ".webp")
            open(webp_file, 'wb').write(''.join(map(chr, header + data)))

            # Let's delete the .mri file
            os.remove(mri_file)

            # if a conversion is asked, convert to jpg,
            # it will be needed in order to use method comic_dl.globalFunctions.GlobalFunctions#conversion
            # will also work with --convert jpg
            jpg_file = str(mri_file).replace(".mri", ".jpg")
            if str(conversion) != "None":
                im = Image.open(webp_file)
                rgb_im = im.convert("RGB")
                rgb_im.save(jpg_file)
                os.remove(webp_file)

    def single_chapter(self, chapter_id, comic_name, chapter_number, download_directory, conversion, delete_files):
        image_api_link = "https://api.mangarockhd.com/query/web400/pages?oid=" + str(chapter_id)
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
        self.file_decryption(path_to_files=directory_path, conversion=conversion) # Calling the method that does the magic!

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

        for single_chapter in chapters_dict:
            self.single_chapter(chapter_id=str(single_chapter), comic_name=comic_name,
                                chapter_number=str(chapters_dict[single_chapter]).strip().title(),
                                download_directory=download_directory, conversion=conversion,
                                delete_files=delete_files)
            if chapter_range != "All" and chapter_range.split("-")[1] == "__EnD__":
                globalFunctions.GlobalFunctions().addOne(self.manga_url)

        return 0
