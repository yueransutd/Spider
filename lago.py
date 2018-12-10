#-*- coding:utf-8 -*-
import requests
import time
import math
from pymongo import MongoClient
import datetime
import json
import pdb
from bs4 import BeautifulSoup
import random
from apscheduler.schedulers.blocking import BlockingScheduler

with open('mongo_config.json', encoding = 'utf-8') as f:
    data = json.load(f, encoding = 'utf-8')

host = data['host']
port = data['port']
col_name_list = list(data['jobList'].keys())

client = MongoClient(host, port)
db = client['lagou']
finish_update = dict({(col_name, False) for col_name in col_name_list})
current_date = datetime.datetime.today().strftime('%Y-%m-%d')
stop_date =  data['jobList'][col_name_list[0]]['crawlTime']

def clearDB():
    for col_name in col_name_list:
        db.drop_collection(col_name)

'''{"host": "10.0.10.147", "port": 27017, "user": "", "pwd": "", "db": "liu", "jobList": {"big_data": {"key": "大数据", "crawlTime": "2018-12-07"}, "AI": {"key": "人工智能", "crawlTime": "2018-12-07"}, "cloud": {"key": "云计算", "crawlTime": "2018-12-07"}, "JAVA": {"key": "java", "crawlTime": "2018-12-07"}, "web": {"key": "前端工程师", "crawlTime": "2018-12-07"}, "database": {"key": "数据库", "crawlTime": "2018-12-04"}, "backend": {"key": "后端开发", "crawlTime": "2018-12-04"}, "operation": {"key": "运维", "crawlTime": "2018-12-04"}, "testing": {"key": "测试", "crawlTime": "2018-12-04"}, "cybersecurity": {"key": "网络安全", "crawlTime": "2018-12-04"}, "app": {"key": "移动开发", "crawlTime": "2018-12-06"}}}'''

def getJobList(url, num, kd):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'Referer': 'https://www.lagou.com/jobs/list_%E8%BD%AF%E4%BB%B6%E5%BC%80%E5%8F%91%E5%B7%A5%E7%A8%8B%E5%B8%88?city=%E6%B7%B1%E5%9C%B3&cl=false&fromSearch=true&labelWords=sug&suginput=%E8%BD%AF%E4%BB%B6'
                }
    my_data = {  
            'first': 'true',  
            'pn':num,  
            'kd':kd }
            #'px': 'new'}
            #'gm': '2000人以上'}    
    return requestData(url, headers, my_data)
    
                
def requestData(url, headers, my_data):
    # request again if request fail
    #max_try = 10
    #for tries in range(max_try):
    while True:
        try:
            res = requests.post(url, headers = headers, data = my_data)
            result = res.json()
            c = result['content']
            return result
        except Exception:
            print ('request too frequent, trying again...')
            time.sleep(random.uniform(3, 10))
                
def updateConfig(col_name, kd):
    #update mongo_config.json
    data['jobList'][col_name]["crawlTime"] = current_date
    with open('mongo_config.json', 'w', encoding = 'utf-8') as file:
        json.dump(data, file, ensure_ascii = False)
    

def getPageNum(count):  
    # 15 positions in each page by default  
    res = math.ceil(count/15)    
    if res > 30:  
        return 30  
    else:  
        return res  
  
def getPageInfo(jobs_list, col_name, collection):  
    global finish_update
    for i in jobs_list: 
        # get update for current date
        #if i['createTime'].split()[0] != stop_date:
        job_info = {} 
        job_info['companyFullName']= i['companyFullName'] 
        job_info['companyShortName']= (i['companyShortName'])  
        job_info['companySize'] = (i['companySize'])  
        job_info['financeStage'] = (i['financeStage'])  
        job_info['district'] = (i['district'])  
        job_info['longitude'] = (i['longitude'])
        job_info['latitude'] = (i['latitude'])
        job_info['jobName'] = (i['positionName'])  
        job_info['jobLables'] = (i['positionLables'])
        job_info['workYear'] = (i['workYear'])  
        job_info['education'] = (i['education'])  
        job_info['salary'] = (i['salary'])  
        job_info['jobAdvantage'] = (i['positionAdvantage']) 
        job_info['industryField'] = (i['industryField'])
        req, add = getAdditionInfo(i['positionId'])
        job_info['requirement'] = req
        job_info['address'] = add
        job_info['createTime'] = (i['createTime'])
        job_info['crawlTime'] = current_date
        collection.insert_one(job_info) #insert each position (dic) to target collection
        #else: 
            #finish_update[col_name] = True
            #break


