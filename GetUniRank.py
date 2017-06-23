# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 09:22:46 2017

@author: jessicasutd
"""
#get the university rank
import urllib2
from bs4 import BeautifulSoup

url='http://www.zuihaodaxue.com/zuihaodaxuepaiming2016.html'
try:
    request=urllib2.Request(url)
    response=urllib2.urlopen(request)
    content=response.read().decode('utf-8')
    soup=BeautifulSoup(content)
    
    #THU
    dic1={'rank': soup.tbody.tr.td.string,
             'name': soup.tbody.tr.div.string,
             'score': soup.tbody.tr.td.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.string,
             'province':soup.tbody.tr.td.next_sibling.next_sibling.next_sibling.next_sibling.string}
    
    
    #from No.2 onwards
    for ns in soup.tbody.tr.next_siblings:
        
        #get rank:
        rank= ns.td.string
        #get name of uni:
        name= ns.div.string
        #get score:
        prov=ns.td.next_sibling.next_sibling.next_sibling.next_sibling
        score= prov.next_sibling.string
        
        #get province:
        province= prov.string
        
        dic={'rank': rank,
             'name': name,
             'score': score,
             'province':province}
 
       
except urllib2.URLError,e:
    if hasattr(e,"code"):
        print e.code
    if hasattr(e,"reason"):
        print e.reason


'''example of one uni: (ns)
<tr class="alt"><td>305</td>
<td><div align="left">四川理工学院</div></td>
<td>四川省</td>
<td>27.2</td>
<td class="hidden-xs need-hidden indicator5">27.6</td>
<td class="hidden-xs need-hidden indicator6" style="display:none;">95.27%</td>
<td class="hidden-xs need-hidden indicator7" style="display:none;">640</td>
<td class="hidden-xs need-hidden indicator8" style="display:none;">0.623</td>
<td class="hidden-xs need-hidden indicator9" style="display:none;">6</td>
<td class="hidden-xs need-hidden indicator10" style="display:none;"></td>
<td class="hidden-xs need-hidden indicator11" style="display:none;">11604</td>
<td class="hidden-xs need-hidden indicator12" style="display:none;">3</td>
<td class="hidden-xs need-hidden indicator13" style="display:none;">3250</td>
</tr>'''