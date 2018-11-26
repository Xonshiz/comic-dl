import re
import globalFunctions
import os
import logging


class StripUtopia(object):
    def __init__(self, manga_url, download_directory, chapter_range, **kwargs):
        current_directory = kwargs.get("current_directory")
        conversion = kwargs.get("conversion")
        keep_files = kwargs.get("keep_files")
        self.logging = kwargs.get("log_flag")
        self.sorting = kwargs.get("sorting_order")
        self.print_index = kwargs.get("print_index")

        page_souce, cookies_main = globalFunctions.GlobalFunctions().page_downloader(manga_url=manga_url)
        self.comic_name = self.name_cleaner(page_souce, manga_url)
        if "/p/" in str(manga_url):
            self.full_series(source=page_souce, comic_url=manga_url, comic_name=self.comic_name, sorting=self.sorting,
                             download_directory=download_directory, chapter_range=chapter_range, conversion=conversion,
                             keep_files=keep_files)
        else:
            self.single_chapter(page_souce, manga_url, self.comic_name, download_directory, conversion, keep_files)

    def name_cleaner(self, source, url):
        # Single : http://striputopija.blogspot.in/2016/05/001_54.html
        # Full : http://striputopija.blogspot.in/p/biser-strip.html
        initial_name = re.search(r"<title>\n(.*?)\n</title>", str(source)).group(1)  # First result is the website name.

        safe_name = re.sub(r"[0-9][a-z][A-Z]\ ", "", str(initial_name))

        name_breaker = safe_name.split("-")[-1]
        manga_name = str(name_breaker.title()).replace("_", " ").replace("Strip-Utopija", "").replace("STRIP-UTOPIJA",
                                                                                                      "").replace(
            "UTOPIJA", "").replace("Utopija", "").replace(":", "").strip()

        return manga_name

    def single_chapter(self, source, comic_url, comic_name, download_directory, conversion, keep_files):
        short_content = source.findAll('div', {'itemprop': 'description articleBody'})
        img_list = re.findall(r'href="(.*?)"', str(short_content))
        chapter_number = str(str(comic_url).split("/")[-1]).replace(".html", "")

        file_directory = globalFunctions.GlobalFunctions().create_file_directory(chapter_number, comic_name)
        directory_path = os.path.realpath(str(download_directory) + "/" + str(file_directory))

        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

        links = []
        file_names = []
        for current_chapter, image_link in enumerate(img_list):
            # file_name = str(img_list.index(image_link))

            logging.debug("image_link : %s" % image_link)

            current_chapter += 1
            file_name = str(globalFunctions.GlobalFunctions().prepend_zeroes(current_chapter, len(img_list))) + ".jpg"
            file_names.append(file_name)
            links.append(image_link)

        globalFunctions.GlobalFunctions().multithread_download(chapter_number, comic_name, comic_url, directory_path,
                                                               file_names, links, self.logging)
            
        globalFunctions.GlobalFunctions().conversion(directory_path, conversion, keep_files, comic_name,
                                                     chapter_number)

        return 0

    def full_series(self, source, comic_url, comic_name, sorting, download_directory, chapter_range, conversion,
                    keep_files):
        all_links = re.findall(r'http://striputopija.blogspot.rs/\d+/\d+/\d+|_.html', str(source))

        if chapter_range != "All":
            # -1 to shift the episode number accordingly to the INDEX of it. List starts from 0 xD!
            starting = int(str(chapter_range).split("-")[0]) - 1

            if str(chapter_range).split("-")[1].isdigit():
                ending = int(str(chapter_range).split("-")[1])
            else:
                ending = len(all_links)

            indexes = [x for x in range(starting, ending)]

            all_links = [all_links[x] for x in indexes][::-1]
        else:
            pass

        if self.print_index:
            idx = 0
            all_chapters = re.findall(r'http://striputopija.blogspot.rs/\d+/\d+/.+.html.+>(.+)</a>', str(source))
            for chap_link in all_chapters:
                idx = idx + 1
                print(str(idx) + ": " + str(chap_link))
            return

        if str(sorting).lower() in ['new', 'desc', 'descending', 'latest']:
            for chap_link in all_links:
                page_souce, cookies_main = globalFunctions.GlobalFunctions().page_downloader(
                    manga_url=chap_link + ".html")
                self.single_chapter(source=page_souce, comic_url=chap_link + ".html", comic_name=comic_name,
                                    download_directory=download_directory,
                                    conversion=conversion, keep_files=keep_files)
                # if chapter range contains "__EnD__" write new value to config.json
                if chapter_range != "All" and chapter_range.split("-")[1] == "__EnD__":
                    globalFunctions.GlobalFunctions().addOne(comic_url)
        elif str(sorting).lower() in ['old', 'asc', 'ascending', 'oldest', 'a']:

            for chap_link in all_links[::-1]:
                page_souce, cookies_main = globalFunctions.GlobalFunctions().page_downloader(
                    manga_url=chap_link + ".html")
                self.single_chapter(source=page_souce, comic_url=chap_link + ".html", comic_name=comic_name,
                                    download_directory=download_directory,
                                    conversion=conversion, keep_files=keep_files)
                # if chapter range contains "__EnD__" write new value to config.json
                if chapter_range != "All" and chapter_range.split("-")[1] == "__EnD__":
                    globalFunctions.GlobalFunctions().addOne(comic_url)

        return 0
