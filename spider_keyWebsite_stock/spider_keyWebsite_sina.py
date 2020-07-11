import sys
sys.path.append("..")
import re
import chardet

import requests
from lxml import etree

import db_redis
import db_oracle_opt
import spider_keyWebsite_parse


HEADER_SINA = {
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
    'Sec-Fetch-User': '?1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Sec-Fetch-Site': 'same-origin',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Host': 'search.sina.com.cn',
}
def get_sina_listurls(str_ename):
    url = 'https://search.sina.com.cn/?q={}&range=all&c=news&sort=time'.format(str_ename)
    #url = 'https://search.sina.com.cn/?q={}&c=news&from=&col=&range=all&source=&country=&size=10&stime=&etime=&time=&dpc=0&a=&ps=0&pf=0&page=22'.format(str_ename)
    resp = requests.get(url, headers=HEADER_SINA)
    cs = chardet.detect(resp.content)
    resp.encoding = cs['encoding']
    parse = spider_keyWebsite_parse.ParseKeyWebsite()
    parse.parse_listpage(resp.text, 'sina.com.cn', '', '', True)
    # select = etree.HTML(resp.text)
    # div_list = select.xpath('//div[@class="box-result clearfix"]')
    # for each_div in div_list:
    #     text = etree.tostring(each_div, method='html')
    #     each_div_selector = etree.HTML(text)
    #     titles = each_div_selector.xpath('//h2/a//text()')
    #     title = ''.join(titles)
    #     str_infos =  each_div_selector.xpath('//h2/span[@class="fgray_time"]//text()')
    #     str_info = ''.join(str_infos)
    #     ctime = re.search('(20\d+-\d+-\d+ \d+:\d+)', str_info).group(1)
    #     #abstracts = each_div_selector.xpath('//div[@class="r-info"]//text()')
    #     abstracts = each_div_selector.xpath('//p[@class="content"]//text()')
    #     abstract = ''.join(abstracts)
    #     print(title)
    #     print(str_info)
    #     print(ctime)
    #     print(abstract)
    #     print('##########################')
    #
    #
    # page_info = select.xpath('//div[@class="l_v2"]//text()')[0]
    # page_info = re.search('新闻(\d*?)篇', page_info).group(1)
    # print(page_info)

if __name__ == '__main__':
    ename = '国家开发银行'
    get_sina_listurls(ename)