#!/usr/bin/python
import re
import numpy
import os.path
import argparse

def parseFile(args):
	filePath = args.filePath
	if not os.path.exists(filePath):
		print ("File " + filePath + " was not found. Exiting")
		exit(1)
	urls = {}
	pattern1 = r"[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}"
	pattern2 = r"[a-f0-9]{32}"
	file = open(filePath, 'r')
	lines = file.readlines()
	file.close()
	length = 0
	for line in lines:
		if 'url' in line and 'took' in line:
			result = re.search("url='(.*)' was", line)
			url = result.group(1)
			url = re.sub(pattern1,"*",url)
			url = re.sub(pattern2,"*",url)
			if len(url) > length:
				length = len(url)
			result = re.search("t='(.*)ms'", line)
			time = result.group(1)
			if url in urls:
				urls[url] = urls[url] + [int(time)]
			else:
				urls[url] = [int(time)]
	url_header = "URL"
	invocations_header = "# invocations"
	avg_header = "Avg. response time"
	print "|" + url_header + " "*(length-3) + "|" + invocations_header + "|" + avg_header + "|"
	for url in urls:
		invocations = str(len(urls[url]))
		avg = str(int(numpy.mean(urls[url]))) + " ms"
		print "|" + url + " "*(length-len(url)) + "|" + invocations + " "*(len(invocations_header)-len(invocations)) + "|" + avg + " "*(len(avg_header)-len(avg)) + "|"

parser = argparse.ArgumentParser(description="parses a tomcat log file for endpoints invocations and response times")
parser.add_argument('--file', dest='filePath', required=True, help='Log file path')
parser.set_defaults(func=parseFile)
args = parser.parse_args()
try:
	args.func(args)
except Exception as err:
	print str(err)