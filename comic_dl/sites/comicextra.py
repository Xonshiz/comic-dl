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
        keep_files = kwargs.get("keep_files")
        self.logging = kwargs.get("log_flag")
        self.sorting = kwargs.get("sorting_order")
        # self.comic_name = self.name_cleaner(manga_url)
        self.print_index = kwargs.get("print_index")

        if "/comic/" not in manga_url:
            # http://www.comicextra.com/captain-marvel-2016/chapter-10
            # http://www.comicextra.com/steven-universe-ongoing/chapter-13
            if "/full" not in manga_url:
                if manga_url[-1] == "/":
                    manga_url += "full"
                else:
                    manga_url += "/full"
            self.single_chapter(manga_url, download_directory,
                                conversion=conversion, keep_files=keep_files)
        else:
            self.full_series(comic_url=manga_url, sorting=self.sorting, download_directory=download_directory,
                             chapter_range=chapter_range, conversion=conversion, keep_files=keep_files)

    def single_chapter(self, comic_url, download_directory, conversion, keep_files):
        comic_name = re.sub(r"[0-9][a-z][A-Z]\ ", "",
                            str(comic_url).split("/")[3].replace("%20", " ").replace("-", " ").title())
        source, cookies = globalFunctions.GlobalFunctions().page_downloader(manga_url=comic_url)
        img_list = []

        first_image_link_bs = source.find_all('div', {'class': 'chapter-main'})
        # print(first_image_link_bs)
        for single_node in first_image_link_bs:
            x = single_node.findAll('img')
            for a in x:
                img_list.append(str(a['src']).strip())
        # http://www.comicextra.com/steven-universe-ongoing/chapter-13
        chapter_number = str(comic_url.split("-")[-1]).replace("/full", "")
        # print(chapter_number)

        # total_pages = re.search(r'>of (.*?)</div>', str(source)).group(1)
        total_pages = len(img_list)
        # print(total_pages)

        file_directory = globalFunctions.GlobalFunctions().create_file_directory(chapter_number, comic_name)
        directory_path = os.path.realpath(str(download_directory) + "/" + str(file_directory))

        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

        links = []
        file_names = []
        for current_chapter, chapter_link in enumerate(img_list):
            current_chapter += 1
            file_name = str(globalFunctions.GlobalFunctions().prepend_zeroes(current_chapter, len(img_list))) + ".jpg"
            
            file_names.append(file_name)
            links.append(chapter_link)

        globalFunctions.GlobalFunctions().multithread_download(chapter_number, comic_name, comic_url, directory_path,
                                                               file_names, links, self.logging)
            
        globalFunctions.GlobalFunctions().conversion(directory_path, conversion, keep_files, comic_name,
                                                     chapter_number)

        return 0

    def full_series(self, comic_url, sorting, download_directory, chapter_range, conversion, keep_files):
        comic_name = re.sub(r"[0-9][a-z][A-Z]\ ", "",
                            str(comic_url).split("/")[4].replace("%20", " ").replace("-", " ").title())
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
        else:
            all_links = all_links
        if not all_links:
            print("Couldn't Find the chapter list")
            return 1
        # all_links.pop(0) # Because this website lists the next chapter, which is NOT available.

        if self.print_index:
            idx = len(all_links)
            for chap_link in all_links:
                print(str(idx) + ": " + chap_link)
                idx = idx - 1
            return

        if str(sorting).lower() in ['new', 'desc', 'descending', 'latest']:
            for chap_link in all_links:
                chap_link += "/full"
                try:
                    self.single_chapter(comic_url=chap_link, download_directory=download_directory,
                                        conversion=conversion, keep_files=keep_files)
                except Exception as ex:
                    logging.error("Error downloading : %s" % chap_link)
                    break  # break to continue processing other mangas
                # if chapter range contains "__EnD__" write new value to config.json
                # @Chr1st-oo - modified condition due to some changes on automatic download and config.
                if chapter_range != "All" and (chapter_range.split("-")[1] == "__EnD__" or len(chapter_range.split("-")) == 3):
                    globalFunctions.GlobalFunctions().addOne(comic_url)

        elif str(sorting).lower() in ['old', 'asc', 'ascending', 'oldest', 'a']:
            for chap_link in all_links[::-1]:
                chap_link += "/full"
                try:
                    self.single_chapter(comic_url=chap_link, download_directory=download_directory,
                                        conversion=conversion, keep_files=keep_files)
                except Exception as ex:
                    logging.error("Error downloading : %s" % chap_link)
                    break  # break to continue processing other mangas
                # if chapter range contains "__EnD__" write new value to config.json
                # @Chr1st-oo - modified condition due to some changes on automatic download and config.
                if chapter_range != "All" and (chapter_range.split("-")[1] == "__EnD__" or len(chapter_range.split("-")) == 3):
                    globalFunctions.GlobalFunctions().addOne(comic_url)

        return 0
