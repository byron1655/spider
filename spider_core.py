# -*- coding: utf-8 -*-
__author__ = 'byron'

import hashlib
import datetime
import traceback
import socket
import os
import string
import re
import time
from bs4 import BeautifulSoup
import urllib2
from urllib2 import Request, urlopen, URLError, HTTPError
from mongodb_helper import MongoDBHelper
from common import Common

class SpiderCore:
    def __init__(self, url="", maxcount=10, maxlevel=3):
        self._url = url
        self._i = 0
        self._maxcount = maxcount
        self._maxlevel = maxlevel

        self._title = 'Untitled Document'
        self._content = ''
        self._level = 0
        db = MongoDBHelper()
        self._db = db

    def getPageInformation(self, url):
        dict_result = {"url": None, "title": None, "content": None, "level": None}
        try:
            req = urllib2.Request(url)
            con = urllib2.urlopen(req)
            doc = con.read()
            con.close()

            soup = BeautifulSoup(doc)
            if soup.title.string is not None:
                title = soup.title.string
            else:
                title = self._title

            content = doc.decode('gbk', 'ignore').encode('utf8')

            dict_result["url"] = url
            dict_result["title"] = title
            dict_result["content"] = content

            return dict_result
        except HTTPError, e:
            return dict_result
        except URLError, e:
            return dict_result
        else:
            return dict_result

    def getPageLinksFromContent(self, info):
        soup = BeautifulSoup(info["content"])
        links = soup.findAll('a')

        pat = re.compile(r'href="([^"]*)"')
        pat2 = re.compile(r'http')
        for item in links:
            if str(item) != "" and not None:
                match = pat.search(str(item))
                if match:
                    href = match.group(1)
                    if pat2.search(href):
                        ans = href
                    else:
                        ans = info[0]+href
                    if Common.isValidUrl(self._url, ans):  # Verify whether legal link
                        info["url"] = ans
                        self._db.saveToPlanLinks(info)  # insert into plan links list
                        #print ans

    def spider(self, i):
        try:
            str_datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            item = self._db.getPlanLink()
            url = item[u'url'].encode('utf-8')
            level = int(item['level'])
            if not Common.isValidUrl(self._url, url):  # Verify whether legal link
                return False
            if url != "":
                self._db.setPlanLinksIndexEd(url)
                print "spider url:", url
                info = self.getPageInformation(url)
                info["level"] = self._level
                self._db.saveToDb(info)
                self._level = level + 1  # level number increase
                info["level"] = self._level
                self.getPageLinksFromContent(info)
                print url, str_datetime
                return True
        except Exception, ex:
            print "[error = 001,num = "+str(i)+"]", ex

    def start(self):
        dict_info = {"url": self._url, "level": self._level}
        self._db.saveToPlanLinks(dict_info)
        for i in range(0, self._maxcount):

            if self._level >= self._maxlevel:
                break

            try:
                self.spider(i)
            except Exception, ex:
                    print "[error = 002,num = " + str(i) + "]"
            finally:
                str_datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                print "spider finish", "[" + str(i) + "]", str_datetime

