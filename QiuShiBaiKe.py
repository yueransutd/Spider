# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import urllib2
import re
page = 1
url = 'http://www.qiushibaike.com/hot/page/' + str(page)
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = { 'User-Agent' : user_agent }
serialNo=0
try:
    request = urllib2.Request(url,headers = headers)
    response = urllib2.urlopen(request)
    content=response.read().decode('utf-8')
    pattern=re.compile('<div class=.*?>.*?<span>(.*?)</span>',re.S)
    items=re.findall(pattern, content)
    for item in items:
        
        haveImg=re.search('img',item)
        if not haveImg:
            serialNo+=1
            print str(serialNo)+'. '+item
        
except urllib2.URLError,e:
    if hasattr(e,"code"):
        print e.code
    if hasattr(e,"reason"):
        print e.reason
        


















