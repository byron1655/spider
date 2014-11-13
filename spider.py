# -*- coding: utf-8 -*-
__author__ = 'byron'
import hashlib
import datetime
import traceback
import os
import re
import time
from spiderCore import SpiderCore

maxcount = 100000
url = "http://news.163.com"
SpiderCore = SpiderCore(url, maxcount)
SpiderCore.start()

def getAutomaticId(name):
    global db
    item = db.ids.findAndModify({
            'query':{'spider': name},
            'update':{'$inc': 1}
        })

    if 'id' in item:
        return item['id']
    return None

