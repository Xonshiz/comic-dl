#!/usr/bin/env python
# -*- coding: utf-8 -*-

import globalFunctions
import re
import os
import logging
import time

from multiprocessing.dummy import Pool as ThreadPool 
from functools import partial

class MangaFox(object):
    def __init__(self, manga_url, download_directory, chapter_range, **kwargs):

        current_directory = kwargs.get("current_directory")
        conversion = kwargs.get("conversion")
        delete_files = kwargs.get("delete_files")
        self.logging = kwargs.get("log_flag")
        self.sorting = kwargs.get("sorting_order")
        self.comic_name = self.name_cleaner(manga_url)
        url_split = str(manga_url).split("/")

        if len(url_split) is 5:
            self.full_series(comic_url=manga_url, comic_name=self.comic_name, sorting=self.sorting,
                             download_directory=download_directory, chapter_range=chapter_range, conversion=conversion,
                             delete_files=delete_files)
        else:
            self.single_chapter(manga_url, self.comic_name, download_directory, conversion=conversion,
                                delete_files=delete_files)

    def name_cleaner(self, url):
        initial_name = str(url).split("/")[4].strip()
        safe_name = re.sub(r"[0-9][a-z][A-Z]\ ", "", str(initial_name))
        manga_name = str(safe_name.title()).replace("_", " ")

        return manga_name

    def single_chapter(self, comic_url, comic_name, download_directory, conversion, delete_files):
        source, cookies_main = globalFunctions.GlobalFunctions().page_downloader(manga_url=comic_url)

        current_chapter_volume = str(re.search(r"current_chapter=\"(.*?)\";", str(source)).group(1))
        chapter_number = re.search(r"c(\d+(\.\d+)?)", current_chapter_volume).group(1)
        series_code = str(re.search(r"series_code=\"(.*?)\";", str(source)).group(1))
        current_page_number = int(str(re.search(r'current_page=(.*?)\;', str(source)).group(1)).strip())
        last_page_number = int(str(re.search(r'total_pages=(.*?)\;', str(source)).group(1)).strip())

        file_directory = str(comic_name) + '/' + str(chapter_number) + "/"
        file_directory = file_directory.replace(":", "-")
        # directory_path = os.path.realpath(file_directory)
        directory_path = os.path.realpath(str(download_directory) + "/" + str(file_directory))

        globalFunctions.GlobalFunctions().info_printer(comic_name, chapter_number, total_chapters=last_page_number)

        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

        links = []
        file_names = []
        for file_name in range(current_page_number, last_page_number + 1):
            # print("Actual file_name : {0}".format(file_name))
            # http://mangafox.me/manga/colette_wa_shinu_koto_ni_shita/v03/c019/2.html
            chapter_url = "http://fanfox.net/manga/" + str(series_code) + "/" + str(
                current_chapter_volume) + "/%s.html" % str(file_name)
            logging.debug("Chapter Url : %s" % chapter_url)

            source_new, cookies_new = globalFunctions.GlobalFunctions().page_downloader(manga_url=chapter_url,
                                                                                        cookies=cookies_main)
            image_link_finder = source_new.findAll('div', {'class': 'read_img'})
            for current_chapter, link in enumerate(image_link_finder):
                x = link.findAll('img')
                for a in x:
                    image_link = a['src']
                    logging.debug("Image Link : %s" % image_link)

                    current_chapter += 1
                    file_name_custom = str(
                        globalFunctions.GlobalFunctions().prepend_zeroes(file_name, last_page_number + 1)) + ".jpg"

                    file_names.append(file_name_custom)
                    links.append(image_link)

        pool = ThreadPool(4)
        pool.map(partial(globalFunctions.GlobalFunctions().downloader, referer=comic_url, directory_path=directory_path), zip(links,file_names))
            
        globalFunctions.GlobalFunctions().conversion(directory_path, conversion, delete_files, comic_name,
                                                     chapter_number)

        return 0

    def full_series(self, comic_url, comic_name, sorting, download_directory, chapter_range, conversion, delete_files):
        # http://mangafox.la/rss/gentleman_devil.xml
        # Parsing RSS would be faster than parsing the whole page.
        rss_url = str(comic_url).replace("/manga/", "/rss/") + ".xml"
        source, cookies = globalFunctions.GlobalFunctions().page_downloader(manga_url=rss_url)

        # all_links = re.findall(r"href=\"(.*?)\" title=\"Thanks for", str(source))
        all_links_temp = re.findall(r"<link/>(.*?).html", str(source))
        all_links = ["http:" + str(link) + ".html" for link in all_links_temp]

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

            all_links = [all_links[len(all_links) - 1 - x] for x in indexes][::-1]
        else:
            all_links = all_links

        if str(sorting).lower() in ['new', 'desc', 'descending', 'latest']:
            for chap_link in all_links:
                try:
                    self.single_chapter(comic_url=str(chap_link), comic_name=comic_name,
                                    download_directory=download_directory, conversion=conversion,
                                    delete_files=delete_files)
                except Exception as ex:
                    logging.error("Error downloading : %s" % chap_link)
                    logging.error(ex)
                    break  # break to continue processing other mangas when chapter doesn't contain images.
                # if chapter range contains "__EnD__" write new value to config.json
                if chapter_range != "All" and chapter_range.split("-")[1] == "__EnD__":
                    globalFunctions.GlobalFunctions().addOne(comic_url)

        elif str(sorting).lower() in ['old', 'asc', 'ascending', 'oldest', 'a']:
            for chap_link in all_links[::-1]:
                try:
                    self.single_chapter(comic_url=str(chap_link), comic_name=comic_name,
                                        download_directory=download_directory, conversion=conversion,
                                        delete_files=delete_files)
                except Exception as ex:
                    logging.error("Error downloading : %s" % chap_link)
                    logging.error(ex)
                    break  # break to continue processing other mangas when chapter doesn't contain images.
                # if chapter range contains "__EnD__" write new value to config.json
                if chapter_range != "All" and chapter_range.split("-")[1] == "__EnD__":
                    globalFunctions.GlobalFunctions().addOne(comic_url)
                print("Waiting For 5 Seconds...")
                time.sleep(5)  # Test wait for the issue #23

        print("Finished Downloading")
        return 0
