import requests
from lxml import etree
import re
from urllib import parse

# HEADERS_BAIDU = {
# 'Host': 'www.baidu.com',
# 'Connection': 'keep-alive',
# 'Accept': '*/*',
# 'is_xhr': '1',
# 'X-Requested-With': 'XMLHttpRequest',
# 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
# 'Referer': 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=2&tn=baiduhome_pg&wd={}&ct=2097152&si={}&rsv_spt=1&oq=%25E5%258C%2597%25E4%25BA%25AC%25E7%259C%25BC%25E7%25A5%259E%25E7%25A7%2591%25E6%258A%2580%25E6%259C%2589%25E9%2599%2590%25E5%2585%25AC%25E5%258F%25B8&rsv_pq=87edbb9d00004dad&rsv_t=a286ytHBPeiBaO6ftUtTSz6%2BHiK6CAtY9cOKGjzzM44%2FkhbPCSVdKGK0S142wLZGMl1B&rqlang=cn&rsv_enter=0&rsv_dl=tb&rsv_btype=t',
# 'Accept-Encoding': 'gzip, deflate, br',
# 'Accept-Language': 'zh-CN,zh;q=0.9',
# 'Cookie': 'BIDUPSID=C620AAACFA1CEEF67A1B6E6F4DBBAB36; PSTM=1591774116; BAIDUID=C663CB5D40080C542C408ADB6F85239C:FG=1; BD_UPN=12314753; BDUSS=2dZZkw4eTlmRmhYNGkwS0lyekE2WUdXWG84UC1WT2Q2amNxbm9jdmZ4cmh-eE5mRVFBQUFBJCQAAAAAAAAAAAEAAAA3NPQPaGRvbmc1MjYAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOFy7F7hcuxea; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=1466_31325_21083_32140_31254_32046_31848_22160; BDRCVFR[feWj1Vr5u3D]=mbxnW11j9Dfmh7GuZR8mvqV; delPer=0; BD_CK_SAM=1; PSINO=1; kleck=466b680c7797325cc3838bc9ec5a3748; H_PS_645EC=a286ytHBPeiBaO6ftUtTSz6%2BHiK6CAtY9cOKGjzzM44%2FkhbPCSVdKGK0S142wLZGMl1B; BDSVRTM=105',
#
# }
#s_word = '北京眼神科技有限公司 雄安'
s_word = '国家开发银行 投资'
#s_word = '天津美杰姆教育科技有限公司'
#s_word = '中海油'
#s_word = '国家开发银行'
search_word = parse.quote(s_word)
#domain = 'sina.com.cn'
domain = 'qq.com'
#domain = 'eyecool.cn'
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
    #'Cookie': 'BDUSS=llWdXNLem5RY2YzYn5nNn44d0NKNzFPYXE4ZmJsbVpxOXFURnJ3UEpkSWtGYlZlRVFBQUFBJCQAAAAAAAAAAAEAAAA3NPQPaGRvbmc1MjYAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACSIjV4kiI1eR;',
    #'Cookie': 'BAIDUID=C663CB5D40080C542C408ADB6F85239C:FG=1;BDUSS=2dZZkw4eTlmRmhYNGkwS0lyekE2WUdXWG84UC1WT2Q2amNxbm9jdmZ4cmh-eE5mRVFBQUFBJCQAAAAAAAAAAAEAAAA3NPQPaGRvbmc1MjYAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOFy7F7hcuxea;',
    #'Cookie':  'BAIDUID=B6A727FAE6EB76758E7FD155AB73230B:FG=1;',
    #'Cookie':  'BAIDUID=C663CB5D40080C542C408ADB6F85239C:FG=1;BDUSS=2dZZkw4eTlmRmhYNGkwS0lyekE2WUdXWG84UC1WT2Q2amNxbm9jdmZ4cmh-eE5mRVFBQUFBJCQAAAAAAAAAAAEAAAA3NPQPaGRvbmc1MjYAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOFy7F7hcuxea;',
    #'Cookie':  'BAIDUID=C663CB5D40080C542C408ADB6F85239C:FG=1;BDUSS=2dZZkw4eTlmRmhYNGkwS0lyekE2WUdXWG84UC1WT2Q2amNxbm9jdmZ4cmh-eE5mRVFBQUFBJCQAAAAAAAAAAAEAAAA3NPQPaGRvbmc1MjYAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOFy7F7hcuxea;',
    #'Cookie':'BAIDUID=C663CB5D40080C542C408ADB6F85239C:FG=1;',
    'Cookie': 'BAIDUID=91917590363D929329FD2B0F652E6DFC:FG=1;',

}

# url = 'https://www.baidu.com/s?ie=utf-8&mod=1&isbd=1&isid=ed1f0e1000122fc3&ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd={}&rsv_pq=b3d3a5f6000c1e98&rsv_t=9d9aaIBWL7oiDuaCOGeHUtJmlDgv1r1QtzBMLbYGnOJ2W28JJeQ6naFPhqs&rqlang=cn&inputT=9924&si={}&ct=2097152&bs={}'.format(
#     search_word, domain, search_word)

