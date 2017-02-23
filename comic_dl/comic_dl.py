#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function
import os
import sys
import argparse
import platform
from honcho import url_checker
import logging
from version import __version__

def version():
    print('\n')
    print('{:^80}'.format('Current Version : %s')%(__version__))
    print('\n')
    print('{:^80}'.format("More info : comic-dl -h"))

def usage():
    print('\n')
    print('{:^80}'.format('################################################'))
    print('{:^80}'.format('Comic-DL Usage'))
    print('{:^80}'.format('################################################\n'))
    print('\n')
    print('{:^80}'.format('Author : Xonshiz | Version : %s')%(__version__))
    print('{:^80}'.format('-------------------------------------------------\n'))
    print("Comic-dl is a command line tool to download manga and comics from various comic and manga sites.")
    print("Using the script is pretty simple and should be easy for anyone familiar with a command line/shell.")
    print('\n')
    print('{:^80}'.format("USAGE : comic-dl -i <URL to comic>"))
    print('\n')
    print("Check Supported websites : https://github.com/Xonshiz/comic-dl/blob/master/Supported_Sites.md ",'\n')
    print("Available Arguments : ")
    print('{:^80}'.format("-i,--input : Specifies the Input URL"))
    print('{:^80}'.format("-h : Prints this help menu"))
    print('{:^80}'.format("--version : Prints the current version and exits"))
    print('{:^80}'.format("-v, --verbose : Prints important debugging messages on screen."))
    print('{:^80}'.format("-a,--about : Shows the info about this script and exits."))
    print('{:^80}'.format("-u,--username : Indicates username for a website."))
    print('{:^80}'.format("-p,--password : Indicates password for a website."))
    print('{:^80}'.format("--sorting : Sorts the download order.(VALUES = asc, ascending,old,new,desc,descending,latest,new)"))
    

def main(argv):
    current_directory = str(os.getcwd())
    parser = argparse.ArgumentParser(description='Comic-dl is a command line tool to download manga and comics from various comic and manga sites.')
    parser.add_argument('--version',action='store_true',help='Shows version and exits' )
    parser.add_argument('-a','--about',action='store_true',help='Shows the info regarding this script' )
    parser.add_argument('-i','--input',nargs=1,help='Inputs the URL to comic')
    parser.add_argument('-p','--password',nargs=1,help='Indicates password for a website',default='None')
    parser.add_argument('-u','--username',nargs=1,help='Indicates username for a website',default='None')
    parser.add_argument("-v", "--verbose", help="Prints important debugging messages on screen.", action="store_true")
    parser.add_argument("--sorting", nargs=1, help="Sorts the download order.")
    
    logger = "False"
    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(format='%(levelname)s: %(message)s', filename="Error Log.log", level=logging.DEBUG)
        logging.debug('You have successfully set the Debugging On.')
        logging.debug("Arguments Provided : %s" % (args))
        logging.debug("Operating System : %s - %s - %s" % (platform.system(), platform.release(), platform.version()))
        logging.debug("Python Version : %s (%s)" % (platform.python_version(), platform.architecture()[0]))
        logger = "True"


    if args.version:
        version()
        sys.exit()

    if args.about:
        usage()
        sys.exit()
    if args.input:
        input_url = str(args.input[0]).strip()
        User_Password = str(args.password[0].strip())
        User_Name = str(args.username[0].strip())
        sortingOrder = str(args.sorting[0].strip())
        url_checker(input_url, current_directory, User_Name, User_Password, logger, sortingOrder)
        sys.exit()

if __name__ == "__main__":
   main(sys.argv[1:])
