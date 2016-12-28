# Comic-DL | [![Build Status](https://travis-ci.org/Xonshiz/comic-dl.svg?branch=master)](https://travis-ci.org/Xonshiz/comic-dl) [![Documentation Status](https://readthedocs.org/projects/comic-dl/badge/?version=latest)](http://comic-dl.readthedocs.io/en/latest/?badge=latest)

Comic-dl is a command line tool to download Comics and Manga from various Manga and Comic sites easily. Idea from [youtube-dl](https://github.com/rg3/youtube-dl)

> Don't overuse this script. Support the developers of those websites by disabling your adblock on their site. 
>Advertisments pay for the website servers.

## Table of Content

* [Supported Sites](http://comic-dl.readthedocs.io/en/latest/Supported_Sites/)
* [Dependencies Installation](#dependencies-installation)
    * [Linux/Debian](#linuxdebian-)
    * [Windows](#windows-)
    * [Mac OS X](#mac-os-x-)
* [Installation](#installation)
* [Python 3 Support](#python-3-support)
* [Windows Binary](#windows-binary)
* [List of Arguments](#list-of-arguments)
* [Usage](#usage)
    * [Windows](#windows)
    * [Linux/Debian](#linuxdebian)
* [Features](#features)
* [Changelog](http://comic-dl.readthedocs.io/en/latest/Changelog/)
* [Opening An Issue/Requesting A Site](#opening-an-issuerequesting-a-site)
    * [Reporting Issues](#reporting-issues)
    * [Suggesting A Feature](#suggesting-a-feature)
* [Contributors](http://comic-dl.readthedocs.io/en/latest/Contributors/)
* [Notes](#notes)

## Supported Websites
You can check the list of supported websites [**`HERE`**](http://comic-dl.readthedocs.io/en/latest/Supported_Sites/).

## Dependencies Installation
This script can run on multiple Operating Systems. So, if you're using the `python` script instead of the `windows binary` of this script, then you'll need to get things ready first. Follow the instructions mentioned below, according to your OS.

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
If you're on windows, then it is recommended to download the [`windows binary`](http://comic-dl.readthedocs.io/en/latest/?badge=latest#windows-binary) for this script. If you use the windows binary, you don't need to install anything. But, if for some weird reason you want to use Python script instead, then follow these steps :

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

Well, if everything came up good without any error(s), then you're good to go!

### Mac OS X :
Mac OS X users will have to fetch their version of `Python` and `Pip`.
* Python installation guide : http://docs.python-guide.org/en/latest/starting/install/osx/
* Pip installation guide : http://stackoverflow.com/questions/17271319/installing-pip-on-mac-os-x
* PhantomJS Mac Binary : http://phantomjs.org/download.html (Download the latest build for your OS)

After downloading and installing these, you need to add PIP & Python in your path. Follow [`THIS LITTLE GUIDE`](http://www.pyladies.com/blog/Get-Your-Mac-Ready-for-Python-Programming/) to install both, Python & pip successfully.

## Installation
After installing and setting up all the dependencies in your Operating System, you're good to go and use this script.
The instructions for all the OS would remain same. Download [`THIS REPOSITORY`](https://github.com/Xonshiz/comic-dl/archive/master.zip) and put it somewhere in your system. Move over the `comic_dl` folder.

**Windows users**, it's better to not place it places where it requires administrator privileges. Good example would be `C:\Windows`. This goes for both, the Python script and the windows binary file (.exe).

**Linux/Debian** users make sure that this script is executable.just run this command, if you run into problem(s) :

`chmod +x comic-dl.py`

and then, execute with this :

`./comic-dl.py`

## Python 3 Support
If you're using python 3, then you'd want to download the contents of the `comic_dl Python3` folder/directory. Everything in that folder has been written and updated to support python 3.

## Windows Binary
It is recommended that windows users use this binary to save both, your head and time from installing all the dependencies. 

You need to download [PhantomJS](http://phantomjs.org/download.html) and keep it in the same directory as that of this windows binary file or you need to have PhantomJS in your path. PhantomJS is required for some websites, which you can check in the [list of supported sites](http://comic-dl.readthedocs.io/en/latest/Supported_Sites/).

If you already have it, then you can download this binary and start using the script right off the bat :
* `Binary (x86)` : [Click Here](https://github.com/Xonshiz/comic-dl/releases/latest)


## List of Arguments
Currently, the script supports these arguments :
```
-h, --help                             Prints the basic help menu of the script and exits.
-i,--input                             Defines the input link to the comic/manga.
-V,--version                           Prints the VERSION and exits.
-a,--about                             Prints ABOUT and USAGE of the script and exits.
-u,--username                          Indicates username for a website.
-p,--password                          Indicates password for a website.
```
#### Note :
Some websites like bato.to don't let you view some pages if you're not logged in. You'll have to create an account and pass the login information to the script via `-p` and `-u` arguments.

## Usage
With this script, you have to pass arguments in order to be able to download anything. Passing arguments in a script is pretty easy. Since the script is pretty basic, it doesn't have too many arguments. Go check the [`ARGUMENTS SECTION`](http://comic-dl.readthedocs.io/en/latest/?badge=latest#list-of-arguments) to know more about which arguments the script offers.

Follow the instructions according to your OS :

### Windows
After you've saved this script in a directory/folder, you need to open `command prompt` and browse to that directory and then execute the script. Let's do it step by step :
* Open the folder where you've downloaded the files of this repository.
* Hold down the **`SHIFT`** key and while holding down the SHIFT key, **`RIGHT CLICK`** and select `Open Command Prompy Here` from the options that show up.
* Now, in the command prompt, type this :

*If you're using the windows binary :*

`comic-dl.exe -i <URL TO THE COMIC>`

*If you're using the Python Script :*

`comic-dl.py -i <URL TO THE COMIC>`

URL can be any URL of the [supported websites](http://comic-dl.readthedocs.io/en/latest/Supported_Sites/).

### Linux/Debian
After you've saved this script in a directory/folder, you need to open `command prompt` and browse to that directory and then execute the script. Let's do it step by step :
* Open a terminal, `Ctrl + Alt + T` is the shortcut to do so (if you didn't know).
* Now, change the current working directory of the terminal to the one where you've downloaded this repository.
* Now, in the Terminal, type this :

`comic-dl.py -i <URL TO THE COMIC>`

URL can be any URL of the [supported websites](http://comic-dl.readthedocs.io/en/latest/Supported_Sites/).

## Features
This is a very basic and small sript, so at the moment it only have a few features.
* Downloads a Single Chapter and puts in a directory with the comic name, volume and chapter.
* Downloads all the chapters available for a series.
* Skip if the file has already been downloaded.
* Show human readable error(s) in most places.

## Changelog
You can check the changelog [**`HERE`**](http://comic-dl.readthedocs.io/en/latest/Changelog/).

## Opening An Issue/Requesting A Site
If your're planning to open an issue for the script or ask for a new feature or anything that requires opening an Issue, then please do keep these things in mind.

### Reporting Issues
If you're about to report some issue with the script, then please do include these things :
* The command your entered. Yes, with the URL
* The output of that command. You can simply copy the text from the terminal/command prompt and paste it. Make sure you put that inside inside `` (tilde).
* Your Operating System and python version.
 
### Suggesting A Feature
If you're here to make suggestions, please follow the basic syntax to post a request :

**Subject** : Something that briefly tells us about the feature.

**Long Explanation** : Describe in details what you want and how you want.

This should be enough, but it'll be great if you can add more ;)

# Notes
comic.naver.com has korean characters and some OS won't handle those characters. So, instead of naming the file folder with the series name in korean, the script will download and name the folder with the comic's ID instead.