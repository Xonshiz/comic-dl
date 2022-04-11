Using The Search
================

In the updated of version 2017.12.28, searching is also available. This
is a rather confusing approach though, so carefully read this section.

When you search via this tool, you will get the list of Manga and their
respective unique IDs, that you will later use to download those Manga.
Firstly, you will search for a Manga, it’ll show it’s unique ID, which
you will copy and then pass into the tool again, it will list all the
chapters listed in that particular Manga. The tool will then ask whether
you want to download all the chapters belonging to that Manga. You can
type in “Yes”, “Y”, “N” or “No” accordingly.

How To Find A Manga:
--------------------

To search for a Manga, you need to use ``-find`` or ``--search``
argument followed by Manga Name.

::

   Windows Binary Command : `comic_dl.exe -find "<name_of_manga>"`
   Python Command : `__main__.py -find "<name_of_manga>"`

For Example : If we wish to search for “One Piece”, we wil use this :
``comic_dl.exe -find "One Piece"``

This will show something like this :

::

   Manga Name  --> Manga ID
   ------------------------
   One Piece: Wanted! --> 4e70ea60c092255ef7006726
   One Piece (Databook) --> 5218b0ef45b9ef8b83731b00
   One Piece x Toriko --> 4e70ea75c092255ef7006ee2
   One Piece dj - Boukyaku Countdown --> 55a19e2b719a1609004ad1f3
   One Piece --> 4e70ea10c092255ef7004aa2
   One Piece Party --> 566d9611719a1697dd8cf79a
   One Piece dj - Tears Will Surely Turn into Strength --> 55a19e31719a1609004ad1f7
   One Piece dj - Lotus Maker --> 55a19e2e719a1609004ad1f5
   One Piece dj - Three Days of Extreme Extravagance --> 55a19e34719a1609004ad1f9

As you can see, all the Manga matching the name show up, along with
their unique IDs. You need to note these IDs down, if you want to
download any of these Manga. Here, for sake of an example, we’ll take
“One Piece” Manga and its ID is : “4e70ea10c092255ef7004aa2”. #### Note
: \* When ever you search/find a Manga, comic_dl makes a
“Manga_Eden_Data.json” file, which more or less serves as a Cache. It’ll
always reference the cache file for the next 24 hours. However, if you
don’t want it to use that cache file, just pass ``--skip-cache``
argument along with your command, and it will ignore the cache
completely and fetch fresh resources and overwrite the older cache to
update it. \* By default, the tool searches for only Manga translated in
English Language. But, if you want to search for Manga translated in
Italian, you can pass this argument : ``--manga-language 1``.

Getting List Of Chapters For A Manga:
-------------------------------------

So, now that you have the Manga’s unique ID (mentioned above), you can
now use that ID to get list of all the chapters for that Manga, or can
even download those chapters directly. So, to list all the chapters of
“One Piece”, we will pass its ID with the argument ``--chapter-id``. The
command will be:

::

   Windows Binary Command : `comic_dl.exe --chapter-id "<unique_id_of_manga>"`
   Python Command : `__main__.py --chapter-id "<unique_id_of_manga>"`

Our example command for One Piece would be :
``comic_dl.exe --chapter-id "4e70ea10c092255ef7004aa2"``

This will return all the chapters, along with their unique IDs, which
can be later used to download a separate chapter.

::

   Chapter Number --> Chapter ID
   -----------------------------
   761.5 --> 54ad50d045b9ef961eeeda2e
   714.5 --> 5552a262719a163d21dc7125
   2 --> 4efe1d2ac0922504a300001a
   127.5 --> 54ad15c445b9ef961eee798b
   4 --> 4efe1d20c092250492000014
   379.5 --> 5372485a45b9ef6a97744417
   217.5 --> 54ad1f3245b9ef961eee826b

.. _note-1:

Note:
~~~~~

-  If you use this command, it’ll just list the chapters and then ask
   whether you want to download the chapters or not. If you wish to
   download the chapters without asking, just pass ``--force-download``
   option along with the main command line. Script will NOT ask you
   anything. It’ll list the chapters and start downloading them.
-  If you wish to download only a few chapters in a range, you can do so
   by giving the good old ``--range`` command. If you pass this
   argument, the script will not ask you whether you want to download
   the chapters or not. You will not need ``--force-download`` option,
   if you are using ``--range`` already.
-  Sorting is NOT supported in this, yet. YET!

Download A Chapter:
-------------------

You can download all the chapters of a Manga, as stated in the previous
step. But, if you wish to download a particular chapter, then you need
to get the unique ID of the chapter (mentioned above) and then download
that chapter separately. You need to use
``--page-id "<unique_id_of_chapter>"`` argument.

::

   Windows Binary Command : `comic_dl.exe --page-id "<unique_id_of_chapter>"`
   Python Command : `__main__.py --page-id "<unique_id_of_chapter>"`

Our example command for One Piece, chapter 2 would be :
``comic_dl.exe --page-id "4efe1d2ac0922504a300001a"`` #### Note: \* If
you download the chapter separately, you will need to provide the
``Manga Name`` and ``Chapter Number`` yourself. Because MangaEden’s API
doesn’t list those values in their JSON reply (weird).