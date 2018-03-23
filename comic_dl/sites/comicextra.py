#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import globalFunctions
import json
import os
import logging


class ComicExtra(object):
    def __init__(self, manga_url, download_directory, chapter_range, **kwargs):
        current_directory = kwargs.get("current_directory")
        conversion = kwargs.get("conversion")
        delete_files = kwargs.get("delete_files")
        self.logging = kwargs.get("log_flag")
        self.sorting = kwargs.get("sorting_order")
        # self.comic_name = self.name_cleaner(manga_url)

        if "/comic/" not in manga_url:
            # http://www.comicextra.com/captain-marvel-2016/chapter-10
            self.single_chapter(manga_url, download_directory,
                                conversion=conversion, delete_files=delete_files)
        else:
            self.full_series(comic_url=manga_url, sorting=self.sorting, download_directory=download_directory,
                             chapter_range=chapter_range, conversion=conversion, delete_files=delete_files)
    #
    # def name_cleaner(self, url):
    #     manga_name = re.sub(r"[0-9][a-z][A-Z]\ ", "", str(url).split("/")[3].replace("%20", " ").replace("-", " ").title())
    #
    #     return manga_name

    def single_chapter(self, comic_url, download_directory, conversion, delete_files):
        comic_name = re.sub(r"[0-9][a-z][A-Z]\ ", "", str(comic_url).split("/")[3].replace("%20", " ").replace("-", " ").title())
        source, cookies = globalFunctions.GlobalFunctions().page_downloader(manga_url=comic_url)
        temp_link = ""

        first_image_link_bs = source.find_all('div', {'class': 'chapter-container'})
        # print(first_image_link_bs)
        for single_node in first_image_link_bs:
            x = single_node.findAll('img')
            for a in x:
                temp_link = str(a['src']).strip()
        # http://readcomics.io/images/manga/captain-marvel-2016/10/1.jpg
        chapter_number = int(temp_link.split("/")[-2])
        # print(chapter_number)

        total_pages = re.search(r'>of (.*?)</div>', str(source)).group(1)
        # print(total_pages)

        file_directory = str(comic_name) + '/' + str(chapter_number) + "/"
        file_directory = file_directory.replace(":", "-")
        directory_path = os.path.realpath(str(download_directory) + "/" + str(file_directory))

        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

        globalFunctions.GlobalFunctions().info_printer(comic_name, chapter_number, total_chapters=total_pages)

        for current_chapter in range(1, int(total_pages)):
            globalFunctions.GlobalFunctions().downloader("http://readcomics.io/images/manga/" +
                                                         str(str(comic_url).split("/")[3]) + "/" + str(chapter_number) +
                                                         "/" + str(current_chapter) + ".jpg",
                                                         str(current_chapter) + ".jpg",
                                                         comic_url, directory_path,
                                                         log_flag=self.logging)

        globalFunctions.GlobalFunctions().conversion(directory_path, conversion, delete_files, comic_name,
                                                     chapter_number)

    def full_series(self, comic_url, sorting, download_directory, chapter_range, conversion, delete_files):
        comic_name = re.sub(r"[0-9][a-z][A-Z]\ ", "", str(comic_url).split("/")[4].replace("%20", " ").replace("-", " ").title())
        source, cookies = globalFunctions.GlobalFunctions().page_downloader(manga_url=comic_url)
        all_links = []
        chap_holder_div = source.find_all('tbody', {'id': 'list'})
        # print(comic_name)
        for single_node in chap_holder_div:
            x = single_node.findAll('a')
            for a in x:
                all_links.append(str(a['href']).strip())

        if chapter_range != "All":
            # -1 to shift the episode number accordingly to the INDEX of it. List starts from 0 xD!
            starting = int(str(chapter_range).split("-")[0]) - 1

            if str(chapter_range).split("-")[1].isdigit():
                ending = int(str(chapter_range).split("-")[1])
            else:
                ending = len(all_links)

            indexes = [x for x in range(starting, ending)]

            all_links = [all_links[x] for x in indexes][::-1]
            # if chapter range contains "__EnD__" write new value to config.json
            if chapter_range.split("-")[1] == "__EnD__":
                globalFunctions.GlobalFunctions().saveNewRange(comic_url, len(all_links))
        else:
            all_links = all_links
        if not all_links:
            print("Couldn't Find the chapter list")
            return 1
        # all_links.pop(0) # Because this website lists the next chapter, which is NOT available.

        if str(sorting).lower() in ['new', 'desc', 'descending', 'latest']:
            for chap_link in all_links:
                try:
                    self.single_chapter(comic_url=chap_link, download_directory=download_directory,
                                        conversion=conversion, delete_files=delete_files)
                except Exception as e:
                    pass

        elif str(sorting).lower() in ['old', 'asc', 'ascending', 'oldest', 'a']:
            for chap_link in all_links[::-1]:
                try:
                    self.single_chapter(comic_url=chap_link,  download_directory=download_directory,
                                        conversion=conversion, delete_files=delete_files)
                except Exception as e:
                    pass

        print("Finished Downloading")
        return 0
