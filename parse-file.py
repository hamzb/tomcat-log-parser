#!/usr/bin/env python
import re
import numpy
import os.path
import argparse

def parseFile(args):
	filePath = args.filePath
	#Checking if the file actually exists, exiting otherwise.
	if not os.path.exists(filePath):
		print ("File " + filePath + " was not found. Exiting")
		exit(1)
	# Initilizing a dict that will store the URLs as keys and the response times as values. Also Defining the regex patterns of the IDs to remove
	urlsDict = {}
	pattern1 = r"[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}"
	pattern2 = r"[a-f0-9]{32}"
	# Attempting to read the file and exiting if it fails
	try:
		file = open(filePath, 'r')
		lines = file.readlines()
		file.close()
	except Exception as err:
		print "Error, could not read file: " + err
		exit(1)
	# Defining a var called length that will store the max length of URLs. It will be used to format the output later.
	length = 0
	for line in lines:
		# Filtering the lines that have URLs and response times
		if 'url' in line and 'took' in line:
			# Extracting the URL, removing IDs
			result = re.search("url='(.*)' was", line)
			url = result.group(1)
			url = re.sub(pattern1,"*",url)
			url = re.sub(pattern2,"*",url)
			if len(url) > length:
				length = len(url)
			# Extracting response times
			result = re.search("t='(.*)ms'", line)
			time = result.group(1)
			# Storing the information in the dict
			if url in urlsDict:
				urlsDict[url] = urlsDict[url] + [int(time)]
			else:
				urlsDict[url] = [int(time)]
	
	# Working on the output: defining the headers and drawing a table. Most python packages for table formatting are not native ones, so I had to draw the table myself
	urlHeader = "URL"
	invocationsHeader = "# invocations"
	avgHeader = "Avg. response time"
	print "|" + urlHeader + " "*(length-len(urlHeader)) + "|" + invocationsHeader + "|" + avgHeader + "|"
	for url in urlsDict:
		invocations = str(len(urlsDict[url]))
		avg = str(int(numpy.mean(urlsDict[url]))) + " ms"
		print "|" + url + " "*(length-len(url)) + "|" + invocations + " "*(len(invocationsHeader)-len(invocations)) + "|" + avg + " "*(len(avgHeader)-len(avg)) + "|"

# Initializing an argparse object that takes the log file path as an argument and setting the default function to execute
parser = argparse.ArgumentParser(description="parses a tomcat log file for endpoints invocations and response times")
parser.add_argument('--file', dest='filePath', required=True, help='Log file path')
parser.set_defaults(func=parseFile)
args = parser.parse_args()
try:
	args.func(args)
except Exception as err:
	print str(err)