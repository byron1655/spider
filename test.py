import hashlib
import time
import datetime
import socket
import urllib2
import os
from bs4 import BeautifulSoup
from pymongo import Connection
from urllib2 import Request, urlopen, URLError, HTTPError
import re
import time


url = "http://www.163.com"

def getPageContent(url):
	result = ""
	try:
		req = urllib2.Request(url)
		con = urllib2.urlopen(req)
		doc = con.read()
		con.close()
		return doc.decode('gbk').encode('utf8')
	except HTTPError, e:
		return result
	except URLError,e:
		return result
	else:
		return result

i = 0
def spider():
	global db,maxcount,i,url
	datetime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
	#item = db.plan_links.find_one({'is_index':0},{'url':1})
	#url = item['url']
	content = getPageContent(url)

	return content

print spider