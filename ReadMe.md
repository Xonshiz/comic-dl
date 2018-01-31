[![N|Solid](https://raw.githubusercontent.com/Xonshiz/comic-dl/master/Images/Icon.png)](https://github.com/Xonshiz/comic-dl)
# Comic-DL | [![Build Status](https://travis-ci.org/Xonshiz/comic-dl.svg?branch=master)](https://travis-ci.org/Xonshiz/comic-dl) [![Documentation Status](https://readthedocs.org/projects/comic-dl/badge/?version=latest)](http://comic-dl.readthedocs.io/en/latest/?badge=latest) | [![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.me/xonshiz)  | [![GitHub release](https://img.shields.io/github/release/xonshiz/comic-dl.svg?style=flat-square)](https://github.com/xonshiz/comic-dl/releases/latest) | [![Github All Releases](https://img.shields.io/github/downloads/xonshiz/comic-dl/total.svg?style=flat-square)](https://github.com/xonshiz/comic-dl/releases)

Comic-dl is a command line tool to download Comics and Manga from various Manga and Comic sites easily. You can search Manga from this tool as well. Idea from [youtube-dl](https://github.com/rg3/youtube-dl)

> Don't overuse this script. Support the developers of those websites by disabling your adblock on their site. 
>Advertisments pay for the website servers.

> Searching and downloading that manga is supported via MangaEden's API : http://www.mangaeden.com/api/

## Table of Content

* [Supported Sites](https://github.com/Xonshiz/comic-dl/blob/master/Supported_Sites.md)
* [Dependencies Installation](#dependencies-installation)
    * [Linux/Debian](#linuxdebian-)
    * [Windows](#windows-)
    * [Mac OS X](#mac-os-x-)
* [Installation](#installation)
* [Python Support](#python-support)
* [Windows Binary](#windows-binary)
* [List of Arguments](#list-of-arguments)
* [Language Codes](#language-codes)
* [Using The Search](#using-the-search)
* [Youtube Tutorial](https://www.youtube.com/watch?v=TmQYhLHEZxA)
* [Usage](#usage)
    * [Windows](#windows)
    * [Linux/Debian](#linuxdebian)
* [Auto Download](#auto-download)
* [Features](#features)
* [Changelog](https://github.com/Xonshiz/comic-dl/blob/master/Changelog.md)
* [Opening An Issue/Requesting A Site](#opening-an-issuerequesting-a-site)
    * [Reporting Issues](#reporting-issues)
    * [Suggesting A Feature](#suggesting-a-feature)
* [Contributors](https://github.com/Xonshiz/comic-dl/blob/master/Contributors.md)
* [Notes](#notes)
* [Donations](#donations)

## Supported Websites
You can check the list of supported websites [**`HERE`**](https://github.com/Xonshiz/comic-dl/blob/master/Supported_Sites.md).

## Dependencies Installation
This script can run on multiple Operating Systems. You need `Node.js` in your system's path for this script to work (You need this on each and every Operating System, even on WINDOWS :/). Download the `Node.Js` from [Node.js official website](https://nodejs.org/en/). Doesn't matter which operating system you're on, this is a must. Follow the instructions mentioned below, according to your OS.

### Linux/Debian :
Since most (if not all) Linux/Debian OS come with python pre-installed, you don't have to install python manually. Make sure you're using python >= 2.7.x though.

We need `pip` to install any external dependenc(ies). So, open any terminal and type in `pip list` and if it shows some data, then it is fine. But, if it shows error, like `pip not found` or something along this line, then you need to install `pip`. Just type this command in terminal :

`sudo apt-get install python-pip`

If you're on Fedora, CentOS/RHEL, openSUSE, Arch Linux, then you simply need to follow [`THIS TUTORIAL`](https://packaging.python.org/install_requirements_linux/) to install `pip`.

If this still doesn't work, then you'll manually need to install pip. Doing so is an easy one time job and you can follow   [`THIS TUTORIAL`](https://pip.pypa.io/en/stable/installing/) to do so.

We need `PhantomJS` to access some websites. So, after all this, we'll install PhantomJS.

First, make sure your system is updated :
```
sudo apt-get update
sudo apt-get install build-essential chrpath libssl-dev libxft-dev
```
Grab Dependencies for PhantomJS (most important) :
```
sudo apt-get install libfreetype6 libfreetype6-dev
sudo apt-get install libfontconfig1 libfontconfig1-dev
```
Grab the suitable `tar.bz2` file from this [link](http://phantomjs.org/download.html)
Extract the contents of this `tar.bz2` file you just downloaded. Open a terminal and follow the commands. 
* Don't forget the change the name of the file(s) mentioned here with the ones that you downloaded.There might be a newer version when you download
```
cd /Name/of_the/directory/that/contains/the/tar_bz2/file
export PHANTOM_JS="phantomjs-2.1.1-linux-x86_64"
sudo tar xvjf $PHANTOM_JS.tar.bz2
```
Once downloaded, move Phantomjs folder to /usr/local/share/ and create a symlink:
```
sudo mv $PHANTOM_JS /usr/local/share
sudo ln -sf /usr/local/share/$PHANTOM_JS/bin/phantomjs /usr/local/bin
```
If none of these commands gave error(s), PhantomJS should be installed in your Linux/Debian systems just fine. You can check it by entering this command in any terminal :
```
phantomjs --version
```

### Windows :
If you're on windows, then it is recommended to download the [`windows binary`](https://github.com/Xonshiz/comic-dl#windows-binary) for this script. If you use the windows binary, you don't need to install anything, except Node.js. But, if for some weird reason you want to use Python script instead, then follow these steps :

* Install Python > 2.7.6. Download the desired installer from [here](https://www.python.org/downloads/).
* [Add it in the system path](http://superuser.com/questions/143119/how-to-add-python-to-the-windows-path) (if not already added).
* If you're using python >2.7.9, you don't need to install `PIP`. However, if you don't have pip installed and added in windows path, then do so by following [this little tutorial](http://stackoverflow.com/a/12476379).
* Download [this `text`]() file and put it in some directory/folder.
* Open Command Prompt and browse to the directory where you downloaded your requiremenets.txt file and run this command :
```
pip install -r requirements.txt
```
* It should install the required external libraries.
* Download PhantomJS : http://phantomjs.org/download.html

Now, install Node.Js as well and make sure it's in your path.

Well, if everything came up good without any error(s), then you're good to go!

### Mac OS X :
Mac OS X users will have to fetch their version of `Python` and `Pip`.
* Python installation guide : http://docs.python-guide.org/en/latest/starting/install/osx/
* Pip installation guide : http://stackoverflow.com/questions/17271319/installing-pip-on-mac-os-x
* PhantomJS Mac Binary : http://phantomjs.org/download.html (Download the latest build for your OS)

After downloading and installing these, you need to add PIP & Python in your path. Follow [`THIS LITTLE GUIDE`](http://www.pyladies.com/blog/Get-Your-Mac-Ready-for-Python-Programming/) to install both, Python & pip successfully.

## Installation
After installing and setting up all the dependencies in your Operating System, you're good to go and use this script.
The instructions for all the OS would remain same. Download [`THIS REPOSITORY`](https://github.com/Xonshiz/comic-dl/archive/master.zip) and put it somewhere in your system. Move over to the `comic_dl` folder.

**Windows users**, it's better to not place it places where it requires administrator privileges. Good example would be `C:\Windows`. This goes for both, the Python script and the windows binary file (.exe).

**Linux/Debian** users make sure that this script is executable.just run this command, if you run into problem(s) :

`chmod +x __main__.py`

and then, execute with this :

`./__main__.py`

## Python Support
This script supports both, Python 3 and Python 2.

## Windows Binary
It is recommended that windows users use this binary to save both, your head and time from installing all the dependencies. 

You need to download and install [Node.js](https://nodejs.org/en/) and make sure it is in your Windows path (watch out for the tick box during install). 

You also need to download [PhantomJS](http://phantomjs.org/download.html) and keep it in the same directory as that of this windows binary file or you need to have PhantomJS in your path. PhantomJS is required for some websites, which you can check in the [list of supported sites](https://github.com/Xonshiz/comic-dl/blob/master/Supported_Sites.md).

If you already have it, then you can download this binary and start using the script right off the bat :
* `Binary (x86)` : [Click Here](https://github.com/Xonshiz/comic-dl/releases/latest)


## List of Arguments
Currently, the script supports these arguments :
```
-h, --help                             Prints the basic help menu of the script and exits.
-i,--input                             Defines the input link to the comic/manga.
-V,--version                           Prints the VERSION and exits.
-u,--username                          Indicates username for a website.
-p,--password                          Indicates password for a website.
-v,--verbose                           Enables Verbose logging.
--sorting							   Sorts the download order.(VALUES = asc, ascending,old,new,desc,descending,latest,new)
-a, --auto                             Download new chapters automatically (needs config file!)
-c, --config                           Generates config file for autodownload function
-dd,--download-directory               Specifies custom download location for the comics/manga.
-rn,--range                            Selects the range of Chapters to download (Default = All) [ Ex : --range 1-10 (This will download first 10 episodes of a series)]
--convert						       Tells the script to convert the downloaded Images to PDF or anything else. (Supported Values : pdf, cbz) (Default : No) [By default, script will not convert anything.]
--keep   							   Tells the script whether to keep the files after conversion or not. (Supported : No, False) (Default : Yes/True) [By default, images will be kept even after conversion.]
--quality   						   Tells the script about the image quality you want to download. (Supported Values : low/bad/worst/mobile/cancer) [By default, images will be downloaded in Highest Quality Available. No need to provide any option.]
-find, --search                        Searches for a manga through the Manga Eden Database.
-ml, --manga-language                  Selects the language for manga. 0 is English (Default) and 1 is Italian.
-sc, --skip-cache                      Forces to skip cache checking.
-cid, --chapter-id                     Takes the Chapter ID to list all the chapters in a Manga.
-fd, --force-download                  Forces download of chapters, when using comic-dl's search function.
-pid, --page-id                        Takes the Page ID to download a particular "chapter number" of a manga.
```

## Language Codes:
These codes correspond to the languages. So, just pass in these language codes, to download Manga/Comic in that language (only supported by few sites).

Language Code --> Language
--------------------------
```
0 --> English
1 --> Italian
2 --> Spanish
3 --> French
4 --> German
5 --> Portuguese
6 --> Turkish
7 --> Indonesian
8 --> Greek
9 --> Filipino
10 --> Polish
11 --> Thai
12 --> Malay
13  --> Hungarian
14 --> Romanian
15 -->  Arabic
16 --> Hebrew
17 --> Russian
18 --> Vietnamese
19 --> Dutch
20 --> Bengali
21 --> Persian
22 --> Czech
23 --> Brazilian
24 --> Bulgarian
25 --> Danish
26 --> Esperanto
27 --> Swedish
28 --> Lithuanian
29 --> Other 
```

#### Note :
1.) Some websites like bato.to don't let you view some pages if you're not logged in. You'll have to create an account and pass the login information to the script via `-p` and `-u` arguments.

2.) Since omgbeaupeep is uh... well, you just need to pass the absolute chapter numbers in the range section for that. For eg : Check out [Richie Rich](http://www.omgbeaupeep.com/comics/Richie_Rich/647/). If you want to download first 600 episodes, you would pass : --range 001-600. Just check the URLs for those chapters and pass accordingly.

## Using The Search
In the updated of version 2017.12.28, searching is also available. This is a rather confusing approach though, so carefully read this section.

When you search via this tool, you will get the list of Manga and their respective unique IDs, that you will later use to download those Manga. Firstly, you will search for a Manga, it'll show it's unique ID, which you will copy and then pass into the tool again, it will list all the  chapters listed in that particular Manga. The tool will then ask whether you want to download all the chapters belonging to that Manga. You can type in "Yes", "Y", "N" or "No" accordingly.

### How To Find A Manga:
To search for a Manga, you need to use `-find` or `--search` argument followed by Manga Name.
```
Windows Binary Command : `comic_dl.exe -find "<name_of_manga>"`
Python Command : `__main__.py -find "<name_of_manga>"`
```

For Example : If we wish to search for "One Piece", we wil use this : `comic_dl.exe -find "One Piece"`

This will show something like this :
```
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
```

As you can see, all the Manga matching the name show up, along with their unique IDs. You need to note these IDs down, if you want to download any of these Manga.
Here, for sake of an example, we'll take "One Piece" Manga and its ID is : "4e70ea10c092255ef7004aa2".
#### Note :
* When ever you search/find a Manga, comic_dl makes a "Manga_Eden_Data.json" file, which more or less serves as a Cache. It'll always reference the cache file for the next 24 hours. However, if you don't want it to use that cache file, just pass `--skip-cache` argument along with your command, and it will ignore the cache completely and fetch fresh resources and overwrite the older cache to update it.
* By default, the tool searches for only Manga translated in English Language. But, if you want to search for Manga translated in Italian, you can pass this argument : `--manga-language 1`.

### Getting List Of Chapters For A Manga:
So, now that you have the Manga's unique ID (mentioned above), you can now use that ID to get list of all the chapters for that Manga, or can even download those chapters directly.
So, to list all the chapters of "One Piece", we will pass its ID with the argument `--chapter-id`. The command will be:
```
Windows Binary Command : `comic_dl.exe --chapter-id "<unique_id_of_manga>"`
Python Command : `__main__.py --chapter-id "<unique_id_of_manga>"`
```

Our example command for One Piece would be : `comic_dl.exe --chapter-id "4e70ea10c092255ef7004aa2"`

This will return all the chapters, along with their unique IDs, which can be later used to download a separate chapter.
```
Chapter Number --> Chapter ID
-----------------------------
761.5 --> 54ad50d045b9ef961eeeda2e
714.5 --> 5552a262719a163d21dc7125
2 --> 4efe1d2ac0922504a300001a
127.5 --> 54ad15c445b9ef961eee798b
4 --> 4efe1d20c092250492000014
379.5 --> 5372485a45b9ef6a97744417
217.5 --> 54ad1f3245b9ef961eee826b
```
#### Note:
* If you use this command, it'll just list the chapters and then ask whether you want to download the chapters or not. If you wish to download the chapters without asking, just pass `--force-download` option along with the main command line. Script will NOT ask you anything. It'll list the chapters and start downloading them.
* If you wish to download only a few chapters in a range, you can do so by giving the good old `--range` command. If you pass this argument, the script will not ask you whether you want to download the chapters or not. You will not need `--force-download` option, if you are using `--range` already.
* Sorting is NOT supported in this, yet. YET!

### Download A Chapter:
You can download all the chapters of a Manga, as stated in the previous step. But, if you wish to download a particular chapter, then you need to get the unique ID of the chapter (mentioned above) and then download that chapter separately.
You need to use `--page-id "<unique_id_of_chapter>"` argument.
```
Windows Binary Command : `comic_dl.exe --page-id "<unique_id_of_chapter>"`
Python Command : `__main__.py --page-id "<unique_id_of_chapter>"`
```
Our example command for One Piece, chapter 2 would be : `comic_dl.exe --page-id "4efe1d2ac0922504a300001a"`
#### Note:
* If you download the chapter separately, you will need to provide the `Manga Name` and `Chapter Number` yourself. Because MangaEden's API doesn't list those values in their JSON reply (weird).


## Youtube Tutorial
[![Check The YouTube Tutorial](https://img.youtube.com/vi/TmQYhLHEZxA/0.jpg)](https://www.youtube.com/watch?v=TmQYhLHEZxA)

## Usage
With this script, you have to pass arguments in order to be able to download anything. Passing arguments in a script is pretty easy. Since the script is pretty basic, it doesn't have too many arguments. Go check the [`ARGUMENTS SECTION`](https://github.com/Xonshiz/comic-dl#list-of-arguments) to know more about which arguments the script offers.

Follow the instructions according to your OS :

### Windows
After you've saved this script in a directory/folder, you need to open `command prompt` and browse to that directory and then execute the script. Let's do it step by step :
* Open the folder where you've downloaded the files of this repository.
* Hold down the **`SHIFT`** key and while holding down the SHIFT key, **`RIGHT CLICK`** and select `Open Command Prompt Here` from the options that show up.
* Now, in the command prompt, type this :

*If you're using the windows binary :*

`comic_dl.exe -i <URL TO THE COMIC>`

*If you're using the Python Script :*

`__main__.py -i <URL TO THE COMIC>`

URL can be any URL of the [supported websites](https://github.com/Xonshiz/comic-dl/blob/master/Supported_Sites.md).

### Linux/Debian
After you've saved this script in a directory/folder, you need to open `command prompt` and browse to that directory and then execute the script. Let's do it step by step :
* Open a terminal, `Ctrl + Alt + T` is the shortcut to do so (if you didn't know).
* Now, change the current working directory of the terminal to the one where you've downloaded this repository.
* Now, in the Terminal, type this :

`__main__.py -i <URL TO THE COMIC>`

URL can be any URL of the [supported websites](https://github.com/Xonshiz/comic-dl/blob/master/Supported_Sites.md).

## Auto Download
You can autodownload the new chapters of your favorite comics by creating a config file in json format.

To generate the config file run the comand below and follow the instructions

```
python __main__.py --config
```
or with the binary 

```
comic_dl.exe --config
```

This commands supports the creation of the config file, the addition and remove of series and the edition of the common download configuration.

Once the config file is generated you can download automatically the new chapters available for your selected comics by running the command bellow. The command will automatically update the config file to the lastest chapter downloaded, so in the next run it'll download just the new ones. 

```
python __main__.py --auto
```
or with the binary 

```
comic_dl.exe --auto
```

_Note: It's not necesary to keep the comic files to download the next chapters._

## Features
This is a very basic and small sript, so at the moment it only have a few features.
* Downloads a Single Chapter and puts in a directory with the comic name, volume and chapter.
* Downloads all the chapters available for a series.
* Skip if the file has already been downloaded.
* Show human readable error(s) in most places.

## Changelog
You can check the changelog [**`HERE`**](https://github.com/Xonshiz/comic-dl/blob/master/Changelog.md).

## Opening An Issue/Requesting A Site
If your're planning to open an issue for the script or ask for a new feature or anything that requires opening an Issue, then please do keep these things in mind.

### Reporting Issues
If you're going to report an issue, then please run the script again with the "-v or --verbose" argument. It should generate a file in the same directory, with the name "Error Log.log". Copy that log file's data and post it on a [Gist](https://gist.github.com/) and share that gist's link while reporting the issue here. Make sure you **EDIT OUT YOUR USERNAME AND PASSWORD**, if supplied within the command.

If you don't include the verbose log, there are chances it'll take time to fix the issue(s) you're having. Please follow this syntax :

**Command You Gave** : What was the command that you used to invoke the script?

**Expected Behaviour** : After giving the above command, what did you expect shoud've happened?

**Actual Behaviour** : What actually happened?

**Link To Gist** : As mentioned earlier, post the error log in a gist and share that link here.

P.S : Just attaching a screenshot will NOT tell or anyone else what happened behind the scenes. So, Error Log is mandatory.

 
### Suggesting A Feature
If you're here to make suggestions, please follow the basic syntax to post a request :

**Subject** : Something that briefly tells us about the feature.

**Long Explanation** : Describe in details what you want and how you want.

This should be enough, but it'll be great if you can add more ;)

# Notes
* comic.naver.com has korean characters and some OS won't handle those characters. So, instead of naming the file folder with the series name in korean, the script will download and name the folder with the comic's ID instead.

* Bato.to requires you to "log in" to read some chapters. So, to be on a safe side, provide the username/password combination to the script via "-p" and "-u" arguments.

* Bato.to also has comics for various languages. You need to pass the language code via "-ml" argument. Read the [Language Codes](#language-codes) section to find out the language codes.

* Bato.to only supports custom language downloads in "Batch" mode.

* URLs with special characters are tricky to work with, because of "Character Encoding". If you wish to download such a comic/manga, you will need to use Python 3 (If on  python) and also, you need to set your terminal's character encoding to "utf-8" or "latin-1". #95 is the same issue.

# Donations
You can always send some money over from this :

Paypal : [![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.me/xonshiz)

Patreon Link : https://www.patreon.com/xonshiz

Any amount is appreciated :)
