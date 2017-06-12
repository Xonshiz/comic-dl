#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cfscrape
import requests
from bs4 import BeautifulSoup
from clint.textui import progress
import os
import shutil
import sys
import logging


class GlobalFunctions(object):
    def page_downloader(self, manga_url, **kwargs):
        headers = {
            'User-Agent':
                'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate'
        }

        sess = requests.session()
        sess = cfscrape.create_scraper(sess)

        connection = sess.get(manga_url, headers=headers, cookies=kwargs.get("cookies"))
        if connection.status_code != 200:
            print("Whoops! Seems like I can't connect to website.")
            print("It's showing : %s" % connection)
            print("Run this script with the --verbose argument and report the issue along with log file on Github.")
            sys.exit(1)
        else:
            page_source = BeautifulSoup(connection.text.encode("utf-8"), "html.parser")
            connection_cookies = sess.cookies

            return (page_source, connection_cookies)

    def downloader(self, image_ddl, file_name, referer, directory_path, **kwargs):
        self.logging = kwargs.get("log_flag")

        file_check_path = str(directory_path) + '/' + str(file_name)
        logging.debug("File Check Path : %s" % file_check_path)
        logging.debug("Download File Name : %s" % file_name)

        if os.path.isfile(file_check_path):
            print('[Comic-dl] File Exist! Skipping : %s\n' % file_name)
            pass

        if not os.path.isfile(file_check_path):
            print('[Comic-dl] Downloading : %s' % file_name)

            headers = {
                'User-Agent':
                    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
                'Accept-Encoding': 'gzip, deflate',
                'Referer': referer
            }

            sess = requests.session()
            sess = cfscrape.create_scraper(sess)
            try:
                r = sess.get(image_ddl, stream=True, headers=headers, cookies=kwargs.get("cookies"))

                if r.status_code != 200:
                    print("Could not download the image.")
                    print("Link said : %s" % r.status_code)
                    pass
                else:
                    with open(file_name, 'wb') as f:
                        total_length = r.headers.get('content-length')
                        # raw.senmanga doesn't return content-length. So, let's just assume 1024.
                        if total_length is None:
                            total_length = 1024

                        for chunk in progress.bar(r.iter_content(chunk_size=1024),
                                                  expected_size=(int(total_length) / 1024) + 1,
                                                  hide=False):
                            if chunk:
                                f.write(chunk)
                                f.flush()

                    file_path = os.path.normpath(file_name)
                    try:
                        shutil.move(file_path, directory_path)
                    except Exception as FileMovingException:
                        print(FileMovingException)
                        os.remove(file_path)
                        pass
            except Exception as Ex:
                print("Some problem occurred while downloading this image")
                print(Ex)
                pass

    def info_printer(self, anime_name, episode_number, **kwargs):
        if not kwargs.get("volume_number"):
            print("\n")
            print('{:^80}'.format('====================================================================='))
            # print('{:^80}'.format("%s - %s" % (anime_name, episode_number)))
            print('{:^80}'.format("Manga Name : %s" % anime_name))
            print('{:^80}'.format("Chapter Number - %s" % episode_number))
            print('{:^80}'.format('=====================================================================\n'))