#域名加搜索词一周内
url = 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd={}&fenlei=256&rsv_pq=acf9d4a100016459&rsv_t=09a5pNAL4%2BHEDI3DxZSG%2B3pbKOFXxN02nZfoTQvMihbRtC8sR%2F%2FbPZVNrm8&rqlang=cn&rsv_enter=0&rsv_dl=tb&rsv_btype=i&inputT=1218&si={}&ct=2097152&gpc=stf%3D1610934199%2C1611538999%7Cstftype%3D1'.format(
    search_word, domain
)
# url = 'https://www.baidu.com/s?wd={}&rsv_spt=1&rsv_iqid=0xc09830e90000b81e&issp=1&f=8&rsv_bp=1&rsv_idx=2&ie=utf-8&rqlang=cn&tn=baiduhome_pg&rsv_enter=1&rsv_dl=tb&rsv_btype=i&inputT=7910&rsv_t=4612YzcG%2B2IsMmWGZ20OOc9y40N8Y7RlBs%2FamcwYKc6DPHyRmyfNvc3af1lo6zhM1Vyp&si={}&ct=2097152&gpc=stf%3D1597913951%2C1598518751%7Cstftype%3D1'.format(
#     search_word, domain
# )


#搜索词一周内
url = 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd={}&fenlei=256&oq=%25E5%259B%25BD%25E5%25AE%25B6%25E5%25BC%2580%25E5%258F%2591%25E9%2593%25B6%25E8%25A1%258C%2520%25E6%258A%2595%25E8%25B5%2584&rsv_pq=be48b79900025912&rsv_t=6106amfyJFnPR%2FZAZUOIerFLV5K6%2B%2Bjna4QKxbd%2Fyd6AMPTYh29s1H%2Bak7o&rqlang=cn&rsv_enter=0&rsv_dl=tb&rsv_btype=t&gpc=stf%3D1610934328%2C1611539128%7Cstftype%3D1&tfflag=1'.format(
    search_word
)
# url = 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd={}&fenlei=256&oq=%25E5%259B%25BD%25E5%25AE%25B6%25E5%25BC%2580%25E5%258F%2591%25E9%2593%25B6%25E8%25A1%258C&rsv_pq=b9ca3270000af527&rsv_t=14baS1jRjujs%2FSra%2BPwhki%2BGKpROXBIVUk9r%2BArMh4M1xygHPFgI6XkkPQQ&rqlang=cn&rsv_enter=0&rsv_dl=tb&rsv_btype=t&inputT=30342&ct=0&gpc=stf%3D1595312152%2C1595916952%7Cstftype%3D1'.format(
#     search_word
# )https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=%E5%9B%BD%E5%AE%B6%E5%BC%80%E5%8F%91%E9%93%B6%E8%A1%8C%20%E6%8A%95%E8%B5%84&fenlei=256&oq=%25E5%259B%25BD%25E5%25AE%25B6%25E5%25BC%2580%25E5%258F%2591%25E9%2593%25B6%25E8%25A1%258C%2520%25E6%258A%2595%25E8%25B5%2584&rsv_pq=91ac49cd00000bf8&rsv_t=4625YhYQu65WfBWo%2FiFXyO2ju9ZW2ey2oZVzhAUW8%2FC2ngq%2B1iXAkuJNML0&rqlang=cn&rsv_enter=0&rsv_dl=tb&rsv_btype=t&gpc=stf%3D1606704178%2C1607308978%7Cstftype%3D1&tfflag=1

# url = 'https://www.baidu.com/s?ie=utf-8&newi=1&mod=1&isbd=1&isid=C663CB5239C33121&wd={}&rsv_spt=1&rsv_iqid=0xac699ad0000c4b6a&issp=1&f=8&rsv_bp=1&rsv_idx=2&ie=utf-8&tn=baiduhome_pg&rsv_enter=1&rsv_dl=ib&rsv_sug3=2&rsv_sid=1466_31325_21083_32140_31254_32046_31848_22160&_ss=1&clist=&hsug=&csor=13&pstg=2&_cr1=27662'.format(
#     search_word
# )
# url = 'https://www.baidu.com/s?wd={}&rsv_spt=1&rsv_iqid=0xc09830e90000b81e&issp=1&f=8&rsv_bp=1&rsv_idx=2&ie=utf-8&rqlang=cn&tn=baiduhome_pg&rsv_enter=0&rsv_dl=tb&oq=%25E5%259B%25BD%25E5%25AE%25B6%25E5%25BC%2580%25E5%258F%2591%25E9%2593%25B6%25E8%25A1%258C%2520%25E6%258A%2595%25E8%25B5%2584&rsv_btype=t&rsv_t=3c33okVpodJ8cceBInyDWVnZGle2edNSsNI7uSvPTZ%2FHIJUJCM3bDKtjhxI2qtFLJLwH&rsv_pq=b5d1df8e00066b2e&gpc=stf%3D1597914632%2C1598519432%7Cstftype%3D1&tfflag=1'.format(
#     search_word
# )
print(url)
#url = 'https://www.baidu.com/s?wd=%E5%8C%97%E4%BA%AC%E7%9C%BC%E7%A5%9E%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%20%E9%9B%84%E5%AE%89&pn=20&oq=%E5%8C%97%E4%BA%AC%E7%9C%BC%E7%A5%9E%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%20%E9%9B%84%E5%AE%89&ct=2097152&ie=utf-8&si=sina.com.cn'
resp = requests.get(url, headers=HEADERS_BAIDU)
resp.encoding = 'utf8'
#print(resp.text)
select = etree.HTML(resp.text.replace('&nbsp;', ''))
div_list = select.xpath('//div[@id="content_left"]/div')
for each_div in div_list:
    text = etree.tostring(each_div, method='html')
    each_div_selector = etree.HTML(text)
    titles = each_div_selector.xpath('//h3/a//text()')
    title = ''.join(titles).split('-')[0]
    print(title)

list_url = select.xpath('//div[@id="page"]/div[@class="page-inner"]/a/@href')[:-1]
print(len(list_url), '############')

