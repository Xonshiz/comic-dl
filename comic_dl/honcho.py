#!/usr/bin/env python
# -*- coding: utf-8 -*-


'''

This python module decides which URL should be assigned to which other module from the site package.

'''



from sites.yomanga import yomanga_Url_Check
from sites.gomanga import gomanga_Url_Check
from sites.mangafox import mangafox_Url_Check
import os
import urllib2




def url_checker(input_url,current_directory):
	
	domain = urllib2.urlparse.urlparse(input_url).netloc

	if domain in ['mangafox.me']:
		mangafox_Url_Check(input_url,current_directory)
		pass
	elif domain in ['yomanga.co']:
		yomanga_Url_Check(input_url,current_directory)
		pass
	elif domain in ['gomanga.co']:
		gomanga_Url_Check(input_url,current_directory)
		pass
	elif domain in ['']:
		print 'You need to specify at least 1 URL. Please run : comic-dl -h'
	else:
		print "%s is unsupported at the moment. Please request on Github repository."%(domain)
