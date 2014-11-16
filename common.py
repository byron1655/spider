# -*- coding: utf-8 -*-
__author__ = 'byron'
import hashlib
import re

class Common:

    @staticmethod
    def getMd5Value(src):
        src = str(src)
        myMd5 = hashlib.md5()
        myMd5.update(src)
        myMd5_Digest = myMd5.hexdigest()
        return myMd5_Digest

    @staticmethod
    def isValidUrl2(url):
        pat = re.compile(r'^https?:/{2}\w.*?[;#?]')
        match = pat.search(str(url))
        if match:
            href = match.group(1)
            return href
        else:
            return url

    @staticmethod
    def isExternalUrl(site_url, ex_url):
        pat = re.compile(r'^http.*(//|\\).*?\/|\\')
        match = pat.search(str(ex_url))
        if match:
            href = match.group()
            if site_url == href:
                return True
            else:
                return False
        else:
            return False

    @staticmethod
    def isValidUrl(site_url, ex_url):
        return Common.isExternalUrl(site_url, ex_url)