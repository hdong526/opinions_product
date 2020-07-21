import re
import datetime
from urllib import parse

from lxml import etree

from config_db import *
from config_spider import *
from spider_keyWebsite_stock.config_keyWebsite import *


class ParseKeyWebsite(object):
    def parse_listpage(self, text, domain, dbRedis_task, dbRedis_duplicate, search_word, bool_first=True):
        try:
            dict_xpaths = KEYWEBSITE_PARSE_RULE[domain]
            select = etree.HTML(text)
            div_list = select.xpath(dict_xpaths['newsdivs'])
            str_spider_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
            for each_div in div_list:
                text = etree.tostring(each_div, method='html')
                each_div_selector = etree.HTML(text)
                titles = each_div_selector.xpath(dict_xpaths['titles'])
                title = ''.join(titles)
                str_infos = each_div_selector.xpath(dict_xpaths['ctime_info'])
                str_info = ''.join(str_infos)
                ctime = re.search(dict_xpaths['ctime_re'], str_info).group(1)
                # abstracts = each_div_selector.xpath('//div[@class="r-info"]//text()')
                abstracts = each_div_selector.xpath(dict_xpaths['abstracts'])
                abstract = ''.join(abstracts)
                url = each_div_selector.xpath(dict_xpaths['url'])[0]
                # print(url)
                # print(title)
                # print(str_info)
                # print(ctime)
                # print(abstract)
                # print('##########################')
                if search_word in title + abstract:
                    if not dbRedis_duplicate.duplicate_exit(REDIS_KEY_DETAIL_URLS, url):
                        print(url)
                        print(title)
                        print(str_info)
                        print(ctime)
                        print(abstract)
                        print('##########################')
                        str_info = SPLIT_SYMBOL.join([url,search_word,domain,ctime,str_spider_time,'站内搜索'])
                        dbRedis_duplicate.tasks_add(REDIS_KEY_DETAIL, str_info)

            if bool_first:
                page_info = select.xpath(dict_xpaths['pages_info'])
                page_info = ''.join(page_info)
                page_info = int(re.search(dict_xpaths['pages_re'], page_info).group(1))
                print(page_info)
                if int(page_info) > 1:
                    pages = int(page_info/dict_xpaths['page_num'])+1 if page_info%dict_xpaths['page_num'] else page_info/dict_xpaths['page_num']
                    # if domain == 'sina.com.cn' and pages > 39:
                    #     pages = 39
                    if domain == 'sina.com.cn' and pages > 10:
                        pages = 10

                    for page_num in range(2, pages + 1):
                        listpage_url = KEYWEBSITE_ENTER_URLS[domain]['other_url'].format(search_word, page_num)
                        list_info = SPLIT_SYMBOL.join([listpage_url, search_word, domain, '站内搜索'])
                        dbRedis_task.tasks_add(REDIS_KEY_KEYWEBSITE_OTHERLISTPAGE, list_info)
                    print(pages)
        except Exception as e:
            print(str(e),'parseerrorparseerrorparseerrorparseerrorparseerror')
            print(search_word, 'yyyyyyy')

