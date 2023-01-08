#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tqdm import tqdm

from .__version__ import __version__
import argparse
import logging
import sys
import platform
from . import honcho
import os
import time
import json
from . import configGenerator

from .readcomiconline import RCO
from .readcomiconline import dataUpdate

CONFIG_FILE = 'config.json'


class ComicDL(object):
    def __init__(self, argv):
        parser = argparse.ArgumentParser(description='Comic_dl is a command line tool to download comics and manga '
                                                     'from various such sites.')

        parser.add_argument('--version', action='store_true', help='Shows version and exits.')
        parser.add_argument('-s', '--sorting', nargs=1, help='Decides downloading order of chapters.')
        parser.add_argument('-a', '--auto', action='store_true',
                            help='Download new chapters automatically (needs config file!)')
        parser.add_argument('-c', '--config', action='store_true',
                            help='Generates config file for autodownload function')
        parser.add_argument('-dd', '--download-directory', nargs=1,
                            help='Decides the download directory of the comics/manga.', default=[os.getcwd()])
        parser.add_argument('-rn', '--range', nargs=1,
                            help='Specifies the range of chapters to download.', default='All')
        parser.add_argument('--convert', nargs=1,
                            help='Tells the script to convert the downloaded Images to PDF or anything else.')
        parser.add_argument('--keep', nargs=1,
                            help='Tells the script whether to keep the files after conversion or not.',
                            default=['True'])
        parser.add_argument('--quality', nargs=1,
                            help='Tells the script which Quality of image to download (High/Low).', default='True')

        parser.add_argument('-i', '--input', nargs=1, help='Inputs the URL to comic.')
        parser.add_argument('-cookie', '--cookie', nargs=1, help='Passes cookie (text format) to be used throughout the session.')

        # Chr1st-oo, added arguments
        parser.add_argument("--comic", action="store_true", help="Add this after -i if you are inputting a comic id or the EXACT comic name.")
        parser.add_argument("-comic-search", "--search-comic", nargs=1, help="Searches for a comic through the gathered data from ReadComicOnline.to")
        parser.add_argument("-comic-info", "--comic-info", nargs=1, help="List all informations for the queried comic.")
        parser.add_argument("--update", nargs=1, help="USAGE: --update <COMIC_LINK OR COMIC_NAME>... Updates the comic database for the given argument.")
        #

        parser.add_argument('--print-index', action='store_true',
                            help='prints the range index for links in the input URL')

        parser.add_argument('-ml', '--manga-language', nargs=1,
                            help='Selects the language for manga.', default='0')

        parser.add_argument('-sc', '--skip-cache', nargs=1,
                            help='Forces to skip cache checking.', default='0')

        parser.add_argument('-p', '--password', nargs=1,
                            help='Takes Password used to log into a website, along with a username/email.',
                            default=['None'])

        parser.add_argument('-u', '--username', nargs=1,
                            help='Takes username/email used to log into a website, along with a password.',
                            default=['None'])

        parser.add_argument("-v", "--verbose", help="Prints important debugging messages on screen.",
                            action="store_true")
        logger = False

        args = parser.parse_args()

        if args.version:
            self.version()
            sys.exit()

        if args.verbose:
            print("\n***Starting the script in Verbose Mode***\n")
            try:
                os.remove("Error_Log.log")
                # with open(str(args.download_directory[0]) + str(os.sep) + "Error_Log.log", "w") as wf:
                #     wf.write("Writing...")
            except Exception as VerboseError:
                # print(VerboseError)
                pass
                logging.basicConfig(format='%(levelname)s: %(message)s',
                                    filename=str(args.download_directory[0]) + str(os.sep) + "Error_Log.log",
                                    level=logging.DEBUG)
            logging.debug("Arguments Provided : %s" % args)
            logging.debug("Operating System : %s - %s - %s" % (platform.system(),
                                                               platform.release(),
                                                               platform.version()
                                                               ))
            logging.debug("Python Version : %s (%s)" % (platform.python_version(), platform.architecture()[0]))
            logging.debug("Script Version : {0}".format(__version__))
            logger = True

        # Chr1st-oo, comic search & comic info
        if args.comic_info or args.search_comic:
            rco = RCO.ReadComicOnline()

            if args.search_comic:
                query = args.search_comic[0]
                rco.comicSearch(query)
            elif args.comic_info:
                query = args.comic_info[0]
                rco.comicInfo(query)

            sys.exit()

        if args.update:
            query = args.update[0]

            if "readcomiconline" in query or "https://" in query or "http://" in query:
                dataUpdate.RCOUpdater(link=query)
            else:
                dataUpdate.RCOUpdater(name=query)

        if args.auto:
            # @dsanchezseco
            # read config file and download each item of list
            data = json.load(open(CONFIG_FILE))
            # common args
            sorting_order = data["sorting_order"]
            download_directory = data["download_directory"]
            conversion = data["conversion"]
            keep_files = data["keep"]
            image_quality = data["image_quality"]
            manual_cookie = data["cookie"]
            pbar_comic = tqdm(data["comics"], dynamic_ncols=True, desc="[Comic-dl] Auto processing", leave=True,
                              unit='comic')
            for elKey in pbar_comic:
                try:
                    pbar_comic.set_postfix(comic_name=elKey)
                    el = data["comics"][elKey]
                    # next chapter to download, if it's greater than available don't download anything
                    download_range = str(el["next"]) + "-__EnD__"
                    if "last" in el and not el["last"] == "None":
                        download_range = str(el["next"]) + "-" + str(el["last"]) + "-RANGE"

                    honcho.Honcho().checker(comic_url=el["url"].strip(), current_directory=os.getcwd(),
                                            sorting_order=sorting_order, logger=logger,
                                            download_directory=download_directory,
                                            chapter_range=download_range, conversion=conversion,
                                            keep_files=keep_files, image_quality=image_quality,
                                            username=el["username"], password=el["password"],
                                            comic_language=el["comic_language"],
                                            cookie=manual_cookie)
                except Exception as ex:
                    pbar_comic.write('[Comic-dl] Auto processing with error for %s : %s ' % (elKey, ex))
            pbar_comic.set_postfix()
            pbar_comic.close()
            sys.exit()

        # config generator
        if args.config:
            # @dsanchezseco
            configGenerator.configGenerator()
            sys.exit()

        if args.input is None:
            if not str(args.search).strip():
                print("I need an Input URL to download from.")
                print("Run the script with --help to see more information.")
        else:
            print_index = False
            manual_cookie = None
            if args.print_index:
                print_index = True
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
            if not args.quality or args.quality == "True":
                args.quality = ["Best"]
            if args.cookie:
                manual_cookie = args.cookie[0]

            # user_input = unicode(args.input[0], encoding='latin-1')
            user_input = args.input[0]

            if args.comic:
                rco = RCO.ReadComicOnline()
                user_input = rco.comicLink(user_input)

                if not user_input:
                    print("No comic found with that name or id.")
                    print("If you are inputting an ID, use -comic-search <QUERY> to determine the id.")
                    print("If you are inputting a name, you must input the exact name of the comic for ")
                    sys.exit()

            start_time = time.time()
            honcho.Honcho().checker(comic_url=user_input, current_directory=os.getcwd(),
                                    sorting_order=args.sorting[0], logger=logger,
                                    download_directory=args.download_directory[0],
                                    chapter_range=args.range, conversion=args.convert[0],
                                    keep_files=args.keep[0], image_quality=args.quality[0],
                                    username=args.username[0], password=args.password[0],
                                    comic_language=args.manga_language[0], print_index=print_index,
                                    cookie=manual_cookie)
            end_time = time.time()
            total_time = end_time - start_time
            print("Total Time Taken To Complete : %s" % total_time)
            sys.exit()

    @staticmethod
    def version():
        print(__version__)
