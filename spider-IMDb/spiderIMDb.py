import requests
import re
import json
from requests.exceptions import RequestException


def get_one_page(url):
    try:
        response=requests.get(url)
        if response.status_code==200: #success
            return response.text
        return None
    except RequestException:
        return None
    
def parse_one_page(html):
    pattern=re.compile('<tr>.*?<a href.*?title="(.*?)" >(.*?)</a>.*?<span class.*?">\(([0-9]*)\)</span>.*?<strong title.*?">([0-9]).([0-9])</strong>',re.S)
    items=re.findall(pattern,html)
    rank=0
    for item in items:
        rank+=1
        yield{
        'rank':rank,
        'actor':item[0],
        'title':item[1],
        'year':item[2],
        'score':str(item[3])+'.'+str(item[4])
        }
        
#Save to txt file        
def write_to_file(content):
    with open('result.txt','a')as f:
        f.write(json.dumps(content)+'\n')
        f.close()
        
def main():
    url='http://www.imdb.com/chart/top'
    html=get_one_page(url)
    i=0
    for item in parse_one_page(html):
        print item
        i+=1
        write_to_file(item)
    print i
    
if __name__=='__main__':
    main()

