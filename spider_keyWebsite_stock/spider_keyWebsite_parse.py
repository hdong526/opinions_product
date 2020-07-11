import re
from urllib import parse

from lxml import etree

from config_keyWebsite import *


class ParseKeyWebsite(object):
    def parse_listpage(self, text, domain, r_db, search_word, bool_first=True):
        dict_xpaths = PARSE_KEYWEBSITE_RULE[domain]
        select = etree.HTML(text)
        div_list = select.xpath(dict_xpaths['newsdivs'])
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
            print(title)
            print(str_info)
            print(ctime)
            print(abstract)
            print('##########################')
        if bool_first:
            page_info = select.xpath(dict_xpaths['pages_info'])
            page_info = ''.join(page_info)
            page_info = int(re.search(dict_xpaths['pages_re'], page_info).group(1))
            print(page_info)

