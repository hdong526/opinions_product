import sys
sys.path.append("..")
import getopt
import warnings
import datetime

import spider_createTasks
from config_db import *
import spider_keyWebsite_stock.spider_keyWebsite_thread as spider_keyWebsite_thread


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

    main_threads(bool_add)


    end = datetime.datetime.now()
    print('结束时间{}'.format(end))
    print('耗时{}'.format(str(end - start)))

if __name__ == '__main__':
    main_spider()