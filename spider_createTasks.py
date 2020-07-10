import pandas as pd

import db_redis
import db_oracle_opt
from config_db import *
from config_spider import *

class CreateTasks(object):
    def __init__(self,redisHost=REDIS_HOST, redisPort=REDIS_PORT, redisDB=REDIS_DB):
        self.db_orcl = db_oracle_opt.OracleEngine()
        self.db_redis = db_redis.RedisQueue(redisHost, redisPort, redisDB)

    def create_keyWebsite_Tasks(self):
        self.db_redis.delete(REDIS_KEY_TASKS_KEYWEBSITE)
        df_ent = self.db_orcl.select_table(ORACLE_TABLE_ENTOUTED, '')
        # list_g = list(df_ent['ENTNAME_GLLZD'])
        # list_e = list(df_ent['ENAME'])
        # list_b= list(df_ent['NAME_BEFORE'])
        # list_enterprise = list(set(list_g + list_e + list_b))
        list_e = list(df_ent['ENAME'])
        list_ent = list(df_ent['ENTNAME'])
        list_g = list(df_ent['ENTNAME_GLLZD'])
        list_b = list(df_ent['NAME_BEFORE'])
        list_enterprise = list(set(list_g + list_e + list_b + list_ent))#[50:]
        # print(list_enterprise)
        print(len(list_enterprise), '企业数')

        str_sql = 'select domain,domain_name from yuqing_domain where c0003=1'
        df_domain = self.db_orcl.get_DataFrame(str_sql)
        dictdomain = df_domain.set_index('DOMAIN')['DOMAIN_NAME'].to_dict()
        print(dictdomain)

        for domain in dictdomain:
            for ename in list_enterprise:
                if ename.strip():
                    task = ename.strip() + SPLIT_SYMBOL + domain + SPLIT_SYMBOL + dictdomain[domain]
                    self.db_redis.tasks_add(REDIS_KEY_TASKS, task)



    def createSearchTasks(self):
        self.db_redis.delete(REDIS_KEY_TASKS)

        df_ent = self.db_orcl.select_table(ORACLE_TABLE_ENTOUTED, '')
        # list_g = list(df_ent['ENTNAME_GLLZD'])
        # list_e = list(df_ent['ENAME'])
        # list_b= list(df_ent['NAME_BEFORE'])
        # list_enterprise = list(set(list_g + list_e + list_b))
        list_e = list(df_ent['ENAME'])
        list_ent = list(df_ent['ENTNAME'])
        list_g = list(df_ent['ENTNAME_GLLZD'])
        list_b = list(df_ent['NAME_BEFORE'])
        list_enterprise = list(set(list_g + list_e + list_b + list_ent))#[50:]
        #print(list_enterprise)
        print(len(list_enterprise), '企业数')

        df_words = self.db_orcl.select_table(ORACLE_TABLE_KEYWORDS, '')
        list_words = list(df_words['WORD'])

        ## 测试
        # list_enterprise = ['北京眼神科技有限公司']
        # list_words = ['雄安']
#         str_sql = '''select t1.domain,domain_name from (select * from (select domain,count(domain) t from yuqing_ls_news where domain != ' ' group by domain order by t desc) where rownum < 31 ) t1
# left join yuqing_domain t2 on t1.domain = t2.domain'''
        str_sql = 'select domain,domain_name from yuqing_domain where flag=1 or c0001=1'
        df_domain = self.db_orcl.get_DataFrame(str_sql)
        dictdomain = df_domain.set_index('DOMAIN')['DOMAIN_NAME'].to_dict()
        #print(dictdomain)
        #############################################


        #print(len(DICTDOMAIN), '域名数')
        #
        # df_domain = self.db_orcl.select_table('yuqing_domain', 'flag=1')[['DOMAIN', 'DOMAIN_NAME']]
        # dictdomain = df_domain.set_index('DOMAIN')['DOMAIN_NAME'].to_dict()
        df_domain_2 = self.db_orcl.select_table('yuqing_domain', 'c0002=1')[['DOMAIN', 'DOMAIN_NAME']]
        dictdomain_2 = df_domain_2.set_index('DOMAIN')['DOMAIN_NAME'].to_dict()
        #
        #
        print('dictdomain', len(dictdomain))
        print('list_enterprise', len(list_enterprise))
        print('word', len(list_words))
        print('dictdomain_2', len(dictdomain_2))

        for domain in dictdomain:
            for ename in list_enterprise:
                for word in list_words:
                    if ename.strip():
                        task = ename.strip() + ' ' + word.strip() + SPLIT_SYMBOL + domain + SPLIT_SYMBOL + dictdomain[domain]
                        self.db_redis.tasks_add(REDIS_KEY_TASKS, task)

        for ename in list_enterprise:
            for word in list_words:
                if ename.strip():
                    task = ename.strip() + ' ' + word.strip() + SPLIT_SYMBOL + ' ' + SPLIT_SYMBOL + ' '
                    self.db_redis.tasks_add(REDIS_KEY_TASKS, task)

        for domain in dictdomain_2:
            for ename in list_enterprise:
                if ename.strip():
                    task = ename.strip() + SPLIT_SYMBOL + domain + SPLIT_SYMBOL + dictdomain_2[domain]
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
    # c = CreateTasks()
    # c.createSearchTasks()
    c = CreateTasks(redisDB=REDIS_KEYWEBSITE)
    c.create_keyWebsite_Tasks()
    #c.createTestTasks()

    #c.insertDomain()