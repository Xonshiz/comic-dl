Notes
=====
-  Readcomiconline.li has been a pain to work with and it might block you out a lot. Now you can use `--cookie` parameter to pass a working cookie. You can retrieve the cookie by checking network tab for `Cookie` value in request headers or by using an external browser plugin. Read more about this on `#299 <https://github.com/Xonshiz/comic-dl/issues/299>`__.

-  comic.naver.com has korean characters and some OS won’t handle those
   characters. So, instead of naming the file folder with the series
   name in korean, the script will download and name the folder with the
   comic’s ID instead.

-  Bato.to requires you to “log in” to read some chapters. So, to be on
   a safe side, provide the username/password combination to the script
   via “-p” and “-u” arguments.

-  Bato.to also has comics for various languages. You need to pass the
   language code via “-ml” argument. Read the `Language Codes <language_codes.html>`_ section to find out the language codes.

-  Bato.to only supports custom language downloads in “Batch” mode.

-  URLs with special characters are tricky to work with, because of
   “Character Encoding”. If you wish to download such a comic/manga, you
   will need to use Python 3 (If on python) and also, you need to set
   your terminal’s character encoding to “utf-8” or “latin-1”. #95 is
   the same issue.