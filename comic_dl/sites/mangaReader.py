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

        # # Total number of pages in a chapter.
        total_pages = int(str(re.search(r'</select> of (.*?)</div>', str(source)).group(1)).strip())
        # print("Total Pages : {0}".format(total_pages))

        file_directory = globalFunctions.GlobalFunctions().create_file_directory(chapter_number, comic_name)
        directory_path = os.path.realpath(str(download_directory) + "/" + str(file_directory))

        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

        globalFunctions.GlobalFunctions().info_printer(comic_name, chapter_number, total_chapters=total_pages)

        for page_number in range(1, total_pages + 1):
            # print(page_number)
            # Ex URL : http://www.mangareader.net/boku-no-hero-academia/1/Page_Number
            next_url = str(comic_url) + "/" + str(page_number)
            # print("Next URL : {0}".format(next_url))
            # Let's use the cookies we established in the main connection and maintain the session.
            next_source, next_cookies = globalFunctions.GlobalFunctions().page_downloader(manga_url=next_url,
                                                                                          cookies=cookies)
            img_holder_div = next_source.find_all('div', {'id': 'imgholder'})

            for single_node in img_holder_div:
                x = single_node.findAll('img')
                for a in x:
                    image_link = str(a['src']).strip()
                    # print("Image Link : {0}".format(image_link))
                    file_name = str(
                        globalFunctions.GlobalFunctions().prepend_zeroes(page_number, total_pages)) + ".jpg"
                    globalFunctions.GlobalFunctions().downloader(image_link, file_name,
                                                                 comic_url, directory_path, log_flag=self.logging)
        globalFunctions.GlobalFunctions().conversion(directory_path, conversion, delete_files,
                                                     comic_name, chapter_number)

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

            if str(chapter_range).split("-")[1].isdigit():
                ending = int(str(chapter_range).split("-")[1])
            else:
                ending = len(all_links)

            indexes = [x for x in range(starting, ending)]
            # [::-1] in sub_list in beginning to start this from the 1st episode and at the last,
            # it is to reverse the list again, because I'm reverting it again at the end.
            all_links = [all_links[x] for x in indexes][::-1]
        else:
            all_links = all_links

        if str(sorting).lower() in ['new', 'desc', 'descending', 'latest']:
            for chap_link in all_links:
                self.single_chapter(comic_url=chap_link, comic_name=comic_name, download_directory=download_directory,
                                    conversion=conversion, delete_files=delete_files)
                # if chapter range contains "__EnD__" write new value to config.json
                if chapter_range != "All" and chapter_range.split("-")[1] == "__EnD__":
                    globalFunctions.GlobalFunctions().addOne(comic_url)

        elif str(sorting).lower() in ['old', 'asc', 'ascending', 'oldest', 'a']:
            for chap_link in all_links[::-1]:
                self.single_chapter(comic_url=chap_link, comic_name=comic_name, download_directory=download_directory,
                                    conversion=conversion, delete_files=delete_files)
                # if chapter range contains "__EnD__" write new value to config.json
                if chapter_range != "All" and chapter_range.split("-")[1] == "__EnD__":
                    globalFunctions.GlobalFunctions().addOne(comic_url)

        print("Finished Downloading")
        return 0
