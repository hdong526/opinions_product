import sys
sys.path.append("..")
from threading import Thread

import db_redis
import db_oracle_opt
from config_db import *
import spider_keyWebsite_stock.spider_keyWebsite_download as spider_keyWebsite_download


class ThreadSpider(Thread):
    def __init__(self, b_spider_add):
        Thread.__init__(self)
        self.daemon = False
        self.b_add = b_spider_add
        self.dbRedis_duplicate = db_redis.RedisQueue(redisDB=REDIS_DB) #去重库
        self.dbRedis = db_redis.RedisQueue(redisDB=REDIS_KEYWEBSITE)   #重点网站任务库
        self.download = spider_keyWebsite_download.Download(self.dbRedis, self.dbRedis_duplicate, b_spider_add)

    def run(self):
        while True:
            try:
                bool_task1 = self.dbRedis.tasks_empty(REDIS_KEY_TASKS_KEYWEBSITE)
                bool_task2 = self.dbRedis.tasks_empty(REDIS_KEY_KEYWEBSITE_OTHERLISTPAGE)
                if not bool_task1:
                    task = self.dbRedis.tasks_pop(REDIS_KEY_TASKS_KEYWEBSITE)
                    if task:
                        self.download.download(task, 'first')
                        #print(task, 11111)
                elif not bool_task2:
                    task = self.dbRedis.tasks_pop(REDIS_KEY_KEYWEBSITE_OTHERLISTPAGE)
                    if task:
                        self.download.download(task, 'other')
                else:
                    break
                # pass
                # bool_taskType3 = self.dbRedis.tasks_empty(REDIS_KEY_DETAIL)
                # if self.b_spider_detail:
                #     bool_taskType1 = True
                #     bool_taskType2 = True
                #     if bool_taskType3:
                #         time.sleep(600)
                #         continue
                # else:
                #     bool_taskType1 = self.dbRedis.tasks_empty(REDIS_KEY_TASKS)
                #     bool_taskType2 = self.dbRedis.tasks_empty(REDIS_KEY_BAIDU_OTHER)
                #
                # if not bool_taskType1:
                #     task = self.dbRedis.tasks_pop(REDIS_KEY_TASKS)
                #     self.download.downloadtask(task, 'baidu_firstPage')
                # elif not bool_taskType2:
                #     baiduOtherUrlTask = self.dbRedis.tasks_pop(REDIS_KEY_BAIDU_OTHER)
                #     self.download.downloadtask(baiduOtherUrlTask, 'baidu_otherpage')
                # elif not bool_taskType3:
                #     newsTask = self.dbRedis.tasks_pop(REDIS_KEY_DETAIL)
                #     self.download.downloadtask(newsTask, 'detail_content')
                # else:
                #     break
            except:
                pass
