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
from pymongo import Connection
from bs4 import BeautifulSoup
import urllib2
from urllib2 import Request, urlopen, URLError, HTTPError
from common import Common

class SpiderCore:
    def __init__(self, url = "", maxcount = 10, maxlevel = 3):
        self._url = url
        self._db = ""
        self.connectMongoDb()
        self._i = 0
        self._maxcount = maxcount
        self._maxlevel = maxlevel

        self._title = 'Untitled Document'
        self._content = ''
        self._level = 0
        print self._db

    def connectMongoDb(self):
        conn = Connection("*", *)
        self._db = conn.spider
        result = self._db.authenticate("*", "*")
        return result

    def setPlanLinksIndexEd(self, url):
        md5_url = Common.getMd5Value(url)
        self._db.plan_links.update(
            {"md5_url": md5_url},
            {"$set": {"is_index": 1}}
        )

    def setPlanLinksIndexEx(self, url):
        md5_url = Common.getMd5Value(url)
        self._db.plan_links.update(
            {"md5_url": md5_url},
            {"$set": {"is_index": 2}}
        )

    def getPageInformation(self, url):
        result = ""
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
            arr_result = [title, content]

            return arr_result
        except HTTPError, e:
            return result
        except URLError, e:
            return result
        else:
            return result

    def saveToDb(self, url, info):
        str_datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        title = info[0]
        content = info[1]
        content_de = content.decode("unicode_escape", 'ignore')
        md5_content = Common.getMd5Value(content)
        self._db.links.save({
            'url': url,
            'title': title,
            'content': content_de,
            'md5_content': md5_content,
            'level': self._level,
            'datetime': str_datetime
        })

    def saveToPlanLinks(self, url):
        md5_url = Common.getMd5Value(url)
        collection = self._db.plan_links.find_one({'md5_url': md5_url}, {'_id': 1})
        if collection:
            return ""

        str_datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        self._db.plan_links.save({
            'url': url,
            'md5_url': md5_url,
            'is_index': 0,
            'level': self._level,
            'get_datetime': str_datetime
        })

    def getPageLinksFromContent(self, url, content):
        soup = BeautifulSoup(content)
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
                        ans = url+href
                    if Common.isValidUrl(self._url, ans):  # Verify whether legal link
                        self.saveToPlanLinks(ans)  # insert into plan links list
                        #print ans

    def spider(self, i):
        try:
            str_datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            item = self._db.plan_links.find_one({'is_index': 0}, {'url': 1, 'level': 1})
            url = item[u'url'].encode('utf-8')
            level = int(item['level'])
            if not Common.isValidUrl(self._url, url):  # Verify whether legal link
                return False
            self.setPlanLinksIndexEd(url)
            print "spider url:", url
            if url != "":
                info = self.getPageInformation(url)
                self.saveToDb(url, info)
                self._level = level + 1  # level number increase
                self.getPageLinksFromContent(url, info[1])
                print url, str_datetime
                return True
        except Exception, ex:
            print "[error = 001,num = "+str(i)+"]", ex

    def start(self):
        self.saveToPlanLinks(self._url)
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

