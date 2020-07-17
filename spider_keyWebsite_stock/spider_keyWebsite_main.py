import sys
sys.path.append("..")
import getopt
import warnings
import datetime
import time
import pandas as pd

import spider_createTasks
import spider_keyWebsite_stock.spider_keyWebsite_thread as spider_keyWebsite_thread

import db_redis
import db_oracle_opt
from config_db import *
from config_spider import *
import spider_keyWebsite_stock.spider_keyWebsite_download as spider_keyWebsite_download


def main_onethreads(bool_add):
    dbRedis_duplicate = db_redis.RedisQueue(redisDB=REDIS_DB)  # 去重库
    dbRedis = db_redis.RedisQueue(redisDB=REDIS_KEYWEBSITE)  # 重点网站任务库
    download = spider_keyWebsite_download.Download(dbRedis, dbRedis_duplicate, bool_add)
    while 1:
        bool_task1 = dbRedis.tasks_empty(REDIS_KEY_TASKS_KEYWEBSITE)
        bool_task2 = dbRedis.tasks_empty(REDIS_KEY_KEYWEBSITE_OTHERLISTPAGE)

        if not bool_task1:
            task = dbRedis.tasks_pop(REDIS_KEY_TASKS_KEYWEBSITE)
            if task:
                download.download(task, 'first')
                # print(task, 11111)
        elif not bool_task2:
            task = dbRedis.tasks_pop(REDIS_KEY_KEYWEBSITE_OTHERLISTPAGE)
            if task:
                download.download(task, 'other')
        else:
            break
        time.sleep(1)

def main_threads(bool_add):
    list_thread_1 = [spider_keyWebsite_thread.ThreadSpider(bool_add) for i in range(8)]
    [thread.start() for thread in list_thread_1]
    [thread.join() for thread in list_thread_1]

def main_spider():
    start = datetime.datetime.now()
    print('开始时间{}'.format(start))

    bool_add = False
    if len(sys.argv) > 1:
        try:
            opts, args = getopt.getopt(sys.argv[1:], "t:")
            for opt, arg in opts:
                if opt == '-t':
                    if arg == 'add':
                        bool_add = True
                        print('增量抓取类型爬虫')
                    else:
                        print('t命令参数错误')
                else:
                    pass
        except getopt.GetoptError:
            print('位置参数错误')

    c = spider_createTasks.CreateTasks(redisDB=REDIS_KEYWEBSITE)
    c.create_keyWebsite_Tasks()

    #main_threads(bool_add)
    main_onethreads(bool_add)


    end = datetime.datetime.now()
    print('结束时间{}'.format(end))
    print('耗时{}'.format(str(end - start)))

def func_error_content(data, dbRedis):
    url = data['URL']
    str_info = SPLIT_SYMBOL.join([url, ' ', ' ', ' ', ' ', ERROE_CONTENT])
    dbRedis.tasks_add(REDIS_KEY_DETAIL, str_info)

## 检测新浪封IP导致采集详情页错误
def opt_error_content():
    dbOracle = db_oracle_opt.OracleEngine()
    dbRedis = db_redis.RedisQueue(redisDB=REDIS_DB)
    str_sql = "select url from yuqing_ls_news_bj where domain='sina.com.cn' and instr(content, '拒绝访问')>0"
    df = dbOracle.get_DataFrame(str_sql)
    df.apply(func_error_content, axis=1, args=(dbRedis, ))
    #dbOracle.
    #str_info = SPLIT_SYMBOL.join([url, ' ', ' ', ' ', ' ', '站内搜索'])

if __name__ == '__main__':
    #main_spider()
    opt_error_content()