import datetime

import requests

import multiprocessing
from multiprocessing import Pool

from spider_thread import ThreadSpider

from config_db import *
from db_redis import RedisQueue


def download(url):
    response = requests.get(url)
    print(url)
    if response.status_code == 200:
        print('xx')

def download2(url, url2):
    response = requests.get(url)
    print(url2)
    if response.status_code == 200:
        print('xx')

def download_process():
    rdb = RedisQueue('127.0.0.1', 6379, 10)
    while True:
        url = rdb.tasks_pop('test2')
        download(url)
        if rdb.tasks_empty('test2'):
            break

def main():
    rdb = RedisQueue('127.0.0.1', 6379, 10)
    list_thread_1 = [ThreadSpider(rdb) for i in range(8)]
    # for c in list_thread_1:
    #     c.start()
    # for c in list_thread_1:
    #     c.join()
    [thread.start() for thread in list_thread_1]
    [thread.join() for thread in list_thread_1]

def main_multiprocesses():

    pool = Pool(processes=8)
    url = "https://www.cnblogs.com/lilyxiaoyy/p/11037401.html"
    for _ in range(100):
        pool.apply_async(download, (url,))

    pool.close()
    pool.join()

def main_multiprocesses_gevent():
    pass
    # processes = []
    # for index in range(4):
    #     processes.append(multiprocessing.Process(target=main_xx))
    #
    # for index in range(4):
    # 	processes[index].start()
    #
    # for index in range(4):
    # 	processes[index].join()

def main_xx():
    pass
    # urll = "https://www.cnblogs.com/lilyxiaoyy/p/11037401.html"
    # rdb = RedisQueue('127.0.0.1', 6379, 10)
    # tasks = []
    # while True:
    #     if not rdb.tasks_empty('test2'):
    #         tasks.append(rdb.tasks_pop('test2'))
    #
    #
    #     pool = gevent.pool.Pool(20)
    #     threads = []
    #     for j in range(25):
    #         threads.append(pool.spawn(download2, urll, urll))
    #     gevent.joinall(threads)

if __name__ == '__main__':
    start = datetime.datetime.now()
    print('开始时间{}'.format(start))
    db = RedisQueue('127.0.0.1', 6379, 10)
    db.delete(REDIS_KEY_TASKS)
    for _ in range(1000):
        db.tasks_add('test2', "https://www.cnblogs.com/lilyxiaoyy/p/11037401.html")

    processes = []
    for index in range(4):
        processes.append(multiprocessing.Process(target=main))
    # for index in range(4):
    #     processes[index].start()
    # for index in range(4):
    #     processes[index].join()

    [process.start() for process in processes]
    [process.join() for process in processes]



    #main_multiprocesses()
    #main_multiprocesses_gevent()

    # list_thread_1 = [ThreadSpider(db) for i in range(8)]
    # for c in list_thread_1:
    #     c.start()
    #
    # for c in list_thread_1:
    #     c.join()

    end = datetime.datetime.now()
    print('结束时间{}'.format(end))
    print('耗时{}'.format(str(end - start)))

    #download("https://www.cnblogs.com/lilyxiaoyy/p/11037401.html")


