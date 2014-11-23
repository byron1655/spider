# -*- coding: utf-8 -*-
__author__ = 'byron'

import time
from pymongo import Connection
from common import Common

class MongoDBHelper:
    def __init__(self):
        self._db = ""
        self.connectMongoDb()
        print self._db

    def connectMongoDb(self):
        conn = Connection("*", "*")
        self._db = conn.spider
        result = self._db.authenticate("*", "*")

        if not result:
            print "MongoDB content failure!"
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

    def saveToDb(self, info):
        str_datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        url = info["url"]
        title = info["title"]
        content = info["content"]
        level = info["level"]
        content_de = content.decode("unicode_escape", 'ignore')
        md5_content = Common.getMd5Value(content)
        self._db.links.save({
            'url': url,
            'title': title,
            'content': content_de,
            'md5_content': md5_content,
            'level': level,
            'datetime': str_datetime
        })

    def saveToPlanLinks(self, info):
        url = info["url"]
        level = info["level"]
        md5_url = Common.getMd5Value(url)
        collection = self._db.plan_links.find_one({'md5_url': md5_url}, {'url': 1})

        if collection is not None:
            #print "Duplicate links"
            return ""

        str_datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        self._db.plan_links.save({
            'url': url,
            'md5_url': md5_url,
            'is_index': 0,
            'level': level,
            'get_datetime': str_datetime
        })

    def getPlanLink(self):
        one = self._db.plan_links.find_one({'is_index': 0}, {'url': 1, 'level': 1})
        return one