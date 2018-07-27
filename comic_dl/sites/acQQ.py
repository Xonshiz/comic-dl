#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import globalFunctions
import json
import os
import logging


from multiprocessing.dummy import Pool as ThreadPool 
from functools import partial

"""A HUGE thanks to @abcfy2 for his amazing implementation of the ac.qq.com APIs.
Original code for ac.qq.com : https://github.com/abcfy2/getComic/
"""


class AcQq(object):
    def __init__(self, manga_url, download_directory, chapter_range, **kwargs):
        current_directory = kwargs.get("current_directory")
        conversion = kwargs.get("conversion")
        delete_files = kwargs.get("delete_files")
        self.logging = kwargs.get("log_flag")
        self.sorting = kwargs.get("sorting_order")
        self.comic_name = self.name_cleaner(manga_url)
        if "/index/" in str(manga_url):
            self.single_chapter(manga_url, self.comic_name, download_directory, conversion=conversion,
                                delete_files=delete_files)
        else:
            self.full_series(comic_url=manga_url, comic_name=self.comic_name, sorting=self.sorting,
                             download_directory=download_directory, chapter_range=chapter_range, conversion=conversion,
                             delete_files=delete_files)

    def name_cleaner(self, url):
        initial_name = re.search(r"id/(\d+)", str(url)).group(1)
        safe_name = re.sub(r"[0-9][a-z][A-Z]\ ", "", str(initial_name))
        manga_name = str(safe_name.title()).replace("_", " ")

        return manga_name

    def single_chapter(self, comic_url, comic_name, download_directory, conversion, delete_files):
        chapter_number = re.search(r"cid/(\d+)", str(comic_url)).group(1)

        source, cookies_main = globalFunctions.GlobalFunctions().page_downloader(manga_url=comic_url)

        base64data = re.findall(r"DATA\s*=\s*'(.+?)'", str(source))[0][1:]
        logging.debug("base64data : %s" % base64data)
        # print(base64data)
        # import sys
        # sys.exit()

        img_detail_json = json.loads(self.__decode_base64_data(base64data))
        logging.debug("img_detail_json : %s" % img_detail_json)

        img_list = []
        for img_url in img_detail_json.get('picture'):
            img_list.append(img_url['url'])
        logging.debug("img_list : %s" % img_list)

        file_directory = str(comic_name) + '/' + str(chapter_number) + "/"
        file_directory = file_directory.replace(":", "-")

        # directory_path = os.path.realpath(file_directory)
        directory_path = os.path.realpath(str(download_directory) + "/" + str(file_directory))

        globalFunctions.GlobalFunctions().info_printer(comic_name, chapter_number, total_chapters=len(img_list))

        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

        # for num, image_link in enumerate(img_list):
        #     print(num)
        links = []
        file_names = []
        for current_chapter, image_link in enumerate(img_list):
            # file_name = "0" + str(img_list.index(image_link)) + "." + str(image_link).split(".")[-1]
            # file_name = str(current_chapter) + '.' + str(image_link).split(".")[-1]
            current_chapter += 1
            file_name = str(globalFunctions.GlobalFunctions().prepend_zeroes(current_chapter, len(img_list))) + ".jpg"
            logging.debug("image_link : %s" % image_link)

            file_names.append(file_name)
            links.append(image_link)

        pool = ThreadPool(4)
        pool.map(partial(globalFunctions.GlobalFunctions().downloader, referer=comic_url, directory_path=directory_path), zip(links,file_names))
            
        globalFunctions.GlobalFunctions().conversion(directory_path, conversion, delete_files, comic_name,
                                                     chapter_number)

        return 0

    def full_series(self, comic_url, comic_name, sorting, download_directory, chapter_range, conversion, delete_files):
        chapter_list = "http://m.ac.qq.com/GetData/getChapterList?id=" + str(comic_name)
        source, cookies = globalFunctions.GlobalFunctions().page_downloader(manga_url=chapter_list)
        content_json = json.loads(str(source))
        logging.debug("content_json : %s" % content_json)
        last = int(content_json['last'])
        first = int(content_json['first'])
        logging.debug("first : %s" % first)
        logging.debug("last : %s" % last)

        all_links = []

        for chapter_number in range(first, last + 1):
            "http://ac.qq.com/ComicView/index/id/538359/cid/114"
            chapter_url = "http://ac.qq.com/ComicView/index/id/%s/cid/%s" % (comic_name, chapter_number)
            all_links.append(chapter_url)

        logging.debug("all_links : %s" % all_links)
        if chapter_range != "All":
            # -1 to shift the episode number accordingly to the INDEX of it. List starts from 0 xD!
            starting = int(str(chapter_range).split("-")[0]) - 1

            if str(chapter_range).split("-")[1].isdigit():
                ending = int(str(chapter_range).split("-")[1])
            else:
                ending = len(all_links)

            indexes = [x for x in range(starting, ending)]
            # [::-1] in sub_list in beginning to start this from the 1st episode and at the last,
            #  it is to reverse the list again, becasue I'm reverting it again at the end.
            all_links = [all_links[x] for x in indexes][::-1]
        else:
            all_links = all_links

        if str(sorting).lower() in ['new', 'desc', 'descending', 'latest']:
            for chap_link in all_links:
                try:
                    logging.debug("chap_link : %s" % chap_link)
                    self.single_chapter(comic_url=str(chap_link), comic_name=comic_name,
                                        download_directory=download_directory, conversion=conversion,
                                        delete_files=delete_files)
                    # if chapter range contains "__EnD__" write new value to config.json
                    if chapter_range != "All" and chapter_range.split("-")[1] == "__EnD__":
                        globalFunctions.GlobalFunctions().addOne(comic_url)
                except Exception as single_chapter_exception:
                    logging.debug("Single Chapter Exception : %s" % single_chapter_exception)
                    print("Some excpetion occured with the details : \n%s" % single_chapter_exception)
                    pass

        elif str(sorting).lower() in ['old', 'asc', 'ascending', 'oldest', 'a']:
            for chap_link in all_links[::-1]:
                try:
                    logging.debug("chap_link : %s" % chap_link)
                    self.single_chapter(comic_url=str(chap_link), comic_name=comic_name,
                                        download_directory=download_directory, conversion=conversion,
                                        delete_files=delete_files)
                    # if chapter range contains "__EnD__" write new value to config.json
                    if chapter_range != "All" and chapter_range.split("-")[1] == "__EnD__":
                        globalFunctions.GlobalFunctions().addOne(comic_url)
                except Exception as single_chapter_exception:
                    logging.debug("Single Chapter Exception : %s" % single_chapter_exception)
                    print("Some excpetion occured with the details : \n%s" % single_chapter_exception)
                    pass

        print("Finished Downloading")
        return 0

    def __decode_base64_data(self, base64data):
        base64DecodeChars = [- 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
                             -1,
                             -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 62, -1, -1,
                             -1,
                             63, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, -1, -1, -1, -1, -1, -1, -1, 0, 1, 2, 3, 4, 5,
                             6, 7,
                             8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, -1, -1, -1, -1, -1,
                             -1,
                             26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48,
                             49,
                             50, 51, -1, -1, -1, -1, -1]
        data_length = len(base64data)
        i = 0
        out = ""
        c1 = c2 = c3 = c4 = 0
        while i < data_length:
            while True:
                c1 = base64DecodeChars[ord(base64data[i]) & 255]
                i += 1
                if not (i < data_length and c1 == -1):
                    break
            if c1 == -1:
                break
            while True:
                c2 = base64DecodeChars[ord(base64data[i]) & 255]
                i += 1
                if not (i < data_length and c2 == -1):
                    break
            if c2 == -1:
                break
            out += chr(c1 << 2 | (c2 & 48) >> 4)
            while True:
                c3 = ord(base64data[i]) & 255
                i += 1
                if c3 == 61:
                    return out
                c3 = base64DecodeChars[c3]
                if not (i < data_length and c3 == - 1):
                    break
            if c3 == -1:
                break
            out += chr((c2 & 15) << 4 | (c3 & 60) >> 2)
            while True:
                c4 = ord(base64data[i]) & 255
                i += 1
                if c4 == 61:
                    return out
                c4 = base64DecodeChars[c4]
                if not (i < data_length and c4 == - 1):
                    break
            out += chr((c3 & 3) << 6 | c4)
        return out
