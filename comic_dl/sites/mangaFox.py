#!/usr/bin/env python
# -*- coding: utf-8 -*-

import globalFunctions
import re
import os
import logging
import time


class MangaFox(object):
    def __init__(self, manga_url, download_directory, chapter_range, **kwargs):

        current_directory = kwargs.get("current_directory")
        conversion = kwargs.get("conversion")
        delete_files = kwargs.get("delete_files")
        self.logging = kwargs.get("log_flag")
        self.sorting = kwargs.get("sorting_order")
        self.comic_name = self.name_cleaner(manga_url)
        url_split = str(manga_url).split("/")

        if len(url_split) is 6:
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
        chapter_number = re.search(r"c(\d+)", current_chapter_volume).group(1)
        series_code = str(re.search(r"series_code=\"(.*?)\";", str(source)).group(1))
        current_page_number = int(str(re.search(r'current_page=(.*?)\;', str(source)).group(1)).strip())
        last_page_number = int(str(re.search(r'total_pages=(.*?)\;', str(source)).group(1)).strip())

        file_directory = str(comic_name) + '/' + str(chapter_number) + "/"

        # directory_path = os.path.realpath(file_directory)
        directory_path = os.path.realpath(str(download_directory) + "/" + str(file_directory))

        globalFunctions.GlobalFunctions().info_printer(comic_name, chapter_number)

        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

        for file_name in range(current_page_number, last_page_number + 1):
            # print("Actual file_name : {0}".format(file_name))
            # http://mangafox.me/manga/colette_wa_shinu_koto_ni_shita/v03/c019/2.html
            chapter_url = "http://mangafox.me/manga/" + str(series_code) + "/" + str(
                current_chapter_volume) + "/%s.html" % str(file_name)
            logging.debug("Chapter Url : %s" % chapter_url)

            source_new, cookies_new = globalFunctions.GlobalFunctions().page_downloader(manga_url=chapter_url,
                                                                                        cookies=cookies_main)
            image_link_finder = source_new.findAll('div', {'class': 'read_img'})
            for link in image_link_finder:
                x = link.findAll('img')
                for a in x:
                    image_link = a['src']
                    # Fix for 30 (File Naming 0's)
                    if len(str(file_name)) < len(str(last_page_number)):
                        number_of_zeroes = len(str(last_page_number)) - len(str(file_name))
                        # If a chapter has only 9 images, we need to avoid 0*0 case.
                        if len(str(number_of_zeroes)) == 0:
                            file_name = str(file_name) + ".jpg"
                        else:
                            file_name = "0"*int(number_of_zeroes) + str(file_name) + ".jpg"
                    else:
                        file_name = str(file_name) + ".jpg"
                    logging.debug("Image Link : %s" % image_link)
                    globalFunctions.GlobalFunctions().downloader(image_link, file_name, chapter_url, directory_path,
                                                                 log_flag=self.logging)

        globalFunctions.GlobalFunctions().conversion(directory_path, conversion, delete_files, comic_name,
                                                     chapter_number)

        return 0

    def full_series(self, comic_url, comic_name, sorting, download_directory, chapter_range, conversion, delete_files):
        source, cookies = globalFunctions.GlobalFunctions().page_downloader(manga_url=comic_url)

        all_links = re.findall(r"href=\"(.*?)\" title=\"Thanks for", str(source))
        logging.debug("All Links : %s" % all_links)

        # Uh, so the logic is that remove all the unnecessary chapters beforehand and then pass the list for further operations.
        if chapter_range != "All":
            # -1 to shift the episode number accordingly to the INDEX of it. List starts from 0 xD!
            starting = int(str(chapter_range).split("-")[0]) - 1
            ending = int(str(chapter_range).split("-")[1])
            indexes = [x for x in range(starting, ending)]
            # [::-1] in sub_list in beginning to start this from the 1st episode and at the last, it is to reverse the list again, becasue I'm reverting it again at the end.
            all_links = [all_links[::-1][x] for x in indexes][::-1]
        else:
            all_links = all_links

        if str(sorting).lower() in ['new', 'desc', 'descending', 'latest']:
            for chap_link in all_links:
                self.single_chapter(comic_url=str(chap_link), comic_name=comic_name, conversion=conversion,
                                    delete_files=delete_files)

        elif str(sorting).lower() in ['old', 'asc', 'ascending', 'oldest', 'a']:
            for chap_link in all_links[::-1]:
                self.single_chapter(comic_url=str(chap_link), comic_name=comic_name,
                                    download_directory=download_directory, conversion=conversion,
                                    delete_files=delete_files)
                print("Waiting For 5 Seconds...")
                time.sleep(5)  # Test wait for the issue #23

        print("Finished Downloading")
        return 0
