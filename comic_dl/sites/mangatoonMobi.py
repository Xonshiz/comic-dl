#!/usr/bin/env python
# -*- coding: utf-8 -*-
from comic_dl import globalFunctions
import os
import logging


class MangatoonMobi(object):
    def __init__(self, manga_url, download_directory, chapter_range, **kwargs):

        current_directory = kwargs.get("current_directory")
        conversion = kwargs.get("conversion")
        keep_files = kwargs.get("keep_files")
        self.logging = kwargs.get("log_flag")
        self.sorting = kwargs.get("sorting_order")
        self.comic_name = None
        self.print_index = kwargs.get("print_index")
        # https://mangatoon.mobi/en/watch/1632209/114816
        if "/watch/" in manga_url:
            self.single_chapter(manga_url, self.comic_name, download_directory, conversion=conversion,
                                keep_files=keep_files)
        else:
            # https://mangatoon.mobi/en/the-call-animals?content_id=1632209
            self.full_series(manga_url, self.comic_name, self.sorting, download_directory, chapter_range=chapter_range,
                             conversion=conversion, keep_files=keep_files)

    def single_chapter(self, comic_url, comic_name, download_directory, conversion, keep_files):
        comic_url = str(comic_url)
        # https://mangatoon.mobi/en/watch/1632209/114816
        chapter_number = comic_url.rsplit('/', 1)[-1]
        links = []
        file_names = []
        source, cookies = globalFunctions.GlobalFunctions().page_downloader(manga_url=comic_url)
        title = source.find_all("div", {"class": "title"})
        if len(title) > 0:
            self.comic_name = title[0].text.strip()
        else:
            self.comic_name = comic_url.rsplit('/', 2)[-2]
        image_holder_divs = source.find_all("div", {"style": "position: relative;"})
        if len(image_holder_divs) > 0:
            for idx, img_tag in enumerate(image_holder_divs):
                x = img_tag.findAll('img')
                for a in x:
                    if "/icon/" not in a['src']:
                        img_url = a['src']
                        links.append(str(img_url).strip())
                        img_extension = str(img_url).rsplit('.', 1)[-1]
                        file_names.append('{0}.{1}'.format(idx, img_extension))
        file_directory = globalFunctions.GlobalFunctions().create_file_directory(chapter_number, self.comic_name)

        directory_path = os.path.realpath(str(download_directory) + "/" + str(file_directory))

        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
        globalFunctions.GlobalFunctions().multithread_download(chapter_number, self.comic_name, comic_url,
                                                               directory_path,
                                                               file_names, links, self.logging)

        globalFunctions.GlobalFunctions().conversion(directory_path, conversion, keep_files, self.comic_name,
                                                     chapter_number)

        return 0

    def full_series(self, comic_url, comic_name, sorting, download_directory, chapter_range, conversion, keep_files):
        source, cookies = globalFunctions.GlobalFunctions().page_downloader(manga_url=comic_url)

        all_links = []
        all_chapter_links = source.find_all("a", {"class": "episode-item-new"})
        for chapter in all_chapter_links:
            chapter_url = "https://mangatoon.mobi{0}".format(chapter['href'])
            all_links.append(chapter_url)

        logging.debug("All Links : {0}".format(all_links))

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
