List of Arguments
=================

Currently, the script supports these arguments :

::

   -h, --help                             Prints the basic help menu of the script and exits.
   -i,--input                             Defines the input link to the comic/manga.
   --print-index                          Prints the range index for links in the input URL
   -V,--version                           Prints the VERSION and exits.
   -u,--username                          Indicates username for a website.
   -p,--password                          Indicates password for a website.
   -v,--verbose                           Enables Verbose logging.
   --sorting                              Sorts the download order.(VALUES = asc, ascending,old,new,desc,descending,latest,new)
   -a, --auto                             Download new chapters automatically (needs config file!)
   -c, --config                           Generates config file for autodownload function
   -dd,--download-directory               Specifies custom download location for the comics/manga.
   -rn,--range                            Selects the range of Chapters to download (Default = All) [ Ex : --range 1-10 (This will download first 10 episodes of a series)]
   --convert                              Tells the script to convert the downloaded Images to PDF or anything else. (Supported Values : pdf, cbz) (Default : No) [By default, script will not convert anything.]
   --keep                                 Tells the script whether to keep the files after conversion or not. (Supported : No, False) (Default : Yes/True) [By default, images will be kept even after conversion.]
   --quality                              Tells the script about the image quality you want to download. (Supported Values : low/bad/worst/mobile/cancer) [By default, images will be downloaded in Highest Quality Available. No need to provide any option.]
   -ml, --manga-language                  Selects the language for manga. 0 is English (Default) and 1 is Italian.
   -sc, --skip-cache                      Forces to skip cache checking.
   --comic                                Add this after -i if you are inputting a comic id or the EXACT comic name.
                                          [ Ex : -i "Deadpool Classic" --comic ]
   -comic-search, --search-comic          Searches for a comic through the scraped data from ReadComicOnline.to
                                          [ Ex : -comic-search "Deadpool" ]
   -comic-info, --comic-info              Lists all the information about the given comic (argument can be either comic id or the exact comic name).
                                          [ Ex : -comic-info "Deadpool Classic" ] or [ Ex : -comic-info 3865 ]
   --update                               Updates the comic database for the given argument.
                                          [ Ex: --update "Deadpool Classic" ] or [ Ex: --update "https://readcomiconline.li/Comic/Deadpool-Classic" ]
   -cookie, --cookie                      Passes a cookie to be used throughout the session.

