#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cfscrape
import requests
import json
import sys
import os
import datetime


class MangaSearch():
    """Lists all the Mangas and their IDs based on user's search string."""
    def __init__(self, search_string, manga_language=0, **kwargs):
        self.search_string = str(search_string).strip()
        self.manga_language = int(manga_language).__str__().strip()
        self.cache_skip = str(kwargs.get("skip_cache"))
        self.json_source = ""

        """Cache will check whether we have the JSON file already or not.If the file exists and it's not older than 1
        day, we can use that to look things up. Otherwise, we need to download the fresh content. And, if anything weird
        happens, we still need to fetch the latest content.
        """
        # If user wants to force shut cache.
        if self.cache_skip != 0:
            if self.cache():
                try:
                    with open("Manga_Eden_Data.json", "rb") as read_file:
                        self.json_source = read_file.read()
                        # self.json_source = json.load(read_file)
                except Exception as FileNotFound:
                    print("Some Error Occurred : {0}".format(FileNotFound))
                    # If error occurs, we need to fetch the whole content again.
                    self.json_source = self.json_download(manga_language=self.manga_language)
            else:
                self.json_source = self.json_download(manga_language=self.manga_language)
        else:
            self.json_source = self.json_download(manga_language=self.manga_language)

        print("Searching for {0} in the Database...".format(search_string))

        if self.json_source and self.search_string:
            self.result = self.id_lookup(json_source=self.json_source, user_string=self.search_string)
            if self.result:
                # print(self.result)
                print("")
                print("Manga Name  --> Manga ID")
                print("------------------------")
                for manga_name in self.result:
                    print("{0} --> {1}".format(str(manga_name), str(self.result[manga_name])))
                print("")
            else:
                print("Nothing Found.")

    def cache(self):
        try:
            file_update_time = datetime.datetime.fromtimestamp(
                os.path.getmtime(os.getcwd() + os.sep + "Manga_Eden_Data.json")).date()
            current_time = datetime.date.today()

            if (current_time - file_update_time).days > 1:
                return False
            else:
                return True
        except Exception as FileNotFound:
            # print("Some Error Occurred : {0}".format(FileNotFound))
            return False

    def json_download(self, manga_language):
        print("Downloading The Latest Data Set...")
        headers = {
            'User-Agent':
                'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate'
        }

        sess = requests.session()
        sess = cfscrape.create_scraper(sess)

        search_url = "http://www.mangaeden.com/api/list/{0}/".format(manga_language)

        connection = sess.get(search_url, headers=headers)
        if connection.status_code != 200:
            print("Whoops! Seems like I can't connect to website.")
            print("It's showing : %s" % connection)
            print("Run this script with the --verbose argument and report the issue along with log file on Github.")
            sys.exit(1)
        else:
            json_data = connection.content
            # print(json_data)
            try:
                # Let's save the JSON data
                with open("Manga_Eden_Data.json", "wb") as write_file:
                    write_file.write(json_data)
            except Exception as WriteError:
                print("Couldn't make Cache : {0}".format(WriteError))
                pass

            return json_data

    def id_lookup(self, json_source, user_string):
        found_values = {}
        formatted_json = json.loads(json_source)
        for x in formatted_json["manga"]:
            # print(x)
            if str(user_string) in str(x.values()):
                found_values[x["t"]] = x["i"]
            else:
                pass
        if found_values:
            return found_values
        else:
            return None
