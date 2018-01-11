#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __version__ import __version__
import argparse
import logging
import sys
import platform
import honcho
import os
import time
import json
import manga_eden
from manga_eden import mangaChapters
from manga_eden import mangaChapterDownload
from manga_eden import mangaSearch


class ComicDL(object):
    def __init__(self, argv):
        parser = argparse.ArgumentParser(description='Comic_dl is a command line tool to download comics and manga '
                                                     'from various such sites.')

        parser.add_argument('--version', action='store_true', help='Shows version and exits.')
        parser.add_argument('-s', '--sorting', nargs=1, help='Decides downloading order of chapters.')
        parser.add_argument('-dd', '--download-directory', nargs=1,
                            help='Decides the download directory of the comics/manga.')
        parser.add_argument('-rn', '--range', nargs=1,
                            help='Specifies the range of chapters to download.', default='All')
        parser.add_argument('--convert', nargs=1,
                            help='Tells the script to convert the downloaded Images to PDF or anything else.')
        parser.add_argument('--keep', nargs=1,
                            help='Tells the script whether to keep the files after conversion or not.',
                            default=['True'])
        parser.add_argument('--quality', nargs=1,
                            help='Tells the script which Quality of image to download (High/Low).', default='True')

        parser.add_argument('-i', '--input', nargs=1, help='Inputs the URL to anime.')

        parser.add_argument('-find', '--search', nargs=1, help='Searches for a manga through the Manga Eden Database.')

        parser.add_argument('-ml', '--manga-language', nargs=1,
                            help='Selects the language for manga.', default='0')

        parser.add_argument('-sc', '--skip-cache', nargs=1,
                            help='Forces to skip cache checking.', default='0')

        parser.add_argument('-cid', '--chapter-id', nargs=1,
                            help='Takes the Chapter ID to list all the chapters in a Manga.')

        parser.add_argument('-pid', '--page-id', nargs=1,
                            help='Takes the Page ID to download a particular "chapter number" of a manga.')

        parser.add_argument("-fd", "--force-download", help="Forces download of chapters, when using comic-dl's"
                                                            " search function.",
                            action="store_true")

        parser.add_argument('-p', '--password', nargs=1,
                            help='Takes Password used to log into a website, along with a username/email.',
                            default=['None'])

        parser.add_argument('-u', '--username', nargs=1,
                            help='Takes username/email used to log into a website, along with a password.',
                            default=['None'])

        parser.add_argument("-v", "--verbose", help="Prints important debugging messages on screen.",
                            action="store_true")
        parser.add_argument("--config-make", help="Prints important debugging messages on screen.",
                            action="store_true")

        parser.add_argument("--auto-download", help="Prints important debugging messages on screen.",
                            action="store_true")

        logger = False
        chapters_to_update = {}

        args = parser.parse_args()

        if args.version:
            self.version()
            sys.exit()

        if args.verbose:
            print("\n***Starting the script in Verbose Mode***\n")
            try:
                os.remove("Error_Log.log")
            except Exception as VerboseError:
                print(VerboseError)
                pass
            logging.basicConfig(format='%(levelname)s: %(message)s', filename="Error_Log.log", level=logging.DEBUG)
            logging.debug("Arguments Provided : %s" % args)
            logging.debug("Operating System : %s - %s - %s" % (platform.system(),
                                                               platform.release(),
                                                               platform.version()
                                                               ))
            logging.debug("Python Version : %s (%s)" % (platform.python_version(), platform.architecture()[0]))
            logger = True

        if args.config_make:
            print("\n***Making Config File***\n")

            config_data = {}
            chapters_dict = {}
            chapters_to_update_list = []
            cache_conversion_type = None
            cache_default_download = None
            more_chapter = True

            try:
                config_data = self.config_reader()
                cache_conversion_type = config_data["conversion_type"]
                cache_default_download = config_data["default_download_location"]
                chapters_dict = config_data["chapter_update"][0]
            except Exception as NoConfigFile:
                pass

            """Since Python 2 takes string inputs from raw_input and python 3 has input() method for every input,
            let's overwrite the input() for python 2. This will ensure that this code works on both, P2 and P3.
            """
            input = None
            try:
                input = raw_input
            except NameError:
                print("Cannot take input")
                pass

            conversion_type = input("In which format do you want to convert? (Leave blank, if not intended) : ")
            # If user doesn't want to convert, save "none" instead.
            config_data["conversion_type"] = ("None" if not cache_conversion_type else cache_conversion_type) if not conversion_type else str(conversion_type).strip().lower()

            # If no default download given, then use the current working directory as default.
            default_download = input("Default Download Location : ")
            config_data["default_download_location"] = (str(os.path.abspath(os.getcwd())) if not cache_default_download
                                                        else cache_default_download) if not default_download else str(
                os.path.abspath(default_download)).strip().lower()

            query_prompt = input("Do you want to add Manga/Comic in the update list? : ")

            if str(query_prompt).strip().lower() in ['true', 'yes', 'y']:
                more_chapter = True
            else:
                more_chapter = False

            while more_chapter:
                chapter_url = input("Enter URL of the chapter : ")
                download_directory = input("Enter download directory (Leave blank, if default needed) : ")
                chapters_dict[str(chapter_url).strip()] = config_data[
                    "default_download_location"] if not download_directory else download_directory

                query_prompt = input("Do you want to add more? : ")
                if str(query_prompt).strip().lower() in ['true', 'yes', 'y']:
                    more_chapter = True
                else:
                    more_chapter = False

            chapters_to_update_list.append(chapters_dict)

            config_data["chapter_update"] = chapters_to_update_list

            try:
                with open("comic_dl_config.config", "wb")  as config_file:
                    config_file.write(json.dumps(config_data))
                print("Successfully Wrote The Config File...")
            except Exception as WriteError:
                print("Couldn't write the config file. Additionally, this error was thrown : ")
                print(WriteError)
                pass

            sys.exit(0)  # No need to move forward. Make  the config file and be done with it.

        if args.search:
            start_time = time.time()
            mangaSearch.MangaSearch(search_string=str(args.search[0]),
                                    manga_language=args.manga_language[0], skip_cache=args.skip_cache[0])

            end_time = time.time()
            total_time = end_time - start_time

            print("Total Time Taken To Search : %s" % total_time)
            print("API Provided By Manga Eden : http://www.mangaeden.com/")
            sys.exit()

        if args.chapter_id:
            force_download = False

            if args.force_download:
                force_download = True
            if type(args.range) == list:
                args.range = args.range[0]
            if not args.sorting:
                args.sorting = ["ascending"]
            elif args.sorting:
                print("Sorting not supported in this section yet.")
            if not args.convert:
                args.convert = ["None"]
            if not args.keep:
                args.keep = ["True"]
            if not args.download_directory:
                args.download_directory = [os.getcwd()]
            start_time = time.time()

            mangaChapters.MangaChapters(chapter_id=args.chapter_id[0], download_directory=args.download_directory[0],
                                        conversion=args.convert[0], delete_files=args.keep[0],
                                        chapter_range=args.range, sorting_order=args.sorting[0],
                                        force_download=force_download)

            end_time = time.time()
            total_time = end_time - start_time

            print("Total Time Taken To Search : %s" % total_time)
            print("API Provided By Manga Eden : http://www.mangaeden.com/")
            sys.exit()

        if args.page_id:
            if not args.convert:
                args.convert = ["None"]
            if not args.keep:
                args.keep = ["True"]
            if not args.download_directory:
                args.download_directory = [os.getcwd()]
            start_time = time.time()
            mangaChapterDownload.MangaChapterDownload(page_id=args.page_id[0],
                                                      download_directory=args.download_directory[0],
                                                      log_flag=logger, conversion=args.convert[0],
                                                      delete_files=args.keep[0])

            end_time = time.time()
            total_time = end_time - start_time

            print("Total Time Taken To Download : %s" % total_time)
            print("API Provided By Manga Eden : http://www.mangaeden.com/")
            sys.exit()

        """This section right here reads the cache file"""
        try:
            args.convert, args.download_directory, chapters_to_update = self.cache()
            # print("Download Directory : {0}".format(args.download_directory[0]))
        except Exception as NoCache:
            pass

        if args.auto_download:
            if not args.sorting:
                args.sorting = ["ascending"]
            if not args.download_directory:
                args.download_directory = [os.getcwd()]
            if type(args.range) == list:
                args.range = args.range[0]
            if not args.convert:
                args.convert = ["None"]
            if not args.keep:
                args.keep = ["True"]
            if not args.quality:
                args.quality = ["Best"]
            for key in chapters_to_update:
                comic_url = key
                directory_address = chapters_to_update[key]
                # print(directory_address)
                downloaded_chapters = []
                for chapter_number in sorted(os.listdir(directory_address)):
                    for number in chapter_number.split():
                        if number.isdigit():
                            downloaded_chapters.append(int(number))
                        else:
                            pass
                last_downloaded_chapter = sorted(downloaded_chapters)[-1]
                args.range = [str(last_downloaded_chapter) + "-a"]

                start_time = time.time()
                honcho.Honcho().checker(comic_url=str(comic_url).strip(), current_directory=os.getcwd(),
                                        sorting_order=args.sorting[0], logger=logger,
                                        download_directory=args.download_directory[0],
                                        chapter_range=args.range[0], conversion=args.convert[0],
                                        delete_files=args.keep[0], image_quality=args.quality[0],
                                        username=args.username[0], password=args.password[0],
                                        comic_language=args.manga_language[0])
                end_time = time.time()
                total_time = end_time - start_time
                print("Total Time Taken To Complete : %s" % total_time)
                sys.exit()

        if not args.input:
            if not str(args.search).strip():
                print("I need an Input URL to download from.")
                print("Run the script with --help to see more information.")
        else:
            if not args.sorting:
                args.sorting = ["ascending"]
            if not args.download_directory:
                args.download_directory = [os.getcwd()]
            if type(args.range) == list:
                args.range = args.range[0]
            if not args.convert:
                args.convert = ["None"]
            if not args.keep:
                args.keep = ["True"]
            if not args.quality:
                args.quality = ["Best"]

            start_time = time.time()
            honcho.Honcho().checker(comic_url=str(args.input[0]).strip(), current_directory=os.getcwd(),
                                    sorting_order=args.sorting[0], logger=logger,
                                    download_directory=args.download_directory[0],
                                    chapter_range=args.range, conversion=args.convert[0],
                                    delete_files=args.keep[0], image_quality=args.quality[0],
                                    username=args.username[0], password=args.password[0],
                                    comic_language=args.manga_language[0])
            end_time = time.time()
            total_time = end_time - start_time
            print("Total Time Taken To Complete : %s" % total_time)
            sys.exit()

    def cache(self):
        try:
            config_data = self.config_reader()
            cache_conversion_type = [''.join(str(config_data["conversion_type"]))]
            cache_default_download = [''.join(str(config_data["default_download_location"]))]
            chapters_dict = config_data["chapter_update"][0]

            return cache_conversion_type,  cache_default_download, chapters_dict
        except Exception as NoConfigFile:
            pass

    @staticmethod
    def version():
        print("Current Version : %s" % __version__)

    def config_reader(self):
        with open("comic_dl_config.config", "rb") as  config_file:
            return json.loads(config_file.readline())
