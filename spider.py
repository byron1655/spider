# -*- coding: utf-8 -*-
__author__ = 'byron'
import datetime
import traceback
import os
import re
import time
from spiderCore import SpiderCore

maxcount = 2000
maxlevel = 5
url = "http://www.lagou.com/"
SpiderCore = SpiderCore(url, maxcount,maxlevel)
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

