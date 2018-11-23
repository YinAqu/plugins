# -*- coding: utf-8 -*-

import json
import urllib.parse
import urllib.request
import os

from albertv0 import *


__iid__ = "PythonInterface/v0.1"
__prettyname__ = "Google英翻中"
__version__ = "1.0"
__trigger__ = "ez "
__author__ = "Yinaqu"
__dependencies__ = []

lineLen = 52 
ua = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
urltmpl = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=zh_CN&dt=t&q=%s"

godenIconPath = iconLookup('goldendict')
gnomeIconPath = iconLookup('gnome-dictionary')

def handleQuery(query):
    if query.isTriggered:
        txt = query.string.strip()
        if txt.endswith('$'):
            items = []
            url = urltmpl % (urllib.parse.quote_plus(txt[0:-1]))
            req = urllib.request.Request(url, headers={'User-Agent': ua})
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode('utf-8'))
                index = 0
                for result in data[0]:
                    iconPath = gnomeIconPath
                    if index % 2 == 0:
                        iconPath = godenIconPath
                    index += 1
                    dest = result[0]
                    src = result[1]
                    length = len(dest) 
                    offset = 0
                    while offset < length:
                        subDest = dest[offset:length]
                        lineTxt = subOneline(subDest)
                        offset += len(lineTxt)
                        items.append(getItem(lineTxt, src, iconPath))
            # item.addAction(ClipAction("Copy translation to clipboard", result))
            return items

        else:
            return getItem(query.string, "按`翻译", gnomeIconPath) 

    
def getItem(text, subtext, iconPath):
    item = Item(id=__prettyname__, icon=iconPath)
    item.text = text
    item.subtext = subtext
    return item 

def isASCChar(ch):
    asc = ord(ch)
    if asc <= 177:
        return True
    return False

def subOneline(txt):
    index = 0
    normalizeLen = 0
    lineTxt = ''
    txtLen = len(txt)
    while(normalizeLen <= lineLen and index < txtLen):
        ch = txt[index]
        if isASCChar(ch):
            normalizeLen += 1
        else:
            normalizeLen += 2
        index += 1
        lineTxt += ch
    return lineTxt
