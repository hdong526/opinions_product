KEYWEBSITE_HEADER = {
    'sina.com.cn':{
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
        'Sec-Fetch-User': '?1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Sec-Fetch-Site': 'same-origin',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Host': 'search.sina.com.cn',
    }
}

KEYWEBSITE_PARSE_RULE = {
    'sina.com.cn':{
        'url' : '//h2/a/@href',
        'newsdivs' : '//div[@class="box-result clearfix"]',
        'titles' : '//h2/a//text()',
        'ctime_info': '//h2/span[@class="fgray_time"]//text()',
        'ctime_re': '(20\d+-\d+-\d+ \d+:\d+)',
        'abstracts': '//p[@class="content"]//text()',
        'pages_info': '//div[@class="l_v2"]//text()',
        'pages_re': '新闻(\d*?)篇',
        'page_num': 10,                                              #每页的新闻数
    }
}

KEYWEBSITE_ENTER_URLS = {
    'sina.com.cn':{
        'first_url': 'https://search.sina.com.cn/?q={}&range=all&c=news&sort=time',
        'other_url': 'https://search.sina.com.cn/?q={}&c=news&from=&col=&range=all&source=&country=&size=10&stime=&etime=&time=&dpc=0&a=&ps=0&pf=0&page={}',
    }
}