Auto Download
=============

You can autodownload the new chapters of your favorite comics by
creating a config file in json format.

To generate the config file run the comand below and follow the
instructions

::

   python __main__.py --config

or with the binary

::

   comic_dl.exe --config

This commands supports the creation of the config file, the addition and
remove of series and the edition of the common download configuration.

Once the config file is generated you can download automatically the new
chapters available for your selected comics by running the command
bellow. The command will automatically update the config file to the
lastest chapter downloaded, so in the next run it’ll download just the
new ones.

::

   python __main__.py --auto

or with the binary

::

   comic_dl.exe --auto

*Note: It’s not necesary to keep the comic files to download the next
chapters.*
