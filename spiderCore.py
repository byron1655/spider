# -*- coding: utf-8 -*-
__author__ = 'byron'

import hashlib
import datetime
import traceback
import socket
import re
from pymongo import Connection
from bs4 import BeautifulSoup
import urllib2
from urllib2 import Request, urlopen, URLError, HTTPError
import time
from common import Common

class SpiderCore:
    def __init__(self, url,maxcount):
        self._url = url
        self.connectMongoDb()
        self._db = ""
        self._i = 0
        self._maxcount = maxcount

    def connectMongoDb(self):
        conn = Connection("*.*.*.*", 27017)
        self._db = conn.spider
        self._db.authenticate("***", "***")

    def setPlanLinksIndex(self, url):
        md5_url = Common.getMd5Value(url)
        self._db.plan_links.update(
            {"md5_url": md5_url},
            {"$set": {"is_index": 1}}
        )

    def getPageContent(self, url):
        result = ""
        try:
            req = urllib2.Request(url)
            con = urllib2.urlopen(req)
            doc = con.read()
            con.close()
            return doc.decode('gbk').encode('utf8')
        except HTTPError, e:
            return result
        except URLError, e:
            return result
        else:
            return result

    def saveToContent(self, url, content):
        datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        content_de = content.decode("unicode_escape", 'ignore')
        md5_content = Common.getMd5Value(content)
        self._db.links.save({
            'url':url,
            'content': content_de,
            'md5_content': md5_content,
            'datetime': datetime
        })

    def getPageLinks(self, url, content):
        soup = BeautifulSoup(content)
        links = soup.findAll('a')

        pat = re.compile(r'href="([^"]*)"')
        pat2 = re.compile(r'http')
        for item in links:
            if str(item) != "":
                match = pat.search(str(item))
                if match:
                    href = match.group(1)
                    if pat2.search(href):
                        ans = href
                    else:
                        ans = url+href
                    print ans
                    saveToPlanLinks(ans) #insert into plan links list

    def spider(self,i):
        try:
            datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            item = self._db.plan_links.find_one({'is_index': 0}, {'url': 1})
            #url = isValidUrl(item[u'url'].encode('utf-8'))
            url = item[u'url'].encode('utf-8')
            self.setPlanLinksIndex(url)
            if url != "":
                content = self.getPageContent(url)
                self._saveToContent(url, content)
                md5_url = hashlib.new("md5", url).hexdigest()
                self._db.plan_links.update({'md5_url': md5_url} ,{"$set": {"is_index": 1}})
                self.getPageLinks(url, content)
                print url, datetime, "\n"
                return True
        except Exception, ex:
            print "[error = 001,num = "+str(i)+"]"

    def start(self):
        for i in range(0, self._maxcount):
            try:
                self.spider(i)
            except Exception, ex:
                    print "[error = 002,num = "+str(i)+"]"
            finally:
                datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                print "spider finish", "[" +str(i) + "]", datetime

