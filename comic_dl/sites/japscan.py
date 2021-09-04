#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re

import cloudscraper
from comic_dl import globalFunctions
from PIL import Image
from bs4 import BeautifulSoup
from tqdm import tqdm

JAPSCAN_URL = 'https://www.japscan.to'


class Japscan():

    def __init__(self, manga_url, download_directory, chapter_range, **kwargs):
        self.scraper = cloudscraper.create_scraper()
        conversion = kwargs.get("conversion")
        keep_files = kwargs.get("keep_files")
        self.logging = kwargs.get("log_flag")
        self.sorting = kwargs.get("sorting_order")
        self.manga_url = manga_url + '/'
        self.print_index = kwargs.get("print_index")

        if 'manga' in manga_url:
            self.comic_id = str(str(manga_url).split("/")[-1])
            self.full_series(comic_id=self.comic_id, sorting=self.sorting, download_directory=download_directory,
                             chapter_range=chapter_range, conversion=conversion, keep_files=keep_files)

        if 'lecture-en-ligne' in manga_url:
            self.comic_id = str(str(manga_url).split("/")[-2])
            chapter_path = re.sub(re.compile(r'.*japscan.to'), '', str(self.manga_url))
            self.single_chapter(chapter_path, comic_id=self.comic_id, download_directory=download_directory,
                                scraper=scraper)

    def full_series(self, comic_id, sorting, download_directory, chapter_range, conversion, keep_files):
        scraper = self.scraper
        content = scraper.get(self.manga_url).content
        chapter_divs = BeautifulSoup(content, features='lxml').findAll('div', {
            'class': 'chapters_list'})

        starting, ending = self.compute_start_end(chapter_divs, chapter_range)

        if self.print_index:
            idx = 0
            for chap_link in chapter_divs[::-1]:
                idx = idx + 1
                print(str(idx) + ": " + re.sub('[\t\r\n]', '', chap_link.find('a').getText()))
            return 0

        for chapter_div in chapter_divs[::-1][starting-1:ending]:
            chapter_path = chapter_div.find(href=True)['href']
            try:
                self.single_chapter(chapter_path, comic_id, download_directory)
            except Exception as ex:
                break  # break to continue processing other mangas
            # @Chr1st-oo - modified condition due to some changes on automatic download and config.
            if chapter_range != "All" and (chapter_range.split("-")[1] == "__EnD__" or len(chapter_range.split("-")) == 3):
                globalFunctions.GlobalFunctions().addOne(self.manga_url)

        return 0

    @staticmethod
    def compute_start_end(chapter_divs, chapter_range):
        if chapter_range != "All":
            starting = int(str(chapter_range).split("-")[0])
            total_chapters = len(chapter_divs)
            if str(chapter_range).split("-")[1].isdigit():
                ending = int(str(chapter_range).split("-")[1])
            else:
                ending = total_chapters

            if ending > total_chapters:
                ending = total_chapters
        else:
            starting = 1
            ending = len(chapter_divs)
        return starting, ending

    def single_chapter(self, chapter_path, comic_id, download_directory):
        scraper = self.scraper
        chapter_url = JAPSCAN_URL + chapter_path
        chapter_name = chapter_path.split('/')[-2]
        pages = BeautifulSoup(scraper.get(chapter_url).content, features='lxml').find('select', {'id': 'pages'})
        page_options = pages.findAll('option', value=True)

        file_directory = globalFunctions.GlobalFunctions().create_file_directory(chapter_name, comic_id)
        directory_path = os.path.realpath(str(download_directory) + "/" + str(file_directory))
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

        links = []
        file_names = []
        pbar = tqdm(page_options, leave=True, unit='image(s)', position=0)
        pbar.set_description('[Comic-dl] Downloading : %s [%s] ' % (comic_id, chapter_name))
        for page_tag in page_options:
            page_url = JAPSCAN_URL + page_tag['value']
            page = BeautifulSoup(scraper.get(page_url).content, features='lxml')
            image_url = page.find('div', {'id': 'image'})['data-src']
            links.append(image_url)
            file_name = image_url.split("/")[-1]
            file_names.append(file_name)
            # pbar = tqdm([image_url], leave=True, unit='image(s)', position=0)
            self.download_image(referer=image_url, directory_path=directory_path, pbar=pbar, image_url=image_url,
                                file_name=file_name)

    def download_image(self, image_url, file_name, referer, directory_path, pbar):

        unscramble = False
        if 'clel' in image_url:
            unscramble = True

        file_check_path = str(directory_path) + os.sep + str(file_name)
        if os.path.isfile(file_check_path):
            pbar.write('[Comic-dl] File Exist! Skipping : %s\n' % file_name)
            pass

        if not os.path.isfile(file_check_path):
            headers = {
                'User-Agent':
                    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
                'Accept-Encoding': 'gzip, deflate',
                'Referer': referer
            }

            image_content = self.scraper.get(image_url, headers=headers).content

            if unscramble is True:
                scrambled_image = file_check_path + '_scrambled'
            else:
                scrambled_image = file_check_path

            file = open(scrambled_image, 'wb')
            file.write(image_content)
            file.close()

            if unscramble is True:
                self.unscramble_image(scrambled_image, file_check_path)
                os.remove(scrambled_image)

        pbar.update()

    def unscramble_image(self, scrambled_image, image_full_path):
        input_image = Image.open(scrambled_image)
        temp = Image.new("RGB", input_image.size)
        output_image = Image.new("RGB", input_image.size)
        for x in range(0, input_image.width, 200):
            col1 = input_image.crop((x, 0, x + 100, input_image.height))
            if (x + 200) <= input_image.width:
                col2 = input_image.crop((x + 100, 0, x + 200, input_image.height))
                temp.paste(col1, (x + 100, 0))
                temp.paste(col2, (x, 0))
            else:
                col2 = input_image.crop((x + 100, 0, input_image.width, input_image.height))
                temp.paste(col1, (x, 0))
                temp.paste(col2, (x + 100, 0))
        for y in range(0, temp.height, 200):
            row1 = temp.crop((0, y, temp.width, y + 100))
            if (y + 200) <= temp.height:
                row2 = temp.crop((0, y + 100, temp.width, y + 200))
                output_image.paste(row1, (0, y + 100))
                output_image.paste(row2, (0, y))
            else:
                row2 = temp.crop((0, y + 100, temp.width, temp.height))
                output_image.paste(row1, (0, y))
                output_image.paste(row2, (0, y + 100))
        output_image.save(image_full_path)
