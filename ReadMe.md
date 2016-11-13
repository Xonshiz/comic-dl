# Comic-DL

Comic-dl is a command line tool to download Comics and Manga from various Manga and Comic sites easily.

> Don't overuse this script. Support the developers of those websites by disabling your adblock on their site. 
>Advertisments pay for the website servers.

### Table of Content

* [Supported Sites](https://github.com/Xonshiz/comic-dl/blob/master/Supported_Sites.md)
* [Dependencies Installation](https://github.com/Xonshiz/comic-dl#dependencies-installation)
    * [Linux/Debian](https://github.com/Xonshiz/comic-dl#linuxdebian-)
    * [Windows](https://github.com/Xonshiz/comic-dl#windows-)
    * [Mac OS X](https://github.com/Xonshiz/comic-dl#mac-os-x-)
* [Installation](https://github.com/Xonshiz/comic-dl#installation)
* [Windows Binary](https://github.com/Xonshiz/comic-dl#windows-binary)
* [List of Arguments](https://github.com/Xonshiz/comic-dl#list-of-arguments)
* [Usage](https://github.com/Xonshiz/comic-dl#usage)
    * [Windows](https://github.com/Xonshiz/comic-dl#windows)
    * [Linux/Debian](https://github.com/Xonshiz/comic-dl#linuxdebian)
* [Features](https://github.com/Xonshiz/comic-dl#features)
* [Changelog](https://github.com/Xonshiz/comic-dl/blob/master/Changelog.md)
* [Opening An Issue/Requesting A Site](https://github.com/Xonshiz/comic-dl#opening-an-issuerequesting-a-site)
    * [Reporting Issues](https://github.com/Xonshiz/comic-dl#reporting-issues)
    * [Suggesting A Feature](https://github.com/Xonshiz/comic-dl#suggesting-a-feature)

## Supported Websites
You can check the list of supported websites [**`HERE`**](https://github.com/Xonshiz/comic-dl/blob/master/Supported_Sites.md).

## Dependencies Installation
This script can run on multiple Operating Systems. So, if you're using the `python` script instead of the `windows binary` of this script, then you'll need to get things ready first. Follow the instructions mentioned below, according to your OS.

### Linux/Debian :
Since most (if not all) Linux/Debian OS come with python pre-installed, you don't have to install python manually. Make sure you're using python >= 2.7.x though.

We need `pip` to install any external dependenc(ies). So, open any terminal and type in `pip list` and if it shows some data, then it is fine. But, if it shows error, like `pip not found` or something along this line, then you need to install `pip`. Just type this command in terminal :

> `sudo apt-get install python-pip`

If you're on Fedora, CentOS/RHEL, openSUSE, Arch Linux, then you simply need to follow [`THIS TUTORIAL`](https://packaging.python.org/install_requirements_linux/) to install `pip`.

If this still doesn't work, then you'll manually need to install pip. Doing so is an easy one time job and you can follow   [`THIS TUTORIAL`](https://pip.pypa.io/en/stable/installing/) to do so.

### Windows :
If you're on windows, then it is recommended to download the [`windows binary`](#) for this script. If you use the windows binary, you don't need to install anything. But, if for some weird reason you want to use Python script instead, then follow these steps :

* Install Python > 2.7.6. Download the desired installer from [here](https://www.python.org/downloads/).
* [Add it in the system path](http://superuser.com/questions/143119/how-to-add-python-to-the-windows-path) (if not already added).
* If you're using python >2.7.9, you don't need to install `PIP`. However, if you don't have pip installed and added in windows path, then do so by following [this little tutorial](http://stackoverflow.com/a/12476379).
* Download [this `text`]() file and put it in some directory/folder.
* Open Command Prompt and browse to the directory where you downloaded your requiremenets.txt file and run this command :
```
pip install -r requirements.txt
```
* It should install the required external libraries.

Well, if everything came up good without any error(s), then you're good to go!

### Mac OS X :
Mac OS X users will have to fetch their version of `Python` and `Pip`.
* Python installation guide : http://docs.python-guide.org/en/latest/starting/install/osx/
* Pip installation guide : http://stackoverflow.com/questions/17271319/installing-pip-on-mac-os-x

After downloading and installing these, you need to add PIP & Python in your path. Follow [`THIS LITTLE GUIDE`](http://www.pyladies.com/blog/Get-Your-Mac-Ready-for-Python-Programming/) to install both, Python & pip successfully.

## Installation
After installing and setting up all the dependencies in your Operating System, you're good to go and use this script.
The instructions for all the OS would remain same. Download [`THIS REPOSITORY`]() and put it somewhere in your system.

**Windows users**, it's better to not place it places where it requires administrator privileges. Good example would be `C:\Windows`. This goes for both, the Python script and the windows binary file (.exe).

**Linux/Debian** users make sure that this script is executable.just run this command, if you run into problem(s) :

> `chmod +x comic-dl.py`

and then, execute with this :

> `./comic-dl.py`

## Windows Binary
It is recommended that windows users use this binary to save both, your head and time from installing all the dependencies. You can download the binary and start using the script right off the bat. Grab the respective binaries from the links below :
* `x86 Systems` : [COMING SOON](#)
* `x64 Systems` : [Click Here](https://github.com/Xonshiz/comic-dl/releases/tag/v2016.11.13)

## List of Arguments
Currently, the script supports these arguments :
```
-h, --help                             Prints the basic help menu of the script and exits.
-i,--input                             Defines the input link to the comic/manga.
-V,--version                           Prints the VERSION and exits.
-a,--about                             Prints ABOUT and USAGE of the script and exits.
```

## Usage
With this script, you have to pass arguments in order to be able to download anything. Passing arguments in a script is pretty easy. Since the script is pretty basic, it doesn't have too many arguments. Go check the [`ARGUMENTS SECTION`] to know more about which arguments the script offers.

Follow the instructions according to your OS :

### Windows
After you've saved this script in a directory/folder, you need to open `command prompt` and browse to that directory and then execute the script. Let's do it step by step :
* Open the folder where you've downloaded the files of this repository.
* Hold down the **`SHIFT`** key and while holding down the SHIFT key, **`RIGHT CLICK`** and select `Open Command Prompy Here` from the options that show up.
* Now, in the command prompt, type this :

*If you're using the windows binary :*
>>> `comic-dl.exe -i <URL TO THE COMIC>`

*If you're using the Python Script :*
>>> `comic-dl.py -i <URL TO THE COMIC>`

URL can be any URL of the [supported websites]().

### Linux/Debian
After you've saved this script in a directory/folder, you need to open `command prompt` and browse to that directory and then execute the script. Let's do it step by step :
* Open a terminal, `Ctrl + Alt + T` is the shortcut to do so (if you didn't know).
* Now, change the current working directory of the terminal to the one where you've downloaded this repository.
* Now, in the Terminal, type this :

>>> `comic-dl.py -i <URL TO THE COMIC>`

URL can be any URL of the [supported websites]().

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
If you're about to report some issue with the script, the please do include these things :
* The command your entered. Yes, with the URL
* The output of that command. You can simply copy the text from the terminal/command prompt and paste it. Make sure you put that output inside `` (tilde).
* Your Operating System and python version.
 
### Suggesting A Feature
If you're here to make suggestions, please follow the basic syntax to post a request :

**Subject** : Something that briefly tells us about the feature.

**Long Explanation** : Describe in details what you want and how you want.

This should be enough, but it'll be great if you can add more ;)
