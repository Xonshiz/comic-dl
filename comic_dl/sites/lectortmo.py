#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import sys

from bs4 import BeautifulSoup

from comic_dl import globalFunctions
import re
import os
import logging
import json
import time


class LectorTmo(object):
    def __init__(self, manga_url, download_directory, chapter_range, **kwargs):

        current_directory = kwargs.get("current_directory")
        conversion = kwargs.get("conversion")
        keep_files = kwargs.get("keep_files")
        self.logging = kwargs.get("log_flag")
        self.sorting = kwargs.get("sorting_order")
        self.comic_name = None
        self.print_index = kwargs.get("print_index")
        if "/library/" in manga_url:
            self.full_series(manga_url, self.comic_name, self.sorting, download_directory, chapter_range=chapter_range,
                             conversion=conversion, keep_files=keep_files)
        # https://lectortmo.com/view_uploads/979773
        elif "/viewer/" in manga_url or "/paginated/" in manga_url or "/view_uploads/" in manga_url:
            self.single_chapter(manga_url, self.comic_name, download_directory, conversion=conversion,
                                keep_files=keep_files)

    def single_chapter(self, comic_url, comic_name, download_directory, conversion, keep_files):
        comic_url = str(comic_url)
        # https://lectortmo.com/viewer/004b1c38ce59f14291118de9f59bed7e/paginated/1
        # https://lectortmo.com/view_uploads/979773
        chapter_number = comic_url.split('/')[-1] if "/view_uploads/" in comic_url else comic_url.split('/')[-3]

        source, cookies = globalFunctions.GlobalFunctions().page_downloader(manga_url=comic_url)
        ld_json_content = source.find_all("script", {"type": "application/ld+json"})
        if len(ld_json_content) > 0:
            cleaned_json_string = ld_json_content[0].next.strip().replace('\n', '')
            loaded_json = json.loads(cleaned_json_string)
            if loaded_json:
                self.comic_name = comic_name = loaded_json['headline']
        links = []
        file_names = []
        img_url = self.extract_image_link_from_html(source=source)
        links.append(img_url)
        img_extension = str(img_url).rsplit('.', 1)[-1]
        unique_id = str(img_url).split('/')[-2]
        file_names.append('{0}.{1}'.format(1, img_extension))

        total_page_list = source.find("select", {"id": "viewer-pages-select"})
        last_page_number = 0
        options = total_page_list.findAll('option')
        if len(options) > 0:
            last_page_number = int(options[-1]['value'])
        if last_page_number <= 0:
            print("Couldn't find all the pages. Exiting.")
            sys.exit(1)
        for page_number in range(2, last_page_number):
            current_url = "https://lectortmo.com/viewer/{0}/paginated/{1}".format(unique_id, page_number)
            print("Grabbing details for: {0}".format(current_url))
            source, cookies = globalFunctions.GlobalFunctions().page_downloader(manga_url=current_url, cookies=cookies)
            image_url = self.extract_image_link_from_html(source=source)
            links.append(image_url)
            img_extension = str(image_url).rsplit('.', 1)[-1]
            file_names.append('{0}.{1}'.format(page_number, img_extension))
            time.sleep(random.randint(1, 6))
        file_directory = globalFunctions.GlobalFunctions().create_file_directory(chapter_number, self.comic_name)

        directory_path = os.path.realpath(str(download_directory) + "/" + str(file_directory))

        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
        globalFunctions.GlobalFunctions().multithread_download(chapter_number, self.comic_name, comic_url, directory_path,
                                                               file_names, links, self.logging)

        globalFunctions.GlobalFunctions().conversion(directory_path, conversion, keep_files, self.comic_name,
                                                     chapter_number)

        return 0

    def full_series(self, comic_url, comic_name, sorting, download_directory, chapter_range, conversion, keep_files):
        source, cookies = globalFunctions.GlobalFunctions().page_downloader(manga_url=comic_url)

        all_links = []
        all_chapter_links = source.find_all("a", {"class": "btn btn-default btn-sm"})
        for chapter in all_chapter_links:
            all_links.append(chapter['href'])

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

        if str(sorting).lower() in ['new', 'desc', 'descending', 'latest']:
            for chap_link in all_links:
                try:
                    self.single_chapter(comic_url=chap_link, comic_name=comic_name,
                                        download_directory=download_directory,
                                        conversion=conversion, keep_files=keep_files)
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
                    self.single_chapter(comic_url=chap_link, comic_name=comic_name,
                                        download_directory=download_directory,
                                        conversion=conversion, keep_files=keep_files)
                except Exception as ex:
                    logging.error("Error downloading : %s" % chap_link)
                    break  # break to continue processing other mangas
                # if chapter range contains "__EnD__" write new value to config.json
                # @Chr1st-oo - modified condition due to some changes on automatic download and config.
                if chapter_range != "All" and (
                        chapter_range.split("-")[1] == "__EnD__" or len(chapter_range.split("-")) == 3):
                    globalFunctions.GlobalFunctions().addOne(comic_url)

        return 0

    def extract_image_link_from_html(self, source):
        image_tags = source.find_all("img", {"class": "viewer-image viewer-page"})
        img_link = None
        for element in image_tags:
            img_link = element['src']
        return img_link
