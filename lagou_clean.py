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
import os
from apscheduler.schedulers.blocking import BlockingScheduler


class cfgOperation:

    def __init__(self):
        return None
    def get(self):
        with open('mongo_config.json', encoding = 'utf-8') as f:
            data = json.load(f, encoding = 'utf-8')
            return data
    def save(self, data, col_name, current_date):
        data['jobList'][col_name]["crawlTime"] = current_date
        with open('mongo_config.json', 'w', encoding = 'utf-8') as file:
            json.dump(data, file, ensure_ascii = False)
    
class mongoOperation:

    def __init__(self):
        return None
    def conn(self, host, port, dbName):
        client = MongoClient(host, port)
        db = client[dbName]
        return db
    def close(self, host, port):
        client = MongoClient(host, port)
        client.close()
    def dropCollections(self, db, collections):  # 清理集合内容
        db[collections].drop()
    

class crawlWork:
    def __init__(self):
        self.request_url = ''
        self.request_key = ''
        self.cfgOperation = cfgOperation()
        self.cfg = self.cfgOperation.get()
        self.mongoOperation = mongoOperation()
        self.db = self.mongoOperation.conn(self.cfg['host'],self.cfg['port'],self.cfg['db'])

    def getJobList(self, url, num, kd):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'Referer': 'https://www.lagou.com/jobs/list_%E8%BD%AF%E4%BB%B6%E5%BC%80%E5%8F%91%E5%B7%A5%E7%A8%8B%E5%B8%88?city=%E6%B7%B1%E5%9C%B3&cl=false&fromSearch=true&labelWords=sug&suginput=%E8%BD%AF%E4%BB%B6'
            }
        self.my_data = {  
            'first': 'true',  
            'pn':num,  
            'kd':kd }
        return self.requestData(url, self.headers, self.my_data)

    def requestData(self, url, headers, my_data):  
        # 请求页面
        while True:
            try:
                res = requests.post(url, headers = headers, data = my_data)
                result = res.json()
                c = result['content']
                return result
            except Exception:
                print ('request too frequent, trying again...')
                time.sleep(random.uniform(3, 10))

    def getPageNum(self, count):  
        # 每页十五个职位招聘信息
        res = math.ceil(count/15)    
        if res > 30:  
            return 30  
        else:  
            return res  
    
    def getPageInfo(self, jobs_list, col_name, collection):  
        # 采集每页职位信息
        for i in jobs_list: 
            job_info = {} 
            job_info['companyFullName']= i['companyFullName']     # 公司全称
            job_info['companyShortName']= (i['companyShortName']) # 公司简称
            job_info['companySize'] = (i['companySize'])          # 公司规模（人数）
            job_info['financeStage'] = (i['financeStage'])        # 公司所在融资阶段
            job_info['district'] = (i['district'])                # 公司地址（区）
            job_info['longitude'] = (i['longitude'])              # 公司地址的经度
            job_info['latitude'] = (i['latitude'])                # 公司地址的纬度
            job_info['jobName'] = (i['positionName'])             # 职位名称
            job_info['jobLables'] = (i['positionLables'])         # 职位所在领域
            job_info['workYear'] = (i['workYear'])                # 工作经验
            job_info['education'] = (i['education'])              # 教育背景
            job_info['salary'] = (i['salary'])                    # 薪资水平
            job_info['jobAdvantage'] = (i['positionAdvantage'])   # 职位优势
            job_info['industryField'] = (i['industryField'])      # 公司所在行业
            req, add = self.getAdditionInfo(i['positionId'])      
            job_info['requirement'] = req                         # 岗位职责与要求
            job_info['address'] = add                             # 公司地址
            job_info['createTime'] = (i['createTime'])            # 信息爬取时间
            job_info['crawlTime'] = self.getCurTime()
            collection.insert_one(job_info) 

    def getLagouTotal(self): 
        # 采集所有职位信息
        url='https://www.lagou.com/jobs/positionAjax.json?city=%E6%B7%B1%E5%9C%B3&needAddtionalResult=false'
        
        for col_name in self.getColNameList(): 
            collection = self.db[col_name] # 每个职位建立一个collection
            kd = self.cfg['jobList'][col_name]['key']
            page_1 = self.getJobList(url,1, kd) 
            total_count = page_1['content']['positionResult']['totalCount']
            num = self.getPageNum(total_count)  
            time.sleep(random.uniform(5,10))  
            print ('Total number of positions in {} :{}, number of pages:{}'.format(kd, total_count,num))
            for n in range(1,num+1): # 对每一页
                start_time = time.time()
                page = self.getJobList(url,n, kd)  
                jobs_list = page['content']['positionResult']['result']
                self.getPageInfo(jobs_list, col_name, collection)  
                time.sleep(random.uniform(5,20)) 
                elapsed_time = time.time() - start_time
                print ('Complete {} pages in {}'.format(n, time.strftime ("%H:%M:%S", time.gmtime(elapsed_time))))
            self.cfgOperation.save(self.cfg, col_name, self.getCurTime())

    def getAdditionInfo(self, positionId):
        # 单独请求每个职位的额外信息
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'Referer': 'https://www.lagou.com/jobs/list_%E8%BD%AF%E4%BB%B6%E5%BC%80%E5%8F%91%E5%B7%A5%E7%A8%8B%E5%B8%88?city=%E6%B7%B1%E5%9C%B3&cl=false&fromSearch=true&labelWords=sug&suginput=%E8%BD%AF%E4%BB%B6'
                    }
        url = 'https://www.lagou.com/jobs/{}.html'.format(str(positionId))
        addr = None
        while not addr:
            response = requests.get(url, headers = headers).text
            soup=BeautifulSoup(response, 'lxml')
            requirement = soup.find('dd', class_ = 'job_bt')
            addr = soup.find('input', {'name' : 'positionAddress'})
            time.sleep(random.uniform(1,3))
            if addr:
                break
        return str(requirement.find('div')), str(addr['value']) # 返回岗位职责与要求，地址
            
    def getColNameList(self):
        return list(self.cfg['jobList'].keys())
    def getCurTime(self):
        return datetime.datetime.today().strftime('%Y-%m-%d')

def main():
    tt = crawlWork()
    tt.getLagouTotal()

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
    