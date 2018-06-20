#!/usr/bin/env python
# -*- coding: utf-8 -*-

import globalFunctions
import re
import os

from multiprocessing.dummy import Pool as ThreadPool 
from functools import partial

class ReadComicBooksOnline():
    def __init__(self, manga_url, download_directory, chapter_range, **kwargs):
        current_directory = kwargs.get("current_directory")
        conversion = kwargs.get("conversion")
        delete_files = kwargs.get("delete_files")
        self.logging = kwargs.get("log_flag")
        self.sorting = kwargs.get("sorting_order")
        self.comic_name = self.name_cleaner(manga_url)

        if "/reader/" in manga_url:
            # http://readcomicbooksonline.net/reader/Batwoman_2017/Batwoman_(2017)_1
            if str(manga_url).split("/")[-1]:
                self.single_chapter(manga_url, self.comic_name, download_directory,
                                    conversion=conversion, delete_files=delete_files)
            else:
                manga_url = str(manga_url).replace("/reader/", "/").lower().replace("_", "-")

                self.full_series(comic_url=manga_url, comic_name=self.comic_name,
                                 sorting=self.sorting, download_directory=download_directory,
                                 chapter_range=chapter_range,
                                 conversion=conversion, delete_files=delete_files)
        else:
            self.full_series(comic_url=manga_url, comic_name=self.comic_name,
                             sorting=self.sorting, download_directory=download_directory, chapter_range=chapter_range,
                             conversion=conversion, delete_files=delete_files)

    def name_cleaner(self, url):
        manga_name = ""
        try:
            manga_name = str(str(url).split("/")[4].strip().replace("_", " ").replace("-", " ").title())
        except:
            manga_name = str(str(url).split("/")[3].strip().replace("_", " ").replace("-", " ").title())
        return manga_name

    def single_chapter(self, comic_url, comic_name, download_directory, conversion, delete_files):
        chapter_number = int(str(comic_url).replace("/", "").split("_")[-1].strip())
        source, cookies = globalFunctions.GlobalFunctions().page_downloader(manga_url=comic_url)
        try:
            first_image_link = "http://readcomicbooksonline.net/reader/mangas" \
                               + str(re.search(r'src="mangas(.*?)\"', str(source)).group(1)).replace(" ", "%20")
        except:
            print("Seems like this page doesn't Exist.")
            print("Or, there's some issue. Open a new 'ISSUE' on Github.")
            return 1
        last_page_number = int(str(re.search(r'</select> of (.*?) <a', str(source)).group(1)).strip())
        img_list = []
        img_list.append(first_image_link)

        for page_number in range(1, last_page_number):
            image_number = first_image_link[-7:].replace(".jpg", "").replace(".png", "").strip()
            image_number_string = str(int(image_number) + 1).zfill(3) + ".jpg"
            image_download_link = first_image_link.replace(image_number + ".jpg", image_number_string)
            first_image_link = image_download_link
            img_list.append(image_download_link)

        file_directory = str(comic_name) + '/' + str(chapter_number) + "/"
        file_directory = file_directory.replace(":", "-")
        directory_path = os.path.realpath(str(download_directory) + "/" + str(file_directory))

        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

        globalFunctions.GlobalFunctions().info_printer(comic_name, chapter_number, total_chapters=len(img_list))

        links = []
        file_names = []
        for current_chapter, image_link in enumerate(img_list):
            current_chapter += 1
            file_name = str(globalFunctions.GlobalFunctions().prepend_zeroes(current_chapter, len(img_list))) + ".jpg"
            file_names.append(file_name)
            links.append(image_link)

        pool = ThreadPool(4)
        pool.map(partial(globalFunctions.GlobalFunctions().downloader, referer=comic_url, directory_path=directory_path), zip(links,file_names))
            
        globalFunctions.GlobalFunctions().conversion(directory_path, conversion, delete_files, comic_name,
                                                     chapter_number)

        return 0

    def full_series(self, comic_url, comic_name, sorting, download_directory, chapter_range, conversion, delete_files):
        source, cookies = globalFunctions.GlobalFunctions().page_downloader(manga_url=comic_url)
        all_links = []
        chap_holder_div = source.find_all('div', {'id': 'chapterlist'})
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

        if str(sorting).lower() in ['new', 'desc', 'descending', 'latest']:
            for chap_link in all_links:
                try:
                    self.single_chapter(comic_url=chap_link, comic_name=comic_name,
                                        download_directory=download_directory,
                                        conversion=conversion, delete_files=delete_files)
                    # if chapter range contains "__EnD__" write new value to config.json
                    if chapter_range.split("-")[1] == "__EnD__":
                        globalFunctions.GlobalFunctions().addOne(comic_url)
                except Exception as e:
                    pass

        elif str(sorting).lower() in ['old', 'asc', 'ascending', 'oldest', 'a']:
            for chap_link in all_links[::-1]:
                try:
                    self.single_chapter(comic_url=chap_link, comic_name=comic_name,
                                        download_directory=download_directory,
                                        conversion=conversion, delete_files=delete_files)
                    # if chapter range contains "__EnD__" write new value to config.json
                    if chapter_range.split("-")[1] == "__EnD__":
                        globalFunctions.GlobalFunctions().addOne(comic_url)
                except Exception as e:
                    pass

        print("Finished Downloading")
        return 0
