import chardet
from urllib import parse

import requests
from requests import Session
from requests import ReadTimeout,ConnectionError

import db_redis
import db_oracle_opt
import spider_parse
from config_db import *
from config_spider import *
from spider_request import ClassRequest

class Download(object):
    def __init__(self, dbRedis, dbOracle, b_add):
        self.session =Session()
        self.html_parse = spider_parse.Parse()
        self.dbRedis = dbRedis
        self.dbOracle = dbOracle
        self.b_add = b_add

    def downloadtask(self, task_info, task_type):
        # '天津美杰姆教育科技有限公司 兼并 @ @ @ @ cfi.net.cn @ @ @ @ 中财网'
        try:
            print(task_info, type(task_info))
            if task_info:
                list_info = task_info.split(SPLIT_SYMBOL)
                if task_type == 'baidu_firstPage':
                    domain = list_info[1]
                    word = list_info[0]
                    s_word = word.strip()
                    search_word = parse.quote(s_word)
                    if self.b_add:
                        if domain.strip():
                            url = 'https://www.baidu.com/s?ie=utf-8&mod=1&isbd=1&isid=ed1f0e1000122fc3&ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd={}&rsv_pq=b3d3a5f6000c1e98&rsv_t=9d9aaIBWL7oiDuaCOGeHUtJmlDgv1r1QtzBMLbYGnOJ2W28JJeQ6naFPhqs&rqlang=cn&inputT=9924&si={}&ct=2097152&bs={}&gpc=stf%3D1593156336%2C1593761136%7Cstftype%3D1'.format(
                                search_word, domain, search_word)
                        else:
                            url = 'https://www.baidu.com/s?ie=utf-8&newi=1&mod=1&isbd=1&isid=C663CB5239C33121&wd={}&rsv_spt=1&rsv_iqid=0xac699ad0000c4b6a&issp=1&f=8&rsv_bp=1&rsv_idx=2&ie=utf-8&tn=baiduhome_pg&rsv_enter=1&rsv_dl=ib&rsv_sug3=2&rsv_sid=1466_31325_21083_32140_31254_32046_31848_22160&_ss=1&clist=&hsug=&csor=13&pstg=2&_cr1=27662&gpc=stf%3D1593156336%2C1593761136%7Cstftype%3D1'.format(
                                search_word
                            )
                    else:
                        if domain.strip():
                            url = 'https://www.baidu.com/s?ie=utf-8&mod=1&isbd=1&isid=ed1f0e1000122fc3&ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd={}&rsv_pq=b3d3a5f6000c1e98&rsv_t=9d9aaIBWL7oiDuaCOGeHUtJmlDgv1r1QtzBMLbYGnOJ2W28JJeQ6naFPhqs&rqlang=cn&inputT=9924&si={}&ct=2097152&bs={}'.format(
                                search_word, domain, search_word)
                        else:
                            url = 'https://www.baidu.com/s?ie=utf-8&newi=1&mod=1&isbd=1&isid=C663CB5239C33121&wd={}&rsv_spt=1&rsv_iqid=0xac699ad0000c4b6a&issp=1&f=8&rsv_bp=1&rsv_idx=2&ie=utf-8&tn=baiduhome_pg&rsv_enter=1&rsv_dl=ib&rsv_sug3=2&rsv_sid=1466_31325_21083_32140_31254_32046_31848_22160&_ss=1&clist=&hsug=&csor=13&pstg=2&_cr1=27662'.format(
                                search_word
                            )
                    #ele = ClassRequest(url, domain, headers=HEADERS_BAIDU)
                    ele = ClassRequest(url, domain, headers=HEADERS_BAIDU_2)
                    qymc = s_word.split(' ')[0]
                    if len(s_word.split(' ')) == 2:
                        key_w = s_word.split(' ')[1]
                    else:
                        key_w = ''
                    try:
                        resp = self.session.send(ele.prepare(), timeout=ele.timeout)
                        resp.encoding = 'utf8'
                        self.html_parse.parse_baidu(
                            resp.text,
                            domain,
                            self.dbRedis,
                            key_w,
                            qymc
                        )
                    except (ConnectionError, ReadTimeout) as e:
                        print(e.args, '##############')
                        self.dbRedis.tasks_add(REDIS_KEY_TASKS, task_info)
                elif task_type == 'baidu_otherpage':
                    #https://www.baidu.com/s?wd=%E5%8C%97%E4%BA%AC%E7%9C%BC%E7%A5%9E%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%20%E9%9B%84%E5%AE%89&pn=10&oq=%E5%8C%97%E4%BA%AC%E7%9C%BC%E7%A5%9E%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%20%E9%9B%84%E5%AE%89&ct=2097152&ie=utf-8&si=sina.com.cn&rsv_idx=1&rsv_pq=f30759640006c22e&rsv_t=bf70ecbFdTuwSc%2BRS4NFWuQHCu8ZXC6aimVN%2Bek%2Fu5eEpYaJ68E3vo0PS9s@@@@sina.com.cn@@@@北京眼神科技有限公司
                    url = list_info[0]
                    url = 'https://www.baidu.com/s?wd=%E5%8C%97%E4%BA%AC%E7%9C%BC%E7%A5%9E%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%20%E9%9B%84%E5%AE%89&pn=20&oq=%E5%8C%97%E4%BA%AC%E7%9C%BC%E7%A5%9E%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%20%E9%9B%84%E5%AE%89&ct=2097152&ie=utf-8&si=sina.com.cn&rsv_idx=1&rsv_pq=9dc2ec1c0004d60b&rsv_t=2ffbH9sp%2BRz%2FQedofXNpdnZriOmTGVDzoQf0HN%2Bnt3KuSvBSRSAfy%2FUJkZM'
                    domain = list_info[1]
                    s_qymc = list_info[2]
                    ele = ClassRequest(url, domain, headers=HEADERS_BAIDU_2)
                    try:
                        resp = self.session.send(ele.prepare(), timeout=ele.timeout)
                        self.html_parse.parse_baidu(
                            resp.text,
                            domain,
                            self.dbRedis,
                            '',
                            s_qymc,
                            bool_first=False
                        )
                    except (ConnectionError, ReadTimeout) as e:
                        print(e.args, '##############')
                        self.dbRedis.tasks_add(REDIS_KEY_BAIDU_OTHER, list_info)
                elif task_type == 'detail_content':
                    #http://www.baidu.com/link?url=ZFo---P_siV1CZ6GgMCNF-JoZ1kwca-z-47XbRapCoaF5OiAmhC4Nk3CGXDHHlnib-klhD2gQ9p2mGeAcoqHqo1W1fmoD99T98G6kupPQW-V-1a1v8K1q7kumtypHIli@@@@北京眼神科技有限公司@@@@sina.com.cn
                    #print(list_info)
                    long_url = list_info[0]
                    qymc = list_info[1]
                    domain = list_info[2]
                    btime =  list_info[3]
                    spider_listpage_time = list_info[4]
                    try:
                        resp = requests.get(long_url, headers=HEADERS_COMMON, timeout=LIMIT_TIMEOUT)
                        url = resp.url
                        if not self.dbRedis.duplicate_exit(REDIS_KEY_DETAIL_URLS, url):
                            cs = chardet.detect(resp.content)
                            resp.encoding = cs['encoding']
                            dict_info = {
                                'url': url,
                                'content': resp.text,
                                'domain': domain,
                                'ename': qymc,
                                'btime': btime,
                                'c0001': spider_listpage_time,
                            }
                            # title, sctime, content = self.html_parse.parse_detail_content(
                            #     resp.text
                            # )
                            # dict_info = {
                            #     'url': url,
                            #     'title': title,
                            #     'content': content,
                            #     'ctime': sctime,
                            #     'domain': domain,
                            #     'ename': qymc,
                            #     'btime': btime,
                            #     'c0001': spider_listpage_time,
                            # }
                            if not self.dbRedis.duplicate_exit(REDIS_KEY_DETAIL_URLS, url):
                                self.dbOracle.insert_one_data(ORACLE_TABLE_NEWS, **dict_info)
                                self.dbRedis.duplicate_add(REDIS_KEY_DETAIL_URLS, url)

                    except (ConnectionError, ReadTimeout) as e:
                        #pass
                        print(e.args, '##############',task_info)
                        #self.dbRedis.tasks_add(REDIS_KEY_DETAIL, list_info)

                else:
                    pass
        except Exception as e:
            print(str(e), '33333333333333333333333', task_info)
            #pass

