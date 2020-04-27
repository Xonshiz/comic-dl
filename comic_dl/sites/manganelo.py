#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

import globalFunctions
import os


class Manganelo():
    def __init__(self, manga_url, download_directory, chapter_range, **kwargs):
        current_directory = kwargs.get("current_directory")
        conversion = kwargs.get("conversion")
        keep_files = kwargs.get("keep_files")
        self.logging = kwargs.get("log_flag")
        self.sorting = kwargs.get("sorting_order")
        self.manga_url = manga_url
        self.print_index = kwargs.get("print_index")

        if "/chapter/" in manga_url:
            self.single_chapter(manga_url=manga_url, download_directory=download_directory,
                                conversion=conversion, keep_files=keep_files)
        else:
            self.full_series(comic_url=self.manga_url, sorting=self.sorting,
                             download_directory=download_directory, chapter_range=chapter_range, conversion=conversion,
                             keep_files=keep_files)

    def single_chapter(self, manga_url, download_directory, conversion, keep_files):
        source, cookies = globalFunctions.GlobalFunctions().page_downloader(manga_url=manga_url)

        if "mangakakalot" in manga_url:
            breadcrumb = source.find('div', {'class': 'breadcrumb'})
            breadcrumb_parts = breadcrumb.findAll('a')
            comic_name = (breadcrumb_parts[1])['title']
            chapter_number = (breadcrumb_parts[2]).find('span').text
        else:  # manganelo
            breadcrumb = source.find('div', {'class': 'panel-breadcrumb'})
            breadcrumb_parts = breadcrumb.findAll('a')
            comic_name = (breadcrumb_parts[1])['title']
            chapter_number = (breadcrumb_parts[2])['title']

        file_directory = globalFunctions.GlobalFunctions().create_file_directory(chapter_number, comic_name)

        directory_path = os.path.realpath(str(download_directory) + os.sep + str(file_directory))

        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

        images = source.findAll('img')

        links = []
        file_names = []
        i = 0
        for image in images:
            image_link = image['src']

            if "/themes/" in image_link:
                continue

            # extension = re.compile('.*\\.').sub('', image_link)
            file_name = str(globalFunctions.GlobalFunctions().prepend_zeroes(i, len(images))) + ".jpg"
            file_names.append(file_name)
            links.append(image_link)
            i += 1

        globalFunctions.GlobalFunctions().multithread_download(chapter_number, comic_name, manga_url, directory_path,
                                                               file_names, links, self.logging)

        globalFunctions.GlobalFunctions().conversion(directory_path, conversion, keep_files, comic_name,
                                                     chapter_number)

        return 0

    def full_series(self, comic_url, sorting, download_directory, chapter_range, conversion, keep_files):

        source, cookies = globalFunctions.GlobalFunctions().page_downloader(manga_url=comic_url)

        if "mangakakalot" in comic_url:
            chapter_list = source.find('div', {'class': 'chapter-list'})
            all_links = chapter_list.findAll('a')
        else:  # manganelo
            chapter_list = source.find('ul', {'class': 'row-content-chapter'})
            all_links = chapter_list.findAll('a')

        chapter_links = []

        for link in all_links:
            chapter_links.append(link['href'])

        # Uh, so the logic is that remove all the unnecessary chapters beforehand
        #  and then pass the list for further operations.
        if chapter_range != "All":
            # -1 to shift the episode number accordingly to the INDEX of it. List starts from 0 xD!
            starting = int(str(chapter_range).split("-")[0]) - 1

            if str(chapter_range).split("-")[1].isdigit():
                ending = int(str(chapter_range).split("-")[1])
            else:
                ending = len(all_links)

            if ending > len(all_links):
                ending = len(all_links)

            indexes = [x for x in range(starting, ending)]

            chapter_links = chapter_links[::-1]
            chapter_links = [chapter_links[x] for x in indexes][::-1]
        else:
            chapter_links = chapter_links

        if self.print_index:
            idx = chapter_links.__len__()
            for chap_link in chapter_links:
                print(str(idx) + ": " + str(chap_link))
                idx = idx - 1
            return

        if str(sorting).lower() in ['new', 'desc', 'descending', 'latest']:
            for chap_link in chapter_links:
                try:
                    self.single_chapter(manga_url=str(chap_link),
                                        download_directory=download_directory, conversion=conversion,
                                        keep_files=keep_files)
                except Exception as ex:
                    self.logging.error("Error downloading : %s" % chap_link)
                    break  # break to continue processing other mangas
                # if chapter range contains "__EnD__" write new value to config.json
                # @Chr1st-oo - modified condition due to some changes on automatic download and config.
                if chapter_range != "All" and (
                        chapter_range.split("-")[1] == "__EnD__" or len(chapter_range.split("-")) == 3):
                    globalFunctions.GlobalFunctions().addOne(comic_url)

        elif str(sorting).lower() in ['old', 'asc', 'ascending', 'oldest', 'a']:
            for chap_link in chapter_links[::-1]:
                try:
                    self.single_chapter(manga_url=str(chap_link),
                                        download_directory=download_directory, conversion=conversion,
                                        keep_files=keep_files)
                except Exception as ex:
                    self.logging.error("Error downloading : %s" % chap_link)
                    break  # break to continue processing other mangas
                # if chapter range contains "__EnD__" write new value to config.json
                # @Chr1st-oo - modified condition due to some changes on automatic download and config.
                if chapter_range != "All" and (
                        chapter_range.split("-")[1] == "__EnD__" or len(chapter_range.split("-")) == 3):
                    globalFunctions.GlobalFunctions().addOne(comic_url)

        return 0
