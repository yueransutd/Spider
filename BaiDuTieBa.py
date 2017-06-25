# -*- coding: utf-8 -*-
"""
Created on Sat Jun 24 14:33:12 2017

@author: jessicasutd
"""

import urllib
import urllib2
from lxml import etree
import re


#To get rid of line break symbols and img tags       
class Tool(object):
    #remove img tag
    removeImg=re.compile('<img.*?>')
    #remove a tag
    removeAddr=re.compile('<a.*?>|</a>')
    #replace line break with \n
    replaceLine=re.compile('<tr>|<div>|</div>|</p>')
    replaceBr=re.compile('<br><br>|<br>')
    
    def replace(self,x):
        x=re.sub(self.removeImg,'',x)
        x=re.sub(self.removeAddr,'',x)
        x=re.sub(self.replaceLine,'\n',x)
        x=re.sub(self.replaceBr,'\n',x)
        
        return x.strip()
    
    
    
class BDTB(Tool):
    
    def __init__(self,baseUrl,seeLz):
        Tool.__init__(self)
        self.baseUrl=baseUrl
        self.seeLz='?see_lz='+str(seeLz)
        #seeLz= 1 if only see Lz
        #       0 if not
        
    def getPage(self, pageNum):
        try:
            url=self.baseUrl+self.seeLz+'&pn='+str(pageNum)
            request=urllib2.Request(url)
            response=urllib2.urlopen(request)
            #print response.read()
            return response.read().decode('utf-8')
        
        except urllib2.URLError,e:
            if hasattr(e,'reason'):
                print 'Request fail', e.reason
                return None

#baseURL='http://tieba.baidu.com/p/3138733512'
#bdtb = BDTB(baseURL,1)
#print bdtb.getPage(1)

    def getTitle(self):
        page=self.getPage(1)
        html = etree.HTML(page)
        res1=html.xpath('//div/h3')
        return res1[0].text
        #纯原创我心中的NBA2014-2015赛季现役50大
    
    #get total number of pages    
    def getPageNum(self):
        page=self.getPage(1)
        html = etree.HTML(page)
        res2=html.xpath('//div[@class="pb_footer"]//div/ul/li/span')
        return res2[2].text
        #5
        
    def getContent(self,page):
        pattern=re.compile('<div id="post_content_.*?>(.*?)</div>',re.S)
        content=self.getPage(page)
        items=re.findall(pattern,content)
        #for item in items:
            #print item
        floor=1
        for item in items:
            print str(floor)+u"楼-----------------------------------------------------------------------"
            print Tool().replace(item)
            floor+=1
        
    
    
    
    
    
baseURL='http://tieba.baidu.com/p/3138733512'
seeLz=raw_input('Only see Lz? Type 1 for yes, 0 for no.')
bdtb = BDTB(baseURL,seeLz)
#bdtb.getPage(1)
print bdtb.getContent(1)            





#Notes:
#1. http://tieba.baidu.com/p/3138733512?see_lz=1&pn=1:
#    baseUrl: http://tieba.baidu.com/p/3138733512
#    param: ?see_lz=1&pn=1 (see lz and page No.)
   


     