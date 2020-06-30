import datetime



SPLIT_SYMBOL = '@@@@'
LIMIT_DATE = datetime.datetime.strptime('2017-01-01','%Y-%m-%d')
LIMIT_TIMEOUT = 15

HEADERS_BAIDU = {
    'Host':'www.baidu.com',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0',
    'Accept':'*/*',
    'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding':'gzip, deflate, br',
    'is_xhr':'1',
    'is_pbs':'',
    'X-Requested-With':'XMLHttpRequest',
    'Connection':'keep-alive',
    'Cookie':  'BAIDUID=B6A727FAE6EB76758E7FD155AB73230B:FG=1;',
}

HEADERS_BAIDU_2 = {
    'Connection':'keep-alive',
    'Cache-Control':'max-age=0',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'zh-CN,zh;q=0.9',
    #'Cookie':'BAIDUID=C663CB5D40080C542C408ADB6F85239C:FG=1; BDUSS=2dZZkw4eTlmRmhYNGkwS0lyekE2WUdXWG84UC1WT2Q2amNxbm9jdmZ4cmh-eE5mRVFBQUFBJCQAAAAAAAAAAAEAAAA3NPQPaGRvbmc1MjYAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOFy7F7hcuxea;',
    #'Cookie':'BAIDUID=C663CB5D40080C542C408ADB6F85239C:FG=1;',,
    'Cookie':  'BAIDUID=B6A727FAE6EB76758E7FD155AB73230B:FG=1;',
}

HEADERS_COMMON = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0',
    'Accept':'*/*',
    'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
}

ERRORCHAR = [
    '\xa5',
    '\u2022',
    '\xa0',
    '\xb3',
    '\xb2',
    "'",
    '\u33a5',
    '\xab',
    '\xbb',
    '\u2022',
    '\uf0d8',
    '\u2205',
    '\ue78d',
    '\u25aa',
    '\u246a',
    '\u246b',
    '\U0001f48a',
    '\u2212',
    '\xac',
    '\u201e',
    '\u2028',
    '\u2219',
    '\u2044',
    #'\u5e74',
    '\u30fb',
    '\ufffd',
    '\xe5',
    '\u200b',
    '\xc3',
    '\xd4',
    '\xc0',
    '\xbc',
    '\xaa',
    '\xc4',
]
str_error_char = '|'.join(ERRORCHAR)