if __name__ == '__main__':
    db_redis = db_redis.RedisQueue()
    db_oracle = db_oracle_opt.OracleEngine()
    dd = Download(db_redis, db_oracle)
    str_1 = 'https://www.baidu.com/s?wd=%E5%8C%97%E4%BA%AC%E7%9C%BC%E7%A5%9E%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%20%E9%9B%84%E5%AE%89&pn=10&oq=%E5%8C%97%E4%BA%AC%E7%9C%BC%E7%A5%9E%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%20%E9%9B%84%E5%AE%89&ct=2097152&ie=utf-8&si=sina.com.cn&rsv_idx=1&rsv_pq=f30759640006c22e&rsv_t=bf70ecbFdTuwSc%2BRS4NFWuQHCu8ZXC6aimVN%2Bek%2Fu5eEpYaJ68E3vo0PS9s@@@@sina.com.cn@@@@北京眼神科技有限公司'
    str_2 = 'http://www.baidu.com/link?url=ZFo---P_siV1CZ6GgMCNF-JoZ1kwca-z-47XbRapCoaF5OiAmhC4Nk3CGXDHHlnib-klhD2gQ9p2mGeAcoqHqo1W1fmoD99T98G6kupPQW-V-1a1v8K1q7kumtypHIli@@@@北京眼神科技有限公司@@@@sina.com.cn'
    str_3 = 'https://www.baidu.com/s?wd=%E4%B8%AD%E5%9B%BD%E8%88%AA%E6%B2%B9%E9%9B%86%E5%9B%A2%E7%9F%B3%E6%B2%B9%E8%82%A1%E4%BB%BD%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%20%E8%A3%81%E5%91%98&pn=50&oq=%E4%B8%AD%E5%9B%BD%E8%88%AA%E6%B2%B9%E9%9B%86%E5%9B%A2%E7%9F%B3%E6%B2%B9%E8%82%A1%E4%BB%BD%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%20%E8%A3%81%E5%91%98&ct=2097152&ie=utf-8&si=bidcenter.com.cn&rsv_idx=1&rsv_pq=dc6ebbd1002b6b73&rsv_t=aed6rOxVhwofSI%2BH1dBvTb143YGvscEjnB1VNfZkbR5wLmN%2Fu4FydmG934M@@@@bidcenter.com.cn@@@@中国航油集团石油股份有限公司 '
    #dd.downloadtask('北京眼神科技有限公司 雄安@@@@sina.com.cn@@@@新浪网', 'baidu_firstPage')

    dd.downloadtask(str_1, 'baidu_otherpage')

    #dd.downloadtask(str_2, 'detail_content')
