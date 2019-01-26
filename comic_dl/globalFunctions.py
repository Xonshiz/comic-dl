#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

import cfscrape
import requests
from bs4 import BeautifulSoup
import os
import shutil
import sys
import logging
import glob
import json
import img2pdf
import math
import threading
from tqdm import tqdm
is_py2 = sys.version[0] == '2'
if is_py2:
    import Queue as queue
else:
    import queue as queue


class GlobalFunctions(object):
    def page_downloader(self, manga_url, scrapper_delay=5, **kwargs):
        headers = kwargs.get("headers")
        if not headers:
            headers = {
                'User-Agent':
                    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
                'Accept-Encoding': 'gzip, deflate'
            }

        sess = requests.session()
        sess = cfscrape.create_scraper(sess, delay=scrapper_delay)

        connection = sess.get(manga_url, headers=headers, cookies=kwargs.get("cookies"))

        if connection.status_code != 200:
            print("Whoops! Seems like I can't connect to website.")
            print("It's showing : %s" % connection)
            print("Run this script with the --verbose argument and report the issue along with log file on Github.")
            raise Warning("can't connect to website %s" % manga_url)
        else:
            page_source = BeautifulSoup(connection.text.encode("utf-8"), "html.parser")
            connection_cookies = sess.cookies

            return page_source, connection_cookies

    def downloader(self, image_and_name, referer, directory_path, **kwargs):
        self.logging = kwargs.get("log_flag")
        pbar = kwargs.get("pbar")

        image_ddl = image_and_name[0]
        file_name = image_and_name[1]
        file_check_path = str(directory_path) + os.sep + str(file_name)

        logging.debug("File Check Path : %s" % file_check_path)
        logging.debug("Download File Name : %s" % file_name)

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

            sess = requests.session()
            sess = cfscrape.create_scraper(sess)
            try:
                r = sess.get(image_ddl, stream=True, headers=headers, cookies=kwargs.get("cookies"))
                r.raise_for_status()
                if r.status_code != 200:
                    pbar.write("Could not download the image.")
                    pbar.write("Link said : %s" % r.status_code)
                    pass
                else:
                    with open(file_name, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=1024):
                            if chunk:
                                f.write(chunk)
                                f.flush()

                    file_path = os.path.normpath(file_name)
                    try:
                        shutil.move(file_path, directory_path)
                    except Exception as file_moving_exception:
                        pbar.write(file_moving_exception)
                        os.remove(file_path)
                        raise file_moving_exception
            except requests.exceptions.HTTPError as errh:
                pbar.write("Http Error:")
                pbar.write(errh.message)
                raise
            except requests.exceptions.ConnectionError as errc:
                pbar.write("Error Connecting:")
                pbar.write(errc.message)
                raise
            except requests.exceptions.Timeout as errt:
                pbar.write("Timeout Error:")
                pbar.write(errt.message)
                raise
            except requests.exceptions.RequestException as err:
                pbar.write("OOps: Something Else")
                pbar.write(err.message)
                raise
            except Exception as ex:
                pbar.write("Some problem occurred while downloading this image: %s " % file_name)
                pbar.write(ex)
                raise

        pbar.update()

    def conversion(self, directory_path, conversion, keep_files, comic_name, chapter_number):
        main_directory = str(directory_path).split(os.sep)
        main_directory.pop()
        converted_file_directory = str(os.sep.join(main_directory)) + os.sep

        if str(conversion).lower().strip() in ['pdf']:
            # Such kind of lambda functions and breaking is dangerous...
            im_files = [image_files for image_files in sorted(glob.glob(str(directory_path) + "/" + "*.jpg"),
                                                              key=lambda x: int(
                                                                  str((x.split('.')[0])).split(os.sep)[-1]))]
            pdf_file_name = str(converted_file_directory) + "{0} - Ch {1}.pdf".format(comic_name, chapter_number)
            try:
                # This block is same as the one in the "cbz" conversion section. Check that one.
                if os.path.isfile(pdf_file_name):
                    print('[Comic-dl] CBZ File Exist! Skipping : {0}\n'.format(pdf_file_name))
                    pass
                else:
                    with open(pdf_file_name, "wb") as f:
                        f.write(img2pdf.convert(im_files))
                        print("Converted the file to pdf...")
            except Exception as FileWriteError:
                print("Couldn't write the pdf file...")
                print(FileWriteError)
                # Let's not delete the files if the conversion failed...
                keep_files = "False"
                pass

        elif str(conversion).lower().strip() in ['cbz']:

            cbz_file_name = str(converted_file_directory) + "{0} - Ch {1}".format(comic_name, chapter_number)
            print("CBZ File : {0}".format(cbz_file_name))

            try:
                """If the .cbz file exists, we don't need to make it again. If we do make it again, it'll make the 
                .zip file and will hit and exception about file existing already. This raised #105.
                So, to fix the #105, we'll add this check and make things work just fine."""
                if os.path.isfile(str(cbz_file_name) + ".cbz"):
                    print('[Comic-dl] CBZ File Exist! Skipping : {0}\n'.format(cbz_file_name))
                    pass
                else:
                    shutil.make_archive(cbz_file_name, 'zip', directory_path, directory_path)
                    os.rename(str(cbz_file_name) + ".zip", (str(cbz_file_name)+".zip").replace(".zip", ".cbz"))
            except Exception as CBZError:
                print("Couldn't write the cbz file...")
                print(CBZError)
                # Let's not delete the files if the conversion failed...
                keep_files = "True"
                pass

        elif str(conversion) == "None":
            pass

        else:
            print("Seems like that conversion isn't supported yet. Please report it on the repository...")
            pass

        if str(keep_files).lower().strip() in ['no', 'false', 'delete']:
            try:
                shutil.rmtree(path=directory_path, ignore_errors=True)
            except Exception as DirectoryDeleteError:
                print("Couldn't move the file or delete the directory.")
                print(DirectoryDeleteError)
                pass
            print("Deleted the files...")

    def addOne(self, comicUrl):
        # @dsanchezseco
        # edit config.json to update nextChapter value
        # @darodi
        # update based on the url value instead of the key value
        data = json.load(open('config.json'))
        for elKey in data["comics"]:
            json_url = data["comics"][elKey]["url"]
            if json_url == comicUrl or json_url == comicUrl + "/":
                data["comics"][elKey]["next"] = data["comics"][elKey]["next"] + 1
        json.dump(data, open('config.json', 'w'), indent=4)

    def prepend_zeroes(self, current_chapter_value, total_images):
        """
        :param current_chapter_value: Int value of current page number. Example : 1, 2, 3
        :param total_images: Total number of images in the
        :return:
        """
        max_digits = int(math.log10(int(total_images))) + 1
        return str(current_chapter_value).zfill(max_digits)

    def multithread_download(self, chapter_number, comic_name, comic_url, directory_path, file_names, links, log_flag,
                             pool_size=4):
        """
        :param chapter_number: string used for the progress bar
        :param comic_name: string used for the progress bar
        :param comic_url: used for the referer
        :param directory_path: used to download
        :param file_names: files names to download
        :param links: links to download
        :param log_flag: log flag
        :param pool_size: thread pool size, default = 4
        :return 0 if no error
        """

        def worker():
            while True:
                try:
                    worker_item = in_queue.get()
                    self.downloader(referer=comic_url, directory_path=directory_path, pbar=pbar, log_flag=log_flag,
                                    image_and_name=worker_item)
                    in_queue.task_done()
                except queue.Empty as ex1:
                    logging.info(ex1)
                    return
                except Exception as ex:
                    err_queue.put(ex)
                    in_queue.task_done()

        in_queue = queue.Queue()
        err_queue = queue.Queue()

        pbar = tqdm(links, leave=True, unit='image(s)', position=0)
        pbar.set_description('[Comic-dl] Downloading : %s [%s] ' % (comic_name, chapter_number))

        for i in range(pool_size):
            t = threading.Thread(target=worker)
            t.daemon = True
            t.start()

        for item in zip(links, file_names):
            in_queue.put(item)

        in_queue.join()  # block until all tasks are done

        try:
            err = err_queue.get(block=False)
            pbar.set_description('[Comic-dl] Error : %s [%s] - %s ' % (comic_name, chapter_number, err))
            raise err
        except queue.Empty:
            pbar.set_description('[Comic-dl] Done : %s [%s] ' % (comic_name, chapter_number))
            return 0
        finally:
            pbar.close()

    @staticmethod
    def create_file_directory(chapter_number, comic_name):
        comic = re.sub('[^\w\-_. \[\]]', '-', str(comic_name))
        chapter = re.sub('[^\w\-_. \[\]]', '-', str(chapter_number))
        file_directory = comic + os.sep + chapter + os.sep
        return file_directory
