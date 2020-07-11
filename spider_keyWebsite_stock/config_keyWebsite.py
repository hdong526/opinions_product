PARSE_KEYWEBSITE_RULE = {
    'sina.com.cn':{
        'newsdivs' : '//div[@class="box-result clearfix"]',
        'titles' : '//h2/a//text()',
        'ctime_info': '//h2/span[@class="fgray_time"]//text()',
        'ctime_re': '(20\d+-\d+-\d+ \d+:\d+)',
        'abstracts': '//p[@class="content"]//text()',
        'pages_info': '//div[@class="l_v2"]//text()',
        'pages_re': '新闻(\d*?)篇',
    }
}