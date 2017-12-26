#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
import logging
from sites import foolSlide
from sites import readcomicOnlineto
from sites import comicNaver
from sites import mangaHere
from sites import rawSenManga
from sites import mangaFox
from sites import omgBeauPeep
from sites import mangaReader
from sites import acQQ
from sites import stripUtopia
from sites import readComicBooksOnline
import globalFunctions


class Honcho(object):
    def checker(self, comic_url, download_directory, chapter_range, **kwargs):

        user_name = kwargs.get("username")
        password = kwargs.get("password")
        current_directory = kwargs.get("current_directory")
        log_flag = kwargs.get("logger")
        sorting = kwargs.get("sorting_order")

        if log_flag is True:
            logging.basicConfig(format='%(levelname)s: %(message)s', filename="Error Log.log", level=logging.DEBUG)
            logging.debug("Comic Url : %s" % comic_url)

        fool_slide = ["yomanga.co", "gomanga.co"]

        domain = urlparse(comic_url).netloc
        logging.debug("Selected Domain : %s" % domain)

        if domain in fool_slide:
            foolSlide.FoolSlide(manga_url=comic_url, logger=logging, current_directory=current_directory,
                                sorting_order=sorting, log_flag=log_flag, download_directory=download_directory,
                                chapter_range=chapter_range, conversion=kwargs.get("conversion"),
                                delete_files=kwargs.get("delete_files"))
            return 0
        elif domain in ["www.readcomiconline.to", "readcomiconline.to"]:
            readcomicOnlineto.ReadComicOnlineTo(manga_url=comic_url, logger=logging,
                                                current_directory=current_directory, sorting_order=sorting,
                                                log_flag=log_flag, download_directory=download_directory,
                                                chapter_range=chapter_range, conversion=kwargs.get("conversion"),
                                                delete_files=kwargs.get("delete_files"), image_quality=kwargs.get("image_quality"))
            return 0
        elif domain in ["www.comic.naver.com", "comic.naver.com"]:
            comicNaver.ComicNaver(manga_url=comic_url, logger=logging, current_directory=current_directory,
                                  sorting_order=sorting, log_flag=log_flag, download_directory=download_directory,
                                  chapter_range=chapter_range, conversion=kwargs.get("conversion"),
                                  delete_files=kwargs.get("delete_files"))
            return 0
        elif domain in ["www.mangahere.co", "mangahere.co"]:
            mangaHere.MangaHere(manga_url=comic_url, logger=logging, current_directory=current_directory,
                                sorting_order=sorting, log_flag=log_flag, download_directory=download_directory,
                                chapter_range=chapter_range, conversion=kwargs.get("conversion"),
                                delete_files=kwargs.get("delete_files"))
            return 0
        elif domain in ["www.raw.senmanga.com", "raw.senmanga.com"]:
            rawSenManga.RawSenaManga(manga_url=comic_url, logger=logging, current_directory=current_directory,
                                     sorting_order=sorting, log_flag=log_flag, download_directory=download_directory,
                                     chapter_range=chapter_range, conversion=kwargs.get("conversion"),
                                     delete_files=kwargs.get("delete_files"))
            return 0
        elif domain in ["www.mangafox.me", "mangafox.me"]:
            mangaFox.MangaFox(manga_url=comic_url, logger=logging, current_directory=current_directory,
                              sorting_order=sorting, log_flag=log_flag, download_directory=download_directory,
                              chapter_range=chapter_range, conversion=kwargs.get("conversion"),
                              delete_files=kwargs.get("delete_files"))
            return 0
        elif domain in ["www.omgbeaupeep.com", "omgbeaupeep.com"]:
            omgBeauPeep.OmgBeauPeep(manga_url=comic_url, logger=logging, current_directory=current_directory,
                                    sorting_order=sorting, log_flag=log_flag, download_directory=download_directory,
                                    chapter_range=chapter_range, conversion=kwargs.get("conversion"),
                                    delete_files=kwargs.get("delete_files"))
            return 0
        elif domain in ["www.ac.qq.com", "ac.qq.com"]:
            acQQ.AcQq(manga_url=comic_url, logger=logging, current_directory=current_directory,
                      sorting_order=sorting, log_flag=log_flag, download_directory=download_directory,
                      chapter_range=chapter_range)
            return 0
        elif domain in ["www.striputopija.blogspot.in", "striputopija.blogspot.in"]:
            stripUtopia.StripUtopia(manga_url=comic_url, logger=logging, current_directory=current_directory,
                      sorting_order=sorting, log_flag=log_flag, download_directory=download_directory,
                      chapter_range=chapter_range)
            return 0
        elif domain in ["www.mangareader.net", "mangareader.net"]:
            mangaReader.MangaReader(manga_url=comic_url, logger=logging, current_directory=current_directory,
                                    sorting_order=sorting, log_flag=log_flag, download_directory=download_directory,
                                    chapter_range=chapter_range, conversion=kwargs.get("conversion"),
                                    delete_files=kwargs.get("delete_files"))
            return 0
        elif domain in ["www.readcomicbooksonline.net", "readcomicbooksonline.net"]:
            readComicBooksOnline.ReadComicBooksOnline(manga_url=comic_url, logger=logging, current_directory=current_directory,
                                    sorting_order=sorting, log_flag=log_flag, download_directory=download_directory,
                                    chapter_range=chapter_range, conversion=kwargs.get("conversion"),
                                    delete_files=kwargs.get("delete_files"))
            return 0
        elif domain in ["www.kissmanga.com", "kissmanga.com"]:
            # kissManga.KissManga(manga_url = comic_url, logger = logging, current_directory = current_directory, sorting_order = sorting)
            print("Under Development!")
            return 0
        elif domain in ["www.bato.to", "bato.to"]:
            # kissManga.KissManga(manga_url = comic_url, logger = logging, current_directory = current_directory, sorting_order = sorting)
            print("Under Development!")
            return 0
        else:
            print("%s is not supported at the moment. You can request it on the Github repository." % domain)
