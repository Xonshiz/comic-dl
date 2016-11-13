#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import re
import os
import sys
from  more_itertools import unique_everseen
import urllib2
import urllib
import shutil
from urllib2 import URLError
from bs4 import BeautifulSoup

def single_chapter(url,current_directory):
	
	if not url:
		print "Couldn't get the URL. Please report it on Github Repository."
		sys.exit(0)
	
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
		
	}
	
	s = requests.Session()
	response = s.get(url, headers=headers)
	tasty_cookies = response.cookies
	
	Page_source = str(response.text.encode('utf-8'))
	
	Series_Name = str(re.search('\/read\/(.*?)/', url).group(1)).strip().replace('_',' ').title() # Getting the Series Name from the URL itself for naming the folder/dicrectories.
	#print "Series Name : ",Series_Name

	try:
		chapter_number = int(str(re.search('0\/(.*?)/', url).group(1)).strip().replace('0','').replace('/','')) # Getting the chapter count from the URL itself for naming the folder/dicrectories in integer.
	except Exception as e:
		#raise e
		chapter_number = 0 # Name the chapter 0 if nothing INTEGER type comes up
	#print "Chapter No : ",chapter_number

	Raw_File_Directory = str(Series_Name)+'/'+"Chapter "+str(chapter_number)
	#print 'Raw_File_Directory : ',Raw_File_Directory
	File_Directory = re.sub('[^A-Za-z0-9\-\.\'\#\/ ]+', '', Raw_File_Directory) # Fix for "Special Characters" in The series name
	#print "File_Directory : ",File_Directory
	Directory_path = os.path.normpath(File_Directory)
	#print "Directory_path : ",Directory_path
	
	
	ddl_image_list = re.findall('comics(.*?)\"', Page_source)
	#print "Older List : ",ddl_image_list

	ddl_list = list(unique_everseen(ddl_image_list))
	#print ddl_list
	#sys.exit()

	print '\n'
	print '{:^80}'.format('%s - %s')%(Series_Name,chapter_number)
	print '{:^80}'.format('=====================================================================\n')

	for i in ddl_list:
		#print i
		if not os.path.exists(File_Directory):
						os.makedirs(File_Directory)
		ddl_image = "http://gomanga.co/reader/content/comics"+str(i).replace('"','').replace('\\','')
		#print ddl_image
		try:
			#u = urllib2.urlopen(ddl_image, cookies=response.cookies)
			u = requests.get(ddl_image,cookies=tasty_cookies)
		except URLError, e:
			if not hasattr(e, "code"):
				raise
			print "Got error from "+ddl_image, e.code, e.msg
			resp = e
		
		File_Name_Final = str(re.findall('\/(\d+)\.[jpg]|[png]', i)).replace("[","").replace("]","").replace("'","").replace(",","").strip()+"."+str(re.findall('\d\.(.*?)$', str(i))).replace(",","").replace("[","").replace("]","").replace("'","").strip()
		File_Check_Path = str(Directory_path)+'/'+str(File_Name_Final)
		if os.path.isfile(File_Check_Path):
				print 'File Exist! Skipping ',File_Name_Final,'\n'
				pass

		if not os.path.isfile(File_Check_Path):	
			print 'Downloading : ',File_Name_Final
			#urllib.urlretrieve(ddl_image, File_Name_Final)
			response = requests.get(ddl_image, stream=True,cookies=tasty_cookies)
			try:
				with open(File_Name_Final, 'wb') as out_file:
					shutil.copyfileobj(response.raw, out_file)
				File_Path = os.path.normpath(File_Name_Final)
			except Exception as e:
				#raise e
				#print e
				print "Couldn't download file from : ",ddl_image
				pass
			try:
				shutil.move(File_Path,Directory_path)
			except Exception, e:
				#raise e
				print e,'\n'
				#os.remove(File_Path)
				pass

	print '\n'
	print "Completed downloading ",Series_Name

def whole_series(url,current_directory):
	if not url:
		print "Couldn't get the URL. Please report it on Github Repository."
	
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
		
	}
	
	s = requests.Session()
	response = s.get(url, headers=headers)
	tasty_cookies = response.cookies
	
	Page_source = str(response.text.encode('utf-8'))

	Series_Name = str(re.search('\/series\/(.*?)/', url).group(1)).strip().replace('_',' ').title() # Getting the Series Name from the URL itself for naming the folder/dicrectories.
	#print "Series Name : ",Series_Name

	soup = BeautifulSoup(Page_source, 'html.parser')

	chapter_text = soup.findAll('div',{'class':'title'})
	#print chapter_text

	for link in chapter_text:
		x = link.findAll('a')
		for a in x:
			url = a['href']
			single_chapter(url,current_directory)

def gomanga_Url_Check(input_url,current_directory):
	
	gomanga_single_regex = re.compile('https?://(?P<host>gomanga.co)/reader/read/(?P<comic_single>[\d\w-]+)/en/(?P<volume>\d+)?/(?P<Chapter>\d+)?()|(/page/(?P<PageNumber>\d+)?)')
	gomanga_whole_regex = re.compile('^https?://(?P<host>gomanga.co)/reader/(?P<series>series)?/(?P<comic>[\d\w-]+)?(\/|.)$')

	lines = input_url.split('\n')
	for line in lines:
		found = re.search(gomanga_single_regex, line)
		if found:
			match = found.groupdict()
			if match['Chapter']:
				url = str(input_url)
				single_chapter(url,current_directory)
			else:
				pass
				

		
		found = re.search(gomanga_whole_regex, line)
		if found:
			match = found.groupdict()
			if match['comic']:
				url = str(input_url)
				whole_series(url,current_directory)
			else:
				pass






