import sys
import time
import getopt
import warnings
import datetime

import multiprocessing
from multiprocessing import Pool

from spider_thread import ThreadSpider
import  spider_createTasks
from config_spider import *

def main(b_spider_add, bool_spider_detail):
    warnings.filterwarnings('ignore')
    list_thread_1 = [ThreadSpider(b_spider_add, bool_spider_detail, ) for i in range(NUM_THREAD)]
    [thread.start() for thread in list_thread_1]
    [thread.join() for thread in list_thread_1]

def main_process_threads(b_spider_add, bool_spider_detail):
    #print(b_spider_add)
    processes = []

    for index in range(NUM_PROCESS):
        processes.append(multiprocessing.Process(target=main, args=(b_spider_add, bool_spider_detail, )))
    # for index in range(4):
    #     processes[index].start()
    # for index in range(4):
    #     processes[index].join()

    [process.start() for process in processes]
    [process.join() for process in processes]

if __name__ == '__main__':
    warnings.filterwarnings('ignore')

    start = datetime.datetime.now()
    print('开始时间{}'.format(start))

    bool_add = False
    bool_detail = False
    if len(sys.argv) > 1:
        try:
            opts, args = getopt.getopt(sys.argv[1:], "t:u:")
            for opt, arg in opts:
                if opt == '-t':
                    if arg == 'add':
                        bool_add = True
                        print('增量抓取类型爬虫')
                    else:
                        print('t命令参数错误')
                elif opt == '-u':
                    if arg == 'detail':
                        bool_detail = True
                        print('详情页抓取')
                    else:
                        print('u命令参数错误')
                else:
                    pass
        except getopt.GetoptError:
            print('位置参数错误')

    if not bool_detail:
        c = spider_createTasks.CreateTasks()
        c.createSearchTasks()

    #main()
    main_process_threads(bool_add, bool_detail)

    end = datetime.datetime.now()
    print('结束时间{}'.format(end))
    print('耗时{}'.format(str(end - start)))


#约1小时，去重321，总量451