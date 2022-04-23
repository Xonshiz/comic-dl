#!/usr/bin/env python
# -*- coding: utf-8 -*-

from comic_dl import globalFunctions
import os
import logging
import json


class QuireManhua(object):
    def __init__(self, manga_url, download_directory, chapter_range, **kwargs):

        current_directory = kwargs.get("current_directory")
        conversion = kwargs.get("conversion")
        keep_files = kwargs.get("keep_files")
        # Cookie could be used by logged-in users to fetch locked content
        self.manual_cookie = kwargs.get("manual_cookies", None)
        self.logging = kwargs.get("log_flag")
        self.sorting = kwargs.get("sorting_order")
        self.comic_name = None
        self.print_index = kwargs.get("print_index")
        self.book_id = 0
        self.chapter_id = 0
        # Remove "/" from end, gets proper result in rsplit
        manga_url = manga_url[:-1] if "/" == manga_url[-1] else manga_url
        url_split = str(manga_url).rsplit('/', 2)
        # https://www.qiremanhua.com/book/10311/
        if url_split[-1].isdigit() and not url_split[-2].isdigit():
            self.book_id = int(url_split[-1])
            self.full_series(manga_url, self.comic_name, self.sorting, download_directory, chapter_range=chapter_range,
                             conversion=conversion, keep_files=keep_files)
        # https://www.qiremanhua.com/book/10311/13943/
        else:
            self.book_id = int(url_split[-2])
            self.chapter_id = int(url_split[-1])
            self.single_chapter(manga_url, self.comic_name, download_directory, conversion=conversion,
                                keep_files=keep_files)

    def single_chapter(self, comic_url, comic_name, download_directory, conversion, keep_files, **kwargs):
        comic_url = str(comic_url)
        chapter_info = kwargs.get("chapters_info", None)
        chapter_number = 0
        chapter_name = None
        if not chapter_info:
            print("Getting chapter info")
            chapter_source = self.get_chapter_list()
            for chapter in chapter_source['data']:
                # https://www.qiremanhua.com/book/10311/13943/
                if int(self.chapter_id) == int(chapter['chapterId']):
                    chapter_number = chapter['chapter_px']
                    chapter_name = chapter['chapterName']
                    break
        else:
            chapter_number = chapter_info['chapter_id']
            chapter_name = chapter_info['chapter_name']

        source, cookies = globalFunctions.GlobalFunctions().page_downloader(manga_url=comic_url,
                                                                            cookies=self.manual_cookie)
        if not self.comic_name:
            com_nm = source.find("a", {"class": "active"})
            if com_nm:
                self.comic_name = com_nm.text
        image_list_elems = source.find_all("img", {"class": "lazy show-menu chapter-img"})
        links = []
        file_names = []
        if len(image_list_elems) > 0:
            for _idx, elem in enumerate(image_list_elems):
                img_url = str(elem['src']).strip()
                links.append(img_url)
                img_extension = str(img_url).rsplit('.', 1)[-1]
                file_names.append('{0}.{1}'.format(_idx, img_extension))
        else:
            print("Locked content. Returning without downloading {0}".format(comic_url))
            return 1

        chapter_name_string = chapter_number if not chapter_name else "{0} - {1}".format(chapter_number, chapter_name)
        file_directory = globalFunctions.GlobalFunctions().create_file_directory(chapter_name_string, self.comic_name)

        directory_path = os.path.realpath(str(download_directory) + "/" + str(file_directory))

        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
        globalFunctions.GlobalFunctions().multithread_download(chapter_name_string, self.comic_name, comic_url,
                                                               directory_path,
                                                               file_names, links, self.logging)

        globalFunctions.GlobalFunctions().conversion(directory_path, conversion, keep_files, self.comic_name,
                                                     chapter_name_string)

        return 0

    def full_series(self, comic_url, comic_name, sorting, download_directory, chapter_range, conversion, keep_files):
        if self.book_id <= 0:
            print("Invalid book Id. Exiting")
            return 0
        source = self.get_chapter_list()

        all_links = []
        chapters_info = {}
        for chapter in source['data']:
            # https://www.qiremanhua.com/book/10311/13943/
            chapter_url = "https://www.qiremanhua.com/book/{0}/{1}".format(self.book_id, chapter['chapterId'])
            all_links.append(chapter_url)
            chapters_info[chapter['chapterId']] = {
                'chapter_id': chapter['chapter_px'],
                'chapter_name': chapter['chapterName']
            }

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

        if self.print_index:
            idx = 0
            for chap_link in all_links:
                idx = idx + 1
                print(str(idx) + ": " + chap_link)
            return
        print(chapters_info)

        if str(sorting).lower() in ['new', 'desc', 'descending', 'latest']:
            for chap_link in all_links:
                try:
                    chap_id = int(chap_link.rsplit('/', 1)[-1])
                    self.single_chapter(comic_url=chap_link, comic_name=comic_name,
                                        download_directory=download_directory,
                                        conversion=conversion, keep_files=keep_files,
                                        chapters_info=chapters_info[chap_id])
                except Exception as ex:
                    logging.error("Error downloading : %s" % chap_link)
                    break  # break to continue processing other mangas
                # if chapter range contains "__EnD__" write new value to config.json
                # @Chr1st-oo - modified condition due to some changes on automatic download and config.
                if chapter_range != "All" and (
                        chapter_range.split("-")[1] == "__EnD__" or len(chapter_range.split("-")) == 3):
                    globalFunctions.GlobalFunctions().addOne(comic_url)
        elif str(sorting).lower() in ['old', 'asc', 'ascending', 'oldest', 'a']:
            # print("Running this")
            for chap_link in all_links[::-1]:
                try:
                    chap_id = int(chap_link.rsplit('/', 1)[-1])
                    self.single_chapter(comic_url=chap_link, comic_name=comic_name,
                                        download_directory=download_directory,
                                        conversion=conversion, keep_files=keep_files,
                                        chapters_info=chapters_info.get(chap_id))
                except Exception as ex:
                    logging.error("Error downloading : %s" % chap_link)
                    break  # break to continue processing other mangas
                # if chapter range contains "__EnD__" write new value to config.json
                # @Chr1st-oo - modified condition due to some changes on automatic download and config.
                if chapter_range != "All" and (
                        chapter_range.split("-")[1] == "__EnD__" or len(chapter_range.split("-")) == 3):
                    globalFunctions.GlobalFunctions().addOne(comic_url)

        return 0

    def get_chapter_list(self):
        chapter_list_url = "https://www.qiremanhua.com/book/ajax_chapteres?bookId={0}".format(self.book_id)
        source, self.manual_cookie = globalFunctions.GlobalFunctions().page_downloader(manga_url=chapter_list_url,
                                                                                       cookies=self.manual_cookie)
        if source:
            source = json.loads(str(source))
        return source
