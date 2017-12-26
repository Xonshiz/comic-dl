#!/usr/bin/env python
# -*- coding: utf-8 -*-

import globalFunctions
import re
import os
import logging


class MangaReader():
    def __init__(self, manga_url, download_directory, chapter_range, **kwargs):
        current_directory = kwargs.get("current_directory")
        conversion = kwargs.get("conversion")
        delete_files = kwargs.get("delete_files")
        self.logging = kwargs.get("log_flag")
        self.sorting = kwargs.get("sorting_order")
        self.comic_name = self.name_cleaner(manga_url)

        """The URLs don't have any keyword that distinguish the URL from being a "Chapter" or "All Chapter" page.
        So, we're going to break the url down and see if the "4th" character after "/".split() is NONE or not.
        """
        # print(str(manga_url).split("/"))
        # print(len(str(manga_url).split("/")))

        splitter = list(str(manga_url).split("/"))
        if len(splitter) == 4:
            # If the link points to a particular chapter, there should be 5 elements at least.
            # Case fo No "/" at the end of the URL.
            fourth_character = False

        elif len(splitter) == 5:
            # If the link points to listing page, but has "/" at the end, it'll still make 5 elements.
            # "/" is at the end, so we get 5 elements in the list with last element being empty.
            if not splitter[-1]:
                # The last 5th element is empty. Hence, we got listing.
                fourth_character = False
            else:
                # We have a number in the last element. Hence, single chapter
                fourth_character = True
        else:
            # Oh well, let's try the full chapter download.
            fourth_character = False

        if not fourth_character:
            # There's no "chapter number", hence, this is the listing page with all the chapters listed.
            self.full_series(comic_url=manga_url, comic_name=self.comic_name,
                             sorting=self.sorting, download_directory=download_directory, chapter_range=chapter_range,
                             conversion=conversion, delete_files=delete_files)
        else:
            self.single_chapter(manga_url, self.comic_name, download_directory, conversion=conversion,
                                delete_files=delete_files)

    def name_cleaner(self, url):
        return str(str(url).split("/")[3].strip().replace("-", " ").title())

    def single_chapter(self, comic_url, comic_name, download_directory, conversion, delete_files):
        chapter_number = int(str(comic_url).split("/")[4])
        source, cookies = globalFunctions.GlobalFunctions().page_downloader(manga_url=comic_url)

        """While inspecting this website, I found something cool. We don't have to traverse each and every page to
        get the next image link. They're incrementing the image file number by "6". For Example :
        Manga Name : http://www.mangareader.net/shingeki-no-kyojin/100
        1st Image : http://i998.mangareader.net/shingeki-no-kyojin/100/shingeki-no-kyojin-10120141.jpg
        2nd Image : http://i998.mangareader.net/shingeki-no-kyojin/100/shingeki-no-kyojin-10120147.jpg
        3rd Image : http://i999.mangareader.net/shingeki-no-kyojin/100/shingeki-no-kyojin-10120153.jpg
        4th Image : http://i999.mangareader.net/shingeki-no-kyojin/100/shingeki-no-kyojin-10120159.jpg
        
        Check the increment of 6.
        """
        # Total number of pages in a chapter.
        total_pages = int(str(re.search(r'</select> of (.*?)</div>', str(source)).group(1)).strip())

        img_list = []
        image_link = ""

        img_holder_div = source.find_all('div', {'id': 'imgholder'})

        for single_node in img_holder_div:
            x = single_node.findAll('img')
            for a in x:
                image_link = str(a['src']).strip()
        # print(image_link)
        img_list.append(str(image_link).strip())
        for image_count in range(1, total_pages):
            image_link = self.link_builder(image_link)
            img_list.append(image_link)

        file_directory = str(comic_name) + '/' + str(chapter_number) + "/"

        directory_path = os.path.realpath(str(download_directory) + "/" + str(file_directory))

        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

        globalFunctions.GlobalFunctions().info_printer(comic_name, chapter_number)

        for image_link in img_list:
            globalFunctions.GlobalFunctions().downloader(image_link, str(int(img_list.index(image_link)) + 1) + ".jpg",
                                                         comic_url, directory_path,
                                                         log_flag=self.logging)

        globalFunctions.GlobalFunctions().conversion(directory_path, conversion, delete_files, comic_name,
                                                     chapter_number)

    def link_builder(self, link):
        file_name = str(link.replace(".jpg", "")).split("-")[-1]

        return str(link).replace("-{0}.".format(file_name), "-" + str(int(file_name) + 6) + ".")

    def full_series(self, comic_url, comic_name, sorting, download_directory, chapter_range, conversion, delete_files):
        source, cookies = globalFunctions.GlobalFunctions().page_downloader(manga_url=comic_url)
        all_links = []

        chap_holder_div = source.find_all('table', {'id': 'listing'})

        for single_node in chap_holder_div:
            x = single_node.findAll('a')
            for a in x:
                all_links.append("http://www.mangareader.net" + str(a['href']).strip())
        logging.debug("all_links : %s" % all_links)

        if chapter_range != "All":
            # -1 to shift the episode number accordingly to the INDEX of it. List starts from 0 xD!
            starting = int(str(chapter_range).split("-")[0]) - 1

            if (str(chapter_range).split("-")[1]).decode().isdecimal():
                ending = int(str(chapter_range).split("-")[1])
            else:
                ending = len(all_links)

            indexes = [x for x in range(starting, ending)]
            # [::-1] in sub_list in beginning to start this from the 1st episode and at the last,
            # it is to reverse the list again, becasue I'm reverting it again at the end.
            all_links = [all_links[::-1][x] for x in indexes][::-1]
        else:
            all_links = all_links

        if str(sorting).lower() in ['new', 'desc', 'descending', 'latest']:
            for chap_link in all_links:
                self.single_chapter(comic_url=chap_link, comic_name=comic_name, download_directory=download_directory,
                                    conversion=conversion, delete_files=delete_files)

        elif str(sorting).lower() in ['old', 'asc', 'ascending', 'oldest', 'a']:
            for chap_link in all_links[::-1]:
                self.single_chapter(comic_url=chap_link, comic_name=comic_name, download_directory=download_directory,
                                    conversion=conversion, delete_files=delete_files)

        print("Finished Downloading")
        return 0
