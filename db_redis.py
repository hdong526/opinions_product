from redis import StrictRedis

from config_db import *


class RedisQueue(object):
    def __init__(self, redisHost=REDIS_HOST, redisPort=REDIS_PORT, redisDB=REDIS_DB):
        self.db = StrictRedis(
            host = redisHost,
            port = redisPort,
            db = redisDB,
            decode_responses = True
        )


    # 去重库操作，set数据类型
    def duplicate_exit(self, key, data):
        return self.db.sismember(key, data)

    # 去重库操作，添加元素，先检查有没有这个元素
    def duplicate_add(self, key, data):
        if not self.duplicate_exit(key, data):
            self.db.sadd(key, data)
            #print('添加成功')

    # 去重库操作，直接添加元素，如果key中有这个元素不会有操作
    def duplicate_add_direct(self, key, data):
        self.db.sadd(key, data)

    # 拿出key对应所有值
    def duplicate_query(self, key):
        return self.db.smembers(key)

    # 查看set类型key的数据总量是多少
    def duplicate_scard(self, key):
        return self.db.scard(key)

    # 删除key,危险操作!
    def delete(self, key):
        self.db.delete(key)

    def tasks_add(self, key, task):
        return self.db.rpush(key, task)

    def tasks_pop(self, key):
        if self.db.llen(key):
            return self.db.lpop(key)
        return False

    def tasks_empty(self, key):
        return self.db.llen(key) == 0




if __name__ == '__main__':
    db = RedisQueue('127.0.0.1', 6379, 10)
    #db.duplicate_add_direct('haha', '87687')
    #print(db.duplicate_query())
    #db.duplicate_delete('haha')
    db.tasks_add('test', 'yyyyyyy')
    print(db.tasks_empty('test'))