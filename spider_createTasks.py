import pandas as pd

import db_redis
import db_oracle_opt
from config_db import *
from config_spider import *

class CreateTasks(object):
    def __init__(self):
        self.db_orcl = db_oracle_opt.OracleEngine()
        self.db_redis = db_redis.RedisQueue()

    def createSearchTasks(self):
        self.db_redis.delete(REDIS_KEY_TASKS)

        df_ent = self.db_orcl.select_table(ORACLE_TABLE_ENTOUTED, '')
        list_g = list(df_ent['ENTNAME_GLLZD'])
        list_e = list(df_ent['ENAME'])
        list_b= list(df_ent['NAME_BEFORE'])
        list_enterprise = list(set(list_g + list_e + list_b))

        print(len(list_enterprise), '企业数')
        df_words = self.db_orcl.select_table(ORACLE_TABLE_KEYWORDS, '')
        list_words = list(df_words['WORD'])

        print(len(DICTDOMAIN), '域名数')
        # for domain in DICTDOMAIN:
        #     for ename in list_enterprise:
        #         for word in list_words:
        #             if ename.strip():
        #                 task = ename.strip() + ' ' + word.strip() + SPLIT_SYMBOL + domain + SPLIT_SYMBOL + DICTDOMAIN[domain]
        #                 self.db_redis.tasks_add(REDIS_KEY_TASKS, task)
        # for ename in list_enterprise:
        #     for word in list_words:
        #         if ename.strip():
        #             task = ename.strip() + ' ' + word.strip() + SPLIT_SYMBOL + ' ' + SPLIT_SYMBOL + ' '
        #             self.db_redis.tasks_add(REDIS_KEY_TASKS, task)

        for domain in DICTDOMAIN:
            for ename in list_enterprise:
                if ename.strip():
                    task = ename.strip() + SPLIT_SYMBOL + domain + SPLIT_SYMBOL + DICTDOMAIN[domain]
                    self.db_redis.tasks_add(REDIS_KEY_TASKS, task)


    def createTestTasks(self):
        self.db_redis.delete(REDIS_KEY_TASKS)
        self.db_redis.tasks_add(REDIS_KEY_TASKS, '北京眼神科技有限公司 雄安@@@@sina.com.cn@@@@新浪网')
        self.db_redis.tasks_add(REDIS_KEY_TASKS, '北京眼神科技有限公司 雄安@@@@sohu.com@@@@搜狐网')
        self.db_redis.tasks_add(REDIS_KEY_TASKS, '北京眼神科技有限公司 雄安@@@@ifeng.com@@@@凤凰网')
        self.db_redis.tasks_add(REDIS_KEY_TASKS, '北京眼神科技有限公司 雄安@@@@qq.com@@@@腾讯网')
        # self.db_redis.tasks_add(REDIS_KEY_TASKS, '北京眼神科技有限公司 雄安@@@@sina.com.cn@@@@新浪网')
        # self.db_redis.tasks_add(REDIS_KEY_TASKS, '北京眼神科技有限公司 雄安@@@@sina.com.cn@@@@新浪网')
        # self.db_redis.tasks_add(REDIS_KEY_TASKS, '北京眼神科技有限公司 雄安@@@@sina.com.cn@@@@新浪网')
        # self.db_redis.tasks_add(REDIS_KEY_TASKS, '北京眼神科技有限公司 雄安@@@@sina.com.cn@@@@新浪网')
        # self.db_redis.tasks_add(REDIS_KEY_TASKS, '北京眼神科技有限公司 雄安@@@@sina.com.cn@@@@新浪网')
        # self.db_redis.tasks_add(REDIS_KEY_TASKS, '北京眼神科技有限公司 雄安@@@@sina.com.cn@@@@新浪网')
        # self.db_redis.tasks_add(REDIS_KEY_TASKS, '北京眼神科技有限公司 雄安@@@@sina.com.cn@@@@新浪网')
        # self.db_redis.tasks_add(REDIS_KEY_TASKS, '北京眼神科技有限公司 雄安@@@@sina.com.cn@@@@新浪网')

    def insertDomain(self):
        #print(DICTDOMAIN_2)
        df = pd.DataFrame(pd.Series(DICTDOMAIN_2), columns = {'domain_name'})
        df = df.reset_index().rename(columns = {'index':'domain'})
        self.db_orcl.insert_DataFrame('yuqing_domain', df)






if __name__ == '__main__':
    c = CreateTasks()
    c.createSearchTasks()
    #c.createTestTasks()

    #c.insertDomain()