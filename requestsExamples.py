# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 13:35:14 2017

@author: jessicasutd
"""


#visit requests api here: http://docs.python-requests.org/en/master/api/
import requests
#r=requests.get("http://baidu.com")
#print type(r)
#print r.status_code
#print r.encoding
#print r.cookies
#print r.text


#post something:
#payload = {'key1': '1', 'key2': 'value2'}
#r = requests.post("http://httpbin.org/post", data=payload)
#print r.text


#upload a file:
#first create a file(.txt), write anything in it
#url='http://httpbin.org/post'
#files={'file':open('test.txt','rb')}
#r=requests.post(url,files=files)
#print r.text
#with open('maybeALargeFile') as f:
    #requests.post('http://.....',data=f)

#every request is a new one
#so we use request.Session()
#s = requests.Session()
#set cookies
#s.get('http://httpbin.org/cookies/set/sessioncookie/null')
#get cookies
#r = s.get("http://httpbin.org/cookies")
#print(r.text)

#which is the same as:
#s=requests.Session()
#s.cookies.update({'sessioncookie':'null'})
#r=s.get('http://httpbin.org/cookies')
#print r.text


#s=requests.Session()
#s.headers.update({'x-test':'true'})
#r=s.get('http://httpbin.org/headers',headers={'x-test2':'false'})
#print r.text

#if no verify, or verify=True: ("bad handshake: Error([('SSL routines', 'ssl3_get_server_certificate', 'certificate verify failed')],)",)
#r = requests.get('https://kyfw.12306.cn/otn/',verify=False)
#print r.text








