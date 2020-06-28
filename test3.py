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


import datetime

a = datetime.datetime.now()
print(a, type(a))

str1 = a.strftime('%Y-%m-%d %H:%M')
print(str1)
