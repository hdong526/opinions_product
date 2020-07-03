# import requests
# import chardet
# from gne import GeneralNewsExtractor
#
# url = 'http://feng.ifeng.com/c/7w1LAhY6gwN'
#
# resp = requests.get(url)
# cs = chardet.detect(resp.content)
# resp.encoding = cs['encoding']
#
# extractor = GeneralNewsExtractor()
# result = extractor.extract(resp.text)
# print(result)


# import datetime
#
# a = datetime.datetime.now()
# print(a, type(a))
#
# str1 = a.strftime('%Y-%m-%d %H:%M')
# print(str1)

import sys
import getopt

if len(sys.argv) > 1:
    try:
        opts, args = getopt.getopt(sys.argv[1:], "t:")
        for opt, arg in opts:
            if opt == '-t':
                if arg == 'add':
                    bool_add = True
                    print('增量抓取类型爬虫')
                    sys.exit()
                else:
                    print('命令错误')
    except getopt.GetoptError:
        print('位置参数错误')

