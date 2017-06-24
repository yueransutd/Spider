# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 10:29:20 2017

@author: jessicasutd
"""
#Xpath & lxml

#nodeName:
    #all child nodes under the node
#/:
    #root element bookstore
#node1/node2:
    #all nodes2 under node1
#//nodeName:
    #all nodeName, regardless of position
#node1//node2:
    #all node2 under node1, regardless of position
#//@lang:
    #all attrs called lang

#Predicates
#/bookstore/book[1]:
    #The first book in bookstore
#/bookstore/book[last()]:
    #The last book in bookstore
#/nookstore/book[position()<3]:
    #The first two books in bookstore
#//title[@lang]:
    #All titles with attr lang
#//title[@lang='eng']:
    #All titles with lang attr named 'eng'
#/bookstore/book[price>35.00]:
    #All books with price element above 35
#/bookstore/book[price>35.00]/title:
    #All titles of books with price element above 35

#*:
#    Any element nodes
#@*:
#    Any attr nodes
#node():
#    Any type nodes
#|:
#    Choose more paths    
    
#/bookstore/*:
#    All child elements under bookstore
#//*:
#    All elements
#//title[@*]:
#    All titles with attrs
#//book/title | //book/price:
#    All title and price element under book    
#    
   
    
from lxml import etree
text = '''
<div>
    <ul>
         <li class="item-0"><a href="link1.html">first item</a></li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-inactive"><a href="link3.html">third item</a></li>
         <li class="item-1"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a>
     </ul>
 </div>
'''

html = etree.HTML(text)
result = etree.tostring(html)
#type(result) is ElementTree
#print(result)    
'''
<html><body><div>
    <ul>
         <li class="item-0"><a href="link1.html">first item</a></li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-inactive"><a href="link3.html">third item</a></li>
         <li class="item-1"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a>
     </li></ul>
 </div>
</body></html>
'''   
#A </li> is deleted here
#lxml correct HTML
#Also added <body>, <html>

#use parse() to read document:
#html = etree.parse('hello.html') #A document called 'hello.html'
#result = etree.tostring(html, pretty_print=True)
#print(result)
#gives out the same result

res1=html.xpath('//li')
#type(res1):
    #list
#res1:
    #[<Element li at 0x1014e0e18>, 
      #<Element li at 0x1014e0ef0>, 
      #<Element li at 0x1014e0f38>, 
      #<Element li at 0x1014e0f80>, 
      #<Element li at 0x1014e0fc8>]

res2=html.xpath('//li/@class')
#res2:
    #['item-0', 'item-1', 'item-inactive', 'item-1', 'item-0']

res3=html.xpath('//li/a[@href="link1.html"]')
#res3:
    #[<Element a at 0x10ffaae18>]

res4=html.xpath('//li/a//@class')
#res4:
    #[]
    
res5=html.xpath('//li[last()]/a/@href')
#res5:
    #['link5.html']

res6=html.xpath('//li[last()-1]/a')
#res6[0].text:
    #fourth item
#res6 is a list, res6[0] is the element in list
#.text is like .string in bs







