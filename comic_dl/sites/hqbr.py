#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import globalFunctions
import json
import os
import logging

from multiprocessing.dummy import Pool as ThreadPool 
from functools import partial

class Hqbr(object):
    def __init__(self, manga_url, download_directory, chapter_range, **kwargs):
        current_directory = kwargs.get("current_directory")
        conversion = kwargs.get("conversion")
        delete_files = kwargs.get("delete_files")
        self.logging = kwargs.get("log_flag")
        self.sorting = kwargs.get("sorting_order")
        self.comic_name = self.name_cleaner(manga_url)

        if "/hqs/" in manga_url:
            # https://hqbr.com.br/hqs/Aves%20de%20Rapina%20(1999)/capitulo/126/leitor/0#1
            self.single_chapter(manga_url, self.comic_name, download_directory,
                                conversion=conversion, delete_files=delete_files)
        else:
            self.full_series(comic_url=manga_url, comic_name=self.comic_name,
                             sorting=self.sorting, download_directory=download_directory, chapter_range=chapter_range,
                             conversion=conversion, delete_files=delete_files)

    def name_cleaner(self, url):
        manga_name = re.sub(r"[0-9][a-z][A-Z]\ ", "", str(url).split("/")[4].split("?")[0].replace("%20", " ").title())

        return manga_name

    def single_chapter(self, comic_url, comic_name, download_directory, conversion, delete_files):
        chapter_number = int(str(comic_url).split("/")[6].strip())
        # print(chapter_number)
        source, cookies = globalFunctions.GlobalFunctions().page_downloader(manga_url=comic_url)
        links_string = re.search(r'pages = \[(.*?)\]', str(source)).group(1)
        img_list = re.findall(r'\"(.*?)\"', str(links_string))

        file_directory = str(comic_name) + '/' + str(chapter_number) + "/"
        file_directory = file_directory.replace(":", "-")
        directory_path = os.path.realpath(str(download_directory) + "/" + str(file_directory))

        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

        globalFunctions.GlobalFunctions().info_printer(comic_name, chapter_number, total_chapters=len(img_list))
        
        links = []
        file_names = []
        for page_count, image_link in enumerate(img_list):
            page_count += 1
            file_name = str(globalFunctions.GlobalFunctions().prepend_zeroes(page_count, len(img_list))) + ".jpg"
           
            file_names.append(file_name)
            links.append("https://hqbr.com.br" + str(image_link))

        pool = ThreadPool(4)
        pool.map(partial(globalFunctions.GlobalFunctions().downloader, referer=comic_url, directory_path=directory_path), zip(links,file_names))
            
        globalFunctions.GlobalFunctions().conversion(directory_path, conversion, delete_files, comic_name,
                                                     chapter_number)

        return 0

    def full_series(self, comic_url, comic_name, sorting, download_directory, chapter_range, conversion, delete_files):
        source, cookies = globalFunctions.GlobalFunctions().page_downloader(manga_url=comic_url)
        all_links = []
        chap_holder_div = source.find_all('table', {'class': 'table table-hover'})
        # print(comic_name)
        for single_node in chap_holder_div:
            x = single_node.findAll('a')
            for a in x:
                all_links.append("https://hqbr.com.br" + str(a['href']).strip())

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
        if not all_links:
            print("Couldn't Find the chapter list")
            return 1
        # all_links.pop(0) # Because this website lists the next chapter, which is NOT available.

        if str(sorting).lower() in ['new', 'desc', 'descending', 'latest']:
            for chap_link in all_links:
                try:
                    self.single_chapter(comic_url=chap_link, comic_name=comic_name,
                                        download_directory=download_directory,
                                        conversion=conversion, delete_files=delete_files)
                    # if chapter range contains "__EnD__" write new value to config.json
                    if chapter_range.split("-")[1] == "__EnD__":
                        globalFunctions.GlobalFunctions().addOne(comic_url)
                except Exception as e:
                    pass

        elif str(sorting).lower() in ['old', 'asc', 'ascending', 'oldest', 'a']:
            for chap_link in all_links[::-1]:
                try:
                    self.single_chapter(comic_url=chap_link, comic_name=comic_name,
                                        download_directory=download_directory,
                                        conversion=conversion, delete_files=delete_files)
                    # if chapter range contains "__EnD__" write new value to config.json
                    if chapter_range.split("-")[1] == "__EnD__":
                        globalFunctions.GlobalFunctions().addOne(comic_url)
                except Exception as e:
                    pass

        print("Finished Downloading")
        return 0
