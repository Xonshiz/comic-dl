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
import glob
import img2pdf


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

            return page_source, connection_cookies

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

    def conversion(self, directory_path, conversion, delete_files, comic_name, chapter_number):

        if str(conversion).lower().strip() in ['pdf']:
            # Such kind of lambda functions and breaking is dangerous...
            im_files = [image_files for image_files in sorted(glob.glob(str(directory_path) + "/" + "*.jpg"),
                                                              key=lambda x: int(
                                                                  str((x.split('.')[0])).split("\\")[-1]))]
            pdf_file_name = "{0} - Ch {1}.pdf".format(comic_name, chapter_number)
            try:
                with open(str(directory_path) + "/" + str(pdf_file_name), "wb") as f:
                    f.write(img2pdf.convert(im_files))
                    print("Converted the file to pdf...")
            except Exception as FileWriteError:
                print("Coudn't write the pdf file...")
                print(FileWriteError)
                # Let's not delete the files if the conversion failed...
                delete_files = "No"
                pass
            try:
                self.conversion_cleaner(file_path=str(directory_path) + "/" + str(pdf_file_name))
            except Exception as FileMoveError:
                print("Could not move the pdf file.")
                print(FileMoveError)
                pass

        elif str(conversion).lower().strip() in ['cbz']:
            # Such kind of lambda functions and breaking is dangerous...

            main_directory = str(directory_path).split('\\')
            main_directory.pop()
            cbz_directory = str('\\'.join(main_directory)) + '\\'

            cbz_file_name = str(cbz_directory) + "{0} - Ch {1}".format(comic_name, chapter_number)

            try:
                shutil.make_archive(cbz_file_name, 'zip', directory_path)
                os.rename(str(cbz_file_name) + ".zip", str(cbz_file_name).replace(".zip", ".cbz"))
            except Exception as CBZError:
                print("Coudn't write the cbz file...")
                print(CBZError)
                # Let's not delete the files if the conversion failed...
                delete_files = "No"
                pass
            try:
                self.conversion_cleaner(file_path=str(directory_path))
            except Exception as FileMoveError:
                print("Could not move the pdf file.")
                print(FileMoveError)
                pass

        elif str(conversion) == "None":
            pass
        else:
            print("Seems like that conversion isn't supported yet. Please report it on the repository...")
            pass

        if str(delete_files).lower().strip() in ['no', 'false', 'delete']:
            for image_files in glob.glob(str(directory_path) + "/" + "*.jpg"):
                try:
                    os.remove(image_files)
                except Exception as FileDeleteError:
                    print("Couldn't delete the image file...")
                    print(FileDeleteError)
                    pass
            print("Deleted the files...")

    def conversion_cleaner(self, file_path):
        print("Cleaning Up...")
        path_breaker = str(file_path).split("/")

        path_breaker.pop()
        old_path = '/'.join(path_breaker)

        path_breaker = str(old_path).split("\\")
        path_breaker.pop()
        new_path = str('/'.join(path_breaker)) + "/"

        try:
            shutil.move(file_path, new_path)
            shutil.rmtree(old_path)
        except Exception as FileDeleteError:
            print("Couldn't move the file or delete the directory.")
            print(FileDeleteError)
            pass
