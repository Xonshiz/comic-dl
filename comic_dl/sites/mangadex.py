#!/usr/bin/env python
# -*- coding: utf-8 -*-
from comic_dl import globalFunctions
import os
import logging
import json


class Mangadex(object):
    def __init__(self, manga_url, download_directory, chapter_range, **kwargs):

        current_directory = kwargs.get("current_directory")
        conversion = kwargs.get("conversion")
        keep_files = kwargs.get("keep_files")
        self.logging = kwargs.get("log_flag")
        self.sorting = kwargs.get("sorting_order")
        self.comic_name = None
        self.print_index = kwargs.get("print_index")
        # https://mangadex.org/chapter/17fd3a89-605d-4f6a-93be-71e559e0889c/4
        if "/chapter/" in manga_url:
            self.single_chapter(manga_url, self.comic_name, download_directory, conversion=conversion,
                                keep_files=keep_files)
        else:
            # https://mangadex.org/title/19465f6a-1c11-4179-891e-68293402b883/seton-academy-join-the-pack
            self.full_series(manga_url, self.comic_name, self.sorting, download_directory, chapter_range=chapter_range,
                             conversion=conversion, keep_files=keep_files)

    def single_chapter(self, comic_url, comic_name, download_directory, conversion, keep_files, volume=None):
        comic_url = str(comic_url)
        chapter_split = comic_url.split('/')
        chapter_id = chapter_split[-2] if len(chapter_split) > 5 else chapter_split[-1]
        links = []
        file_names = []
        chapter_number = chapter_id
        # Get image info
        # https://api.mangadex.org/at-home/server/17fd3a89-605d-4f6a-93be-71e559e0889c?forcePort443=false
        api_images = "https://api.mangadex.org/at-home/server/{0}?forcePort443=false".format(chapter_id)
        source_image_list, cookies = globalFunctions.GlobalFunctions().page_downloader(manga_url=api_images)
        # Get chapter info
        api_chapter_info = "https://api.mangadex.org/chapter/{0}?includes[]=scanlation_group&includes[]=manga&includes[]=user".format(chapter_id)
        source_chapter_info, cookies = globalFunctions.GlobalFunctions().page_downloader(manga_url=api_chapter_info)
        source_chapter_info = json.loads(str(source_chapter_info))
        image_info = json.loads(str(source_image_list))
        base_image_url = image_info['baseUrl']
        base_hash = image_info['chapter']['hash']
        images = image_info['chapter']['data']
        for idx, image in enumerate(images):
            links.append("{0}/data/{1}/{2}".format(base_image_url, base_hash, image))
            img_extension = str(image).rsplit('.', 1)[-1]
            file_names.append('{0}.{1}'.format(idx, img_extension))
        if source_chapter_info:
            chapter_number = source_chapter_info['data']['attributes']['chapter']
            for relation in source_chapter_info['data']['relationships']:
                if self.comic_name:
                    break
                if relation['type'] == "manga":
                    try:
                        self.comic_name = relation['attributes']['title']['en']
                        break
                    except Exception as NameNotFound:
                        dict_obj = dict(relation['attributes']['title'])
                        for key in dict_obj.keys():
                            self.comic_name = dict_obj[key]
                            # We'll take the first one that comes and break out of this loop
                            break
        else:
            self.comic_name = chapter_id
        file_directory = globalFunctions.GlobalFunctions().create_file_directory(chapter_number, self.comic_name)
        if volume:
            file_directory = file_directory.rsplit(os.sep, 2)[0]
            file_directory = globalFunctions.GlobalFunctions().create_file_directory(chapter_number, file_directory + os.sep + volume, os.sep)
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
        comic_id = str(comic_url).rsplit('/', 2)[-2]
        comic_detail_url = "https://api.mangadex.org/manga/{0}/aggregate?translatedLanguage[]=en".format(comic_id)
        source, cookies = globalFunctions.GlobalFunctions().page_downloader(manga_url=comic_detail_url)
        source = json.loads(str(source))

        all_links = []
        all_volumes = {}
        volumes = dict(source['volumes'])
        for volume in volumes.keys():
            volume_info = dict(volumes[volume])
            chapters = dict(volume_info.get('chapters', {}))
            for chapter in chapters.keys():
                chapter = dict(chapters[chapter])
                # https://mangadex.org/chapter/17fd3a89-605d-4f6a-93be-71e559e0889c/4
                chapter_url = "https://mangadex.org/chapter/{0}/{1}".format(chapter.get('id'), chapter.get('chapter', 1))
                all_links.append(chapter_url)
                all_volumes[chapter_url] = "Volume {0}".format(volume)





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
                                        conversion=conversion, keep_files=keep_files,
                                        volume=all_volumes.get(chap_link))
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
                                        conversion=conversion, keep_files=keep_files,
                                        volume=all_volumes.get(chap_link))
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
