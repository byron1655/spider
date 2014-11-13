# -*- coding: utf-8 -*-
__author__ = 'byron'
import hashlib
import re

class Common:

    @staticmethod
    def getMd5Value(self, src):
        src = str(src)
        myMd5 = hashlib.md5()
        myMd5.update(src)
        myMd5_Digest = myMd5.hexdigest()
        return myMd5_Digest

    @staticmethod
    def isValidUrl(self, url):
        pat = re.compile(r'^https?:/{2}\w.*?[;#?]')
        match = pat.search(str(url))
        print "url = " + str(url)
        if match:
            href = match.group(1)
            return href
        else:
            return ""