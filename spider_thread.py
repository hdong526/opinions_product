import requests
from threading import Thread

import spider_download
from config_db import *
import db_redis
import db_oracle_opt

class ThreadSpider(Thread):
    def __init__(self,):
        Thread.__init__(self)
        self.daemon = False
        self.dbRedis = db_redis.RedisQueue()
        self.dbOracle = db_oracle_opt.OracleEngine()
        self.download = spider_download.Download(self.dbRedis, self.dbOracle)

    def run(self):
        while True:
            try:
                # bool_taskType1 = True
                # bool_taskType2 = True
                bool_taskType1 = self.dbRedis.tasks_empty(REDIS_KEY_TASKS)
                bool_taskType2 = self.dbRedis.tasks_empty(REDIS_KEY_BAIDU_OTHER)
                bool_taskType3 = self.dbRedis.tasks_empty(REDIS_KEY_DETAIL)
                if not bool_taskType1:
                    task = self.dbRedis.tasks_pop(REDIS_KEY_TASKS)
                    self.download.downloadtask(task, 'baidu_firstPage')
                elif not bool_taskType2:
                    baiduOtherUrlTask = self.dbRedis.tasks_pop(REDIS_KEY_BAIDU_OTHER)
                    self.download.downloadtask(baiduOtherUrlTask, 'baidu_otherpage')
                elif not bool_taskType3:
                    newsTask = self.dbRedis.tasks_pop(REDIS_KEY_DETAIL)
                    self.download.downloadtask(newsTask, 'detail_content')
                else:
                    break
            except:
                pass


    # def download(self, url):
    #     response = requests.get(url)
    #     if response.status_code == 200:
    #         print('xx')

