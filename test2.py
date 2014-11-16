# -*- coding: utf-8 -*-
__author__ = 'byron'

from common import Common
from bs4 import BeautifulSoup

site_url = "http://news.163.com/"
ex_url = "http://www.163.com/#f=topnav"
v = Common.isValidUrl(site_url, ex_url)

print v

if not v:
    print "aaa"


m = "<!DOCTYPE HTML><title>拉勾网-最专业的互联网招聘平台</title>"
soup = BeautifulSoup(m)

print soup.title

if soup.title.string is not None:
    print soup.title.string
else:
    print '22'

print soup.originalEncoding