# get all info
def getLagouTotal(): 
    url='https://www.lagou.com/jobs/positionAjax.json?city=%E6%B7%B1%E5%9C%B3&needAddtionalResult=false'
    
    for col_name in col_name_list:
        collection = db[col_name]
        kd = data['jobList'][col_name]['key']
        page_1 = getJobList(url,1, kd) 
        total_count = page_1['content']['positionResult']['totalCount']
        num = getPageNum(total_count)  
        time.sleep(random.uniform(5,10))  
        print ('Total number of positions in {} :{}, number of pages:{}'.format(kd, total_count,num))
        for n in range(1,num+1):
            start_time = time.time()
            page = getJobList(url,n, kd)  
            jobs_list = page['content']['positionResult']['result']
            getPageInfo(jobs_list, col_name, collection)  
            elapsed_time = time.time() - start_time
            print ('Complete {} pages in {}'.format(n, time.strftime ("%H:%M:%S", time.gmtime(elapsed_time))))
            time.sleep(random.uniform(5,20)) 
        updateConfig(col_name, kd)

# get update for a specific date    
def getLagouUpdate():    
    url='https://www.lagou.com/jobs/positionAjax.json?city=%E6%B7%B1%E5%9C%B3&needAddtionalResult=false'
        
    global finish_update
    for col_name in col_name_list:
        collection = db[col_name]
        kd = data['jobList'][col_name]['key']
        page_1 = getJobList(url,1, kd) 
        total_count = page_1['content']['positionResult']['totalCount']
        num = getPageNum(total_count)  
        time.sleep(random.uniform(5,10))  
        print ('Total number of positions in {} :{}, number of pages:{}'.format(kd, total_count,num))
        for n in range(1, num+1):
            start_time = time.time()
            page = getJobList(url,n, kd)  
            jobs_list = page['content']['positionResult']['result']
            getPageInfo(jobs_list, col_name, collection)  
            elapsed_time = time.time() - start_time
            print ('Complete {} pages in {}'.format(n, time.strftime ("%H:%M:%S", time.gmtime(elapsed_time))))
            time.sleep(random.uniform(5,20)) 
            if finish_update[col_name]:
                print ('finish fetching date for '+ kd + ' until ' + current_date + ' at ' + time.asctime( time.localtime(time.time())))
                break
        updateConfig(col_name, kd) # update config file after finishing fetching each job 

def getAdditionInfo(positionId):
    global req_time
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'Referer': 'https://www.lagou.com/jobs/list_%E8%BD%AF%E4%BB%B6%E5%BC%80%E5%8F%91%E5%B7%A5%E7%A8%8B%E5%B8%88?city=%E6%B7%B1%E5%9C%B3&cl=false&fromSearch=true&labelWords=sug&suginput=%E8%BD%AF%E4%BB%B6'
                }
    url = 'https://www.lagou.com/jobs/{}.html'.format(str(positionId))
    addr = None
    while not addr:
        response = requests.get(url, headers = headers).text
        soup=BeautifulSoup(response, 'lxml')
        #print(soup)
        requirement = soup.find('dd', class_ = 'job_bt')
        #requirement =  re.findall(re.compile('.*?<div>(.*?)</div>.*?'), requirement)
        addr = soup.find('input', {'name' : 'positionAddress'})
        time.sleep(random.uniform(1,3))
        #print(addr)
        if addr:
            break
    return str(requirement.find('div')), str(addr['value'])

def main():
    getLagouTotal()

def schedulerCrawl():
    main()
    scheduler = BlockingScheduler()  # 计划性任务，定时任务
    scheduler.add_job(main, 'cron', hour = 00,minute = 00,second = 00, replace_existing=True)
    try:
        scheduler.start()  # 采用的是阻塞的方式，只有一个线程专职做调度的任务
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print('Exit The Job!')

if __name__ == '__main__':
    schedulerCrawl()


