#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import os
import re
import sys
import urllib2
import urllib
import shutil
from bs4 import BeautifulSoup
from urllib2 import URLError

def single_chapter(url,current_directory):
	if not url:
		print "Couldn't get the URL. Please report it on Github Repository."
		sys.exit(0)
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
		
	}
	
	response = requests.get(url, headers=headers)
	Page_source = str(response.text.encode('utf-8'))
	
	try:
		Series_Name = str(re.search('manga\/(.*?)/v', url).group(1)).strip().replace('_',' ').title() # Getting the Series Name from the URL itself for naming the folder/dicrectories.
	except Exception as e:
		#raise e
		#print "Error : ",e,'\n'
		Series_Name = str(re.search('manga\/(.*?)/c', url).group(1)).strip().replace('_',' ').title() # Getting the Series Name from the URL itself for naming the folder/dicrectories.
	
	#print "Series Name : ",Series_Name

	try:
		volume_number = "Volume " + str(re.search('v(.*?)/c', url).group(1)).strip() # Getting the volume count from the URL itself for naming the folder/dicrectories.
	except Exception as e:
		#raise e
		volume_number = "Volume 01"
	#print "Volume No : ",volume_number
	try:
		chapter_number = int(str(re.search('\/c(.*?)/\d', url).group(1)).strip()) # Getting the chapter count from the URL itself for naming the folder/dicrectories in integer.
	except Exception as e:
		#raise e
		chapter_number = float(str(re.search('\/c(.*?)/\d', url).group(1)).strip()) # Getting the chapter count from the URL itself for naming the folder/dicrectories in float.
	#print "Chapter No : ",chapter_number
	First_chapter_link = str(re.search('http://(.*?)/(.*?)/manga/(.*?)/(.*?)/compressed/(.*?)\.jpg', Page_source).group(0)).strip() # Fix if they change the CDN all of a sudden.
	#print First_chapter_link
	current_chapter_count = int(str(re.search('current_page\=(.*?)\;', Page_source).group(1)).strip()) # Getting the last chapter number from the URL itself for naming the folder/dicrectories.
	last_chapter_count = int(str(re.search('total_pages\=(.*?)\;', Page_source).group(1)).strip()) # Getting the last chapter number from the URL itself for naming the folder/dicrectories.
	#print "Last Chapter : ",last_chapter_count

	Raw_File_Directory = str(Series_Name)+'/'+str(volume_number)+'/'+"Chapter "+str(chapter_number)
	#print 'Raw_File_Directory : ',Raw_File_Directory
	File_Directory = re.sub('[^A-Za-z0-9\-\.\'\#\/ ]+', '', Raw_File_Directory) # Fix for "Special Characters" in The series name
	#print "File_Directory : ",File_Directory
	Directory_path = os.path.normpath(File_Directory)
	#print "Directory_path : ",Directory_path

	print '\n'
	print '{:^80}'.format('%s - %s')%(Series_Name,chapter_number)
	print '{:^80}'.format('=====================================================================\n')

	for x in range(current_chapter_count,last_chapter_count+1):
		#print x
		if not os.path.exists(File_Directory):
						os.makedirs(File_Directory)
		if len(str(x)) == 1:
			ddl_image = First_chapter_link.replace('001.jpg','00{0}.jpg'.format(x))
			
			#print ddl_image
			try:
				u = urllib2.urlopen(ddl_image)
			except URLError, e:
				if not hasattr(e, "code"):
					raise
				print "Got error from "+ddl_image, e.code, e.msg
				resp = e
			
			File_Name_Final = str(x).strip()+".jpg"
			File_Check_Path = str(Directory_path)+'/'+str(File_Name_Final)
			#print "Final Check Path : ",File_Check_Path

			if os.path.isfile(File_Check_Path):
				print 'File Exist! Skipping ',File_Name_Final,'\n'
				pass

			if not os.path.isfile(File_Check_Path):	
				print 'Downloading : ',File_Name_Final
				urllib.urlretrieve(ddl_image, File_Name_Final)
				File_Path = os.path.normpath(File_Name_Final)
				try:
					shutil.move(File_Path,Directory_path)
				except Exception, e:
					#raise e
					print e,'\n'
					os.remove(File_Path)
					pass

		else :
			
			ddl_image = First_chapter_link.replace('001','0{0}'.format(x))
			
			#print ddl_image
			try:
				u = urllib2.urlopen(ddl_image)
			except URLError, e:
				if not hasattr(e, "code"):
					raise
				print "Got error from "+ddl_image, e.code, e.msg
				resp = e
			
			File_Name_Final = str(x).strip()+".jpg"
			File_Check_Path = str(Directory_path)+'/'+str(File_Name_Final)
			#print "Final Check Path : ",File_Check_Path

			if os.path.isfile(File_Check_Path):
				print 'File Exist! Skipping ',File_Name_Final,'\n'
				pass

			if not os.path.isfile(File_Check_Path):	
				print 'Downloading : ',File_Name_Final
				urllib.urlretrieve(ddl_image, File_Name_Final)
				File_Path = os.path.normpath(File_Name_Final)
				try:
					shutil.move(File_Path,Directory_path)
				except Exception, e:
					#raise e
					print e,'\n'
					os.remove(File_Path)
					pass
	print '\n'
	print "Completed downloading ",Series_Name

def whole_series(url,current_directory):
	if not url:
		print "Couldn't get the URL. Please report it on Github Repository."

	try:
		Series_Name = str(re.search('manga\/(.*?)/', url).group(1)).strip() # Getting the Series Name from the URL itself for naming the folder/dicrectories.
	except Exception as e:
		#raise e
		print 'Check if the URL is correct or not. Report on Github.'
	#print "Series Name : ",Series_Name

	
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
		
	}
	
	response = requests.get(url, headers=headers)
	Page_source = str(response.text.encode('utf-8'))
	
	try:
		chapter_link_format = "http://mangafox.me/manga/"+str(Series_Name)+"/v"
		#print 'UP : ',chapter_link_format
		links = re.findall('{0}(.*?)html'.format(chapter_link_format),Page_source)
		#print "Lower links : ",links

		if len(links) == 0:
			chapter_link_format = "http://mangafox.me/manga/"+str(Series_Name)+"/c"
			#print chapter_link_format
			links = re.findall('{0}(.*?)html'.format(chapter_link_format),Page_source)


	except Exception as e:
		#raise e
		print "Error : ",e,'\n',"Please report this error on Github repository."

	
	for x in links:
		#print x
		chapter_link = str(str(chapter_link_format)+str(x)+"html").strip()
		#print "URL : ",chapter_link
		single_chapter(chapter_link,current_directory)

def mangafox_Url_Check(input_url,current_directory):
	
	mangafox_single_regex = re.compile('https?://(?P<host>mangafox.me)/manga/(?P<comic>[\d\w-]+)(?P<Volume>(/v\d+)|(.))/(?P<chapter>c\d+(\.\d)?)?/(?P<issue>\d+)?\.html')
	mangafox_whole_regex = re.compile('^https?://(?P<host>mangafox.me)/manga/(?P<comic_series>[\d\w-]+)?|(\/)$')

	lines = input_url.split('\n')
	for line in lines:
		found = re.search(mangafox_single_regex, line)
		if found:
			match = found.groupdict()
			if match['issue']:
				url = str(input_url)
				single_chapter(url,current_directory)
			else:
				pass
				

		
		found = re.search(mangafox_whole_regex, line)
		if found:
			match = found.groupdict()
			if match['comic_series']:
				url = str(input_url)
				whole_series(url,current_directory)
			else:
				pass
