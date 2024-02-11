#!/usr/bin/env python
# -*- coding: utf-8 -*-
import base64
from comic_dl import globalFunctions
import re
import os
import logging
import time
import platform


class ReadComicOnlineLi(object):
    def __init__(self, manga_url, download_directory, chapter_range, **kwargs):

        current_directory = kwargs.get("current_directory")
        self.manual_cookie = kwargs.get("manual_cookies", None)
        conversion = kwargs.get("conversion")
        keep_files = kwargs.get("keep_files")
        self.logging = kwargs.get("log_flag")
        self.sorting = kwargs.get("sorting_order")
        self.image_quality = kwargs.get("image_quality")
        self.comic_name = self.name_cleaner(manga_url)
        self.print_index = kwargs.get("print_index")

        url_split = str(manga_url).split("/")

        self.appended_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'en-US,en;q=0.9;q=0.8;q=0.7',
            'Sec-Ch-Ua-Platform': platform.system(),
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1'
        }

        # Sometimes, this value came out to be 6, instead of 5. Hmmmmmmmm weird.
        if len(url_split) in [5]:
            # Removing "6" from here, because it caused #47
            self.full_series(comic_url=manga_url.replace("&readType=1", ""), comic_name=self.comic_name,
                             sorting=self.sorting, download_directory=download_directory, chapter_range=chapter_range,
                             conversion=conversion, keep_files=keep_files)
        else:
            if "&readType=0" in manga_url:
                manga_url = str(manga_url).replace(
                    "&readType=0", "&readType=1")  # All Images in one page!
            # disabled to fix #132 and #145
            # elif "&readType=1" not in manga_url:
            #     manga_url = str(manga_url) + "&readType=1"  # All Images in one page!
            self.single_chapter(manga_url, self.comic_name, download_directory, conversion=conversion,
                                keep_files=keep_files)

    def single_chapter(self, comic_url, comic_name, download_directory, conversion, keep_files):
        # print("Received Comic Url : {0}".format(comic_url))
        print("Fooling CloudFlare...Please Wait...")
        if not comic_url.endswith("#1"):
            comic_url += "#1"

        if not self.appended_headers.get('cookie', None) and self.manual_cookie:
            self.appended_headers['cookie'] = self.manual_cookie
        self.appended_headers['referer'] = comic_url

        chapter_number = str(comic_url).split(
            "/")[5].split("?")[0].replace("-", " - ")

        file_directory = globalFunctions.GlobalFunctions(
        ).create_file_directory(chapter_number, comic_name)
        directory_path = os.path.realpath(
            str(download_directory) + "/" + str(file_directory))

        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

        main_directory = str(directory_path).split(os.sep)
        main_directory.pop()
        converted_file_directory = str(os.sep.join(main_directory)) + os.sep
        # For https://github.com/Xonshiz/comic-dl/issues/247
        if str(conversion) != "None":
            base_file_name = str(converted_file_directory) + "{0} - Ch {1}".format(
                globalFunctions.easySlug(comic_name), chapter_number)
            if os.path.isfile("{0}.cbz".format(base_file_name)) or os.path.isfile("{0}.pdf".format(base_file_name)):
                print('Converted File already exists. Skipping.')
                return 0

        source, cookies = globalFunctions.GlobalFunctions().page_downloader(
            manga_url=comic_url, scrapper_delay=10, append_headers=self.appended_headers)

        img_list = re.findall(r"lstImages.push\('(.+?)'",
                              str(source))

        if len(img_list) == 0:
            data_src = re.findall(r'data-src="(.*?)"', str(source))
            if len(data_src) > 0:
                img_list = data_src

        if str(self.image_quality).lower().strip() in ["low", "worst", "bad", "cancer", "mobile"]:
            print("Downloading In Low Quality...")

        links = []
        file_names = []
        img_list = self.get_image_links(img_list)

        for current_chapter, image_link in enumerate(img_list):
            image_link = str(image_link).strip().replace("\\", "")
            logging.debug("Image Link : %s" % image_link)

            if str(self.image_quality).lower().strip() in ["low", "worst", "bad", "cancer", "mobile"]:
                image_link = image_link.replace(
                    "=s0", "=s1600").replace("/s0", "/s1600")
            # Change low quality to best.
            image_link = image_link.replace(
                "=s1600", "=s0").replace("/s1600", "/s0")

            current_chapter += 1
            file_name = str(globalFunctions.GlobalFunctions().prepend_zeroes(
                current_chapter, len(img_list))) + ".jpg"

            file_names.append(file_name)
            links.append(image_link)

        globalFunctions.GlobalFunctions().multithread_download(chapter_number, comic_name, comic_url, directory_path,
                                                               file_names, links, self.logging)

        globalFunctions.GlobalFunctions().conversion(directory_path, conversion, keep_files, comic_name,
                                                     chapter_number)

        return 0

    def name_cleaner(self, url):
        initial_name = str(url).split("/")[4].strip()
        safe_name = re.sub(r"[0-9][a-z][A-Z]\ ", "", str(initial_name))
        manga_name = str(safe_name.title()).replace("-", " ")

        return manga_name

    def full_series(self, comic_url, comic_name, sorting, download_directory, chapter_range, conversion, keep_files):
        print("Fooling CloudFlare...Please Wait...")
        if not self.appended_headers.get('cookie', None) and self.manual_cookie:
            self.appended_headers['cookie'] = self.manual_cookie
        self.appended_headers['referer'] = comic_url
        source, cookies = globalFunctions.GlobalFunctions().page_downloader(
            manga_url=comic_url, scrapper_delay=10, append_headers=self.appended_headers)

        all_links = []

        listing_table = source.find_all("table", {"class": "listing"})

        for elements in listing_table:
            x = elements.findAll('a')
            for a in x:
                all_links.append(str(a['href']).strip())

        """Readcomiconline.li shows the chapters in the Descending order. The 1st chapter is at the bottom, hence, at
           the end of the list. So, we'll reverse the list, to perform the ranging functionality properly.
           This is a fix for issues like #74.
        """
        all_links.reverse()

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
                chap_link = "https://readcomiconline.li" + chap_link
                try:
                    self.single_chapter(comic_url=chap_link, comic_name=comic_name, download_directory=download_directory,
                                        conversion=conversion, keep_files=keep_files)
                    # 5 second wait before downloading next chapter. Suggestion in #261
                    time.sleep(5)
                except Exception as ex:
                    logging.error("Error downloading : %s" % chap_link)
                    break  # break to continue processing other mangas
                # if chapter range contains "__EnD__" write new value to config.json
                # @Chr1st-oo - modified condition due to some changes on automatic download and config.
                if chapter_range != "All" and (chapter_range.split("-")[1] == "__EnD__" or len(chapter_range.split("-")) == 3):
                    globalFunctions.GlobalFunctions().addOne(comic_url)

        elif str(sorting).lower() in ['old', 'asc', 'ascending', 'oldest', 'a']:
            for chap_link in all_links[::-1]:
                chap_link = "https://readcomiconline.li" + chap_link
                try:
                    self.single_chapter(comic_url=chap_link, comic_name=comic_name, download_directory=download_directory,
                                        conversion=conversion, keep_files=keep_files)
                    # 5 second wait before downloading next chapter. Suggestion in #261
                    time.sleep(5)
                except Exception as ex:
                    logging.error("Error downloading : %s" % chap_link)
                    break  # break to continue processing other mangas
                # if chapter range contains "__EnD__" write new value to config.json
                # @Chr1st-oo - modified condition due to some changes on automatic download and config.
                if chapter_range != "All" and (chapter_range.split("-")[1] == "__EnD__" or len(chapter_range.split("-")) == 3):
                    globalFunctions.GlobalFunctions().addOne(comic_url)

        return 0

    def get_image_links(self, img_list):
        import binascii

        def beau(url):
            url = url.replace("_x236", "d")
            url = url.replace("_x945", "g")

            if url.startswith("https"):
                return url

            url, sep, rest = url.partition("?")
            containsS0 = "=s0" in url
            url = url[:-3 if containsS0 else -6]
            url = url[4:22] + url[25:]
            url = url[0:-6] + url[-2:]
            url = binascii.a2b_base64(url).decode()
            url = url[0:13] + url[17:]
            url = url[0:-2] + ("=s0" if containsS0 else "=s1600")
            return "https://2.bp.blogspot.com/" + url + sep + rest

        return [beau(url) for url in img_list]
