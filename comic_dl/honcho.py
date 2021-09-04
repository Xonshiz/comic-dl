#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
import logging
from .sites import foolSlide
from .sites import readcomicOnlineli
from .sites import comicNaver
from .sites import mangaHere
from .sites import rawSenManga
from .sites import mangaFox
from .sites import omgBeauPeep
from .sites import mangaReader
from .sites import mangaEden
from .sites import acQQ
from .sites import stripUtopia
from .sites import readComicBooksOnline
from .sites import readComicsWebsite
from .sites import batoto
from .sites import hqbr
from .sites import comicextra
from .sites import readComicsIO
from .sites import japscan
from .sites import manganelo


class Honcho(object):
    def comic_language_resolver(self, language_code):
        # Will return the Language Name corresponding to the language code.
        language_dict = {
            '0': 'English',
            '1': 'Italian',
            '2': 'Spanish',
            '3': 'French',
            '4': 'German',
            '5': 'Portuguese',
            '6': 'Turkish',
            '7': 'Indonesian',
            '8': 'Greek',
            '9': 'Filipino',
            '10': 'Polish',
            '11': 'Thai',
            '12': 'Malay',
            '13 ': 'Hungarian',
            '14': 'Romanian',
            '15': ' Arabic',
            '16': 'Hebrew',
            '17': 'Russian',
            '18': 'Vietnamese',
            '19': 'Dutch',
            '20': 'Bengali',
            '21': 'Persian',
            '22': 'Czech',
            '23': 'Brazilian',
            '24': 'Bulgarian',
            '25': 'Danish',
            '26': 'Esperanto',
            '27': 'Swedish',
            '28': 'Lithuanian',
            '29': 'Other'
        }
        return language_dict[language_code]

    def checker(self, comic_url, download_directory, chapter_range, **kwargs):

        user_name = kwargs.get("username")
        password = kwargs.get("password")
        current_directory = kwargs.get("current_directory")
        log_flag = kwargs.get("logger")
        sorting = kwargs.get("sorting_order")
        comic_language = kwargs.get("comic_language")
        print_index = kwargs.get("print_index")

        if log_flag is True:
            logging.basicConfig(format='%(levelname)s: %(message)s', filename="Error Log.log", level=logging.DEBUG)
            logging.debug("Comic Url : %s" % comic_url)

        domain = urlparse(comic_url).netloc
        logging.debug("Selected Domain : %s" % domain)

        # Remove the "/" from ending to make checking URL for Full Series or Single Chapter easier.
        if comic_url[-1] == "/":
            comic_url = comic_url[:-1]

        if domain in ["yomanga.co", "gomanga.co"]:
            foolSlide.FoolSlide(manga_url=comic_url, logger=logging, current_directory=current_directory,
                                sorting_order=sorting, log_flag=log_flag, download_directory=download_directory,
                                chapter_range=chapter_range, conversion=kwargs.get("conversion"),
                                keep_files=kwargs.get("keep_files"))
            return 0
        elif domain in ["www.readcomiconline.li", "readcomiconline.li"]:
            readcomicOnlineli.ReadComicOnlineLi(manga_url=comic_url, logger=logging,
                                                current_directory=current_directory, sorting_order=sorting,
                                                log_flag=log_flag, download_directory=download_directory,
                                                chapter_range=chapter_range, conversion=kwargs.get("conversion"),
                                                keep_files=kwargs.get("keep_files"),
                                                image_quality=kwargs.get("image_quality"),
                                                print_index=print_index)
            return 0
        elif domain in ["www.comic.naver.com", "comic.naver.com"]:
            comicNaver.ComicNaver(manga_url=comic_url, logger=logging, current_directory=current_directory,
                                  sorting_order=sorting, log_flag=log_flag, download_directory=download_directory,
                                  chapter_range=chapter_range, conversion=kwargs.get("conversion"),
                                  keep_files=kwargs.get("keep_files"),
                                  print_index=print_index)
            return 0
        elif domain in ["www.mangahere.co", "mangahere.co", "www.mangahere.cc", "mangahere.cc"]:
            mangaHere.MangaHere(manga_url=comic_url, logger=logging, current_directory=current_directory,
                                sorting_order=sorting, log_flag=log_flag, download_directory=download_directory,
                                chapter_range=chapter_range, conversion=kwargs.get("conversion"),
                                keep_files=kwargs.get("keep_files"),
                                print_index=print_index)
            return 0
        elif domain in ["www.raw.senmanga.com", "raw.senmanga.com"]:
            rawSenManga.RawSenaManga(manga_url=comic_url, logger=logging, current_directory=current_directory,
                                     sorting_order=sorting, log_flag=log_flag, download_directory=download_directory,
                                     chapter_range=chapter_range, conversion=kwargs.get("conversion"),
                                     keep_files=kwargs.get("keep_files"),
                                     print_index=print_index)
            return 0
        elif domain in ["www.mangafox.me", "mangafox.me", "www.mangafox.la", "mangafox.la", "www.fanfox.net",
                        "fanfox.net"]:
            mangaFox.MangaFox(manga_url=comic_url, logger=logging, current_directory=current_directory,
                              sorting_order=sorting, log_flag=log_flag, download_directory=download_directory,
                              chapter_range=chapter_range, conversion=kwargs.get("conversion"),
                              keep_files=kwargs.get("keep_files"),
                              print_index=print_index)
            return 0
        elif domain in ["www.omgbeaupeep.com", "omgbeaupeep.com", "www.otakusmash.com", "otakusmash.com"]:
            omgBeauPeep.OmgBeauPeep(manga_url=comic_url, logger=logging, current_directory=current_directory,
                                    sorting_order=sorting, log_flag=log_flag, download_directory=download_directory,
                                    chapter_range=chapter_range, conversion=kwargs.get("conversion"),
                                    keep_files=kwargs.get("keep_files"),
                                    print_index=print_index)
            return 0
        #  TODO KO --print-index -i http://ac.qq.com/Comic/comicInfo/id/547059?trace_id=907_27.156.162.231_1539265645  broken?
        elif domain in ["www.ac.qq.com", "ac.qq.com"]:
            acQQ.AcQq(manga_url=comic_url, logger=logging, current_directory=current_directory,
                      sorting_order=sorting, log_flag=log_flag, download_directory=download_directory,
                      chapter_range=chapter_range,
                      print_index=print_index)
            return 0
        elif domain in ["www.striputopija.blogspot.in", "striputopija.blogspot.in", "www.striputopija.blogspot.com",
                        "striputopija.blogspot.com"]:
            stripUtopia.StripUtopia(manga_url=comic_url, logger=logging, current_directory=current_directory,
                                    sorting_order=sorting, log_flag=log_flag, download_directory=download_directory,
                                    chapter_range=chapter_range,
                                    print_index=print_index)
            return 0
        elif domain in ["www.mangareader.net", "mangareader.net"]:
            mangaReader.MangaReader(manga_url=comic_url, logger=logging, current_directory=current_directory,
                                    sorting_order=sorting, log_flag=log_flag, download_directory=download_directory,
                                    chapter_range=chapter_range, conversion=kwargs.get("conversion"),
                                    keep_files=kwargs.get("keep_files"),
                                    print_index=print_index)
            return 0
        elif domain in ["www.readcomicbooksonline.net", "readcomicbooksonline.net", "www.readcomicbooksonline.org",
                        "readcomicbooksonline.org"]:
            readComicBooksOnline.ReadComicBooksOnline(manga_url=comic_url, logger=logging,
                                                      current_directory=current_directory, sorting_order=sorting,
                                                      log_flag=log_flag, download_directory=download_directory,
                                                      chapter_range=chapter_range, conversion=kwargs.get("conversion"),
                                                      keep_files=kwargs.get("keep_files"),
                                                      print_index=print_index)
            return 0
        #  TODO KO seems broken
        elif domain in ["www.readcomics.website", "readcomics.website"]:
            readComicsWebsite.ReadComicsWebsite(manga_url=comic_url, logger=logging,
                                                current_directory=current_directory, sorting_order=sorting,
                                                log_flag=log_flag, download_directory=download_directory,
                                                chapter_range=chapter_range, conversion=kwargs.get("conversion"),
                                                keep_files=kwargs.get("keep_files"),
                                                print_index=print_index)
            return 0
        elif domain in ["www.japscan.to"]:
            japscan.Japscan(manga_url=comic_url, logger=logging, current_directory=current_directory,
                            sorting_order=sorting, log_flag=log_flag, download_directory=download_directory,
                            chapter_range=chapter_range, conversion=kwargs.get("conversion"),
                            keep_files=kwargs.get("keep_files"),
                            print_index=print_index)
            return 0
        elif domain in ["www.hqbr.com.br", "hqbr.com.br"]:
            hqbr.Hqbr(manga_url=comic_url, logger=logging, current_directory=current_directory,
                      sorting_order=sorting, log_flag=log_flag, download_directory=download_directory,
                      chapter_range=chapter_range, conversion=kwargs.get("conversion"),
                      keep_files=kwargs.get("keep_files"),
                      print_index=print_index)
            return 0
        elif domain in ["www.comicextra.com", "comicextra.com"]:
            comicextra.ComicExtra(manga_url=comic_url, logger=logging, current_directory=current_directory,
                                  sorting_order=sorting, log_flag=log_flag, download_directory=download_directory,
                                  chapter_range=chapter_range, conversion=kwargs.get("conversion"),
                                  keep_files=kwargs.get("keep_files"),
                                  print_index=print_index)
            return 0
        #  TODO KO seems broken
        elif domain in ["www.readcomics.io", "readcomics.io"]:
            readComicsIO.ReadComicsIO(manga_url=comic_url, logger=logging, current_directory=current_directory,
                                      sorting_order=sorting, log_flag=log_flag, download_directory=download_directory,
                                      chapter_range=chapter_range, conversion=kwargs.get("conversion"),
                                      keep_files=kwargs.get("keep_files"),
                                      print_index=print_index)
            return 0
        elif domain in ["www.kissmanga.com", "kissmanga.com"]:
            # kissManga.KissManga(manga_url = comic_url, logger = logging,
            #  current_directory = current_directory, sorting_order = sorting)
            print("Under Development!")
            return 0
        elif domain in ["www.bato.to", "bato.to"]:
            batoto.Batoto(manga_url=comic_url, logger=logging, current_directory=current_directory,
                          sorting_order=sorting, log_flag=log_flag, download_directory=download_directory,
                          chapter_range=chapter_range, conversion=kwargs.get("conversion"),
                          keep_files=kwargs.get("keep_files"), username=user_name, password=password,
                          comic_language=self.comic_language_resolver(comic_language),
                          print_index=print_index)
            return 0
        elif domain in ["manganelo.com", "mangakakalot.com", "manganato.com", "readmanganato.com"]:
            manganelo.Manganelo(manga_url=comic_url, logger=logging, current_directory=current_directory,
                                sorting_order=sorting, log_flag=log_flag, download_directory=download_directory,
                                chapter_range=chapter_range, conversion=kwargs.get("conversion"),
                                keep_files=kwargs.get("keep_files"),
                                print_index=print_index)
            return 0
        elif domain in ["www.mangaeden.com"]:
            if print_index:
                print("please use -find and -cid instead!")
                return -1
            mangaEden.MangaEden(manga_url=comic_url, logger=logging, current_directory=current_directory,
                                sorting_order=sorting, log_flag=log_flag, download_directory=download_directory,
                                chapter_range=chapter_range, conversion=kwargs.get("conversion"),
                                keep_files=kwargs.get("keep_files"))
            return 0
        else:
            print("%s is not supported at the moment. You can request it on the Github repository." % domain)
