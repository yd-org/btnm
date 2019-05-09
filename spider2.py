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
base_url = "https://www.80s.tw/movie/list/----g-p/{}"

def geturls():
    dic = []
    for i in range(1,8):
        header1 = random.choice(headers)
        response = requests.get(base_url.format(i), headers=header1)
        text = response.text
        html = etree.HTML(text)
        urls = html.xpath('//ul[@class="me1 clearfix"]/li/a/@href')
        pfs = html.xpath('//span[@class="poster_score"]/text()')
        urls = list(map(lambda x:"https://www.80s.tw"+x, urls))
        n = 0
        for url in urls:
            pf = pfs[n]
            movie = parase_page(url, pf)
            n += 1
            dic.append(movie)
    return dic

def parase_page(url, pf):
    header = random.choice(headers)
    response = requests.get(url, headers=header)
    text = response.text
    html = etree.HTML(text)
    image_url = html.xpath('//div[@class="img"]/img/@src')
    if len(image_url) == 0:
        image_url = "../static/cl.png"
    else:
        image_url = "http:"+image_url[0]
    title = html.xpath('//h1/text()')
    if len(title) == 0:
        title = "电影名称获取失败"
    else:
        title = title[0]
    info = html.xpath('//div[@class="info"]/span[1]/text()')
    if len(info) == 0:
        info = html.xpath('//div[@class="info"]/span[2]/text()')
        if len(info) == 0:
            info = "描述信息获取失败"
        else:
            info = info[0].strip()
    else:
        info = info[0].strip()
        if info == "":
            info = "描述信息获取失败"
    if len(info) > 20:
        info = info[0:20]+"..."
    download_url = html.xpath('//span[@class="xunlei dlbutton1"]/a[@rel="nofollow"]/@href')
    if len(download_url) == 0:
        download_url = ""
    else:
        download_url = download_url[0]
    movie = (image_url, title, info, download_url, '3',pf)
    return movie
def run2():
    imformations = geturls()
    from dbtool import getconn
    conn = getconn()
    cursor = conn.cursor()
    cursor.execute("delete from MOVIES where TYPE='3'")
    cursor.executemany("INSERT INTO MOVIES VALUES (%s,%s,%s,%s,%s,%s)",imformations)
    conn.close()
