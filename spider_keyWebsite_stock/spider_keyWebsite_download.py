import chardet
import requests
from requests import ReadTimeout,ConnectionError

from config_spider import *
from spider_keyWebsite_stock.config_keyWebsite import *
import spider_keyWebsite_stock.spider_keyWebsite_parse as spider_keyWebsite_parse


class Download(object):
    def __init__(self, dbRedis_task, dbRedis_duplicate, b_add):
        self.html_parse = spider_keyWebsite_parse.ParseKeyWebsite()
        self.dbRedis_task = dbRedis_task
        self.dbRedis_duplicate = dbRedis_duplicate
        self.b_add = b_add
        self.parse = spider_keyWebsite_parse.ParseKeyWebsite()


    def download(self, task_info, task_type):
        print(task_info, 1111111, task_type)
        try:
            list_info = task_info.split(SPLIT_SYMBOL)
            if task_type == 'first':
                s_word = list_info[0]
                domain = list_info[1]
                url = KEYWEBSITE_ENTER_URLS[domain]['first_url'].format(s_word)
                bool_first = True
            elif task_type == 'other':
                url = list_info[0]
                domain = list_info[2]
                s_word = list_info[1]
                bool_first = False
            else:
                pass
            print(url, domain, s_word, '###############')
            resp = requests.get(url, headers=KEYWEBSITE_HEADER[domain])
            cs = chardet.detect(resp.content)
            resp.encoding = cs['encoding']
            #print(resp.text)
            self.parse.parse_listpage(resp.text, domain, self.dbRedis_task, self.dbRedis_duplicate, s_word, bool_first)

        except Exception as e:
            print(str(e), '33333333333333333333333', task_info)