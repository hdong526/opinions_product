import warnings
import datetime

import multiprocessing
from multiprocessing import Pool

from spider_thread import ThreadSpider
import  spider_createTasks

def main():
    warnings.filterwarnings('ignore')
    list_thread_1 = [ThreadSpider() for i in range(4)]
    [thread.start() for thread in list_thread_1]
    [thread.join() for thread in list_thread_1]

def main_process_threads():
    processes = []
    for index in range(4):
        processes.append(multiprocessing.Process(target=main))
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

    # c = spider_createTasks.CreateTasks()
    # c.createSearchTasks()
    #main()
    main_process_threads()

    end = datetime.datetime.now()
    print('结束时间{}'.format(end))
    print('耗时{}'.format(str(end - start)))


#约1小时，去重321，总量451