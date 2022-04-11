Dependencies Installation
=========================

This script can run on multiple Operating Systems. You need ``Node.js``
in your system’s path for this script to work (You need this on each and
every Operating System, even on WINDOWS :/). Download the ``Node.Js``
from `Node.js official website <https://nodejs.org/en/>`__. Doesn’t
matter which operating system you’re on, this is a must. Follow the
instructions mentioned below, according to your OS.

Linux/Debian :
--------------

Since most (if not all) Linux/Debian OS come with python pre-installed,
you don’t have to install python manually. Make sure you’re using python
>= 2.7.x though.

We need ``pip`` to install any external dependency(ies). So, open any
terminal and type in ``pip list`` and if it shows some data, then it is
fine. But, if it shows error, like ``pip not found`` or something along
this line, then you need to install ``pip``. Just type this command in
terminal :

``sudo apt-get install python-pip``

If you’re on Fedora, CentOS/RHEL, openSUSE, Arch Linux, then you simply
need to follow
`THIS TUTORIAL <https://packaging.python.org/install_requirements_linux/>`__
to install ``pip``.

If this still doesn’t work, then you’ll manually need to install pip.
Doing so is an easy one time job and you can follow
`THIS TUTORIAL <https://pip.pypa.io/en/stable/installing/>`__ to do
so.

Windows :
---------

If you’re on windows, then it is recommended to download the `Windows Binary <windows_binary.html>`_
for this script. If you use the windows binary, you don’t need to
install anything, except Node.js. But, if for some weird reason you want
to use Python script instead, then follow these steps :

-  Install Python > 2.7.6. Download the desired installer from
   `here <https://www.python.org/downloads/>`__.
-  `Add it in the system
   path <http://superuser.com/questions/143119/how-to-add-python-to-the-windows-path>`__
   (if not already added).
-  If you’re using python >2.7.9, you don’t need to install ``PIP``.
   However, if you don’t have pip installed and added in windows path,
   then do so by following `this little
   tutorial <http://stackoverflow.com/a/12476379>`__.
-  Download `this
   `text <https://github.com/Xonshiz/comic-dl/blob/master/requirements.txt>`__
   file and put it in some directory/folder.
-  Open Command Prompt and browse to the directory where you downloaded
   your requiremenets.txt file and run this command :

::

   pip install -r requirements.txt

-  It should install the required external libraries.

Now, install Node.Js as well and make sure it’s in your path.

Well, if everything came up good without any error(s), then you’re good
to go!

Mac OS X :
----------

Mac OS X users will have to fetch their version of ``Python`` and
``Pip``.

1. Python installation guide :
http://docs.python-guide.org/en/latest/starting/install/osx/

2. Pip installation guide :
http://stackoverflow.com/questions/17271319/installing-pip-on-mac-os-x

After downloading and installing these, you need to add PIP & Python in
your path. Follow
`THIS LITTLE GUIDE <http://www.pyladies.com/blog/Get-Your-Mac-Ready-for-Python-Programming/>`__
to install both, Python & pip successfully.