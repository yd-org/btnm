import requests, random
from lxml import etree
headers = [
            {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0'},
            {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'},
            {'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/44.0.2403.155 Safari/537.36'},
            {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'},
            {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36'},
            {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36'},
            {'User-Agent':'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; pl-PL; rv:1.0.1) Gecko/20021111 Chimera/0.6'},
            {'User-Agent':'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/419 (KHTML, like Gecko, Safari/419.3) Cheshire/1.0.ALPHA'},
            {'User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en) AppleWebKit/418.9 (KHTML, like Gecko, Safari) Cheshire/1.0.UNOFFICIAL'},
            {'User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; fr; rv:1.9.2.28) Gecko/20120308 Camino/2.1.2 (MultiLang) (like Firefox/3.6.28)'},
            {'User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en; rv:1.9.0.10pre) Gecko/2009041800 Camino/2.0b3pre (like Firefox/3.0.10pre)'},
            {'User-Agent':'Mozilla/5.0 (X11; U; Win95; en-US; rv:1.8.1) Gecko/20061125 BonEcho/2.0'},
            {'User-Agent':'Mozilla/5.0 (BeOS; U; BeOS BePC; en-US; rv:1.8.1.17) Gecko/20080831 BonEcho/2.0.0.17'},
            {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.4pre) Gecko/20070410 BonEcho/2.0.0.4pre'},
            {'User-Agent':'Mozilla/5.0 (Windows; U; WinNT; en; rv:1.0.2) Gecko/20030311 Beonex/0.8.2-stable'},
            {'User-Agent':'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; Avant Browser; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)'},
            {'User-Agent':'Mozilla/5.0 (compatible; ABrowse 0.4; Syllable)'},
            {'User-Agent':'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR 3.5.30729)'},
            {'User-Agent':'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; Acoo Browser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)'},
            {'User-Agent':'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Acoo Browser; .NET CLR 2.0.50727; .NET CLR 1.1.4322)'},
            {'User-Agent':'Mozilla/4.0 (compatible; MSIE 7.0; America Online Browser 1.1; Windows NT 5.1; (R1 1.5); .NET CLR 2.0.50727; InfoPath.1)'},
            {'User-Agent':'Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; rev1.5; Windows NT 5.1; SV1; .NET CLR 1.1.4322; InfoPath.1)'},
            {'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; AOL 9.7; AOLBuild 4343.19; Windows NT 6.1; WOW64; Trident/5.0; FunWebProducts)'},
            {'User-Agent':'Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.6; AOLBuild 4340.5004; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'},
            {'User-Agent':'Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.6; AOLBuild 4340.128; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.648; .NET CLR 3.5.21022)'},
            {'User-Agent':'Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.5; AOLBuild 4337.43; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.5.21022; .NET CLR 3.5.30729; .NET CLR 3.0.30618)'}
]
base_url = "https://www.cili8.biz/s/{}_rel_1.html"
def cili(keyword):
    dic = []
    header = random.choice(headers)
    response = requests.get(base_url.format(keyword), headers = header)
    text = response.text
    html = etree.HTML(text)
    searchitems = html.xpath('//div[@class="search-item"]')
    for searchitem in searchitems:
        btid = searchitem.xpath('./div[1]/h3/a/@href')[0].replace('/detail/','').replace('.html','')
        title = "".join(searchitem.xpath('./div[1]/h3/a//text()'))
        size = searchitem.xpath('./div[3]/span[3]/b/text()')[0]
        day = searchitem.xpath('./div[3]/span[2]/b/text()')[0]
        hits = searchitem.xpath('./div[3]/span[4]/b/text()')[0]
        dic.append((btid, title, size, day, hits))
    return dic
