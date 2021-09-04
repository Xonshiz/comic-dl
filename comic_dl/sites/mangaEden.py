#!/usr/bin/env python
# -*- coding: utf-8 -*-

from comic_dl import globalFunctions
import re

from comic_dl .manga_eden import mangaChapters


class MangaEden:
    def __init__(self, manga_url, download_directory, chapter_range, **kwargs):
        conversion = kwargs.get("conversion")
        keep_files = kwargs.get("keep_files")
        self.logging = kwargs.get("log_flag")
        self.sorting = kwargs.get("sorting_order")

        source, cookies = globalFunctions.GlobalFunctions().page_downloader(manga_url=manga_url)
        chapter_id = str(re.search(r"window.manga_id2\s*=\s*\"(.*?)\";", str(source)).group(1))

        mangaChapters.MangaChapters(chapter_id=chapter_id, download_directory=download_directory,
                                    conversion=conversion, keep_files=keep_files,
                                    chapter_range=chapter_range, sorting_order=self.sorting,
                                    force_download="True", comic_url=manga_url)
