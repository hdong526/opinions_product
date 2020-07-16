import sys
sys.path.append("..")
import re
import chardet

import requests
from lxml import etree

import db_redis
import db_oracle_opt
import spider_createTasks
from config_db import *
import spider_keyWebsite_stock.spider_keyWebsite_parse as spider_keyWebsite_parse
from spider_keyWebsite_stock.config_keyWebsite import *


def get_sina_listurls(str_ename, dbRedistask, dbRedisduplicate):
    url = 'https://search.sina.com.cn/?q={}&range=all&c=news&sort=time'.format(str_ename)
    #url = 'https://search.sina.com.cn/?q={}&c=news&from=&col=&range=all&source=&country=&size=10&stime=&etime=&time=&dpc=0&a=&ps=0&pf=0&page=22'.format(str_ename)
    resp = requests.get(url, headers=KEYWEBSITE_HEADER['sina.com.cn'])
    cs = chardet.detect(resp.content)
    resp.encoding = cs['encoding']
    parse = spider_keyWebsite_parse.ParseKeyWebsite()
    parse.parse_listpage(resp.text, 'sina.com.cn', dbRedistask, dbRedisduplicate, str_ename, True)

if __name__ == '__main__':
    c = spider_createTasks.CreateTasks(redisDB=REDIS_KEYWEBSITE)
    c.create_keyWebsite_Tasks()
    dbRedis_task = db_redis.RedisQueue(redisDB=REDIS_KEYWEBSITE)
    dbRedis_duplicate = db_redis.RedisQueue(redisDB=REDIS_DB)
    ename = '国家开发银行'
    get_sina_listurls(ename, dbRedis_task, dbRedis_duplicate)