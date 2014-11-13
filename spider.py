import hashlib
import time
import datetime
import traceback
import socket
import urllib2
import os
from bs4 import BeautifulSoup
from pymongo import Connection
from urllib2 import Request, urlopen, URLError, HTTPError
import re
import time

db = ""
maxcount = 100000
url = "http://news.163.com"


def getMd5Value(src):
    src = str(src)
    myMd5 = hashlib.md5()
    myMd5.update(src)
    myMd5_Digest = myMd5.hexdigest()
    return myMd5_Digest

def getAutomaticId(name):
    global db
    item = db.ids.findAndModify({
            'query':{'spider': name},
            'update':{'$inc': 1}
        })

    if 'id' in item:
        return item['id']
    return None

def connectMongoDb():
    global db
    conn = Connection("*.*.*.*",27017)
    db = conn.spider
    db.authenticate("***","***")

def saveToContent(url,content):
    global db
    datetime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    content_de = content.decode("unicode_escape",'ignore')
    md5_content = getMd5Value(content)
    db.links.save({
        'url':url,
        'content':content_de,
        'md5_content':md5_content,
        'datetime':datetime
    })

def saveToPlanLinks(url):
    global db
    datetime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    md5_url = getMd5Value(url)
    db.plan_links.save({
        'url':url,
        'md5_url':md5_url,
        'is_index':0,
        'get_datetime':datetime
    })

def setPlanLinksIndex(url):
    global db
    md5_url = getMd5Value(url)
    db.plan_links.update(
        {"md5_url":md5_url},
        {"$set":{"is_index":1}}
    )

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

def getPageLinks(url,content):
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


def isValidUrl(url):
    pat = re.compile(r'^https?:/{2}\w.*?[;#]')
    match = pat.search(str(url))
    print "url = " + str(url)
    if match:
        href = match.group(1)
        return href
    else:
        return ""

i = 0
def spider(i):
    global db
    try:
        datetime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        item = db.plan_links.find_one({'is_index':0},{'url':1})
        #url = isValidUrl(item[u'url'].encode('utf-8'))
        url = item[u'url'].encode('utf-8')
        setPlanLinksIndex(url)
        if url != "":
            content = getPageContent(url)
            saveToContent(url,content)
            md5_url = hashlib.new("md5",url).hexdigest()
            db.plan_links.update({'md5_url':md5_url},{"$set":{"is_index":1}})
            getPageLinks(url,content)
            print url,datetime,"\n"
    except Exception,ex:
        print "[error = 001,num = "+str(i)+"]"


connectMongoDb()

saveToPlanLinks(url)

for i in range(0,maxcount):
    try:
        spider(i)
    except Exception,ex:
            print "[error = 002,num = "+str(i)+"]"
    finally:
        datetime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        print "spider finish","[" +str(i) + "]",datetime

