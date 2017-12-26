#!/usr/bin/env python
# -*- coding: utf-8 -*-

import globalFunctions
import re
import os
import logging


class ReadComicOnlineTo(object):
    def __init__(self, manga_url, download_directory, chapter_range, **kwargs):

        current_directory = kwargs.get("current_directory")
        conversion = kwargs.get("conversion")
        delete_files = kwargs.get("delete_files")
        self.logging = kwargs.get("log_flag")
        self.sorting = kwargs.get("sorting_order")
        self.image_quality = kwargs.get("image_quality")
        self.comic_name = self.name_cleaner(manga_url)



        url_split = str(manga_url).split("/")

        if len(url_split) in [5]: # Sometimes, this value came out to be 6, instead of 5. Hmmmmmmmm weird.
            # Removing "6" from here, because it caused #47
            print("Downloading Full!")
            self.full_series(comic_url=manga_url.replace("&readType=1", ""), comic_name=self.comic_name,
                             sorting=self.sorting, download_directory=download_directory, chapter_range=chapter_range,
                             conversion=conversion, delete_files=delete_files)
        else:
            if "&readType=0" in manga_url:
                manga_url = str(manga_url).replace("&readType=0", "&readType=1")  # All Images in one page!
            elif "&readType=1" not in manga_url:
                manga_url = str(manga_url) + "&readType=1"  # All Images in one page!
            self.single_chapter(manga_url, self.comic_name, download_directory, conversion=conversion,
                                delete_files=delete_files)

    def single_chapter(self, comic_url, comic_name, download_directory, conversion, delete_files):
        chapter_number = str(comic_url).split("/")[5].split("?")[0].replace("-", " - ")

        source, cookies = globalFunctions.GlobalFunctions().page_downloader(manga_url=comic_url)

        image_list = re.findall(r"lstImages.push\(\"(.*?)\"\);", str(source))


        file_directory = str(comic_name) + '/' + str(chapter_number) + "/"

        # directory_path = os.path.realpath(file_directory)
        directory_path = os.path.realpath(str(download_directory) + "/" + str(file_directory))

        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

        globalFunctions.GlobalFunctions().info_printer(comic_name, chapter_number)

        image_len = len(image_list)
        if str(self.image_quality).lower().strip() in ["low", "worst", "bad", "cancer", "mobile"]:
            print("Downloading In Low Quality...")
        for link in image_list:
            link = link.replace("\\", "")
            # file_name = str(link).split("/")[-1].strip()
            #file_name = "0" + str(image_list.index(link)) + ".jpg"

            if len(str(image_list.index(link))) < len(str(image_len)):
                number_of_zeroes = len(str(image_len)) - len(str(image_list.index(link)))
                # If a chapter has only 9 images, we need to avoid 0*0 case.
                if len(str(number_of_zeroes)) == 0:
                    file_name = str(image_list.index(link)) + ".jpg"
                else:
                    file_name = "0" * int(number_of_zeroes) + str(image_list.index(link)) + ".jpg"
            else:
                file_name = str(image_list.index(link)) + ".jpg"

            logging.debug("Image Link : %s" % link)
            link = link.replace("=s1600", "=s0").replace("/s1600", "/s0") # Change low quality to best.

            if str(self.image_quality).lower().strip() in ["low", "worst", "bad", "cancer", "mobile"]:
                link = link.replace("=s0", "=s1600").replace("/s0", "/s1600")
            globalFunctions.GlobalFunctions().downloader(link, file_name, comic_url, directory_path)

        globalFunctions.GlobalFunctions().conversion(directory_path, conversion, delete_files, comic_name,
                                                     chapter_number)

        return 0

    def name_cleaner(self, url):
        initial_name = str(url).split("/")[4].strip()
        safe_name = re.sub(r"[0-9][a-z][A-Z]\ ", "", str(initial_name))
        manga_name = str(safe_name.title()).replace("-", " ")

        return manga_name

    def full_series(self, comic_url, comic_name, sorting, download_directory, chapter_range, conversion, delete_files):
        series_name_raw = str(comic_url).split("/")[3].strip()
        source, cookies = globalFunctions.GlobalFunctions().page_downloader(manga_url=comic_url)

        link_regex = "<a href=\"/" + str(series_name_raw) + "/(.*?)\""
        all_links = list(re.findall(link_regex, str(source)))

        logging.debug("All Links : %s" % all_links)

        # Uh, so the logic is that remove all the unnecessary chapters beforehand and then pass the list for further operations.
        if chapter_range != "All":
            # -1 to shift the episode number accordingly to the INDEX of it. List starts from 0 xD!
            starting = int(str(chapter_range).split("-")[0]) - 1

            if str(chapter_range).split("-")[1].decode().isdecimal():
                ending = int(str(chapter_range).split("-")[1])
            else:
                ending = len(all_links)

            indexes = [x for x in range(starting, ending)]
            # [::-1] in sub_list in beginning to start this from the 1st episode and at the last, it is to reverse the list again, becasue I'm reverting it again at the end.
            all_links = [all_links[::-1][x] for x in indexes][::-1]
        else:
            all_links = all_links

        if str(sorting).lower() in ['new', 'desc', 'descending', 'latest']:
            for chap_link in all_links:
                chap_link = "http://readcomiconline.to/Comic/" + chap_link
                self.single_chapter(comic_url=chap_link, comic_name=comic_name, download_directory=download_directory,
                                    conversion=conversion, delete_files=delete_files)

        elif str(sorting).lower() in ['old', 'asc', 'ascending', 'oldest', 'a']:
            for chap_link in all_links[::-1]:
                chap_link = "http://readcomiconline.to/Comic/" + chap_link
                self.single_chapter(comic_url=chap_link, comic_name=comic_name, download_directory=download_directory,
                                    conversion=conversion, delete_files=delete_files)

        print("Finished Downloading")
        return 0
