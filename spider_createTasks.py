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
        list_enterprise = list(df_ent['ENTNAME_GLLZD'])
        df_words = self.db_orcl.select_table(ORACLE_TABLE_KEYWORDS, '')
        list_words = list(df_words['WORD'])

        for domain in DICTDOMAIN:
            for ename in list_enterprise:
                for word in list_words[0:5]:
                    task = ename.strip() + ' ' + word.strip() + SPLIT_SYMBOL + domain + SPLIT_SYMBOL + DICTDOMAIN[domain]
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

if __name__ == '__main__':
    c = CreateTasks()
    c.createSearchTasks()
    #c.createTestTasks()