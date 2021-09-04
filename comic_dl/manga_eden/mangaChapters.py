#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cloudscraper
import requests
import json
import sys
# import mangaChapterDownload
# from comic_dl import globalFunctions
from .mangaChapterDownload import *


class MangaChapters():
    """Lists all the chapters and their IDs for a particular Manga."""
    def __init__(self, chapter_id, download_directory, **kwargs):
        self.chapter_id = str(chapter_id).strip()
        self.download_range = str(kwargs.get("chapter_range"))

        self.sorting_order = str(kwargs.get("sorting_order"))
        self.force_download = str(kwargs.get("force_download"))
        self.comic_url = str(kwargs.get("comic_url"))
        self.download_confirmation = "no"

        self.json_source = self.json_download(chapter_id=self.chapter_id)
        self.chapters, self.manga_name = self.id_lookup(json.loads(self.json_source))

        if self.chapters:
            final_chapter_dict = {}

            print("Chapter Number --> Chapter ID")
            print("-----------------------------")
            for chapter in self.chapters:
                print("{0} --> {1}".format(chapter, self.chapters[chapter]))
            print("")

            if self.download_range != "All":
                self.download_confirmation = "yes"
                self.force_download =  "True"

            # If '-fd' command has NOT been passed, we'll ask the user whether they want to download chapters or not.
            if self.force_download == "False":
                try:
                    self.download_confirmation = str(
                        raw_input("Do you want to download all the chapters? : ")).strip().lower()
                except Exception as WrongInputType:
                    # If python3, then raw_input() won't work.
                    self.download_confirmation = str(
                        input("Do you want to download all the chapters? : ")).strip().lower()
            # If a user has provided RANGE, then obviously, they want to download the chapters.
            else:
                self.download_confirmation = "yes"

            # print("self.download_range : {0}".format(self.download_range))
            # print("self.download_confirmation : {0}".format(self.download_confirmation))

            if self.download_confirmation in ["yes", "y"]:
                if self.download_range != "All":

                    # -1 to shift the episode number accordingly to the INDEX of it. List starts from 0 xD!
                    starting = int(str(self.download_range).split("-")[0])

                    if (str(self.download_range).split("-")[1]).decode().isdecimal():
                        ending = int(str(self.download_range).split("-")[1])
                    else:
                        ending = len(self.chapters)

                    for chapter in self.chapters:
                        if chapter >= starting and chapter <= ending:
                            final_chapter_dict[chapter] = str(self.chapters[chapter])
                        else:
                            pass
                else:
                    final_chapter_dict = self.chapters

                for chapter in final_chapter_dict:
                    MangaChapterDownload(page_id=final_chapter_dict[chapter], download_directory=download_directory,
                                         manga_name=str(self.manga_name), chapter_number=str(chapter))

                    # if chapter range contains "__EnD__" write new value to config.json
                    if self.download_range != "All" and not ((str(self.download_range).split("-")[1]).decode().isdecimal()):
                            globalFunctions.GlobalFunctions().addOne(self.comic_url)

            else:
                sys.exit()
        else:
            print("No Chapter Found. Please Double Check the Chapter ID.")


    def json_download(self, chapter_id):
        headers = {
            'User-Agent':
                'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate'
        }

        sess = requests.session()
        sess = cloudscraper.create_scraper(sess)

        search_url = "http://www.mangaeden.com/api/manga/{0}/".format(chapter_id)

        connection = sess.get(search_url, headers=headers)
        if connection.status_code != 200:
            print("Whoops! Seems like I can't connect to website.")
            print("It's showing : %s" % connection)
            print("Run this script with the --verbose argument and report the issue along with log file on Github.")
            sys.exit(1)
        else:
            json_data = connection.content

            return json_data

    def id_lookup(self, json_source):
        chapters = {}

        """Example of a chapter array element: 
        [ 
            5, # <-- chapter's number 
            1275542373.0, # <-- chapter's date 
            "5", # <-- chapter's title 
            "4e711cb0c09225616d037cc2" # <-- chapter's ID (chapter.id in the next section) 
        ],
        """
        list_of_chapters = list(json_source["chapters"])
        # print(json_source["title"])

        for chapter in list_of_chapters:
            chapters[chapter[0]] = str(chapter[-1])

        # Let's sort this dictionary based on the chapter count (KEYS).
        sorted(chapters.items(), key=lambda s: s[0])

        if chapters:
            return chapters, str(json_source["title"])
        else:
            return None, str(json_source["title"])
