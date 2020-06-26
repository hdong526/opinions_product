import re
from urllib import parse

from lxml import etree
from gne import GeneralNewsExtractor

from config_db import *
from config_spider import *


class Parse(object):
    def __init__(self):
        pass

    #bool_first是否是首页
    def parse_baidu(self, text, domain, r_db, str_word, qymc, bool_first=True):
        #print(text)
        re_time = '(^\d{4}年\d{1,2}月\d{1,2}日)'
        select = etree.HTML(text.replace('&nbsp;', ''))
        div_list = select.xpath('//div[@id="content_left"]/div')
        for each_div in div_list:
            text = etree.tostring(each_div, method='html')
            each_div_selector = etree.HTML(text)
            titles = each_div_selector.xpath('//h3/a//text()')
            title = ''.join(titles).split('-')[0]  # .replace(u'\xbb',u'')
            #print(title)
            abstracts = each_div_selector.xpath('//div[@class="c-abstract"]//text()')
            abstract = ''.join(abstracts)
            #print(abstract)
            try:
                if re.search('(^\d+天前)', abstract):
                    str_time = re.search('(^\d+天前)', abstract).group(1)
                elif re.search('(^\d+小时前)', abstract):
                    str_time = re.search('(^\d+小时前)', abstract).group(1)
                elif re.search('(^\d+分钟前)', abstract):
                    str_time = re.search('(^\d+分钟前)', abstract).group(1)
                else:
                    str_time = re.search(re_time, abstract).group(1)
                    date_time = datetime.datetime.strptime(str_time, '%Y年%m月%d日')
                    if date_time < LIMIT_DATE:
                        continue
                re.search(qymc, title + abstract).group()

                detail_url = each_div_selector.xpath('//h3/a/@href')[0]

                # dict_info = {
                #     'title': title,
                #     'str_time': str_time,
                #     'detail_url': detail_url,
                #     's_word':str_word,#搜索的关键词
                #     'qymc':qymc,
                #     'domain':domain,
                # }
                #if '香港' in title:
                str_info = detail_url + SPLIT_SYMBOL + qymc + SPLIT_SYMBOL + domain + SPLIT_SYMBOL + str_time
                print(title,str_time,str_word,qymc)
                r_db.tasks_add(REDIS_KEY_DETAIL, str_info)

            except Exception as e:
                #print(e)
                continue

        if bool_first:
            list_url = select.xpath('//div[@id="page"]/a/@href')[:-1]
            for i in list_url:
                url = parse.urljoin('https://www.baidu.com', i)
                #print(url)
                dict_info = {
                    'url': url,
                    'domain': domain,
                    's_word':str_word,
                    'qymc':qymc,
                }
                str_info = SPLIT_SYMBOL.join([url, domain, qymc])
                r_db.tasks_add(REDIS_KEY_BAIDU_OTHER, str_info)

    def parse_detail_content(self, text):
        extractor = GeneralNewsExtractor()
        result = extractor.extract(text)
        #print(result)
        title = result['title']
        content = result['content']
        stime = result['publish_time']
        # try:
        #     list_word = re.findall(self.l_content_word, title + content)
        #     word = '_'.join(list(set(list_word)))
        # except:
        #     word = ''
        content = re.sub(u'[\U00010000-\U0010ffff]', '', content)  ##去除四个字符的表情
        title = re.sub(u'[\U00010000-\U0010ffff]', '', title)  ##去除四个字符的表情
        content = re.sub(str_error_char, '', content.strip())
        title = re.sub(str_error_char, '', title.strip())
        return title, stime, content
    #
    # def parse_detail_content(self, text, domain, xpath_title, xpath_content):
    #     try:
    #         select = etree.HTML(text)
    #         l_title = select.xpath(xpath_title)
    #         title = ' '.join([i.strip() for i in l_title])
    #         #print(title, '(((((((((((((')
    #         l_content = select.xpath(xpath_content)
    #         content = ' '.join([i.strip() for i in l_content]).replace("'", '').replace('&nbsp;', '')
    #
    #     except:
    #         #print('#######################')
    #
    #         title = re.search('<title>(.*?)</title>', text).group(1)
    #         content = re.sub('<.*?>', '', text)
    #
    #
    #     try:
    #         list_word = re.findall(self.l_content_word, title + content)
    #         word = '_'.join(list(set(list_word)))
    #     except:
    #         word = ''
    #     content = re.sub(u'[\U00010000-\U0010ffff]', '', content)  ##去除四个字符的表情
    #     title = re.sub(u'[\U00010000-\U0010ffff]', '', title)  ##去除四个字符的表情
    #     return title, content, word
    #
